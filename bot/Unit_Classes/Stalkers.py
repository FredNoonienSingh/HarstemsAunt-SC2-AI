from typing import Optional

import numpy as np

from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.position import Point2
from sc2.ids.ability_id import AbilityId

from HarstemsAunt.pathing import Pathing
from Unit_Classes.baseClassGround import BaseClassGround

from HarstemsAunt.common import logger


class Stalkers(BaseClassGround):
    """ Extension of BaseClassGround """

    async def _do_blink(self):
        logger.info(f"BLINK is not yet implemented")