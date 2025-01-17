from typing import Optional

import numpy as np

from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.position import Point2

# pylint: disable=E0401
from HarstemsAunt.pathing import Pathing
from HarstemsAunt.common import ATTACK_TARGET_IGNORE,PRIO_ATTACK_TARGET

class BaseClassGround:

    def __init__(self, bot:BotAI, pathing:Pathing):
        self.bot:BotAI=bot
        self.pathing:Pathing=pathing

    @property
    def get_recharge_spot(self) -> Point2:
        return self.pathing.find_closest_safe_spot(
            self.bot.game_info.map_center, self.pathing.ground_grid
        )

    async def handle_attackers(self, units: Units, attack_target: Point2) -> None:
        grid: np.ndarray = self.pathing.ground_grid

        for unit in units:
            enemies = self.bot.enemy_units.\
                filter(lambda enemy: enemy.distance_to(unit) > unit.range+12)
            if enemies:
                attack_pos = self.pick_enemy_target(enemies, unit)
            else:
                attack_pos = self.pathing.find_path_next_point(
                    unit.position, attack_target, grid
                )
            unit.attack(attack_pos)

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

    async def stay_out_of_range(self, unit:Unit):
        enemy_units:Units = self.bot.enemy_units.closer_than(15, unit)
        # 15 is the hightest attack range in the Game / any unit further away cant be in range 
        enemy_structures:Units = self.bot.enemy_structures.closer_than(8, unit)
        # 8 is the range of a turret with range upgrade - no structure has a higher range 
        possible_threads: list = [unit for unit in enemy_units]
        for structure in enemy_structures:
            possible_threads.append(structure)
        for enemy in possible_threads:
            if not enemy.can_attack:
                continue
            if unit.is_flying:
                if enemy.can_attack_air and enemy.distance_to(unit)< enemy.air_range+2:
                    unit.move(unit.position.towards(enemy, -1))
                    continue
            if enemy.can_attack_ground and enemy.distance_to(unit)<enemy.ground_range+2:
                unit.move(unit.position.towards(enemy, -5))

    @staticmethod
    def pick_enemy_target(enemies: Units, attacker:Unit) -> Unit:
        #TODO: #35 This should not be tinkered with any further, TARGETING will take care of it
        prio_targets = enemies.filter(lambda unit: unit.type_id in PRIO_ATTACK_TARGET\
            and not unit in ATTACK_TARGET_IGNORE)
        if prio_targets:
            return prio_targets.closest_to(attacker)
        return min(
            enemies,
            key=lambda e: (e.health + e.shield, e.tag),
        )
