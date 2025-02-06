"""make linter shut up"""
# pylint: disable=C0103
# pylint: disable=E0401

from sc2.unit import Unit
from sc2.units import Units
from Unit_Classes.baseClassGround import BaseClassGround


class Immortals(BaseClassGround):
    """ Extension of BaseClassGround """

    async def handle_attackers(self, units: Units, attack_targer: Point2) -> None:
        """
        Handles Attackers
        """
    
