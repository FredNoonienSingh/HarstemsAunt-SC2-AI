""" Benchmarks the UnitMicro of any two BurnySC2 Bots """
from typing import List,Dict,Tuple

#from datetime import datetime

# pylint: disable=C0411
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.position import Point2
from sc2.ids.unit_typeid import UnitTypeId

# pylint: disable=E0402
from .utils import Utils
from .scenario import Scenario
from .result import Result
from .common import WORKER_IDS, TOWNHALL_IDS

class Benchmark:

    def __init__(self, bot:BotAI) -> None:
        self.bot:BotAI = bot
        self.current_index:int = 0
        self.scenario_running = False
        self.start_time = bot.time
        self.scenario:Scenario = None

    @property
    def record_path(self) -> str:
        """creates a path to store the benchmark run"""
        bot_name:str = self.bot.name
        version:str = self.bot.version
        benchmark_name:str = f"benchmark_{bot_name}_v{version}"

        return f"benchmarks/data/{benchmark_name}.csv"

    @property
    def scenarios(self) -> List[Scenario]:
        """builds a list of scenario"""

        positions:List[Point2] = [
           self.bot.game_info.map_center,
           self.bot.enemy_start_locations[0],
           self.bot.start_location
        ] + self.bot.expand_locs

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

    async def destroy_workers(self) -> None:
        """Destroy enemy workers"""
        enemy_workers: Units = \
            self.bot.enemy_units.filter(lambda unit: unit.type_id in WORKER_IDS)
        if enemy_workers:
            await self.bot.client.debug_kill_unit(enemy_workers)

    async def __call__(self) -> None:
        await self.destroy_workers()
        if not self.scenario_running:
            await self.build_scenario()

        if self.scenario_running:
            if self.scenario.end_condition():
                result:Result = await self.scenario.end()
                await self.end_benchmark(result)
            else:
                if self.bot.enemy_units:
                    for unit in self.bot.enemy_units:
                        unit.attack(self.scenario.position)
                if self.bot.units and self.bot.enemy_units:
                    cam_center: Point2 = self.bot.units.center.towards(self.bot.enemy_units.center, 2)
                    self.bot.client.move_camera(cam_center)
                if self.bot.units and not self.bot.enemy_units:
                    self.bot.client.move_camera(self.bot.units.center)

    async def clear_all(self, blind:bool=True):
        """clears all units and structures, beside the Townhalls """
        if blind:
            await self.bot.client.debug_show_map()

        await self.destroy_workers()

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
            await self.bot.client.debug_show_map()
        return True

    async def build_scenario(self) -> None:
        """Build current scenario"""

        await self.clear_all(False)

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

    async def end_benchmark(self, result: Result) -> None:
        """ Ends the benchmarks run and writes the results to csv files"""
        path:str = self.record_path
        content:dict = result.as_dict()
        Utils.write_dict_to_csv(content, path)
        if self.current_index < len(self.scenarios) -1:
            self.current_index += 1
        else:
            await self.bot.client.leave()
        self.scenario_running = False
