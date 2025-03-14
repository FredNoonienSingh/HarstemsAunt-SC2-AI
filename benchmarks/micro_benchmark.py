""" Benchmarks the UnitMicro of any two BurnySC2 Bots """
from typing import List,Dict,Tuple

from datetime import datetime

# pylint: disable=C0411
from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.position import Point2
from sc2.ids.unit_typeid import UnitTypeId


# pylint: disable=E0402
from .utils import Utils
from .szenario import Scenario
from .result import Result
from .common import WORKER_IDS

class MicroBenchmark:

    def __init__(self, bot:BotAI) -> None:
        self.bot:BotAI = bot
        self.current_index:int = 0
        self.scenario_running = False
        self.start_time = bot.time
        self.scenario:Scenario = None

    @property
    def record_path(self) -> str:
        """creates a path to store the benchmark run"""
        time:datetime = datetime.now()
        time_string:str = time.strftime("%y_%m_%d_%H_%M")
        bot_name:str = self.bot.name
        benchmark_name:str = f"benchmark_{bot_name}_@_{time_string}"
        
        return f"benchmarks/data/{benchmark_name}.csv"

    @property
    def scenarios(self) -> List[Scenario]:

        positions:List[Point2] = [
           self.bot.game_info.map_center,
           #self.bot.enemy_start_locations[0],
           #self.bot.start_location
        ] #+ self.bot.expand_locs

        Benchmarks:List[Dict] = []
        
        for pos in positions:
            Benchmarks.append({"title":"Stalker_vs_RoachRavager",
                               "position":pos,
                               "enemy_units":[(UnitTypeId.ROACH, 6), (UnitTypeId.RAVAGER, 3)],
                               "own_units":[(UnitTypeId.STALKER, 8)]
                               }
                            )
            Benchmarks.append({"title":"Tempest_vs_BC",
                               "position":pos,
                               "enemy_units":[(UnitTypeId.BATTLECRUISER, 1)],
                               "own_units":[(UnitTypeId.TEMPEST, 1)]
                               }
                            )
            Benchmarks.append({"title":"zealots_vs_zerglings",
                               "position":pos,
                               "enemy_units":[(UnitTypeId.ZERGLING, 10)],
                               "own_units":[(UnitTypeId.ZEALOT, 5)]
                               }
                            )
        return Benchmarks

    @property
    def current_scenario(self) -> Scenario:
        """returns the current scenario"""
        if self.current_index <= len(self.scenarios):
            return self.scenarios[self.current_index]

    async def __call__(self) -> None:
        # Enemybots are not stopping to build workers
        # -> therefore they need to be removed when they are build
        enemy_workers: Units = \
            self.bot.enemy_units.filter(lambda unit: unit.type_id in WORKER_IDS)
        if enemy_workers:
            await self.bot.client.debug_kill_unit(enemy_workers)

        if self.bot.units and self.bot.enemy_units:
            enemy_center:Point2 = self.bot.enemy_units.center
            camera_unit:Unit = self.bot.units.closest_to(enemy_center)
            await self.bot.client.move_camera(camera_unit)

        if self.scenario_running:
            if self.scenario.end_condition(self.start_time):
                result:Result = await self.scenario.end()
                await self.write_benchmark(result)
                self.scenario_running = False
            """
            if not self.scenario_running:
                if self.current_index < len(self.scenarios)-1:
                    self.current_index += 1
                else:
                    self.current_index = 0
            """
        else:
            await self.build_scenario()

        if self.current_index == 0 and not self.scenario_running:
            await self.build_scenario()

    async def build_scenario(self) -> None:
        """Build current scenario"""

        engagement_title:str = self.current_scenario.get("title")
        engagement_position: Point2 = self.current_scenario.get("position")
        enemy_units:List[Tuple[UnitTypeId,int]] = self.current_scenario.get("enemy_units")
        own_units:List[Tuple[UnitTypeId, int]] = self.current_scenario.get("own_units")

        self.scenario = Scenario(self.bot, engagement_title, engagement_position, enemy_units, own_units)
        await self.bot.client.move_camera(engagement_position)
        await self.scenario.start_benchmark(False)

        for unit in self.bot.units:
            self.bot.army_groups[0].add_combat_unit(unit)

        self.scenario_running = True
        self.start_time = self.bot.time

    async def write_benchmark(self, result: Result) -> None:
        """ Ends the benchmarks run and writes the results to csv files"""
        path:str = self.record_path
        content:dict = result.as_dict()
        Utils.write_dict_to_csv(content, path)
        #await self.bot.client.leave()