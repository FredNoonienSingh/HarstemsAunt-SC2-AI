""" dataclass for targetAllocations  """
from dataclasses import dataclass

from math import inf
from typing import Union

from sc2.unit import Unit
from bot.HarstemsAunt.misc.unitmarker import UnitMarker

@dataclass
class Allocation:
    """
        Holds data about the allocation of an target for a CU
    """
    target: Union[Unit, UnitMarker]
    allocation_time: int # tick on which the allocation was made
    allocation_score: float
    allocation_lifetime:float = inf
    risk: float = 0.5
    # Signifies to the CU how big of a risk it may take (0-1)
    # for example a BC in the Mining Line would be 1
    # - which means loss of the unit is acceptable
    # default should be around .5 -
    # which means losing more than 50% health is not acceptable
    stickiness:float = 15
    # Used to set how much higher a new
    # TAS has to be so that a new target gets allocated
    # by new_tas = tas - (1/stickiness * tas)
