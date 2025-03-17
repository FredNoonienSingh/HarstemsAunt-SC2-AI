
# pylint: disable=C0411
from sc2.units import Units
from sc2.bot_ai import BotAI

class EnemyBehavior:
    def __init__(self, bot:BotAI):
        self.bot = bot

    async def attack_towards(self, units:Units) -> None:
        """enemy behavior"""
        for unit in units:
            if self.bot.units.closer_than(unit.ground_range+20, unit):
                unit.attack(unit.position\
                    .towards(self.bot.units.center, 2))
            else:
                unit.attack(self.bot.start_location)

    async def attack_weakest(self, units:Units) -> None:
        """enemy behavior"""
        for unit in units:
            attackble_units:Units = self.bot.units.closer_than(unit.ground_range+20, unit)
            if attackble_units:
                target = min(
                    attackble_units,
                    key=lambda e: (e.health + e.shield, e.tag),
                )
                unit.attack(target)
            else:
                unit.attack(self.bot.start_location)

    async def attack_closest(self, units:Units) -> None:
        """enemy behavior"""
        for unit in units:
            if self.bot.units.closer_than(unit.ground_range+20, unit):
                unit.attack(self.bot.units.closest_to(unit))
            else:
                unit.attack(self.bot.start_location)
