from typing import Optional

import numpy as np

from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.position import Point2
from sc2.ids.ability_id import AbilityId

from HarstemsAunt.pathing import Pathing
from HarstemsAunt.common import ATTACK_TARGET_IGNORE, ALL_STRUCTURES,\
    logger

MIN_SHIELD_AMOUNT:float = 0.25

class Stalkers:
    def __init__(self, bot:BotAI, pathing: Pathing):
        self.bot: BotAI = bot
        self.pathing: Pathing = pathing
        
        self.blink_range: float = self.bot.game_data.abilities[
            AbilityId.EFFECT_BLINK_STALKER.value
        ]._proto.cast_range

    @property
    def get_recharge_spot(self) -> Point2:
        return self.pathing.find_closest_safe_spot(
            self.bot.game_info.map_center, self.pathing.ground_grid
        )

    async def handle_attackers(self, units: Units, attack_target: Point2) -> None:
        grid: np.ndarray = self.pathing.ground_grid
        for unit in units:
            # pull back low health reapers to heal
            if unit.health_percentage < MIN_SHIELD_AMOUNT:
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


            # check for nearby target fire
            target: Optional[Unit] = None
            if close_enemies:
                in_attack_range: Units = close_enemies.in_attack_range_of(unit)
                if in_attack_range:
                    target = self.pick_enemy_target(in_attack_range)
                else:
                    target = self.pick_enemy_target(close_enemies)

            if target and unit.weapon_cooldown == 0:
                unit.attack(target)
                continue

            # no target and in danger, run away
            if not self.pathing.is_position_safe(grid, unit.position):
                self.move_to_safety(unit, grid)
                continue

            # get to the target
            if unit.distance_to(attack_target) > 5:
                # only make pathing queries if enemies are close
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

    def move_to_safety(self, unit: Unit, grid: np.ndarray):
        """
        Find a close safe spot on our grid
        Then path to it
        """
        safe_spot: Point2 = self.pathing.find_closest_safe_spot(unit.position, grid)
        move_to: Point2 = self.pathing.find_path_next_point(
            unit.position, safe_spot, grid
        )
        unit.move(move_to)

    @staticmethod
    def pick_enemy_target(enemies: Units) -> Unit:
        """For best enemy target from the provided enemies
        TODO: If there are multiple units that can be killed in one shot,
        pick the highest value one
        """
        return min(
            enemies,
            key=lambda e: (e.health + e.shield, e.tag),
        )

    async def _do_blink(self):
        logger.info(f"BLINK is not yet implemented")