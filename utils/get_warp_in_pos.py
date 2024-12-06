from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId


def get_warp_in_pos(bot:BotAI):
    if not bot.units(UnitTypeId.WARPPRISM):
        if bot.supply_army > 10:
            return bot.structures(UnitTypeId.PYLON).in_closest_distance_to_group([x for x in bot.units if x not in bot.workers])
        else:
            return bot.structures(UnitTypeId.PYLON).closest_to(bot.enemy_start_locations[0]).position.towards(bot.enemy_start_locations[0], distance=1, limit=False)
    else:
        if bot.enemy_units:
            active_prism = bot.units(UnitTypeId.WARPPRISM).closest_to(bot.enemy_units.center)
        else:
           active_prism = bot.units(UnitTypeId.WARPPRISM).closest_to(bot.enemy_start_locations[0]) 
        return active_prism.position
