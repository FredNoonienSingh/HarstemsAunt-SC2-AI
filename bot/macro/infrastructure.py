from typing import Union

from sc2.bot_ai import BotAI
from sc2.data import Race
from sc2.unit import Unit
from sc2.position import Point2, Point3
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId

from actions.build_structure import build_structure
from utils.can_build import can_build_structure

from HarstemsAunt.common import INITIAL_TECH

async def build_infrastructure(bot:BotAI, worker:Unit, build_pos: Union[Point2,Point3,Unit]) -> None:
    enemy_race: Race = bot.enemy_race
    tech_buildings: list = INITIAL_TECH.get(enemy_race)
    tech_0: UnitTypeId = tech_buildings[0]
    tech_1: UnitTypeId = tech_buildings[1]

    if not bot.structures(UnitTypeId.PYLON) and can_build_structure(bot, UnitTypeId.PYLON):
        await bot.build(UnitTypeId.PYLON, build_worker=worker, near=build_pos, max_distance=0)
    if not bot.structures(UnitTypeId.GATEWAY) and not bot.structures(UnitTypeId.WARPGATE) \
        and can_build_structure(bot, UnitTypeId.GATEWAY):
            await bot.build(UnitTypeId.GATEWAY, build_worker=worker, near=build_pos)
    