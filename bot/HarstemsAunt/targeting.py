""" Allocates Enemy Units """

import numpy as np
from math import pi
from typing import Union, List, Dict, Set

# pylint: disable=E0402
from .utils import Utils
from .unitmarker import UnitMarker
from .combat_unit import CombatUnit
from .combat_flyer import CombatFlyer
from .common import logger

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
    #cost_score:float = Utils.sigmoid((np.sqrt(unit.minerals_cost) + 2.85 * np.sqrt(unit.vespne_cost))/100)
    return Utils.sigmoid(dps_score*health_score)*-1

class TargetAllocator:
    """
        will be implemented in .army_group 
    """

    def __init__(self,
                 bot:BotAI,
                 units:List[CombatUnit],
                 targets:Set
                 ) -> None:
        self.bot=bot
        self.units=units
        self.targets=targets
        self.allocated_targets:Dict = {}

    def allocate_targets(self, units:Units, targets:Set) -> Dict:
        """allocates targets to units"""
        self.units = units
        self.targets = targets
        
        for unit in self.units:
            if not unit.unit:
                continue
            enemies_in_range:Units = unit.enemies_in_range
            if enemies_in_range:
                enemies_in_range = enemies_in_range.sorted(lambda e:
                    e.distance_to(unit.unit.position)
                )
                self.allocated_targets[unit.tag] = enemies_in_range[0]
                continue
            if unit.enemies_in_proximity:
                closest_unit:Unit = unit.enemies_in_proximity.closest_to(unit.unit.position)
                self.allocated_targets[unit.tag] = closest_unit
                continue
            if self.targets:
                targets = list(self.targets)
                #targets.sort()
                self.allocated_targets[unit.tag] = targets[0]
                continue
            if self.bot.enemy_structures:
                closest_structure = self.bot.enemy_structures.closest_to(unit.unit.position)
                self.allocated_targets[unit.tag] = closest_structure
                continue
            self.allocated_targets[unit.tag] = self.bot.enemy_start_locations[0]
            continue

