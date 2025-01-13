""" Army Group class"""
from __future__ import annotations
from enum import Enum
from typing import Union
import numpy as np

from .utils import Utils
from .pathing import Pathing
from .common import WORKER_IDS, RUN_BY_SIZE, logger


from sc2.unit import Unit
from sc2.units import Units
from sc2.ids.unit_typeid import UnitTypeId
from sc2.bot_ai import BotAI
from sc2.position import Point2, Point3

class GroupStatus(Enum):
    """Enum representing the State """
    ATTACKING = 1
    DEFENDING = 2
    RETREATING = 3
    REGROUPING = 4

class GroupTypeId(Enum):
    """Enum representing the Group State ID """
    ARMY = 1
    RUN_BY = 2

class ArmyGroup:
    """Class representing an Army Group """
    def __init__(self, bot:BotAI, unit_list:list,\
        units_in_transit:list,pathing:Pathing,group_type:GroupTypeId=GroupTypeId.ARMY):
        self.bot:BotAI = bot
        self.name = "Attack Group Alpha"
        self.requested_units:list = []
        self.unit_list:list = unit_list
        self.units_in_transit:list = units_in_transit
        self.pathing:Pathing = pathing
        self.status:GroupStatus = GroupStatus.ATTACKING
        self.GroupTypeId = group_type

    @property
    def units(self) -> Units:
        """ Units Object containing the all units in Group """
        return self.bot.units.filter(lambda unit: unit.tag in self.unit_list)

    @property
    def supply(self) -> int:
        """ Supply Cost of Units in Group """
        if self.units:
            return sum([self.bot.calculate_supply_cost(unit.type_id) \
                for unit in self.units if unit.can_attack])
        return 0

    @property
    def enemy_supply_in_proximity(self) -> int:
        """Enemy Supply in the Area"""
        enemy_units = self.bot.enemy_units.closer_than(25, self.position)\
            .filter(lambda unit: unit.type_id not in WORKER_IDS)
        if enemy_units:
            return sum([self.bot.calculate_supply_cost(unit.type_id) for unit in enemy_units])
        return 0

    @property
    def supply_delta(self) -> int:
        """ Difference betweem own and enemy supply"""
        return self.supply-self.enemy_supply_in_proximity

    @property
    def reinforcements(self) -> Units:
        """ Reinforcements moving to the Army Position"""
        return self.bot.units.filter(lambda unit: unit.tag in self.units_in_transit)

    @property
    def position(self) -> Point2:
        """ Center of Army Group """
        if self.units:
            return self.units.center
        return self.bot.main_base_ramp.top_center

    @property
    def ground_dps(self) -> float:
        """Sum of ground_dps of Units in Group"""
        return sum([unit.ground_dps for unit in self.units])

    @property
    def air_dps(self) -> float:
        """Sum of air_dps of Units in Group"""
        return sum([unit.air_dps for unit in self.units])

    @property
    def average_health_percentage(self) -> float:
        """Sum of ground_dps of Units in Group"""
        if not self.units:
            return 0
        return 1/len(self.units)*sum([unit.health_percentage for unit in self.units])

    @property
    def average_shield_percentage(self) -> float:
        """average Shield Percentage"""
        if not self.units:
            return 0
        return 1/len(self.units)*sum([unit.shield_percentage for unit in self.units])

    @property
    def has_detection(self) -> float:
        """Returns if the the Army Group contains a detector"""
        if self.units.filter(lambda unit: unit.is_detector):
            return True
        return False

    @property
    def attack_target(self) -> Union[Point2, Unit]:
        """Current Attack Target of the Army Group """
        #TODO #30 Rework when regrouping is working as it is supposed to
        return self.bot.enemy_start_locations[0]

    @attack_target.setter
    def attack_target(self, new_attack_target:Union[Point2,Point3,Unit]):
        """ sets new attack target """
        self.attack_target = new_attack_target

    @property
    def retreat_pos(self) -> Union[Point2,Point3,Unit]:
        """ position to which the group retreats to """
        return self.bot.start_location

    @retreat_pos.setter
    def retreat_pos(self, new_retreat_pos:Union[Point2,Point3,Unit]):
        """ sets new attack target """
        self.retreat_pos = new_retreat_pos

    def request_unit(self) -> UnitTypeId:
        """ Adds Units based on Logic to the List requested Units

        Returns:
            UnitTypeId: Type of requested Unit
        """
        #TODO: THIS SHOULD BE A POLYMORPHIC APPROACH TO AVOID LARGE FUNCTIONS, BUT FOR NOW INNER FUNCTIONS WILL DO
        def _runby_request():
            """ reuest unit for Run-By Army group"""
            opponent_has_detection:bool = self.bot.macro.build_order.opponent_has_detection
            if len(self.unit_list) + len(self.units_in_transit) < RUN_BY_SIZE:
                if self.bot.structures.filter(lambda struct: struct.type_id in [UnitTypeId.GATEWAY, UnitTypeId.WARPGATE]):
                    if self.bot.units(UnitTypeId.DARKSHRINE).ready and not opponent_has_detection:
                        requested_unit: UnitTypeId = UnitTypeId.DARKTEMPLAR
                        if not requested_unit in self.requested_units:
                            self.requested_units.append(requested_unit)
                        return
                    requested_unit: UnitTypeId = UnitTypeId.ZEALOT
                    if not requested_unit in self.requested_units:
                        self.requested_units.append(requested_unit)
                    return

        def _army_request():
            """ request unit for "normal" Army group  """
            gate_aliases:list = [UnitTypeId.GATEWAY, UnitTypeId.WARPGATE]
            if self.bot.structures.filter(lambda struct: struct.type_id in gate_aliases):
                stalkers:int = len(self.units(UnitTypeId.STALKER))
                zealots:int = len(self.units(UnitTypeId.ZEALOT)) +1
                
                if self.bot.structures(UnitTypeId.TEMPLARARCHIVE) and len(self.units(UnitTypeId.HIGHTEMPLAR)) < 2:
                    requested_unit: UnitTypeId = UnitTypeId.HIGHTEMPLAR
                    if not requested_unit in self.requested_units:
                        self.requested_units.append(requested_unit)

                if not zealots < stalkers:
                    requested_unit: UnitTypeId = UnitTypeId.ZEALOT
                    if not requested_unit in self.requested_units:
                        self.requested_units.append(requested_unit)
                else:
                    requested_unit: UnitTypeId = UnitTypeId.STALKER
                    if not requested_unit in self.requested_units:
                        self.requested_units.append(requested_unit)

            if self.bot.structures(UnitTypeId.ROBOTICSFACILITY):
                if not self.has_detection:
                    requested_unit: UnitTypeId = UnitTypeId.OBSERVER
                else:
                    requested_unit: UnitTypeId = UnitTypeId.IMMORTAL
                if not requested_unit in self.requested_units:
                    self.requested_units.append(requested_unit)


            if self.bot.structures(UnitTypeId.STARGATE):
                if len(self.bot.units.flying) > \
                    len(self.bot.enemy_units.filter(lambda unit: unit.is_flying and unit.can_attack)):
                    requested_unit: UnitTypeId = UnitTypeId.PHOENIX
                    if not requested_unit in self.requested_units:
                        self.requested_units.append(requested_unit)

        #match self.GroupTypeId:
            #case GroupTypeId.RUN_BY:
             #   logger.info("not Testing Runbys right now")
#                _runby_request()
            #case GroupTypeId.ARMY:
        _army_request()

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
        """ attack command for the army group"""
        # TODO: WHEN ALL UNITS_CLASSES ARE IMPLEMENTED THIS CAN JUST ONE CALL TO HANDLE ATTACKERS
        stalkers: Units = self.units(UnitTypeId.STALKER)
        zealots: Units = self.units(UnitTypeId.ZEALOT)
        Immortals: Units = self.units(UnitTypeId.IMMORTAL)
        observer: Units = self.units(UnitTypeId.OBSERVER)

        if stalkers:
            await self.bot.stalkers.handle_attackers(
                stalkers, attack_target
            )
        if Immortals:
            await self.bot.stalkers.handle_attackers(
                Immortals, attack_target
            )
        if zealots:
            await self.bot.zealots.handle_attackers(
                zealots, attack_target
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
            if not Utils.in_proximity_to_point(unit,self.retreat_pos,15):
                    unit.move(
                           self.pathing.find_path_next_point(
                               unit.position, self.retreat_pos, grid
                            )
                        )
                    
        #self.observer.retreat(self.units(UnitTypeId.OBSERVER), self.retreat_pos)

    #TODO: #31 Regroup Units by Range
    def regroup(self) -> None:
        """ regroup command for the group  """

        if not self.units.filter(lambda unit: unit.distance_to(self.position) > 5):
            return

        self.units.furthest_to(self.position).move(self.position)

    # TODO: #29 very basic, needs to be Adjusted to account for different, Unit types
    def defend(self, position:Union[Point2,Point3,Unit]) -> None:
        """ defent command for the group"""
        enemy_units = self.bot.enemy_units.closer_than(25, position)
        for unit in self.units:
            grid:np.ndarray = self.pathing.air_grid if unit.is_flying \
                else self.pathing.ground_grid
            if not Utils.in_proximity_to_point(self.bot, unit, position, 20):
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
        if not self.requested_units:
            self.request_unit()
        #last_status: GroupStatus = self.status

        # Move Units in Transit to Army_group:
        for unit in self.reinforcements:
            grid: np.ndarray = self.pathing.ground_grid
            unit.attack(
                self.pathing.find_path_next_point(
                    unit.position, self.position, grid
                )
            )
            if Utils.in_proximity_to_point(unit, self.position, 2):
                self.units_in_transit.remove(unit.tag)
                self.unit_list.append(unit.tag)
                await self.bot.chat_send(f"Army Group: {self.name} got reinforced by {unit.type_id}")

        # CHECK DEFEND POSITION
        for townhall in self.bot.townhalls:
            enemies_in_area = self.bot.enemy_units.closer_than(30, townhall)
            if enemies_in_area:
                supply_in_area = sum([self.bot.calculate_supply_cost(unit.type_id) for unit in enemies_in_area])
                if supply_in_area > 10:
                    self.defend(townhall)
                    self.status = GroupStatus.DEFENDING
                    return

        # TODO add check if enemy_supply in Target_area > self.supply
        # CHECK RETREAT CONDITIONS
        shield_condition = self.average_shield_percentage < .45
        supply_condition = self.supply <= self.enemy_supply_in_proximity
        if Utils.and_or(shield_condition, supply_condition) or len(self.units) < len(self.units_in_transit):
            self.retreat()
            self.status = GroupStatus.RETREATING
            return

        #self.regroup()
        await self.attack(target)
        self.status = GroupStatus.ATTACKING