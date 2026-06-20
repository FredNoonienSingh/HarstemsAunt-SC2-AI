from enum import Enum

class GroupStatus(Enum):
    """Enum representing the State """
    ATTACKING = 1
    DEFENDING = 2
    RETREATING = 3
    REGROUPING = 4
