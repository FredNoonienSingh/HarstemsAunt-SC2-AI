from typing import Union
from math import sin, pi, cos

from sc2.unit import Unit
from sc2.bot_ai import BotAI
from sc2.position import Point2, Point3, Pointlike

class DebugTools:

    def __init__(self, bot:BotAI) -> None:
        self.bot = bot

    def debug_build_pos(self, pos:Union[Point2, Point3, Pointlike]):
        z = self.bot.get_terrain_z_height(pos)+1
        x,y = pos.x, pos.y
        pos_3d = Point3((x,y,z))
        self.bot.client.debug_sphere_out(pos_3d ,.2, (255,255,0))

    def draw_gameinfo(self):
        text:str = ""
        supply:int = self.bot.supply_army
        enemy_supply:int=self.bot.enemy_supply
        text = text +(f"supply: {supply}\nenemy_supply: {enemy_supply}\n")
        minerals:int= self.bot.minerals
        gas:int = self.bot.vespene
        text = text +(f"\nIncome: {minerals, gas}\n")
        self.bot.client.debug_text_screen(str(text), (0,.125), color=None, size=14)

    def unit_label(self, unit:Unit):
        text:str=f"Type: {unit.type_id}\nHealth: {unit.health}\nOrders: {unit.orders} \nPos {unit.position3d}"
        self.bot.client.debug_text_world(text,unit,color=(255,90,0),size=12)

    def unit_range(self, unit:Unit):
        if unit.can_attack_ground:
            self.bot.client.debug_sphere_out(unit,unit.ground_range,(0,255,0))
        if unit.can_attack_air:
            self.bot.client.debug_sphere_out(unit,unit.air_range,(255,0,25))

    def render_unit_vision(self, unit:Unit):
        terrain_height = self.bot.get_terrain_z_height(unit)+1
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
            line: Point3 = Point3((x,y, self.bot.get_terrain_z_height(Point2((x,y)))+1))
            color: tuple = (0, 255, 0)
            if not self.bot.game_info.pathing_grid.is_set(Point2((int(line.x), int(line.y)))):
                color :tuple= (0, 0, 255)
            self.bot.client.debug_sphere_out(Point3((x,y,terrain_height)), .1, color)
            self.bot.client.debug_line_out(origin, line, color)