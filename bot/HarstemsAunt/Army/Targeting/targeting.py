""" Allocates Enemy Units """
from typing import List, Dict, Set

# pylint: disable=E0401
from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI


from bot.HarstemsAunt.Army.Units.combat_unit import CombatUnit
##from bot.HarstemsAunt.Army.Targeting.targeting_utils import TargetingUtils

# TODO: Rework from the Ground up
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
                    e.distance_to(unit.position)
                )
                self.allocated_targets[unit.tag] = enemies_in_range[0]
                continue
            if unit.enemies_in_proximity:
                closest_unit:Unit = \
                    unit.enemies_in_proximity.closest_to(unit.unit.position)
                self.allocated_targets[unit.tag] = closest_unit
                continue
            if self.targets:
                targets = list(self.targets)
                #targets.sort()
                self.allocated_targets[unit.tag] = targets[0]
                continue
            if self.bot.enemy_structures:
                closest_structure = \
                    self.bot.enemy_structures.closest_to(unit.unit.position)
                self.allocated_targets[unit.tag] = closest_structure
                continue
            self.allocated_targets[unit.tag] = self.bot.enemy_start_locations[0]
            continue

