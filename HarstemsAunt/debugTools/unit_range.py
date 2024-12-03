from sc2.unit import Unit
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId

def unit_range(bot: BotAI, unit: Unit):
    if unit.can_attack_ground:
        bot.client.debug_sphere_out(unit ,unit.ground_range, (0,255,0))
    if unit.can_attack_air: 
        bot.client.debug_sphere_out(unit, unit.air_range, (255, 0, 25))