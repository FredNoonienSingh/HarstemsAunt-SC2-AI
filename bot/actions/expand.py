""" Holds Function to Expand """

from typing import Union
from sc2.bot_ai import BotAI
from sc2.position import Point2, Point3
from sc2.ids.unit_typeid import UnitTypeId


async def expand(bot:BotAI):
    if not bot.already_pending(UnitTypeId.NEXUS) and len(bot.structures(UnitTypeId.NEXUS))<bot.base_count:
        location:Union[Point2,Point3] = await bot.get_next_expansion()
        if location:
            if not bot.enemy_units.filter(lambda unit: unit.distance_to(location) < 2.75):
                # Misplacing townhalls causes the Bot to crash, therefore it must be checked if the
                # Area is free to build
                # 2.75 is the radius of a nexus -
                # if a unit is closer than this a nexus would be build away from the location
                await bot.build(UnitTypeId.NEXUS, near=location, max_distance=0)