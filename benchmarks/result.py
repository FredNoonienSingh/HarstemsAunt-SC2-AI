from typing import Tuple
from enum import Enum

from datetime import datetime

class EndCondition(Enum):
    """EndCondition of a Benchmark"""
    VICTORY = 1
    DEFEAT = 2
    TIME_OUT = 3

class Result:
    """ More or less a DataClass at the moment, 
        but that may change in the next few hours so 
        i implemented it like this
    """
    def __init__(self,
                 benchmark:str,
                 bot_version:str,
                 benchmarked_map: str,
                 start_position:Tuple[float, float],
                 time_running:float,
                 dealt_damage:float,
                 taken_damage:float,
                 destroyed_enemy_units:int,
                 destroyed_friendly_units:int,
                 end_condition:EndCondition) -> None:
        self.benchmark = benchmark
        self.bot_version = bot_version
        self.benchmarked_map = benchmarked_map
        self.start_position = start_position
        self.start_time:datetime = datetime.now()
        self.time_running = time_running
        self.dealt_damage = dealt_damage
        self.taken_damage = taken_damage
        self.destroyed_enemy_units = destroyed_enemy_units
        self.destroyed_friendly_units = destroyed_friendly_units
        self.end_condition = end_condition

    def __repr__(self) -> str:
        return f"""Benchmark: {self.benchmark}\n\t
             ran for {self.time_running}\t
             \nDAMAGE: 
             {self.dealt_damage} damage given\n\t
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
            "map": self.benchmarked_map,
            "start_pos": self.start_position,
            "started_at": self.start_time,
            "time_running": self.time_running,
            "dealt_damage": self.dealt_damage,
            "taken_damage": self.taken_damage,
            "destroyed_enemy_units": self.destroyed_enemy_units,
            "destroyed_friendly_units": self.destroyed_friendly_units,
            "end_condition": self.end_condition,  # Store the name of the enum
        }
