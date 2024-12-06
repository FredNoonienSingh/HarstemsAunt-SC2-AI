
from typing import Union

from sc2.unit import Unit
from sc2.bot_ai import BotAI
from sc2.position import Point2, Point3
from sc2.ids.ability_id import AbilityId
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.unit_typeid import UnitTypeId
from utils.can_build import can_build_unit

from utils.get_warp_in_pos import get_warp_in_pos

async def warp_in_unit(bot: BotAI, unit:UnitTypeId, warp_in_position:Union[Point3, Unit]) -> bool:
    pos = warp_in_position.position.to2.random_on_distance(4)
    placement = await bot.find_placement(AbilityId.WARPGATETRAIN_STALKER, pos, placement_step=1)

    for gate in bot.structures(UnitTypeId.WARPGATE).idle:
        if can_build_unit(bot, unit):
            gate.warp_in(unit, placement)
            return True
        break
    return False

async def build_gateway_units(bot:BotAI,unit_type:UnitTypeId):
    if can_build_unit(bot, unit_type):
        for gate in bot.structures(UnitTypeId.GATEWAY):
            if gate.is_idle and UpgradeId.WARPGATERESEARCH not in bot.researched:
                gate.train(unit_type)
            else:
                warp_in_pos = get_warp_in_pos(bot)
                await warp_in_unit(bot, unit_type, warp_in_pos)

async def build_stargate_units(bot:BotAI, unit_type:UnitTypeId):
    if can_build_unit(bot, unit_type):
        for gate in bot.structures(UnitTypeId.STARGATE):
            if gate.is_idle:
                gate.train(unit_type)

async def build_robo_units(bot:BotAI, unit_type:UnitTypeId):
    if can_build_unit(bot, unit_type):
        for robo in bot.structures(UnitTypeId.ROBOTICSFACILITY):
            if robo.is_idle:
                robo.train(unit_type)

