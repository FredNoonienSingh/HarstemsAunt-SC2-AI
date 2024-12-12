from sc2.pixel_map import PixelMap

class InfluenceMap(PixelMap):

    """ 
        PixelMap storing numeric values based on the "danger" for a given point,
        
    """
    
    def __init__(self, proto, in_bits = False):
        super().__init__(proto, in_bits)

    def check_here(self):
        return "Here"