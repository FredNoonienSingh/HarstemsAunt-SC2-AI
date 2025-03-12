""" Marker to be created when unit left vision """
#from typing import Union, List

from sc2.unit import Unit
from sc2.position import Point2
from sc2.ids.unit_typeid import UnitTypeId

class UnitMarker:
    """
    A marker shall be created whenever a enemy Unit leaves the vision of the
    bot, this marker shall remain on that position up to a certain age or if the position
    is in vision again. 
    
    Markers shall add influence according to their unit_type to the appropriate influence map.

    Needs to get the whole unit not just type, so that the marker can contain additional data

    """
    def __init__(self,
                unit:Unit,
                created_at_iteration: int,
                ):
        # A bit shit to implement it like this but thats the fastest will fix it later
        #self.unit:Unit = unit # -> i think this is not needed -> i was wrong, dont remove it again 
        self.type_id :UnitTypeId = unit.type_id
        self.can_attack_ground:bool = unit.can_attack_ground
        self.can_attack_air:bool = unit.can_attack_air
        self.can_attack_both:bool = unit.can_attack_both
        self.ground_dps:float = unit.ground_dps
        self.ground_range:float = unit.ground_range
        self.air_dps:float = unit.air_dps
        self.air_range:float = unit.air_range
        self.is_detector:bool = unit.is_detector
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
        return f"marker for {self.type_id} at position {self.position}"

    def __call__(self) -> None:
        """
            updating the unit markers once per frame may add additional computational 
            cost, but maybe it is possible to predict the next position of a unit

        """
        pass

    # This could probably be removed
    def age_in_frames(self, iteration:int) -> int:
        """ Returns the Age of the marker in Frames """
        return iteration - self.created_at


class StructureMarker:
    """
    May not be necessary 
    """

    def __init__(self,
                 structure:Unit,
                 created_at_iteration: int
                 ):
        self.structure = structure
        self.type_id: UnitTypeId = structure.type_id
        self.position:Point2 = structure.position
        self.health: float = structure.health_percentage
        self.created_at: int = created_at_iteration
