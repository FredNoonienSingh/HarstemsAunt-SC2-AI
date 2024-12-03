
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from utils.can_build import can_research_upgrade

def get_upgrades(bot:BotAI) -> None:
    if bot.structures(UnitTypeId.TWILIGHTCOUNCIL).idle and can_research_upgrade(bot,UpgradeId.BLINKTECH):
        bot.research(UpgradeId.BLINKTECH)

    if bot.units(UnitTypeId.ZEALOT):
        if bot.structures(UnitTypeId.TWILIGHTCOUNCIL).idle and can_research_upgrade(bot,UpgradeId.CHARGE):
            bot.research(UpgradeId.CHARGE)
