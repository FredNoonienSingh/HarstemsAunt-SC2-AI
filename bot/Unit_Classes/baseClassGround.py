from typing import Optional

import numpy as np

from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.position import Point2

from HarstemsAunt.pathing import Pathing
from HarstemsAunt.common import ATTACK_TARGET_IGNORE, MIN_SHIELD_AMOUNT,\
    ALL_STRUCTURES, PRIO_ATTACK_TARGET, logger

class BaseClassGround:
    def __init__(self, bot:BotAI, pathing:Pathing):
        self.bot:BotAI=bot
        self.pathing:Pathing=pathing

    @property
    def get_recharge_spot(self) -> Point2:
        # Thats stupid, unless the recharge rate is insane
        
        return self.pathing.find_closest_safe_spot(
            self.bot.game_info.map_center, self.pathing.ground_grid
        )
    
    async def handle_attackers(self, units: Units, attack_target: Point2) -> None:
        grid: np.ndarray = self.pathing.ground_grid
        for stalker in units:
            
            
            # Keep out of Range, if Shields are low, removes to much supply from fights to fast
            if stalker.shield_percentage < MIN_SHIELD_AMOUNT \
                and not self.pathing.is_position_safe(grid, stalker.position):
                self.move_to_safety(stalker, grid)
                continue

            # When enemy_units are visible
            if self.bot.enemy_units:
                visible_units = self.bot.enemy_units.closer_than(stalker.ground_range+2, stalker)
                enemy_structs = self.bot.enemy_structures.closer_than(20, stalker)

                # Attack if Possible
                if stalker.weapon_ready:
                    if visible_units:
                        target = self.pick_enemy_target(visible_units, stalker)
                        stalker.attack(target)
                    if not visible_units and enemy_structs:
                        target = enemy_structs.closest_to(stalker)
                        stalker.attack(target)
                    if not visible_units and not enemy_structs:
                        stalker.attack(
                            self.pathing.find_path_next_point(
                            stalker.position, attack_target, grid
                            )
                        )

                # Move out of range if attacking is not possible
                elif not stalker.weapon_ready and visible_units:
                    threads = self.bot.enemy_units.filter(lambda Unit: Unit.distance_to(stalker) <= Unit.ground_range+1)
                    if threads:
                        if not self.pathing.is_position_safe(grid, stalker.position):
                            self.move_to_safety(stalker, grid)
                        else:
                            continue
                else:
                    stalker.attack(
                         self.pathing.find_path_next_point(
                        stalker.position, attack_target, grid
                    )
                    )
            else:
                stalker.attack(
                     self.pathing.find_path_next_point(
                        stalker.position, attack_target, grid
                    )
                )

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
    def pick_enemy_target(enemies: Units, attacker:Unit) -> Unit:
        #TODO: This should not be tinkered with any further, TARGETING will take care of it
        prio_targets = enemies.filter(lambda unit: unit.type_id in PRIO_ATTACK_TARGET)
        if prio_targets:
            return prio_targets.closest_to(attacker)
        return min(
            enemies,
            key=lambda e: (e.health + e.shield, e.tag),
        )
