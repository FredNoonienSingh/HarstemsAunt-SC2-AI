from sc2.unit import Unit
from sc2.bot_ai import BotAI
from sc2.position import Point2, Point3
from sc2.ids.unit_typeid import UnitTypeId

from utils.get_army_target import get_army_target
from actions.unit_controll import control_stalkers,\
    control_phoenix, control_zealots

async def micro(bot: BotAI) -> None:
    """Handles Micro of Fighting Units

    Args:
        bot (BotAI): Instance of HarstemsAunt
    """

    army_target = get_army_target(bot)
    z = bot.get_terrain_z_height(army_target)+1
    x,y = army_target.x, army_target.y
    pos_3d = Point3((x,y,z))

    bot.client.debug_sphere_out(pos_3d, 3, (255,200,255))

    for zealot in bot.units(UnitTypeId.ZEALOT):
        await control_zealots(bot, zealot,army_target)
    await control_stalkers(bot, army_target)
    await control_phoenix(bot)