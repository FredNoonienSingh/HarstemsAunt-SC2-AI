from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId
from utils.can_build import can_build_structure

async def build_supply(bot: BotAI, build_pos) -> None:
    if not bot.can_afford(UnitTypeId.PYLON) or bot.supply_cap == 200:
        return
    if can_build_structure(bot,UnitTypeId.PYLON) and not \
        bot.already_pending(UnitTypeId.PYLON) and bot.supply_left < 8 \
            and len(bot.structures(UnitTypeId.NEXUS))>= 2 and bot.structures(UnitTypeId.CYBERNETICSCORE):
        worker = bot.workers.prefer_idle.closest_to(build_pos)
        await bot.build(UnitTypeId.PYLON, build_worker=worker, near=build_pos)