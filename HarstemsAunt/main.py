"""
    MainClass of the Bot handling

"""
from common import MAP_LIST
from random import choice

"""SC2 Imports"""

from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.unit import Unit
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.player import Bot, Computer, Human
from sc2.ids.unit_typeid import UnitTypeId

"""Utils"""
from utils.can_build import can_build_unit, can_build_structure, can_research_upgrade

class HarstemsAunt(BotAI):

    def __init__(self, debug:bool=False) -> None:
        self.race = Race.Protoss
        self.name = "HarstemsAunt"
        self.version = "0.1"
        self.debug = debug

    async def on_start(self):
        pass

    async def on_step(self, iteration):
        print(f"running at iteration {iteration}")
        if self.townhalls and self.units:
            for townhall in self.townhalls:
                if townhall.is_idle and can_build_unit(self, UnitTypeId.PROBE):
                    townhall.train(UnitTypeId.PROBE)
            return
        await self.client.leave()

    async def on_end(self,game_result):
        await self.client.leave()

if __name__ == "__main__":
    AiPlayer = HarstemsAunt()
    print("Bot starting")

    races:list = [
        Race.Terran,
        Race.Zerg,
        Race.Protoss
    ]

    enemy:Race = choice(races)

    run_game(maps.get(choice(MAP_LIST)),
             [
                 Bot(AiPlayer.race, HarstemsAunt(debug=True)),
                 Computer(enemy, difficulty=(Difficulty.Hard))
             ],
             realtime=False
        )
