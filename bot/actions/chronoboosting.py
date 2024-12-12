
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.ids.buff_id import BuffId
from actions.abilliies import chronoboost

async def chronoboosting(bot:BotAI) -> None:
    structures = bot.structures.filter(lambda struct: not struct.is_idle and \
        not struct.has_buff(BuffId.CHRONOBOOSTENERGYCOST))
    chrono_nexus = bot.structures(UnitTypeId.NEXUS).filter(lambda nexus: nexus.energy > 50)
    if structures:
        for nexus in chrono_nexus:
            await chronoboost(bot, nexus,structures[0])