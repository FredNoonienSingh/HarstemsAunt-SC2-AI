from sc2.unit import Unit
from sc2.units import Units

from sc2.position import Point2, Point3
from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId

from army_group.army_group import ArmyGroup

class BaseClassRanged(Unit):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def kite(self) -> None:
