from typing import Union

from sc2.unit import Unit
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId
from sc2.position import Point2, Point3, Pointlike


def debug_build_pos(bot: BotAI, pos:Union[Point2, Point3, Pointlike]):
    z = bot.get_terrain_z_height(pos)+1
    x,y = pos.x, pos.y
    pos_3d = Point3((x,y,z))
    bot.client.debug_sphere_out(pos_3d ,.2, (255,255,0))