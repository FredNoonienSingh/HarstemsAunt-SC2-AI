from typing import Union

from sc2.bot_ai import BotAI
from sc2.position import Point2, Point3

from utils.in_proximity import in_proximity_to_point

def get_army_target(bot:BotAI) -> Union[Point2, Point3]:

    if bot.enemy_units:
        return bot.enemy_units.center
    else:
        return bot.enemy_start_locations[0]

def check_position(bot:BotAI) -> bool:
    if bot.units.filter(lambda unit: unit.distance_to(bot.last_enemy_army_pos) < unit.sight_range):
            return True
    return False