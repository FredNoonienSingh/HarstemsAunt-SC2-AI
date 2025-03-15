"""Replacement for UnitClass"""
from enum import Enum
from typing import Union, List

import numpy as np

# pylint: disable=E0402
# from .utils import Utils
from .unitmarker import UnitMarker
from .common import MIN_SHIELD_AMOUNT, RANGE_BUFFER,\
    PROXIMITY,PRIO_ATTACK_TARGET, ALL_STRUCTURES, logger

# pylint: disable=C0411
from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.position import Point2,Point3


class FightStatus(Enum):
    """Could be named better, will be used to report to the 
        Group if the unit is ready to engage
    """
    FIGHTING = 1
    RETREATING = 2
    DESTROYED = 3


class CombatUnit:
    """Base Class for new UnitClass, controls a single unit not all units of a type
        will replace the old UnitClasses
    """
    def __init__(self,bot:BotAI ,unit_tag:int,pathing_grid:np.ndarray) -> None:
        # I NEED TO BE REMOVED, WHEN I GET DESTROYED
        self.bot = bot
        self.unit_tag = unit_tag
        self.pathing_grid = pathing_grid

    def __call__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"combat unit {self.unit.type_id} at \
            {self.unit.position} currently {self.fight_status}"

    @property
    def unit(self) -> Unit:
        """The unit property."""
        return self.bot.units.find_by_tag(self.unit_tag)

    @property
    def tag(self) -> int:
        """unique identifier for unit"""
        return self.unit.tag

    @property
    def safe_spot(self) -> Point2:
        """ Returns the closest safe spot to the unit """
        return self.bot.pathing.find_closest_safe_spot(
                self.unit.position, self.pathing_grid)

    @property
    def position3d(self) -> Point3:
        """position of the unit as Point3"""
        return self.unit.position3d

    @property
    def friendlies_in_proximity(self) -> Units:
        """ friendly Units in proyimity to self, 
            PROXIMITY value is specified in HarstemsAunt.common

        Returns:
            Units: Units close to self
        """
        return self.bot.units.closer_than(PROXIMITY,self.unit)

    @property
    def markers_in_proximity(self) -> List[UnitMarker]:
        """The markers_in_proximity property."""
        if self.bot.unitmarkers and self.unit:
            return [marker for marker in self.bot.unitmarkers if\
                    self.unit.position.distance_to(marker.position) >\
                    self.unit.sight_range + 1]
        return

    @property
    def enemies_in_proximity(self) -> Units:
        """The enemies_in_proximity property."""
        if self.bot.enemy_units and self.unit:
            return self.bot.enemy_units.closer_than(25, self.unit)\
                .filter(lambda unit: unit.type_id not in ALL_STRUCTURES)
        return

    @property
    def in_attack_range_of(self) -> Units:
        """returns all enemies that currently can attack the unit
                i just saw, there is a implementation of this 

                I should benchmark both to test if i want to keep this
        """
        if self.enemies_in_proximity:
            if self.unit.is_flying:
                return self.enemies_in_proximity\
                        .filter(lambda enemy: enemy.can_attack_air \
                        and enemy.distance_to(self.unit) + RANGE_BUFFER <= enemy.air_range)
            if self.bot.enemy_units:
                return self.enemies_in_proximity.filter(lambda enemy: enemy.can_attack_ground \
                    and enemy.distance_to(self.unit) + RANGE_BUFFER <= enemy.ground_range)
        return None

    @property
    def potential_damage_taken(self) -> float:
        """returns the amount of damage the unit may take at the current position """
        if self.in_attack_range_of:
            if self.unit.is_flying:
                return sum([unit.air_dps for unit in list(self.in_attack_range_of)])
            if self.in_attack_range_of:
                return sum([unit.ground_dps for unit in list(self.in_attack_range_of)])
        return 0.0

    @property
    def potential_damage_given(self) -> float:
        """The potential_damage_give property."""
        if self.enemies_in_proximity:
            sorted_enemies = self.enemies_in_proximity\
                    .sort(lambda enemy: self.unit.calculate_dps_vs_target(enemy))
            return self.unit.calculate_dps_vs_target(sorted_enemies[0])
        return 0.0

    @property
    def can_survive_fleeing(self) -> bool:
        """ Returns true, 
            if unit will not be destroyed in current fight and transit to safe spot
        """
        # More readable then just a massive oneliner
        if self.potential_damage_taken:
            movement_speed:float = self.unit.movement_speed
            distance_to_safety:float = self.unit.distance_to(self.safe_spot)
            time_in_danger:float = distance_to_safety/movement_speed
            damage_over_time:float = self.potential_damage_taken*time_in_danger

            #does not account for the fact that the potential damage is /
            # probally spread out over multiple units
            # could be improved by dividing the damage by own units in proximity
            return self.unit.health > damage_over_time\
                /len(self.friendlies_in_proximity)/2
                # assuming that on average half of the units are closer to the enemies
        return True

    @property
    def fight_status(self) -> FightStatus:
        """Returns the current fighting status of the Unit """
        if self.unit:
            if self.unit.shield_percentage > MIN_SHIELD_AMOUNT:# or not self.can_survive_fleeing:
                return FightStatus.FIGHTING
            return FightStatus.RETREATING
        return FightStatus.DESTROYED

    def cast_influence(self) -> np.ndarray:
        """ returns an np.array to influence the pathing Grid
            -> goal of this function is to get Units to create formations and
                stopping them from blocking each other

            # Maybe a whole map is not necessary ... 

        Returns:
            np.ndarray: influence grid
        """
        pass

    async def move(self, target_position:Union[Point2, Point3, Unit]) -> None:
        """ moves the unit to a given point """
        self.unit.move(
                   self.bot.pathing.find_path_next_point(
                       self.unit.position, target_position, self.pathing_grid
                    )
                )

    async def engage(self, attack_target:Union[Unit, Point2]) -> None:
        """replacement for handle_attackers """
        # This is just for testing
        #logger.info(f"{self}\n{self.unit.ground_range}")
        if not self.unit:
            if self.bot.debug:
                logger.warning(f"Unit not existing ->")
            return
        
        enemies_can_be_attacked = []
        if self.enemies_in_proximity:
            enemies_can_be_attacked:Units = self.enemies_in_proximity.filter(lambda unit: self.unit.calculate_damage_vs_target(unit)[0] > 0)
        if enemies_can_be_attacked:
            prio_targets = enemies_can_be_attacked.filter(lambda unit: unit.type_id in PRIO_ATTACK_TARGET)
            if prio_targets:
                target = prio_targets.closest_to(self.unit)
            target = min(
                enemies_can_be_attacked,
                key=lambda e: (e.health + e.shield, e.tag),
            )

        elif self.markers_in_proximity:
            target:Union[Unit, Point2] = self.markers_in_proximity[0].position

        elif not self.markers_in_proximity and not self.enemies_in_proximity\
            and self.bot.enemy_units:
                enemies: Units = self.bot.enemy_units
                prio_targets = enemies.filter(lambda unit: unit.type_id in PRIO_ATTACK_TARGET and\
                    self.unit.calculate_damage_vs_target(unit)[0] > 2)
                if prio_targets:
                    target = prio_targets.closest_to(self.unit)
                target = min(
                    enemies,
                    key=lambda e: (e.health + e.shield, e.tag),
                    )
        else:
            target:Union[Unit, Point2] = attack_target
        if self.bot.debug and self.unit:
            self.bot.debug_tools.debug_targeting(self, target)

        if isinstance(target,Unit):
            target = target.position

        target:Point2 = self.bot.pathing.find_path_next_point(
                    self.unit.position, target, self.pathing_grid
                )

        #logger.error(self.in_attack_range_of)

        if self.unit.weapon_ready:
            self.unit.attack(target)
        if not self.unit.weapon_ready and self.in_attack_range_of: 
            self.unit.move(self.safe_spot)

    async def disengage(self, retreat_position: Point2) -> None:
        """ replacement for move to safety
            -> This should contain stutter stepping, for ranged Units
        """
        if not self.unit:
            if self.bot.debug:
                logger.warning("Unit not existing")
            return
        move_to: Point2 = self.bot.pathing.find_path_next_point(
            self.unit.position, retreat_position, self.pathing_grid
        )
        if self.can_survive_fleeing:
            if self.unit.ground_range > 3 or self.unit.air_range > 3:
                if self.unit.weapon_ready and self.enemies_in_proximity\
                    and self.fight_status == FightStatus.FIGHTING:
                    # IS THERE unit turn rate property ?
                    self.unit.attack(move_to)
                    return
            self.unit.move(move_to)
            return
        else:
            self.unit.attack(self.unit.position)
