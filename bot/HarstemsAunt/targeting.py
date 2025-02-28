""" Allocates Enemy Units """

import numpy as np
from math import pi
from typing import Union, List, Dict

# pylint: disable=E0402
from .utils import Utils
from .unitmarker import UnitMarker
from .combat_unit import CombatUnit

# pylint: disable=E0401
from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.position import Point2
# from sc2.ids.unit_typeid import UnitTypeId


def target_allocation_score(bot:BotAI,unit:Unit) -> float:
    """ calculates the TAS for the unit

    Args:
        unit (Unit): Enemy Unit

    Returns:
        float: TAS (see dev_notebooks/unit_value.ipynb)
    """
    fraction_ground: float = len(bot.units.filter(lambda unit: not unit.is_flying))/len(bot.units)
    fraction_flying: float = len(bot.units.filter(lambda unit: unit.is_flying))/len(bot.units)

    dps_score:float = np.sqrt(pi*((unit.air_range**2)*(fraction_flying*unit.air_dps))+((unit.ground_range**2)*(fraction_ground*unit.ground_dps)))/10
    health_score:float = 3/2 -Utils.sigmoid(unit.health/10)
    cost_score:float = Utils.sigmoid((np.sqrt(unit.minerals_cost) + 2.85 * np.sqrt(unit.vespne_cost))/100)
    return Utils.sigmoid(dps_score*health_score*cost_score)

class TargetAllocator:
    """
        will be implemented in .army_group 
    """

    def __init__(self, bot:BotAI) -> None:
        self.bot = bot
        self.targets: Dict[int: List[Union[Unit, UnitMarker]]] = {}

    def __call__(self, units:Units, attack_target:Union[Unit, Point2]) -> None:
        self.targets = {}
        # self.allocate_targets(units, attack_target)

    def __repr__(self) -> str:
        return f"TargetAllocator targets: {self.targets}"

    @property
    def units(self) -> Units:
        pass

    @property
    def enemy_units(self) -> Units:
        """Just returns the enemy_units in the bot class """
        return self.bot.enemy_units

    @property
    def unitmarkers(self) -> List[UnitMarker]:
        """ Returns unitmarkers from bot"""
        return self.bot.unitmarkers

    @property
    def targets_to_allocate(self) -> List[Union[Unit, UnitMarker]]:
        """ returns all units and Unitmarker that can be engaged """
        enemies: List[Unit] = list(self.enemy_units)
        markers: List[UnitMarker] = self.bot.unitmakers
        return enemies + markers

    def allocate_targets(self) -> None:
        """ Allocates targets to combat units """
        # THE TARGETS SHOULD BE SORTED BY VALUE
         # Value needs to be calculated by:
            # -> DPS
            # -> Energy
            # -> Health
            # -> gas cost
            # -> mineral cost
            # -> is_constructing_scv
        # allocate to units first

        # THIS IS FUCKING INEFFICIENT, VALUE OF UNITS THAT ARE IN RANGE OF MULTIPLE UNITS WOULD BE CALCULATED 
        # MORE THAN ONCE
        def calculate_unit_value(unit:Unit) -> float:
            # maybe just a polynomial ?
            mineral_cost, vespene_cost = self.bot.calculate_value(unit.type_id)
            
            # Wrong SYNTAX
            
            return ((unit.ground_dps + unit.air_dps)^3 + ((1/unit.health)^2) + (vespene_cost + mineral_cost))

    def get_target_for(self, unit_tag:int) -> Unit:
        """returns target for unit """
        return self.targets.get(unit_tag)

