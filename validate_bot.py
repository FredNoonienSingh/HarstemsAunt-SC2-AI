import sys
from random import choice
from HarstemsAunt.main import HarstemsAunt
from HarstemsAunt.common import MAP_LIST, RACES

from training_bots.lift_hide import Lift
from training_bots.lift_topright import LiftTopRight
from training_bots.PF_rush import PFrush
from training_bots.pool12_allin import Pool12AllIn
from training_bots.single_worker_attack import SingleWorker
from training_bots.worker_rush import WorkerRushBot

from __init__ import run_ladder_game

from sc2 import maps
from sc2.main import run_game
from sc2.data import Difficulty,Race
from sc2.player import Bot, Computer

bot = Bot(Race.Protoss, HarstemsAunt())
training_bots = [
    #Bot(Lift.RACE, Lift()),
    Bot(LiftTopRight.RACE, LiftTopRight())
]


# Start game
if __name__ == "__main__":
    
    for t_bot in training_bots:
        # Local game
        print("Starting local game...")
        run_game(maps.get(choice(MAP_LIST)), \
            [Computer(choice(RACES), Difficulty.Harder), t_bot], \
                realtime=False, sc2_version="5.0.10")
