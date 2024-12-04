from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId
from actions.stay_out_range import stay_out_of_range
from utils.in_proximity import is_close_to_unit

from actions.abilliies import blink

async def control_stalkers(bot:BotAI):
    for stalker in bot.units(UnitTypeId.STALKER):
        if stalker.weapon_ready and stalker.shield_percentage > .55:
            if bot.enemy_units:
                attack_pos = stalker.position3d.towards(bot.enemy_units.closest_to(stalker), 12)
            elif bot.enemy_structures:
                attack_pos = stalker.position3d.towards(bot.enemy_structures.closest_to(stalker), 12)
            else:
                attack_pos = stalker.position3d.towards(bot.enemy_start_locations[0], 12)
            stalker.attack(attack_pos)
        else:
            if [x for x in bot.enemy_units if x.can_attack]:
                pos = stalker.position3d.towards(bot.enemy_units.closest_to(stalker), -15)
                if await bot.can_cast(stalker, AbilityId.EFFECT_BLINK, pos) and stalker.shield_percentage < .33:
                    await blink(bot, stalker, pos)
                else:
                    stalker.move(pos)

async def control_zealots(bot:BotAI):
    
    target_types:list = [
    UnitTypeId.HATCHERY, 
    UnitTypeId.LAIR, 
    UnitTypeId.HIVE,
    UnitTypeId.COMMANDCENTER, 
    UnitTypeId.ORBITALCOMMAND,
    UnitTypeId.PLANETARYFORTRESS,
    UnitTypeId.NEXUS
    ]
    if bot.enemy_units:
        targets = bot.enemy_structures.filter(lambda unit: unit.type_id in target_types)
        for zealot in bot.units(UnitTypeId.ZEALOT):
            zealot.attack(bot.enemy_start_locations[0])

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
                    