import numpy as np

from typing import Union

from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.position import Point2, Point3

from HarstemsAunt.pathing import Pathing
from HarstemsAunt.common import WORKER_IDS

class Observer:
    def __init__(self, bot:BotAI, pathing:Pathing) -> None:
        self.bot:BotAI = bot
        self.pathing:Pathing = pathing

    @property
    def movement_grid(self) -> np.ndarray:
        return self.pathing.detection_grid


    async def move(self, units: Units, target:Union[Point2, Point3, Unit]) -> None:
        for unit in units:
            #If Enemy Units in the Area -> move to enemy Center
            enemies: Units = self.bot.enemy_units.closer_than(unit.sight_range+5,unit)\
                .filter(lambda unit: unit not in WORKER_IDS)
            move_target = enemies.center if enemies else target
            next_step = self.pathing.find_path_next_point(
                unit.position, move_target, self.movement_grid
            )
            unit.move(next_step)

    async def retreat(self, units:Units, retreat_pos: Union[Point2, Point3, Unit]) -> None:
        for unit in units:
            next_step = self.pathing.find_path_next_point(
                unit.position, retreat_pos, self.movement_grid
            )
            unit.move(next_step)