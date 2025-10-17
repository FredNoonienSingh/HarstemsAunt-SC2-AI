"""Replacement for UnitClass"""
from typing import Union

# pylint: disable=E0402
# from .utils import Utils
from .unitmarker import UnitMarker
from .combat_unit import CombatUnit
from .common import RANGE_BUFFER,UNIT_LABEL_FONT_SIZE,ALL_STRUCTURES

# pylint: disable=C0411
from sc2.unit import Unit
from sc2.units import Units
from sc2.position import Point2

class Zealot(CombatUnit):
    """Zealot Class"""

    @property
    def enemies_in_proximity(self) -> Units:
        """The enemies_in_proximity property."""
        if self.bot.enemy_units and self.unit:
            return self.bot.enemy_units.closer_than(25, self.unit)\
                .filter(lambda unit: unit.type_id not in ALL_STRUCTURES and not\
                    unit.is_flying
                    )
        return

    async def engage(self, attack_target:Union[Unit, Point2]) -> None:
        """replacement for handle_attackers """
        if not self.unit:
            return

        if self.unit and self.bot.debug:
            self.bot.client.debug_text_world(self.unit_label, \
                self.unit, size=UNIT_LABEL_FONT_SIZE)

        if not self.unit.distance_to(attack_target) <= self.unit.ground_range+RANGE_BUFFER:
            if isinstance(target,Union[Unit, UnitMarker]):
                target = target.position

            move_to:Point2 = self.bot.pathing.find_path_next_point(
                        self.unit.position, target, self.pathing_grid
                    )
            self.unit.move(move_to)
        else:
            self.unit.attack(attack_target)
