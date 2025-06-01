"""Replacement for UnitClass"""
from typing import Union

# pylint: disable=E0402
# from .utils import Utils
from .unitmarker import UnitMarker
from .combat_unit import CombatUnit
from .common import RANGE_BUFFER,UNIT_LABEL_FONT_SIZE,logger

# pylint: disable=C0411
from sc2.unit import Unit
from sc2.position import Point2,Point3
from sc2.ids.ability_id import AbilityId


class Stalker(CombatUnit):
    """Stalker Class """

    def blink(self,target:Union[Point2, Point3, Unit]):
        """cast the blink ability"""
        self.unit(AbilityId.EFFECT_BLINK_STALKER, target)

    async def engage(self, attack_target:Union[Unit, Point2]) -> None:
        """replacement for handle_attackers """
        if not self.unit:
            return

        if self.unit and self.bot.debug:
            self.bot.client.debug_text_world(self.unit_label, \
                self.unit, size=UNIT_LABEL_FONT_SIZE)

        logger.info(self.in_attack_range_of)
        
        try:
            if isinstance(attack_target,Union[Unit, UnitMarker]):
                target = attack_target.position
            else:
                target = attack_target

            if not self.unit.distance_to(attack_target) <= self.unit.ground_range+RANGE_BUFFER:

                move_to:Point2 = self.bot.pathing.find_path_next_point(
                            self.unit.position, target, self.pathing_grid
                        )
                self.unit.move(move_to)

            if self.unit.weapon_cooldown <= 5:
                self.unit.attack(target)

            else:
                position:Point2 = self.get_retreat_pos()
                blink_pos:Point2 = self.unit.position.towards(position, 6)
                if self.can_cast(AbilityId.EFFECT_BLINK_STALKER, blink_pos) and self.in_attack_range_of:
                    self.blink(blink_pos)
                self.unit.move(position)
        except Exception as e:
            logger.warning(e)


    async def disengage(self, retreat_position: Point2) -> None:
        """overwrite for CombatUnit.disengage"""
        if not self.unit:
            return
        self.bot.client.debug_text_world(self.unit_label,\
            self.unit, size=UNIT_LABEL_FONT_SIZE)
        move_to: Point2 = self.bot.pathing.find_path_next_point(
            self.unit.position, retreat_position, self.pathing_grid
        )
        blink_pos:Point2 = self.unit.position.towards(retreat_position, 6)
        if self.can_cast(AbilityId.EFFECT_BLINK_STALKER, blink_pos):
            self.blink(blink_pos)
        if self.unit.weapon_cooldown == 0 and self.enemies_in_range:
            closest_unit: Unit = self.enemies_in_proximity.closest_to(self.unit)
            self.unit.attack(closest_unit)
            return
        self.unit.move(move_to)
        return
