from sc2.unit import Unit
from sc2.bot_ai import BotAI
from sc2.position import Point2, Point3
from sc2.ids.unit_typeid import UnitTypeId



async def micro(bot: BotAI) -> None:
    """Handles Micro of Fighting Units

    Args:
        bot (BotAI): Instance of HarstemsAunt
    """

    army_target = bot.get_attack_target
    z = bot.get_terrain_z_height(army_target)+1
    x,y = army_target.x, army_target.y
    pos_3d = Point3((x,y,z))

    bot.client.debug_sphere_out(pos_3d, 3, (255,200,255))

    # call attack method in our reaper class
    await bot.stalkers.handle_attackers(
            bot.units(UnitTypeId.STALKER), army_target
    )