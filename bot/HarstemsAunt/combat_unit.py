"""Replacement for UnitClass"""
from enum import Enum
from typing import Union, List

import numpy as np

# pylint: disable=E0402
from .utils import Utils
from .unitmarker import UnitMarker
from .common import MIN_SHIELD_AMOUNT, RANGE_BUFFER

# pylint: disable=C0411
from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.position import Point2


class FightStatus(Enum):
    """Could be named better, will be used to report to the 
        Group if the unit is ready to engage
    """
    FIGHTING = 1
    RETREATING = 1


class CombatUnit:
    """Base Class for new UnitClass, controls a single unit not all units of a type
        will replace the old UnitClasses
    """
    def __init__(self,bot:BotAI ,unit_tag:int,pathing_grid:np.ndarray) -> None:
        self.bot = bot
        self.unit_tag = unit_tag
        self.pathing_grid = pathing_grid

    def __call__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"combat unit {self.unit.type_id} at {self.unit.position} currently {self.fight_status}"

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
    def markers_in_proximity(self) -> List[UnitMarker]:
        """The markers_in_proximity property."""
        return [marker for marker in self.bot.unitmarkers if\
                self.unit.position.distance_to(marker.position) >\
                self.unit.vision_range + 1]

    @property
    def enemies_in_proximity(self) -> Units:
        """The enemies_in_proximity property."""
        return self.bot.enemy_units.closer_than(15, self.unit)

    @property
    def in_attack_range_of(self) -> Units:
        """returns all enemies that currently can attack the unit
                i just saw, there is a implementation of this 

                I should benchmark both to test if i want to keep this

        """
        if self.unit.is_flying:
            return self.enemies_in_proximity\
                    .filter(lambda enemy: enemy.can_attack_air \
                    and enemy.distance_to(self.unit) + RANGE_BUFFER <= enemy.air_range)
        return self.enemies_in_proximity.filter(lambda enemy: enemy.can_attack_ground \
                and enemy.distance_to(self.unit) + RANGE_BUFFER <= enemy.ground_range)

    @property
    def potential_damage_taken(self) -> float:
        """returns the amount of damage the unit may take at the current position """
        if self.unit.is_flying:
            return sum([unit.air_dps for unit in list(self.in_attack_range_of)])
        return sum([unit.ground_dps for unit in list(self.in_attack_range_of)])

    @property
    def potential_damage_given(self) -> float:
        """The potential_damgae_give( property."""
        sorted_enemies = self.enemies_in_proximity\
                .sort(lambda enemy: self.unit.calculate_dps_vs_target(enemy))
        return self.unit.calculate_dps_vs_target(sorted_enemies[0])

    @property
    def can_survive_fleeing(self) -> bool:
        """ Returns true, 
            if unit will not be destroyed in current fight and transit to safespot
        """
        # More readable then just a massive oneliner
        movement_speed:float = self.unit.movement_speed
        distance_to_safty:float = self.unit.distance_to(self.safe_spot)
        time_in_danger:float = distance_to_safty/movement_speed
        damage_over_time:float = self.potential_damage_taken*time_in_danger

        #does not account for the fact that the potential damage is probally spread out over multiple units 
        return self.unit.health > damage_over_time

    @property
    def fight_status(self) -> FightStatus:
        """Returns the current fighting status of the Unit """
        if self.unit.shield_percentage > MIN_SHIELD_AMOUNT or not self.can_survive_fleeing:
            return FightStatus.FIGHTING
        return FightStatus.RETREATING

    async def engage(self, attack_target:Union[Unit, Point2]) -> None:
        """replacement for handle_attakers """
        pass

    async def disengage(self, retreat_position: Point2) -> None:
        """ replacement for move to safty"""
        pass
