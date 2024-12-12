from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId
from actions.build_army import \
    build_gateway_units, build_stargate_units

async def build_army(bot:BotAI) -> None:
    
    zealot_count = len(bot.units(UnitTypeId.ZEALOT)) if bot.units(UnitTypeId.ZEALOT) else 3
    stalker_count = len(bot.units(UnitTypeId.STALKER)) if bot.units(UnitTypeId.STALKER) else 1
    
    if stalker_count/zealot_count <= 3:
        await build_gateway_units(bot, UnitTypeId.STALKER)
    else:
        await build_gateway_units(bot, UnitTypeId.ZEALOT)
    await build_stargate_units(bot, UnitTypeId.PHOENIX)
