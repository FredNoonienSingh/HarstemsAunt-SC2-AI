from typing import Union

from sc2.bot_ai import BotAI
from sc2.ids.ability_id import AbilityId
from sc2.unit import Unit
from sc2.position import Point3


async def set_rally(bot:BotAI, unit:Unit, target:Union[Point3, Unit]):
    bot.do(unit(AbilityId.RALLY_BUILDING,target))

async def set_nexus_rally(bot:BotAI, nexus:Unit, target:Union[Point3, Unit]):
    bot.do(nexus(AbilityId.RALLY_NEXUS, target))