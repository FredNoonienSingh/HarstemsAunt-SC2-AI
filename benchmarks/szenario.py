""" scenario class for Benchmarks"""
from typing import Union, List, Tuple
import time

# pylint: disable=C0411
from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.position import Point2
from sc2.ids.unit_typeid import UnitTypeId

# pylint: disable=E0402
from .common import TOWNHALL_IDS
from .recorder import record_benchmark
from .result import Result, EndCondition


@record_benchmark(['enemy_units', 'own_units'])
class Scenario:

    def __init__(self,
                 bot:BotAI,
                 title:str,
                 position:Union[Point2,Unit],
                 enemy_units: List[Tuple[UnitTypeId,int]],
                 own_units: List[Tuple[UnitTypeId,int]],
                 engagement_radius:float = 5,
                 max_runtime: float = 30
                 ) ->None:
        self.bot = bot
        self.title = title
        self.position = position
        self.enemy_units = enemy_units
        self.own_units = own_units
        self.engagement_radius = engagement_radius
        self.max_runtime = max_runtime
        self.start_time = self.bot.time
        self.running = False
        self.ending_condition:EndCondition = None

    def __repr__(self) -> None:
        return f"Scenario {self.title} playing at {self.position}"

    async def toggle_vision(self) -> None:
        await self.bot.client.debug_show_map()

    async def clear_all(self, blind:bool=True):
        """clears all units and structures, beside the Townhalls """
        if blind:
            await self.toggle_vision()

        enemies:Units = self.bot.enemy_units
        own_units:Units = self.bot.units
        enemy_structure:Units = self.bot.enemy_structures.filter\
            (lambda struct: struct.type_id not in TOWNHALL_IDS)
        own_structures:Units = self.bot.structures.filter\
            (lambda struct: struct.type_id not in TOWNHALL_IDS)

        destroy_list:List = [enemies, own_units, enemy_structure, own_structures]
        for units in destroy_list:
            if units:
                await self.bot.client.debug_kill_unit(units)
        if blind:
            await self.toggle_vision()
        return True

    async def start_benchmark(self, blind:bool=True) -> None:
        """Starts the time for the benchmark"""

        if await self.clear_all(blind):
            current_time:int = self.bot.time
            self.start_time = current_time
            for instruction in self.enemy_units:
                await self.bot.client.debug_create_unit(
                    [[instruction[0], instruction[1],
                    self.position.\
                          towards(self.bot.enemy_start_locations[0],self.engagement_radius),2]]
                )
            for instruction in self.own_units:
                await self.bot.client.debug_create_unit(
                    [[instruction[0], instruction[1],
                    self.position.\
                          towards(self.bot.start_location,self.engagement_radius),1]]
                )

            # Let the enemy attack:
            await self.bot.client.debug_control_enemy()
            for unit in self.bot.enemy_units:
                unit.attack(self.position)
            await self.bot.client.debug_control_enemy()

    def calculate_destroyed_units(self) -> Tuple[int, int]:
        """ calculates how many units got destroyed

        Returns:
            Tuple[int, int]: destroyed enemies, destroyed friendlies
        """
        enemy_unit_count:int = sum([x[1] for x in self.enemy_units])
        friendly_unit_count:int = sum([x[1] for x in self.own_units])

        remaining_enemies:int = len(self.bot.enemy_units)
        remaining_units: int = len(self.bot.units)

        return (enemy_unit_count-remaining_enemies,
                friendly_unit_count-remaining_units)

    def end_condition(self) -> bool:
        """Overwritten in SuBclasses """
        current_time:int = self.bot.time
        runtime = current_time - self.start_time
        under_runtime:bool = current_time >= self.start_time+self.max_runtime
        
        if not self.bot.enemy_units.filter(lambda unit: unit.type_id not in TOWNHALL_IDS)\
            and runtime > 2:
            self.ending_condition = EndCondition.VICTORY
            return True
        if not self.bot.units.filter(lambda unit: unit.type_id not in TOWNHALL_IDS)\
            and runtime > 2:
            self.ending_condition = EndCondition.DEFEAT
            return True
        if under_runtime:
            self.ending_condition = EndCondition.TIME_OUT
            return True
        return False

    async def end(self) -> Result:
        time:float = self.bot.time - self.start_time
        bot_version: str = self.bot.version
        map_name:str = self.bot.game_info.map_name

        destroyed, lost = self.calculate_destroyed_units()

        #await self.clear_all(False)

        return Result(self.title,
                      bot_version,
                      map_name,
                      self.position,
                      time,
                      0,
                      0,
                      destroyed,
                      lost,
                      self.ending_condition)

