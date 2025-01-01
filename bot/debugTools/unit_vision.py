from math import sin, pi, cos

from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.position import Point3, Point2

def render_unit_vision(bot: BotAI, unit:Unit):
    terrain_height = bot.get_terrain_z_height(unit)+1
    origin:Unit = unit
    num_points:int = 16  # Number of points on the circle
    angle_increment = 2*pi / num_points  # Angle increment between points
    radius:float = 4
    target_x:float = origin.position_tuple[0] # X-coordinate of the target point
    target_y:float = origin.position_tuple[1]  # Y-coordinate of the target point
    # Iterate through a range of angles
    for i in range(num_points):
        angle:float = i * angle_increment
        x:float = target_x + radius * cos(angle)
        y:float = target_y + radius * sin(angle)
        line: Point3 = Point3((x,y, bot.get_terrain_z_height(Point2((x,y)))+1))
        color: tuple = (0, 255, 0)
        if not bot.game_info.pathing_grid.is_set(Point2((int(line.x), int(line.y)))):
            color :tuple= (0, 0, 255)
        bot.client.debug_sphere_out(Point3((x,y,terrain_height)), .1, color)
        bot.client.debug_line_out(origin, line, color)