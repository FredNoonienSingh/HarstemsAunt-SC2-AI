"""SC2 Imports"""
from sc2 import maps
from sc2.unit import Unit
from sc2.bot_ai import BotAI
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.unit_typeid import UnitTypeId
from sc2.player import Bot, Computer, Human

from main import run_ai

diffs = [
    Difficulty.VeryEasy,
    Difficulty.Easy,
    Difficulty.Medium,
    Difficulty.Hard,
    Difficulty.VeryHard,
    Difficulty.CheatVision,
    Difficulty.CheatMoney,
    Difficulty.CheatInsane
]

races = [
    Race.Zerg,
    Race.Protoss,
    Race.Terran
]

for dif in diffs:
    for r in races:
        run_ai(r, dif, False)