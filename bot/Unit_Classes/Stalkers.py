from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.ids.ability_id import AbilityId

MIN_SHIELD_AMOUNT:float = 0.25

class Stalker:
    def __init__(self, bot:BotAI):
        self.ai: BotAI = bot

        self.blink_range: float = self.ai.game_data.abilities[
            AbilityId.EFFECT_BLINK_STALKER.value
        ]._proto.cast_range

        