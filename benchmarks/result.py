from typing import Tuple, List
from enum import Enum
from datetime import datetime

import numpy as np
from sc2.ids.unit_typeid import UnitTypeId

# pylint: disable=E0402
from .utils import Utils

class EndCondition(Enum):
    """EndCondition of a Benchmark"""
    VICTORY = 1
    DEFEAT = 2
    TIME_OUT = 3
    PENDING = 4

class Result:
    """ More or less a DataClass at the moment, 
        but that may change in the next few hours so 
        i implemented it like this
    """
    def __init__(self,
                 benchmark:str,
                 comment:str,
                 bot_version:str,
                 benchmarked_map: str,
                 start_position:Tuple[float, float],
                 enemy_behavior: str,
                 has_creep: bool,
                 enemy_units: List[Tuple[UnitTypeId, int]],
                 own_units:List[Tuple[UnitTypeId, int]],
                 time_running:float,
                 score:float,
                 life_damage_dealt:float,
                 shield_damage_dealt: float,
                 life_damage_taken:float,
                 shield_damage_taken:float,
                 destroyed_enemy_units:int,
                 destroyed_friendly_units:int,
                 observations:List[Tuple],
                 pathing_grids:List[np.ndarray],
                 end_condition:EndCondition) -> None:
        self.benchmark = benchmark
        self.comment = comment
        self.bot_version = bot_version
        self.current_git_hash = Utils.get_git_head()
        self.benchmarked_map = benchmarked_map
        self.start_position = start_position
        self.enemy_behavior = enemy_behavior
        self.has_creep = has_creep
        self.start_time:datetime = datetime.now()
        self.enemy_units = enemy_units
        self.own_units = own_units
        self.time_running = time_running
        self.score = score, 
        self.life_damage_dealt = life_damage_dealt
        self.shield_damage_dealt = shield_damage_dealt
        self.life_damage_taken = life_damage_taken
        self.shield_damage_taken = shield_damage_taken
        self.destroyed_enemy_units = destroyed_enemy_units
        self.destroyed_friendly_units = destroyed_friendly_units
        self.observations= observations
        self.pathing_grids = pathing_grids
        self.end_condition = end_condition

    def __repr__(self) -> str:
        return f"""Benchmark: {self.benchmark}\n\t
             ran for {self.time_running}\t
             \nDAMAGE: 
             {self.taken_damage} damage taken\n\t
             \nUNITS:
             destroyed {self.destroyed_enemy_units} Units
             lost {self.destroyed_friendly_units} Units
             ended in {self.end_condition}"""

    def as_dict(self) -> dict:
        """Returns the Result object as a dictionary."""
        return {
            "benchmark": self.benchmark,
            "bot_version": self.bot_version,
            "comment": self.comment,
            "branch": self.current_git_hash,
            "map": self.benchmarked_map,
            "start_pos": self.start_position,
            "started_at": self.start_time,
            "enemy_behavior": self.enemy_behavior,
            "has_creep": self.has_creep,
            "enemy_units": self.enemy_units,
            "own_units": self.own_units,
            "time_running": self.time_running,
            "score": self.score[0],
            "life_damage_dealt": self.life_damage_dealt,
            "shield_damage_dealt":self.shield_damage_dealt,
            "life_damage_taken":self.life_damage_taken,
            "shield_damage_taken":self.shield_damage_taken,
            "destroyed_enemy_units": self.destroyed_enemy_units,
            "destroyed_friendly_units": self.destroyed_friendly_units,
            #"observations": self.observations,
            #"ground_grid": self.pathing_grids[0],
            #"air_grid": self.pathing_grids[1],
            "end_condition": self.end_condition,  # Store the name of the enum
        }
