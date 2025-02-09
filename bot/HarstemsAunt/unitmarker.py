"""
Marker to be created when unit left vision
"""
from typing import Union, List

from sc2.unit import Unit
from sc2.position import Point2, Point3
from sc2.ids.unit_typeid import UnitTypeId


class UnitMarker: 
    """
    A marker shall be created whenever a enemy Unit leaves the vision of the 
    bot, this marker shall remain on that position up to a certain age or if the position 
    is in vision again. 
    
    Markers shall add influnce acording to their unit_type to the appropriate influence map. 

    Needs to get the whole unit not just type, so that the marker can contain addinal data

    """
    def __new__(cls,
                unit:Unit,
                created_at_iteration: int, 
                ):
        instance = super().__new__(cls)
        cls.unit_typeid :UnitTypeId = unit.type_id
        cls.position: Point2 = unit.position
        cls.unit_tag: int = unit.tag
        cls.health: float = unit.health_percentage
        cls.created_at:int = created_at_iteration
        return instance
   
    def __repr__(self) -> str: 
        return f"marker for {self.unit_typeid} at position {self.position}"

    def age_in_frames(self, interation:int) -> int:
        """ Returns the Age of the marker in Frames """
        return interation - self.created_at
