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
        self.center:Point2 = Point2((abs(upper_left.x + self.width), abs(self.upper_left.y - self.height)))
        self.ramps = None
        self.units = None
        self.enemy_units = None

    def render_sector(self) -> None:
        color = (255, 255, 0) if self.units else (255,0, 255)
        z_1 = 15#self.bot.get_terrain_z_height(self.upper_left)+10
        z_2 = 15#self.bot.get_terrain_z_height(self.lower_right)+10
        pos_1_3d = Point3((self.upper_left.x, self.upper_left.y, z_1))
        pos_2_3d = Point3((self.lower_right.x, self.lower_right.y, z_2))

        self.bot.client.debug_box_out(pos_1_3d, pos_2_3d, color)
    """
    def ramps_in_sector(self) -> List:
        ramps = self.bot.game_info.map_ramps
        return ramps.filter(lambda unit: self.find_maps_in_sector(unit))

    def destructables_in_sector(self) -> Units:
        if self.bot.destructables:
            return self.bot.destructables.filter(lambda unit: self.in_sector(unit))
        return None

    def units_in_sector(self) -> Units:
        if self.bot.units:
            return self.bot.units(lambda unit: self.in_sector(unit))
        return None

    def enemy_units_in_sector(self) -> Units:
        if self.bot.enemy_units:
            return self.bot.enemy_units.filter(lambda unit: self.in_sector(unit))
        return None
    
    def find_maps_in_sector(self, ramp: Ramp) -> List:
        min_x, max_x = self.upper_left.x, self.lower_right.x
        min_y, max_y = self.lower_right.y, self.upper_left.y
        bottom_x, bottom_y = ramp.bottom_center.x, ramp.bottom_center.y
        top_x, top_y = ramp.top_center.x, ramp.top_center.y
        bottom_in_sector:bool = min_x <= bottom_x <= max_x and min_y <= bottom_y <= max_y
        top_in_sector:bool = min_x <= top_x <= max_x and min_y <= top_y <= max_y

        return (bottom_in_sector and top_in_sector) or (bottom_in_sector or top_in_sector)

    def in_sector(self,unit:Unit) -> bool:
        min_x, max_x = self.upper_left.x, self.lower_right.x
        min_y, max_y = self.lower_right.y, self.upper_left.y
        return min_x <= unit.x <= max_x and min_y <= unit.y <= max_y

    """
    def build_sector(self) -> None:
        self.bot.logger.info("building sectors")
        #self.ramps = self.ramps_in_sector()
        #self.units = self.units_in_sector()
        #self.enemy_units = self.enemy_units_in_sector()

    def update(self) -> None:
        self.bot.logger.info("updating sectors")
        #self.units = self.units_in_sector()
        #self.enemy_units = self.enemy_units_in_sector()