"""SC2 Imports"""
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId

"""MACRO"""
from macro.upgrade import get_upgrades
from macro.game_start import game_start
from macro.build_army import build_army
from macro.infrastructure import build_infrastructure

"""Actions"""
from actions.expand import expand
from actions.build_structure import build_gas
from actions.build_supply import build_supply
from actions.chronoboosting import chronoboosting

"""Utils"""
from utils.can_build import can_build_unit
from utils.handle_alerts import handle_alerts


async def marco(bot:BotAI, worker, build_pos) -> None:
    await chronoboosting(bot)
    await build_infrastructure(bot,worker, build_pos)
    get_upgrades(bot)
    await build_army(bot)
    await build_supply(bot, build_pos)
    await expand(bot)
    handle_alerts(bot, bot.alert)

    if bot.time < 180:
        await game_start(bot, worker)

    for townhall in bot.townhalls:
        minerals = bot.expansion_locations_dict[townhall.position].mineral_field

        if not minerals:
            if not townhall in bot.mined_out_bases:
                bot.mined_out_bases.append(townhall)

        if not len(bot.mined_out_bases) == len(bot.temp):
            bot.base_count += 1
            bot.temp = bot.mined_out_bases


        if townhall.is_ready and bot.structures(UnitTypeId.PYLON) \
            and bot.structures(UnitTypeId.GATEWAY) and\
            len(bot.structures(UnitTypeId.ASSIMILATOR)) < bot.gas_count \
            and not bot.already_pending(UnitTypeId.ASSIMILATOR):
                await build_gas(bot, townhall)
        # Build_Probes
        probe_count:int = len(bot.structures(UnitTypeId.NEXUS))*16 + len(bot.structures(UnitTypeId.ASSIMILATOR))*3
        if townhall.is_idle and can_build_unit(bot, UnitTypeId.PROBE) and len(bot.workers) < probe_count:
            townhall.train(UnitTypeId.PROBE)
