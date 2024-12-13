from typing import Union
from random import choice

from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.position import Point2, Point3
from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId
from HarstemsAunt.common import TOWNHALL_IDS

from actions.abilliies import blink
from utils.in_proximity import is_close_to_unit
from actions.stay_out_range import stay_out_of_range

async def control_stalkers(bot:BotAI, target_pos:Union[Point2, Point3]):
    for stalker in bot.units(UnitTypeId.STALKER):
        if bot.enemy_units.filter(lambda unit: unit.type_id not in [UnitTypeId.LARVA, UnitTypeId.EGG]):
            visible_units = bot.enemy_units.filter(lambda unit: unit.type_id not in [UnitTypeId.LARVA, UnitTypeId.EGG])\
                .closer_than(stalker.sight_range, stalker)
            enemy_structs = bot.enemy_structures.closer_than(20, stalker)

            if stalker.weapon_ready:
                if visible_units:
                    target = visible_units.closest_to(stalker)
                    stalker.attack(target)
                if not visible_units and enemy_structs:
                    target = enemy_structs.closest_to(stalker)
                    stalker.attack(target)

            elif not stalker.weapon_ready and visible_units:
                threads = bot.enemy_units.filter(lambda Unit: Unit.distance_to(stalker) <= Unit.ground_range+2)
                if threads:
                    target = stalker.position.towards(threads.closest_to(stalker), -5)
                    stalker.move(target)
                else:
                    return
            else:
                stalker.attack(target_pos)
        else:
            stalker.attack(target_pos)

async def control_zealots(bot:BotAI,zealot, target_pos):
    target_types:list = TOWNHALL_IDS
    if bot.enemy_units:
        targets = bot.enemy_structures.filter(lambda unit: unit.type_id in target_types)
        if targets:
            target = targets.furthest_to(bot.enemy_units.center)
        else:
            target = bot.enemy_start_locations[0]
        zealot.attack(target.position.towards(bot.game_info.map_center, -5))
    else:
        zealot.attack(target_pos)

async def control_phoenix(bot:BotAI):
    targets = bot.enemy_units.filter(lambda unit: unit.is_flying)
    threads = bot.enemy_units.filter(lambda unit: unit.can_attack_air)
    for phoenix in bot.units(UnitTypeId.PHOENIX):
        if phoenix.weapon_ready and phoenix.shield_percentage > .55:
            if targets:
                attack_targets = targets.sorted(lambda u: u.health + u.shield,True)
                if attack_targets:
                    phoenix.attack(attack_targets[0].position)
                else:
                    phoenix.attack(targets.closest_distance_to(phoenix))
            else:
                for expansion in list(bot.expand_locs):
                    phoenix.move(expansion, True)
        else:
            for thread in threads:
                if phoenix.distance_to(thread) <= thread.air_range:
                    phoenix.move(phoenix.position3d.towards(thread, -thread.air_range+1))
                    