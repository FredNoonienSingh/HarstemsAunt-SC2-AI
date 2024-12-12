from typing import List

from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.game_info import Ramp
from sc2.position import Point2, Point3


class MapSector:
    def __init__(self,bot:BotAI,upper_left:Point2,lower_right:Point2):
        self.bot: BotAI = bot
        self.upper_left: Point2 = upper_left
        self.lower_right: Point2 = lower_right
        self.width:int = abs(upper_left.x - lower_right.x)
        self.height:int = abs(upper_left.y - lower_right.y)
        self.center:Point2 = Point2((abs(upper_left.x + self.width),\
            abs(self.upper_left.y - self.height)))
        self.ramps = None
        self.units = None
        self.enemy_units = None

    def render_sector(self) -> None:
        color = (255, 255, 0) if self.enemy_units else (255,0, 255)
        z_1 = 15
        z_2 = 15
        pos_1_3d = Point3((self.upper_left.x+20, self.upper_left.y+20, z_1))
        pos_2_3d = Point3((self.lower_right.x+20, self.lower_right.y+20, z_2))

        for ramp in self.ramps:
            x,y = ramp
            z = self.bot.get_terrain_z_height(ramp) + 1
            ramp_top_3d = Point3((x,y,z))
            self.bot.client.debug_sphere_out(ramp_top_3d,.2,(255,0,255))
        self.bot.client.debug_box_out(pos_1_3d, pos_2_3d, color)

    def ramps_in_sector(self) -> List:
        ramps = self.bot.game_info.map_ramps
        temp:list = []
        for ramp in ramps:
            if self.find_ramps_in_sector(ramp):
                x,y = ramp.top_center
                temp.append(Point2((x,y)))
        return temp

    def destructables_in_sector(self) -> Units:
        if self.bot.destructables:
            return self.bot.destructables.filter(lambda unit: self.in_sector(unit) is True)
        return None

    def units_in_sector(self) -> Units:
        if self.bot.units:
            return self.bot.units.filter(lambda unit: self.in_sector(unit) is True)
        return None

    def enemy_units_in_sector(self) -> Units:
        if self.bot.enemy_units:
            return self.bot.enemy_units.filter(lambda unit: self.in_sector(unit)is True)
        return None
    
    def find_ramps_in_sector(self, ramp: Point2) -> List:
        min_x, max_x = self.upper_left.x, self.lower_right.x
        min_y, max_y = self.upper_left.y,self.lower_right.y
        top_x, top_y = ramp.top_center.x, ramp.top_center.y
        return min_x <= top_x <= max_x and min_y <= top_y <= max_y


    def in_sector(self,unit:Unit) -> bool:
        min_x, max_x = self.upper_left.x, self.lower_right.x
        min_y, max_y = self.upper_left.y,self.lower_right.y
        return min_x <= unit.position.x <= max_x and min_y <= unit.position.y <= max_y

    def build_sector(self) -> None:

        self.ramps = self.ramps_in_sector()
        self.units = self.units_in_sector()
        self.enemy_units = self.enemy_units_in_sector()

    def update(self) -> None:
        self.units = self.units_in_sector()
        self.enemy_units = self.enemy_units_in_sector()