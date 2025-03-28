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
from sc2.player import Bot, Computer
from sc2.data import Difficulty,AIBuild, Race
from HarstemsAunt.main import HarstemsAunt
from HarstemsAunt.common import MAP_LIST, logger

from benchmarks.utils import Utils

parser = argparse.ArgumentParser(prog='Harstems Aunt')

races_dict: dict = {
    'terran': Race.Terran, 
    'zerg': Race.Zerg,
    'protoss': Race.Protoss,
    'random': Race.Random
}

builds_dict:dict = {
        'random':AIBuild.RandomBuild,
        'rush':AIBuild.Rush,
        'timing':AIBuild.Timing,
        'power':AIBuild.Power,
        'macro':AIBuild.Macro,
        'air':AIBuild.Air
}

difficulty_dict:dict = {
        'very_easy':Difficulty.VeryEasy,
        'easy':Difficulty.Easy,
        'medium':Difficulty.Medium,
        'medium_hard':Difficulty.MediumHard,
        'hard':Difficulty.Hard,
        'harder':Difficulty.Harder,
        'very_hard':Difficulty.VeryHard,
        'cheat_0':Difficulty.CheatVision,
        'cheat_1':Difficulty.CheatMoney,
        'cheat_2':Difficulty.CheatInsane,
}

def run_full_benchmark(arguments:dict) -> None:
    """This will run a big benchmark before deploying"""
    logger.info("Benchmarking against AI_Players")
    bot = Bot(Race.Protoss,HarstemsAunt(debug=False,benchmark=False))
    for race in races_dict.values():
        for difficulty in [Difficulty.VeryHard,Difficulty.CheatVision,Difficulty.CheatMoney,Difficulty.CheatInsane]:
            enemy_bot = Computer(race, difficulty)
            arena = maps.get(choice(MAP_LIST))
            game_result = run_game(arena,[bot,enemy_bot],realtime=arguments.realtime, sc2_version=arguments.sc2_version)
            result_dict = {
                "difficulty": difficulty, 
                "map": arena,
                "result": game_result
            }
            Utils.write_dict_to_csv(result_dict, "benchmarks/data/full_bench.csv")

    logger.info("Benchmarking Scenarios")
    bot = Bot(Race.Protoss,HarstemsAunt(debug=False,benchmark=True))
    enemy_bot = Computer(Race.Protoss, Difficulty.CheatInsane)
    for arena in MAP_LIST:
        arena = maps.get(arena)
        run_game(arena,[bot,enemy_bot],\
            realtime=arguments.realtime, \
            sc2_version=arguments.sc2_version
            )


# Start game
if __name__ == "__main__":

    if "--LadderServer" in sys.argv:
        bot = Bot(Race.Protoss, HarstemsAunt())
        # Ladder game started by LadderManager
        logger.info("Starting ladder game...")
        result, opponentid = run_ladder_game(bot)
        logger.info(f"{result}, against opponent , {opponentid}")

    else:
        BenchmarkSettings = parser.add_argument_group('Benchmark Settings')
        BenchmarkSettings.add_argument('-bench', '--benchmark',
                                      action='store_true'
                                      )
        BenchmarkSettings.add_argument('-bm', '--benchmark_message',
                                      type=str,
                                      help="message that will be recorded in Benchmark output",
                                      default=None
                                      )
        BenchmarkSettings.add_argument('-bmax_iter', '--benchmark_max_iterations',
                                      type=int,
                                      help="Number of maximum iterations for Benchmark"
                                      )
        BenchmarkSettings.add_argument('-fb', '--full_benchmark',
                                       action='store_true'
                                       )

        DebugSettings = parser.add_argument_group('Debug Settings')
        DebugSettings.add_argument('-d', '--debug',
                                 action='store_true'
                                 )
        DebugSettings.add_argument('-dc', '--debug_config',
                                   type=str,
                                   default='bot/configs/debug_config.json'
                                   )

        BotSettings = parser.add_argument_group("Bot Settings")
        BotSettings.add_argument('-r','--race',
                                type=str,
                                help="Name of Enemy Race terran, zerg, protoss",
                                default='terran'
                                )
        BotSettings.add_argument('-di','--difficulty',
                                type=str,
                                help="strength of the enemy player",
                                default='hard'
                                )
        BotSettings.add_argument(
                                '-aiB', '--ai_build',
                                type=str,
                                default=None
                                )
        BotSettings.add_argument('-m','--map',
                                type=str,
                                help="Name of the Map",
                                default=None
                                )
        BotSettings.add_argument('-t', '--realtime',
                                 action='store_true'
                                 )
        BotSettings.add_argument('-v','--sc2_version',
                                type=str,
                                help="Version of the sc2 client",
                                default="5.0.10"
                                )

        logger.info("Starting local game...")
        args = parser.parse_args()

        if args.realtime:
            logger.warning("running in realtime may lead to unexpected behavior and crashes")



        full_benchmark: bool = args.full_benchmark

        if full_benchmark:
            run_full_benchmark(args)
            sys.exit()

        enemy_race: Race = races_dict.get(args.race)
        enemy_strength: Difficulty = difficulty_dict.get(args.difficulty)
        ai_build: AIBuild = builds_dict.get(args.ai_build)

        debug_params: dict = Utils.read_json(args.debug_config)

        bot = Bot(Race.Protoss,\
            HarstemsAunt(debug=args.debug,\
                #debug_config=args.debug_config,\
                benchmark=args.benchmark
                )
            )
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
