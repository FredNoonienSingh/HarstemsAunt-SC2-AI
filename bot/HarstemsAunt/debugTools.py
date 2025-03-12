"""Module containing a Debug Class"""
# pylint: disable=C0103
from typing import Union
from math import sin, pi, cos, atan2

# pylint: disable=E0401
from sc2.unit import Unit
from sc2.data import Race
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId
from sc2.position import Point2, Point3, Pointlike

# pylint: disable=E0402
from .utils import Utils
from .army_group import ArmyGroup
from .unitmarker import UnitMarker
from .common import DEBUG_FONT_SIZE,logger
from .combat_unit import CombatUnit, FightStatus


class DebugTools:
    """ Collection of debug tools  """

    def __init__(self, bot:BotAI) -> None:
        self.bot = bot

    def debug_pos(self, pos:Union[Point2, Point3, Pointlike]):
        """ Draws sphere a given position
        Args:
            pos (Union[Point2, Point3, Pointlike]): position that will be shown
        """
        pos_3d = Utils.create_3D_point(pos)
        self.bot.client.debug_sphere_out(pos_3d ,.2, (255,255,0))

    def draw_gameinfo(self):
        """draws the information about the game to the screen"""
        text:str = ""
        supply:int = self.bot.supply_army
        enemy_supply:int=self.bot.enemy_supply
        text:str = text +(f"supply: {supply}\nenemy_supply: {enemy_supply}\n")
        minerals:int= self.bot.minerals
        gas:int = self.bot.vespene
        text:str = text +(f"\nIncome: {minerals, gas}\n")
        self.bot.client.debug_text_screen(str(text), (0,.125), color=None, size=14)

    def unit_label(self, unit:Unit):
        """ Draws information about the unit in a label at the unit 

        Args:
            unit (Unit): Unit which will be labeled
        """
        text:str=f"Type: {unit.type_id}\nHealth: \
            {unit.health}\nOrders: {unit.orders} \nPos {unit.position3d}"
        self.bot.client.debug_text_world(text,unit,color=(255,90,0),size=12)

    def unit_range(self, unit:Unit):
        """ draws range of unit

        Args:
            unit (Unit): unit whom's range will be 
        """
        if unit.can_attack_ground:
            self.bot.client.debug_sphere_out(unit,unit.ground_range,(0,255,0))
        if unit.can_attack_air:
            self.bot.client.debug_sphere_out(unit,unit.air_range,(255,0,25))

    # This is very old -> i think it is copied over from Lore
    def render_unit_vision(self, unit:Unit):
        """ draws units vision, draws a raycasting approach that is no longer in use

        Args:
            unit (Unit): unit who's vision will be displayed
        """
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

    def draw_vespene_pos(self) -> None:
        """renders the the position of the first two vespene geysers"""
        start_pos: Point2 = self.bot.start_location
        geysers = self.bot.vespene_geyser.closer_than(12, start_pos)
        for geyser in geysers:
            self.bot.client.debug_sphere_out(geyser, 2, (255,255,255))

    def draw_unit_marker(self, marker:UnitMarker) -> None:
        """renders a unitmarker"""
        pos: Point2 = marker.position
        z = self.bot.get_terrain_z_height(pos)+1
        x,y = pos.x, pos.y
        pos_3d = Point3((x,y,z))
        self.bot.client.debug_sphere_out(pos_3d ,.2, marker.color)

    def draw_step_time_label(self):
        """draws step time min, avg, max and last"""
        labels = ["min_step","avg_step","max_step","last_step"]
        for i, value in enumerate(self.bot.step_time):
            if value > 34:
                color = (0, 0, 255)
            else:
                color = (0, 255, 0)
            self.bot.client.debug_text_screen(f"{labels[i]}: {round(value,3)}", \
                (0, 0.025+(i*0.025)), color=color, size=DEBUG_FONT_SIZE)

    async def debug_micro(self) -> None:
        """build Stalker/Zealot for both players to debug unit behavior"""
        units_dict: dict = {
            Race.Zerg:[UnitTypeId.MUTALISK, UnitTypeId.CORRUPTOR],
            Race.Terran:[UnitTypeId.VIKING, UnitTypeId.LIBERATOR],
            Race.Protoss:[UnitTypeId.PHOENIX, UnitTypeId.VOIDRAY]
        }
        units:list = units_dict.get(self.bot.enemy_race)

        await self.bot.client.debug_tech_tree()
        #await self.client.debug_show_map()
        await self.bot.client.debug_create_unit(\
            [[UnitTypeId.PHOENIX, 6, self.bot.start_location, 1]])
        await self.bot.client.debug_create_unit(\
            [[UnitTypeId.VOIDRAY, 2, self.bot.start_location, 1]])
        await self.bot.client.debug_create_unit(\
            [[units[0], 5, self.bot.enemy_start_locations[0], 2]])
        await self.bot.client.debug_create_unit(\
            [[units[1], 2, self.bot.enemy_start_locations[0], 2]])

    def draw_army_group_label(self,iterator:int, group:ArmyGroup) -> None:
        """ draws ArmyGroup onto the screen"""
        self.bot.client.debug_text_screen(f"{group.group_type_id}: {group.attack_target}",\
            (.25+(iterator*0.25), 0.025), color=(255,255,255), size=DEBUG_FONT_SIZE)
        self.bot.client.debug_text_screen(f"Supply:{group.supply}\
            Enemy Supply:{group.enemy_supply_in_proximity}",\
            (.25+(iterator*0.27), 0.05), color=(255,255,255), size=DEBUG_FONT_SIZE)
        self.bot.client.debug_text_screen(f"requested:{group.requested_units}",\
            (.25+(iterator*0.27), 0.075), color=(255,255,255), size=DEBUG_FONT_SIZE)

    async def speed_things_up(self) -> None:
        """makes things faster -> just for debugging """
        await self.bot.client.debug_fast_build() #Buildings take no time
        await self.bot.client.debug_all_resources() #Free minerals and gas

    def debug_targeting(self,unit:Unit, target:Union[Unit, Point2]) -> None:
        """ Draws a line to the current Target of the given Unit
            and a sphere at the target
        Args:
            unit (Unit): _description_
            target (Union[Unit, Point2]): _description_
        """
        logger.info(f"target:{target}")
        unit_position:Point3 = unit.position3d
        if isinstance(target, Point2):
            target = Utils.create_3D_point(self.bot,target)
        if isinstance(target, Unit):
            target = target.position3d
        self.bot.client.debug_line_out(unit_position, target, (0,0,255))
        self.bot.client.debug_sphere_out(target,.75, (0,0,255))

    def debug_build_pos(self) -> None:
        """draws are sphere at the build pos"""
        pos:Union[Point2, Unit] = self.bot.macro.build_order.get_build_pos()
        if isinstance(pos, Unit):
            self.bot.client.debug_sphere_out(pos ,1, (255,255,0))
            return
        pos_3D = Utils.create_3D_point(self.bot,pos)
        self.bot.client.debug_sphere_out(pos_3D ,1, (255,255,0))

    def debug_unit_direction(self, unit:Unit) -> None:
        """Renders a debug sphere and a line to the Point where the 
            unit is facing
        """
        distance: float = 2
        direction: float = unit.facing
        x,y = unit.position
        q_x = x + distance*cos(direction)
        q_y = y + distance*sin(direction)
        pos_3D = Utils.create_3D_point(self.bot,Point2((q_x,q_y)))
        self.bot.client.debug_sphere_out(pos_3D ,.25, (0,255,0))
        self.bot.client.debug_line_out(unit.position3d, pos_3D, (0,255,0))

    def debug_angle_to_target(self, unit:Unit) -> None:
        """ Renders the a debug sphere and a line pointing to
            the closest enemy unit 

        Args:
            unit (Unit): unit to render angle
        """
        distance:float = 2
        Px,Py = unit.position

        if self.bot.enemy_units:
            closest_enemy:Unit = self.bot.enemy_units.closest_to(unit)
            Qx,Qy = closest_enemy.position
        else:
            Qx,Qy = self.bot.enemy_start_locations[0]

        delta_x:float = Px-Qx
        delta_y:float = Py-Qy
        theta:float = atan2(delta_x, delta_y)

        if theta < 0:
            theta += 2 * pi

        TargetX = Px + distance*cos(theta)
        TargetY = Py + distance*sin(theta)
        pos_3D = Utils.create_3D_point(self.bot,Point2((TargetX,TargetY)))
        self.bot.client.debug_sphere_out(pos_3D ,.25, (0,0,255))
        self.bot.client.debug_line_out(unit.position3d, pos_3D, (0,0,255))

    def debug_fighting_status(self, combat_unit:CombatUnit) -> None:
        """ Draws a green Sphere around the Unit if the Unit is attacking, 
            and a red one when it wants to retreat

        Args:
            combat_unit (_type_): _description_
        """

        color:tuple = (0,0,255) if combat_unit.fight_status == FightStatus.RETREATING else (0,255,0)
        self.bot.client.debug_sphere_out(combat_unit.position3d,.75, color)
