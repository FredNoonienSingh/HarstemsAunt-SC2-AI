"""
Marker to be created when unit left vision
"""
from typing import Union, List

from sc2.unit import Unit
from sc2.position import Point2, Point3
from sc2.ids.unit_typeid import UnitTypeId

from .common import logger

class UnitMarker: 
    """
    A marker shall be created whenever a enemy Unit leaves the vision of the 
    bot, this marker shall remain on that position up to a certain age or if the position 
    is in vision again. 
    
    Markers shall add influnce acording to their unit_type to the appropriate influence map. 

    Needs to get the whole unit not just type, so that the marker can contain addinal data

    """
    def __init__(self,
                unit:Unit,
                created_at_iteration: int, 
                ):
        # A bit shit to implement it like this but thats the fastest will fix it later
        self.unit:Unit = unit
        self.unit_typeid :UnitTypeId = unit.type_id
        self.position: Point2 = unit.position
        self.unit_tag: int = unit.tag
        self.health: float = unit.health_percentage
        self.created_at:int = created_at_iteration
    
    @property
    def color(self):
        """The color property."""
        if self.health < .25:
            return (0, 0, 255)
        elif self.health < .75:
            return (0, 155, 255)
        return (255,255,0)

    def __repr__(self) -> str: 
        return f"marker for {self.unit_typeid} at position {self.position}"

    def age_in_frames(self, interation:int) -> int:
        """ Returns the Age of the marker in Frames """
        return interation - self.created_at
