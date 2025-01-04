from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId
from actions.build_army import \
    build_gateway_units, build_stargate_units, build_robo_units

from HarstemsAunt.common import UNIT_COMPOSIOTION

async def build_army(bot:BotAI) -> None:
    #TODO: #53 Find a better way to control Army composition
    #TODO: #54 Implement a Check for detectors in Enemy Comp, if not at DTs

    stalkers:int = len(bot.units(UnitTypeId.STALKER))
    # +1 to avoid ZeroDivision exception
    zealots:int = len(bot.units(UnitTypeId.ZEALOT)) +1
    
    if not stalkers or stalkers/zealots < 3:
        await build_gateway_units(bot, UnitTypeId.STALKER)
    else:
        await build_gateway_units(bot, UnitTypeId.ZEALOT)
       # await build_stargate_units(bot, UnitTypeId.PHOENIX)

    if not bot.units(UnitTypeId.OBSERVER):
        await build_robo_units(bot, UnitTypeId.OBSERVER)
    else:
        await build_robo_units(bot, UnitTypeId.IMMORTAL)