from enum import Enum

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
                 time_running:float,
                 dealt_damage:float,
                 taken_damage:float,
                 destroyed_enemy_units:int,
                 destroyed_friendly_units:int,
                 end_condition:EndCondition) -> None:
        self.benchmark = benchmark
        self.time_running = time_running
        self.dealt_damage = dealt_damage
        self.taken_damage = taken_damage
        self.destroyed_enemy_units = destroyed_enemy_units
        self.destroyed_friendly_units = destroyed_friendly_units
        self.end_condition = end_condition

    def __repr__(self) -> str:
        return f"Benchmark: {self.benchmark}\n\tran for {self.time_running}\n\tended in {self.end_condition}"
