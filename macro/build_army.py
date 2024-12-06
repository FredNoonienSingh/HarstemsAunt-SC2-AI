from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId
from actions.build_army import \
    build_gateway_units, build_stargate_units

async def build_army(bot:BotAI) -> None:
    if len(bot.units(UnitTypeId.STALKER)) > 20:
        await build_gateway_units(bot, UnitTypeId.ZEALOT)
    await build_gateway_units(bot, UnitTypeId.STALKER)
    await build_stargate_units(bot, UnitTypeId.PHOENIX)
