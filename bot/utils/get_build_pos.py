from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId

def get_build_pos(bot:BotAI):
    if not bot.structures(UnitTypeId.PYLON):
       return bot.main_base_ramp.protoss_wall_pylon
    elif not bot.structures(UnitTypeId.GATEWAY) and not bot.already_pending(UnitTypeId.GATEWAY):
        return bot.main_base_ramp.protoss_wall_warpin
    else:
        return bot.structures(UnitTypeId.NEXUS)[0].position3d.towards(bot.game_info.map_center, 5)
    
