"""Replacement for UnitClass"""
from typing import Union

# pylint: disable=E0402
# from .utils import Utils
from .unitmarker import UnitMarker
from .combat_unit import CombatUnit, FightStatus
from .common import RANGE_BUFFER,UNIT_LABEL_FONT_SIZE,logger

# pylint: disable=C0411
from sc2.unit import Unit
from sc2.position import Point2
#from sc2.ids.buff_id import BuffId


class Immortal(CombatUnit):
    """Immortal """

    @property
    def fight_status(self) -> FightStatus:
        """Returns the current fighting status of the Unit """
        if self.unit:
            if self.unit.shield_health_percentage >= .25:
                # or not self.can_survive_fleeing:
                return FightStatus.FIGHTING
            return FightStatus.RETREATING
        return FightStatus.DESTROYED


    async def engage(self, attack_target:Union[Unit, Point2]) -> None:
        """replacement for handle_attackers """
        if not self.unit:
            return

        if self.unit and self.bot.debug:
            self.bot.client.debug_text_world(self.unit_label, \
                self.unit, size=UNIT_LABEL_FONT_SIZE)

        try:
            if isinstance(attack_target,Union[Unit, UnitMarker]):
                target = attack_target.position
            else:
                target = attack_target

            if not self.unit.distance_to(target) <= self.unit.ground_range+RANGE_BUFFER:
                move_to:Point2 = self.bot.pathing.find_path_next_point(
                            self.unit.position, target, self.pathing_grid
                        )
                self.unit.move(move_to)

            if self.unit.weapon_cooldown <= 5:
                if isinstance(attack_target, UnitMarker):
                    self.unit.attack(attack_target.position)
                else:
                    self.unit.attack(attack_target)

            else:
                #if not self.unit.has_buff(BuffId.TAKENDAMAGE):
                position:Point2 = self.get_retreat_pos()
                self.unit.move(position)
        except Exception as e:
            logger.warning(e)

    async def disengage(self, retreat_position: Point2) -> None:
        """ replacement for move to safety
            -> This should contain stutter stepping, for ranged Units
        """
        if not self.unit:
            if self.bot.debug:
                logger.warning("Unit not existing")
            return
        self.bot.client.debug_text_world(self.unit_label,\
            self.unit, size=UNIT_LABEL_FONT_SIZE)
        move_to: Point2 = self.bot.pathing.find_path_next_point(
            self.unit.position, retreat_position, self.pathing_grid
        )
        if self.unit.weapon_cooldown == 0 and self.enemies_in_range:
            closest_unit: Unit = self.enemies_in_proximity.closest_to(self.unit)
            self.unit.attack(move_to)
            return
        self.unit.move(move_to)
        return

