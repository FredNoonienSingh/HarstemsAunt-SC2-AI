
from sc2.units import Units
from sc2.position import Point2, Point3

class ArmyGroup(Units):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_pos: Point2 = None
        self.retreat_pos: Point2 = None
        #self.units 