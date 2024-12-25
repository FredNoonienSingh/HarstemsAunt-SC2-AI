
from typing import Optional

import numpy as np

from sc2.unit import Unit
from sc2.units import Units
from sc2.position import Point2

from Unit_Classes.baseClassGround import BaseClassGround
from HarstemsAunt.common import ATTACK_TARGET_IGNORE


class Zealot(BaseClassGround):
    # Overwritten from BaseClassGround

    async def handle_attackers(self, units: Units, attack_target: Point2) -> None:
        grid: np.ndarray = self.pathing.ground_grid
        for unit in units:
            friendly_units = self.bot.units.filter(lambda u: u.tag != unit.tag)
            friendly_positions = [unit.position for unit in friendly_units]
            enemies = self.bot.enemy_units.closer_than(15, unit)
            if not enemies.filter(lambda unit:
                unit.ground_dps > 0 and
                not unit.is_flying
                ):
                attack_pos = self.pathing.find_path_next_point(
                    unit.position, attack_target, grid
                )
                if attack_pos not in friendly_positions:
                    unit.attack(attack_pos)
                else:
                    attack_pos = self.pathing.find_path_next_point(
                        friendly_units.closest_to(unit).position, attack_target, grid
                    )
                    unit.attack(attack_pos)
                return
            unit.attack(self.pick_enemy_target(enemies, unit))
            return

    async def retreat(self, retreat_pos: Point2):
        grid: np.ndarray = self.pathing.ground_grid
        for unit in self.units:
            move_to: Point2 = self.pathing.find_path_next_point(
            unit.position, retreat_pos, grid
            )
            unit.move(move_to)

    @staticmethod
    def pick_enemy_target(enemies: Units, unit: Unit) -> Unit:
        fighting_units: Units = enemies.filter(lambda unit:
            unit.ground_dps > 5 and
            not unit.is_flying
            )
        if fighting_units:
            return fighting_units.closest_to(unit)
        return enemies.closest_to(unit)
