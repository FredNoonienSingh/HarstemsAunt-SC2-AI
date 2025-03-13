""" scenario class for Benchmarks"""
from typing import Union, List, Tuple

import numpy as np

# pylint: disable=C0411
from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.position import Point2,Point3
from sc2.ids.unit_typeid import UnitTypeId

from .result import Result, EndCondition

from HarstemsAunt.common import TOWNHALL_IDS, logger

class Scenario:

    def __init__(self,
                 bot:BotAI,
                 title:str,
                 position:Union[Point2,Unit],
                 enemy_units: List[UnitTypeId],
                 own_units: List[UnitTypeId],
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
        self.is_running = False
        self.is_done = False
        self.ending_condition:EndCondition = None

    async def start_benchmark(self) -> None:
        """Starts the time for the benchmark"""
        current_time:int = self.bot.time
        self.start_time = current_time
        self.is_running = True

    def end_condition(self, time) -> bool:
        """Overwritten in SuBclasses """
        current_time:int = self.bot.time
        under_runtime:bool = current_time >= time+self.max_runtime

        if not self.bot.enemy_units.filter(lambda unit: unit.type_id not in TOWNHALL_IDS):
            logger.info(f"Benchmark ended because there a no Enemy Units remaining")
            self.ending_condition = EndCondition.VICTORY
            return True
        if not self.bot.units.filter(lambda unit: unit.type_id not in TOWNHALL_IDS):
            logger.info(f"Benchmark ended because there a no Units remaining")
            self.ending_condition = EndCondition.DEFEAT
            return True
        if under_runtime:
            logger.info(f"Benchmark timed out")
            self.ending_condition = EndCondition.TIME_OUT
            return under_runtime

    def end(self) -> Result:
        self.is_running = False
        self.is_done = True
        time:float = self.bot.time - self.start_time
        return Result(self.title,time, 0, 0, 0, 0, self.ending_condition)
