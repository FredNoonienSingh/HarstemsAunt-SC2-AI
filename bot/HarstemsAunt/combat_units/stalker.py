"""Replacement for UnitClass"""
from enum import Enum
from typing import Union, List
 
import numpy as np

# pylint: disable=E0402
# from .utils import Utils
from .unitmarker import UnitMarker
from .combat_unit import CombatUnit
from .common import MIN_SHIELD_AMOUNT, RANGE_BUFFER,\
    PROXIMITY,PRIO_ATTACK_TARGET, ALL_STRUCTURES, logger

# pylint: disable=C0411
from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.game_info import Ramp
from sc2.position import Point2,Point3
from sc2.ids.ability_id import AbilityId


class Stalker(CombatUnit):

    def blink(self,target:Union[Point2, Point3, Unit]):
        """cast the blink ability"""
        self.unit(AbilityId.EFFECT_BLINK_STALKER, target)

    async def engage(self, attack_target:Union[Point2, Point3, Unit]) -> None:
        """overwrite for CombatUnit.engage"""
        pass

    async def disengage(self, retreat_position: Point2) -> None:
        """overwrite for CombatUnit.disengage"""
        pass

