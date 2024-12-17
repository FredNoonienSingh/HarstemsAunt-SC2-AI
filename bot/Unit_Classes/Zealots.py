
from typing import Optional

import numpy as np

from sc2.unit import Unit
from sc2.units import Units
from sc2.position import Point2

from Unit_Classes.baseClassGround import BaseClassGround
from HarstemsAunt.common import ATTACK_TARGET_IGNORE

MIN_SHIELD_AMOUNT = 0.5

class Zealot(BaseClassGround):
    # Overwritten from BaseClassGround
    async def handle_attackers(self, units: Units, attack_target: Point2) -> None:
        grid: np.ndarray = self.pathing.ground_grid
        for unit in units:
            if unit.shield_percentage < MIN_SHIELD_AMOUNT \
                and not self.pathing.is_position_safe(grid, unit.position):
                unit.move(
                    self.pathing.find_path_next_point(
                        unit.position, self.get_recharge_spot, grid
                    )
                )
                continue

            close_enemies: Units = self.bot.enemy_units.filter(
                lambda u: u.position.distance_to(unit) < 15.0
                and not u.is_flying
                and unit.type_id not in ATTACK_TARGET_IGNORE
            )

            target: Optional[Unit] = None
            if close_enemies:
                in_attack_range: Units = close_enemies.in_attack_range_of(unit)
                if in_attack_range:
                    target = self.pick_enemy_target(in_attack_range, unit)
                else:
                    target = self.pick_enemy_target(close_enemies, unit)

            if target:
                unit.attack(target)
                continue

            if not self.pathing.is_position_safe(grid, unit.position):
                self.move_to_safety(unit, grid)
                continue

            if unit.distance_to(attack_target) > 5:
                if close_enemies:
                    unit.move(
                        self.pathing.find_path_next_point(
                            unit.position, attack_target, grid
                        )
                    )
                else:
                    unit.move(attack_target)
            else:
                unit.attack(attack_target)

    @staticmethod
    def pick_enemy_target(enemies: Units, unit: Unit) -> Unit:
        fighting_units: Units = enemies.filter(lambda unit: unit.ground_dps > 5)
        if fighting_units:
            return fighting_units.closest_to(unit)
        return enemies.closest_to(unit)
