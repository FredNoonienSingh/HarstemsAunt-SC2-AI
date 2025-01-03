from __future__ import annotations
from functools import cached_property
from typing import Union
import numpy as np
from enum import Enum

"""SC2 Imports"""
from sc2.unit import Unit
from sc2.units import Units
from sc2.ids.unit_typeid import UnitTypeId
from sc2.bot_ai import BotAI
from sc2.position import Point2, Point3

"""Utils"""
from utils.and_or import and_or
from utils.can_build import can_build_unit
from utils.in_proximity import in_proximity_to_point
from HarstemsAunt.pathing import Pathing
from HarstemsAunt.common import WORKER_IDS,logger

class GroupStatus(Enum):
    ATTACKING = 1
    DEFENDING = 2
    RETREATING = 3
    REGROUPING = 4


class ArmyGroup:
    def __init__(self, bot:BotAI, unit_list:list,units_in_transit:list,pathing:Pathing):
        self.bot:BotAI = bot
        self.name = "Attack Group Alpha"
        self.unit_list:list = unit_list
        self.units_in_transit:list = units_in_transit
        self.pathing:Pathing = pathing
        self.status:GroupStatus = GroupStatus.ATTACKING

    @property
    def units(self) -> Units:
        return self.bot.units.filter(lambda unit: unit.tag in self.unit_list)

    @property
    def supply(self) -> int:
        if self.units:
            return sum([self.bot.calculate_supply_cost(unit.type_id) \
                for unit in self.units if unit.can_attack])
        return 0

    @property
    def enemy_supply_in_proximity(self) -> int:
        enemy_units = self.bot.enemy_units.closer_than(25, self.position)\
            .filter(lambda unit: unit.type_id not in WORKER_IDS)
        if enemy_units:
            return sum([self.bot.calculate_supply_cost(unit.type_id) for unit in enemy_units])
        return 0

    @property
    def supply_delta(self) -> int:
        return self.supply-self.enemy_supply_in_proximity

    @property
    def reinforcements(self) -> Units:
        return self.bot.units.filter(lambda unit: unit.tag in self.units_in_transit)

    @property
    def position(self) -> Point2:
        if self.units:
            return self.units.center
        return self.bot.game_info.map_center

    @property
    def ground_dps(self) -> float:
        return sum([unit.ground_dps for unit in self.units])

    @property
    def air_dps(self) -> float:
        return sum([unit.air_dps for unit in self.units])

    @property
    def average_health_percentage(self) -> float:
        if not self.units:
            return 0
        return 1/len(self.units)*sum([unit.health_percentage for unit in self.units])

    @property
    def average_shield_precentage(self) -> float:
        if not self.units:
            return 0
        return 1/len(self.units)*sum([unit.shield_percentage for unit in self.units])

    @property
    def has_detection(self) -> float:
        if self.units.filter(lambda unit: unit.is_detector):
            return True
        return False

    @property
    def attack_target(self) -> Union[Point2, Unit]:
        #TODO #30 Rework when regrouping is working as it is supposed to
        return self.bot.enemy_start_locations[0]

    @property
    def attack_pos(self) -> Union[Point2,Point3,Unit]:
        return self.position.towards(self.attack_target, 10)

    @attack_target.setter
    def attack_target(self, new_attack_pos:Union[Point2,Point3,Unit]):
        self.attack_target = new_attack_pos

    @property
    def retreat_pos(self) -> Union[Point2,Point3,Unit]:
        return self.bot.start_location

    @retreat_pos.setter
    def retreat_pos(self, new_retreat_pos:Union[Point2,Point3,Unit]):
        self.retreat_pos = new_retreat_pos

    # TODO: #32 Implement Logic to Allocate production capacity to army_groups
    def request_unit(self, structure_type: UnitTypeId) -> UnitTypeId:
        """ 

        Args:
            structure_type (UnitTypeId): _description_

        Returns:
            UnitTypeId: _description_
        """
        pass

    def remove_unit(self, unit_tag:str) -> bool:
        """ Removes are unit from ArmyGroup 

        Args:
            unit_tag (str): tag of the Unit that is going to be removed

        Returns:
            bool: # Returns true if the Unit was in the ArmyGroup and has been removed
        """
        if unit_tag in self.unit_list:
            self.unit_list.remove(unit_tag)
            return True
        return False

    def merge_groups(self, army_group:ArmyGroup) -> bool:
        """ Merges ArmyGroup into ArmyGroup
        Args:
            army_group (ArmyGroup): army group that is supposed to get merged 

        Returns:
            bool: returns True if Groups got merged
        """
        if army_group in self.bot.army_groups:
            self.unit_list.extend(army_group.unit_list)
            self.bot.army_groups.remove(army_group)
            return True
        return False

    async def attack(self, attack_target:Union[Point2, Point3, Unit]) -> None:
        stalkers: Units = self.units(UnitTypeId.STALKER)
        zealots: Units = self.units(UnitTypeId.ZEALOT)
        observer: Units = self.units(UnitTypeId.OBSERVER)

        if stalkers:
            await self.bot.stalkers.handle_attackers(
                self.units(UnitTypeId.STALKER), attack_target
            )
        if zealots:
            await self.bot.zealots.handle_attackers(
                self.units(UnitTypeId.ZEALOT), attack_target
            )
        if observer:
            await self.bot.observers.move(
                observer, attack_target
            )

    def move(self,target_pos:Union[Point2, Point3, Unit]) -> None:
        """ Moves Army towards position

        Args:
            target_pos (Union[Point2, Point3, Unit]): _description_
        """
        for unit in self.units:

            # This could be handled more efficient if i could overwrite the Unit move command

            grid:np.ndarray = self.pathing.air_grid if unit.is_flying \
                else self.pathing.ground_grid
            unit.move(
                   self.pathing.find_path_next_point(
                       unit.position, target_pos, grid
                    )
                )

    def retreat(self) -> None:
        """Moves Army back to retreat position
        """
        grid:np.ndarray = self.pathing.ground_grid

        #Early return if units are safe
        if all(self.pathing.is_position_safe(grid, unit.position,2) for unit in self.units):
            self.regroup()
            return

        for unit in self.units:
            # This could be handled more efficient if i could overwrite the Unit move command
            if self.pathing.is_position_safe(grid, unit.position):
               continue
            if not in_proximity_to_point(self.bot, unit, self.retreat_pos, 15):
                    unit.move(
                           self.pathing.find_path_next_point(
                               unit.position, self.retreat_pos, grid
                            )
                        )
        #self.observer.retreat(self.units(UnitTypeId.OBSERVER), self.retreat_pos)

    #TODO: #31 Regroup Units by Range
    def regroup(self) -> None:

        if not self.units.filter(lambda unit: unit.distance_to(self.position) > 15):
            return

        self.units.furthest_to(self.position).move(self.position)


    # TODO: #29 very basic, needs to be Adjusted to account for different, Unit types
    def defend(self, position:Union[Point2,Point3,Unit]) -> None:
        enemy_units = self.bot.enemy_units.closer_than(25, position)
        for unit in self.units:
            grid:np.ndarray = self.pathing.air_grid if unit.is_flying \
                else self.pathing.ground_grid
            if not in_proximity_to_point(self.bot, unit, position, 20):
                unit.move(
                    self.pathing.find_path_next_point(
                        unit.position, self.retreat_pos, grid
                    )
                )
                continue
            if enemy_units:
                unit.attack(enemy_units.closest_to(unit))

    async def update(self, target:Union[Point2, Point3, Unit]):
        """ Method controlling the Behavior of the Group,\
            shall be called every tick in main.py 
        """

        last_status: GroupStatus = self.status

        # Move Units in Transit to Army_group:
        for unit in self.reinforcements:
            grid: np.ndarray = self.pathing.ground_grid
            unit.attack(
                self.pathing.find_path_next_point(
                    unit.position, self.position, grid
                )
            )
            if in_proximity_to_point(self.bot, unit, self.position, 10):
                self.units_in_transit.remove(unit.tag)
                self.unit_list.append(unit.tag)
                await self.bot.chat_send(f"Army Group: {self.name} got reinforced by {unit.type_id}")

        # CHECK DEFEND POSITION
        for townhall in self.bot.townhalls:
            enemys_in_area = self.bot.enemy_units.closer_than(30, townhall)
            if enemys_in_area:
                supply_in_area = sum([self.bot.calculate_supply_cost(unit.type_id) for unit in enemys_in_area])
                if supply_in_area > 10:
                    self.defend(townhall)
                    self.status = GroupStatus.DEFENDING
                    return

        # TODO add check if enemy_supply in Target_area > self.supply
        # CHECK RETREAT CONDITIONS
        shield_condition = self.average_shield_precentage < .45
        supply_condition = self.supply <= self.enemy_supply_in_proximity
        if and_or(shield_condition, supply_condition):
            self.retreat()
            self.status = GroupStatus.RETREATING
            return

        #self.regroup()
        await self.attack(target)
        self.status = GroupStatus.ATTACKING