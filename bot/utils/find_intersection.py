import math
import numpy as np
from typing import Iterable
from sc2.position import Point2


def get_intersections(p0: Point2, r0: float, p1: Point2, r1: float) -> Iterable[Point2]:
    """ Generator yielding the Intersection of 2 circles

    Args:
        p0 (Point2): Origin of Circle_0
        r0 (float): radius of Circle_0
        p1 (Point2): Origin of Circle_1
        r1 (float): radius of Circle_1

    Yields:
        Iterator[Iterable[Point2]]: Intersection points
    """
    
    p01 = p1 - p0
    d = np.linalg.norm(p01)
    if d == 0:
        return  # intersection is empty or infinite
    if d < abs(r0 - r1):
        return  # circles inside of each other
    if r0 + r1 < d:
        return  # circles too far apart
    a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
    h = math.sqrt(r0 ** 2 - a ** 2)
    pm = p0 + (a / d) * p01
    po = (h / d) * np.array([p01.y, -p01.x])
    yield pm + po
    yield pm - po
