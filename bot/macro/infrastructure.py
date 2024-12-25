from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId

from actions.build_structure import build_structure
from utils.can_build import can_build_structure


async def build_infrastructure(bot:BotAI, worker, build_pos) -> None:
    # TODO: This needs to be reworked so it allows reactions to Enemy Comp
        if not bot.structures(UnitTypeId.PYLON) and can_build_structure(bot, UnitTypeId.PYLON):
            await bot.build(UnitTypeId.PYLON, build_worker=worker, near=build_pos, max_distance=0)
        if (len(bot.structures(UnitTypeId.GATEWAY))+len(bot.structures(UnitTypeId.WARPGATE)))<4\
            and can_build_structure(bot, UnitTypeId.GATEWAY):
            await bot.build(UnitTypeId.GATEWAY, build_worker=worker, near=build_pos)
        if not bot.structures(UnitTypeId.CYBERNETICSCORE) and len(bot.structures(UnitTypeId.NEXUS))==2:
            await build_structure(bot, UnitTypeId.CYBERNETICSCORE, build_pos, worker)
        if not bot.structures(UnitTypeId.TWILIGHTCOUNCIL) and not bot.already_pending(UnitTypeId.TWILIGHTCOUNCIL):
            await build_structure(bot, UnitTypeId.TWILIGHTCOUNCIL, build_pos, worker)