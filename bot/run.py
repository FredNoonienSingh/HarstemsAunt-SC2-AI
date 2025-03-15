"""make linter shut up"""
# pylint: disable=C0103
# pylint: disable=E0401
# pylint: disable=E0611
import sys
import argparse
from random import choice

from __init__ import run_ladder_game

from sc2 import maps
from sc2.main import run_game
from sc2.data import Difficulty, Race
from sc2.player import Bot, Computer

from HarstemsAunt.main import HarstemsAunt
from HarstemsAunt.common import MAP_LIST, logger

parser = argparse.ArgumentParser(prog='Harstems Aunt')

races_dict: dict = {
    'terran': Race.Terran, 
    'zerg': Race.Zerg,
    'protoss': Race.Protoss
}

difficulty_dict:dict = {
    'very_easy': Difficulty.VeryEasy, 
    'easy': Difficulty.Easy, 
    'hard': Difficulty.Hard
}

# Start game
if __name__ == "__main__":

    if "--LadderServer" in sys.argv:
        bot = Bot(Race.Protoss, HarstemsAunt())
        # Ladder game started by LadderManager
        logger.info("Starting ladder game...")
        result, opponentid = run_ladder_game(bot)
        logger.info(f"{result}, against opponent , {opponentid}")

    else:
        parser.add_argument('-bench', '--benchmark',
                            action='store_true')
        parser.add_argument('-d', '--debug',
                    action='store_true')
        parser.add_argument('-t', '--realtime',
                    action='store_true')
        parser.add_argument('-r','--race',
                            type=str,
                            help="Name of Enemy Race terran, zerg, protoss",
                            default='terran')
        parser.add_argument('-di','--difficulty',
                            type=str,
                            help="strength of the enemy player",
                            default='hard')
        parser.add_argument('-m','--map',
                            type=str,
                            help="Name of the Map",
                            default=None)
        parser.add_argument('-v','--sc2_version',
                            type=str,
                            help="Version of the sc2 client",
                            default="5.0.10")

        logger.info("Starting local game...")
        args = parser.parse_args()

        if args.realtime:
            logger.warning("running in realtime may lead to unexpected behavior and crashes")

        enemy_race: Race = races_dict.get(args.race)
        enemy_strength: Difficulty = difficulty_dict.get(args.difficulty)

        bot = Bot(Race.Protoss, HarstemsAunt(debug=args.debug, benchmark=args.benchmark))
        enemy_bot = Computer(enemy_race, enemy_strength)

        if args.map:
            try:
                arena = maps.get(args.map)
            # pylint: disable=W0718
            except Exception as e:
                logger.warning("Map can't be found... \n\t\tloading random map...")
                arena = maps.get(choice(MAP_LIST))
        else:
            arena = maps.get(choice(MAP_LIST))

        run_game(arena,[bot,enemy_bot],realtime=args.realtime, sc2_version=args.sc2_version)
