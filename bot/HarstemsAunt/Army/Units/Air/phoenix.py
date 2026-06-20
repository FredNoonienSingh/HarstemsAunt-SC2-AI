"""Replacement for UnitClass"""
from typing import Union

# pylint: disable=E0402
# from bot.HarstemsAunt.utils import Utils
from bot.HarstemsAunt.misc.unitmarker import UnitMarker
from bot.HarstemsAunt.Army.Units.combat_flyer import CombatFlyer
from bot.HarstemsAunt.common import RANGE_BUFFER,PRIO_ATTACK_TARGET,UNIT_LABEL_FONT_SIZE,logger

# pylint: disable=C0411
from sc2.unit import Unit
from sc2.position import Point2,Point3
from sc2.ids.ability_id import AbilityId

class Phoenix(CombatFlyer):
    """Phoenix Class """

    async def engage(self, attack_target:Union[Unit, Point2]) -> None:
        """ replacement for handle_attackers """
        if not self.unit:
            return

        if self.unit and self.bot.debug:
            self.bot.client.debug_text_world(self.unit_label, \
                self.unit, size=UNIT_LABEL_FONT_SIZE)

        try:
            if self.air_targets_in_proximity:
                prio_targets:Unit = \
                    self.air_targets_in_proximity.filter\
                        (lambda unit: unit.type_id in PRIO_ATTACK_TARGET and\
                        unit.distance_to(self.unit) <= self.unit.air_range+RANGE_BUFFER
                        )
                if prio_targets:
                    target = prio_targets.closest_to(self.unit)
                else:
                    target = self.enemies_in_proximity.closest_to(self.unit.position)

            elif self.ground_targets_in_proximity:
                prio_targets:Unit = \
                    self.air_targets_in_proximity.filter\
                        (lambda unit: unit.type_id in PRIO_ATTACK_TARGET and\
                        unit.distance_to(self.unit) <= self.unit.air_range+RANGE_BUFFER
                        )
                if prio_targets:
                    target = prio_targets.closest_to(self.unit)
                else:
                    target = self.enemies_in_proximity.closest_to(self.unit.position)

            else:
                target:Union[Unit, Point2] = attack_target
            if self.bot.debug and self.unit:
                try:
                    self.bot.debug_tools.debug_targeting(self, target)
                # pylint: disable=W0718
                except Exception as e:
                    logger.warning(f"can't run debug method for {self.unit} due to {e}")


            if not self.unit.distance_to(target) <= self.unit.air_range+RANGE_BUFFER:
                if isinstance(target,Union[Unit, UnitMarker]):
                    target = target.position

                move_to:Point2 = self.bot.pathing.find_path_next_point(
                            self.unit.position, target, self.pathing_grid
                        )
                self.unit.move(move_to)
                return
            if target.is_flying:
                if self.unit.weapon_cooldown <= 5:
                    self.unit.attack(target)

                else:
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
        self.unit.move(move_to)
