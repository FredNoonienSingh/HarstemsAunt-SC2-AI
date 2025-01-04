""" Currently not in Use -> can be removed after refactoring """
from sc2.bot_ai import BotAI
from sc2.unit import Unit
from sc2.units import Units


async def stay_out_of_range(bot:BotAI, unit:Unit):
    enemy_units:Units = bot.enemy_units.closer_than(15, unit)
    # 15 is the hightest attack range in the Game / any unit further away cant be in range 
    enemy_structures:Units = bot.enemy_structures.closer_than(8, unit)
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

    