from HarstemsAunt.common import logger
from Unit_Classes.baseClassGround import BaseClassGround


class Stalkers(BaseClassGround):
    """ Extension of BaseClassGround """

    async def _do_blink(self):
        logger.info(f"BLINK is not yet implemented")