
# pylint: disable=C0411
from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI

class EnemyBehavior:
    def __init__(self, bot:BotAI):
        self.bot = bot

    async def attack_retreat(self, units:Units) -> None:
        """Attacks and retreats when can't attack """
        for unit in units:
            targets:Units = self.bot.units
            if targets:
                target:Unit = min(targets,key=lambda e: (e.health + e.shield, e.tag))
                if unit.shield_health_percentage < 0.95 and unit.distance_to(targets.closest_to(unit))<9:
                    anchor_unit:Unit = targets.closest_to(unit)
                    unit.move(unit.position.towards(anchor_unit, -1))
                    continue
                unit.attack(target)

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
            targets:Units = self.bot.units.closer_than(unit.ground_range+20, unit)
            if targets:
                target = min(
                    targets,
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
