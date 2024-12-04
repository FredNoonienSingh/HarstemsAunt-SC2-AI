
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from utils.can_build import can_research_upgrade

def get_upgrades(bot:BotAI) -> None:

    attack = [
        UpgradeId.PROTOSSGROUNDWEAPONSLEVEL1,
        UpgradeId.PROTOSSGROUNDWEAPONSLEVEL2,
        UpgradeId.PROTOSSGROUNDWEAPONSLEVEL3,
    ]
    
    amor = [
        UpgradeId.PROTOSSGROUNDARMORSLEVEL1,
        UpgradeId.PROTOSSGROUNDARMORSLEVEL2,
        UpgradeId.PROTOSSGROUNDARMORSLEVEL3
    ]

    for forge in bot.structures(UnitTypeId.FORGE):
            for upgrades in attack:
                if upgrades not in bot.researched:
                   upgrade(bot, UnitTypeId.FORGE, upgrade)
            for upgrades in amor:
                if upgrades not in bot.researched:
                    upgrade(bot, UnitTypeId.FORGE, upgrade)

    if bot.structures(UnitTypeId.TWILIGHTCOUNCIL):
        if not UpgradeId.BLINKTECH in bot.researched:
            upgrade(bot, UnitTypeId.TWILIGHTCOUNCIL, UpgradeId.BLINKTECH)
        if not UpgradeId.CHARGE in bot.researched:
            upgrade(bot, UnitTypeId.TWILIGHTCOUNCIL, UpgradeId.CHARGE)
    


def upgrade(bot:BotAI, Upgrade_structure:UnitTypeId, Upgrade_id:UpgradeId) -> None:
        if bot.structures(Upgrade_structure).idle and can_research_upgrade(bot,Upgrade_id):
            bot.research(Upgrade_id)
 