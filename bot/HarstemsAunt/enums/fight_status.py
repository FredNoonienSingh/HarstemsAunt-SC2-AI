"""fight status Enum"""

from enum import Enum

class FightStatus(Enum):
    """Could be named better, will be used to report to the 
        Group if the unit is ready to engage
    """
    FIGHTING = 1
    RETREATING = 2
    DESTROYED = 3
    DEFENDING = 4