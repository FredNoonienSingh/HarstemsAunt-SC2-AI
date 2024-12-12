from sc2.bot_ai import BotAI
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.unit_typeid import UnitTypeId


def can_build_structure(bot:BotAI, structure_id)-> bool:
    return bot.can_afford(structure_id) and bot.tech_requirement_progress(structure_id)

def can_build_unit(bot:BotAI, unit_id, probe_limit:int=66) ->bool:
    if unit_id == UnitTypeId.PROBE and bot.can_feed(UnitTypeId.PROBE) and len(bot.units(unit_id)) > probe_limit:
        return False
    return bot.can_afford(unit_id) and bot.can_feed(unit_id) and bot.tech_requirement_progress(unit_id)

def can_research_upgrade(bot:BotAI,upgrade_id)->bool:
    return bot.can_afford(upgrade_id) and not bot.already_pending_upgrade(upgrade_id) and bot.tech_requirement_progress(upgrade_id)

