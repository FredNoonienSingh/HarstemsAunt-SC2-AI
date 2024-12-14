from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId
from actions.build_army import \
    build_gateway_units, build_stargate_units

from HarstemsAunt.common import UNIT_COMPOSIOTION

async def build_army(bot:BotAI) -> None:
    #TODO: Find a better way to control Army composition
    #TODO: Implement a Check for detectors in Enemy Comp, if not at DTs

    if True:
        await build_gateway_units(bot, UnitTypeId.ZEALOT)
    else:
        await build_gateway_units(bot, UnitTypeId.ZEALOT)
        await build_stargate_units(bot, UnitTypeId.PHOENIX)
