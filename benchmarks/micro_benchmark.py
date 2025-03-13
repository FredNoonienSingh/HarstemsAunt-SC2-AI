""" Benchmarks the UnitMicro of any two BurnySC2 Bots """
from typing import Union, List

import numpy as np

# pylint: disable=C0411
from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.position import Point2,Point3
from sc2.ids.unit_typeid import UnitTypeId

from .szenario import Scenario
from .result import Result, EndCondition

# pylint: disable=E0401
from HarstemsAunt.utils import Utils
from HarstemsAunt.unitmarker import UnitMarker
from HarstemsAunt.common import TOWNHALL_IDS,WORKER_IDS, logger


class MicroBenchmark:

    def __init__(self, bot:BotAI) -> None:
        self.bot:BotAI = bot
        self.current_index:int = 0
        self.scenario_running = False
        self.start_time = bot.time
        self.results:List[Result] = []

    @property
    def scenarios(self) -> List[Scenario]:

        positions:List[Point2] = [
           self.bot.game_info.map_center,
           self.bot.enemy_start_locations[0],
           self.bot.start_location
        ] + self.bot.expand_locs

        Benchmarks:List[Scenario] = []
        
        for pos in positions:
            BENCHMARK_0: Scenario =  Scenario(self.bot,
                                              "Stalker/Immortal_vs_Marine/Marauder",
                                              pos,
                                                [(UnitTypeId.MARINE, 5), (UnitTypeId.MARAUDER, 2)],
                                                [(UnitTypeId.STALKER, 5), (UnitTypeId.IMMORTAL, 1)],
                                              )
            Benchmarks.append(BENCHMARK_0)
            
            """"
            BENCHMARK_1: Scenario =  Scenario(self.bot,
                                              "Voidray/Phoenix",
                                              pos,
                                                [(UnitTypeId.PHOENIX, 3), (UnitTypeId.VOIDRAY, 2)],
                                                [(UnitTypeId.PHOENIX, 3), (UnitTypeId.VOIDRAY, 2)],
                                              )
            Benchmarks.append(BENCHMARK_1)
            BENCHMARK_2: Scenario =  Scenario(self.bot,
                                              "Marines/Tank",
                                              pos,
                                                [(UnitTypeId.MARINE, 12), (UnitTypeId.SIEGETANK, 1)],
                                                [(UnitTypeId.VOIDRAY, 3)],
                                              )
            Benchmarks.append(BENCHMARK_2)
            BENCHMARK_3: Scenario =  Scenario(self.bot,
                                              "Zealot_vs_Zergling",
                                              pos,
                                                [(UnitTypeId.ZERGLING, 5)],
                                                [(UnitTypeId.ZEALOT, 3)],
                                              )
            Benchmarks.append(BENCHMARK_3)
            BENCHMARK_4: Scenario =  Scenario(self.bot,
                                              "Stalker@Disadvantage",
                                              pos,
                                                [(UnitTypeId.STALKER, 4)],
                                                [(UnitTypeId.STALKER, 3)],
                                              )
            Benchmarks.append(BENCHMARK_4)
            BENCHMARK_5: Scenario =  Scenario(self.bot,
                                              "Tempest_vs_BC",
                                              pos,
                                                [(UnitTypeId.BATTLECRUISER, 4)],
                                                [(UnitTypeId.TEMPEST, 3)],
                                              )
            Benchmarks.append(BENCHMARK_5)
            BENCHMARK_6: Scenario =  Scenario(self.bot,
                                              "Stalker_vs_R/R",
                                              pos,
                                                [(UnitTypeId.ROACH, 6), (UnitTypeId.RAVAGER, 3)],
                                                [(UnitTypeId.STALKER, 8)],
                                              )
            Benchmarks.append(BENCHMARK_6)
            """
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
            if self.current_scenario.end_condition(self.start_time):
                result:Result = self.current_scenario.end()
                logger.error(result)
                self.results.append(result)
                self.scenario_running = False
                if self.current_index < len(self.scenarios) -1:
                    self.current_index += 1
                else:
                    self.current_index = 0

        else:
            await self.build_scenario()

        if self.current_index == 0 and not self.scenario_running:
            await self.build_scenario()

    async def clear_scenario(self) -> None:
        """Kills all Units"""
        #await self.bot.client.debug_show_map()
        enemies:Units = self.bot.enemy_units.filter(lambda struct: struct.type_id not in TOWNHALL_IDS)
        own_units:Units = self.bot.units.filter(lambda struct: struct.type_id not in TOWNHALL_IDS)
        #enemy_structures:Units = self.bot.enemy_structures.filter(lambda struct: struct.type_id not in TOWNHALL_IDS)
        #structures: Units = self.bot.structures.filter(lambda struct: struct.type_id not in TOWNHALL_IDS)

        destroy_list:List = [enemies, own_units]

        for units in destroy_list:
            #logger.warning(f" i am going to destroy these units: \n{units}")
            if units:
                await self.bot.client.debug_kill_unit(units)
        
        #await self.bot.client.debug_show_map()

    async def build_scenario(self) -> None:
        """Build current scenario"""
        engagement_position: Point2 = self.current_scenario.position
        engagement_radius:float = self.current_scenario.engagement_radius
        await self.bot.client.move_camera(engagement_position)
        await self.clear_scenario()
        
        for element in self.current_scenario.enemy_units:
            await self.bot.client.debug_create_unit(\
                [[element[0], element[1], \
                    engagement_position.towards(self.bot.enemy_start_locations[0],engagement_radius), 2]])
        for element in self.current_scenario.own_units:
            await self.bot.client.debug_create_unit(\
                [[element[0], element[1], engagement_position.towards(self.bot.start_location, engagement_radius), 1]])

        for unit in self.bot.units:
            #self.bot.army_groups[0].
            self.bot.army_groups[0].add_combat_unit(unit)

        await self.current_scenario.start_benchmark()
        self.scenario_running = True
        self.start_time = self.bot.time
