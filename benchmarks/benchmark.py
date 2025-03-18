""" Benchmarks the UnitMicro of any BurnySC2 """
from typing import List,Dict,Tuple
from functools import cached_property

from random import choice
#from datetime import datetime

# pylint: disable=C0411
from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.position import Point2
from sc2.ids.unit_typeid import UnitTypeId

# pylint: disable=E0402
from .utils import Utils
from .result import Result
from .scenario import Scenario
from .enemy_behavior import EnemyBehavior
from .common import WORKER_IDS, TOWNHALL_IDS,logger


ENDLESS: bool = False
class Benchmark:
    """Benchmaker for unit micro of BurnySC2 Bots"""

    def __init__(self,
                 bot:BotAI,
                 path_to_config:str="benchmarks/configs/config.json",
                 ) -> None:
        self.bot:BotAI = bot
        self.path_to_config = path_to_config
        self.current_index:int = 0
        self.scenario_running:bool = False
        self.start_time:int = bot.time
        self.scenario:Scenario = None
        self.enemy_behavior:EnemyBehavior = EnemyBehavior(self.bot)

    @cached_property
    def config(self) -> Dict:
        """loads config file and returns the content"""
        config:Dict = Utils.read_json(self.path_to_config)
        if not config:
            logger.warning("could not open config, loading defaults")
            return {
                    "endless":True,
                    "save_data":True,
                    "verbose": True,
                    "blind":False,
                    "max_runtime": 3,
                    "scenarios":"benchmarks/configs/short_test.json",
                    "output_dir":"benchmarks/data/"}
        return config

    @property
    def record_path(self) -> str:
        """creates a path to store the benchmark run"""
        bot_name:str = self.bot.name
        version:str = self.bot.version
        benchmark_name:str = f"benchmark_{bot_name}_v{version}"

        return f"{self.config['output_dir']}/{benchmark_name}.csv"

    @cached_property
    def scenarios(self) -> List[Scenario]:
        """builds a list of scenario"""
        temp:List = []
        unit_id = {str(unit_id): unit_id for unit_id in UnitTypeId}
        instructions:Dict = Utils.read_json(self.config['scenarios'])
        try:
            for instruction in instructions['benchmarks']:
                for pos in instruction['positions']:
                    positions:Tuple[Point2] = self.get_position(pos)
                    scenario:Dict = {
                    'title': instruction['title'],
                    'position_name': pos,
                    'enemy_position': positions[0],
                    'position': positions[1],
                    'enemy_units':\
                        [[unit_id.get(unit['unit_type']),unit['unit_count']]\
                        for unit in instruction['enemy_units']],
                    'own_units':\
                        [[unit_id.get(unit['unit_type']),unit['unit_count']]\
                        for unit in instruction['own_units']],
                    'options': instruction['options']
                    }
                    temp.append(scenario)
        # pylint: disable=W0718
        except Exception as e:
            logger.warning(e)

        return temp

    @property
    def current_scenario(self) -> Scenario:
        """returns the current scenario"""
        if self.current_index <= len(self.scenarios) -1:
            return self.scenarios[self.current_index]

    @property
    def next_scenario(self) -> Scenario:
        """returns the next scenario"""
        if self.current_index <= len(self.scenarios) -1:
            return self.scenarios[self.current_index+1]

    def get_position(self, position_name:str="center") -> Tuple[Point2]:
        """ returns the position on the map for a given position name"""
        enemy_spawn = self.bot.enemy_start_locations[0]
        spawn = self.bot.start_location
        center = self.bot.game_info.map_center
        ramps:Units = self.bot.game_info.map_ramps
        ramp:Unit = choice(ramps)

        positions:Dict[str:Point2] = {
            "ramp_top":(
                ramp.bottom_center.towards(ramp.top_center,-3),
                ramp.top_center.towards(ramp.bottom_center, -3)
                ),
            "ramp_bottom":(
                ramp.top_center.towards(ramp.bottom_center, -3),
                ramp.bottom_center.towards(ramp.top_center,-3)
            ),
            "enemy_spawn":(
                enemy_spawn.towards(center, -3),
                enemy_spawn.towards(center, 3)
            ),
            "spawn":(
                spawn.towards(center, 3),
                spawn.towards(center, -3)
            ),
            "center":(
                center.towards(enemy_spawn, 3),
                center.towards(spawn, 3)
            ),
            "center_crossed":(
                center.towards(enemy_spawn, -3),
                center.towards(spawn, -3)
            )
        }
        return positions.get(position_name, None)

    def record_damage_taken(self, damage:float) -> None:
        """records damage to scenario"""
        if self.scenario:
            self.scenario.damage_taken += damage

    def render_overlay(self) -> None:
        """renders overlay"""
        self.bot.client.debug_text_screen(
                "BENCHMARK", (0.01,.35),(255,255,0),26
            )
        self.bot.client.debug_text_screen(
            f"At Benchmark {self.current_index +1} of {len(self.scenarios)+1}",
            (0.02, 0.40), (255,255,0), 12
        )
        if self.scenario:
            self.bot.client.debug_text_screen(
                f"{self.scenario.title} @ {self.scenario.position_name}",
                (0.02, 0.42), (255,255,0), 12
            )
            self.bot.client.debug_text_screen(
                f"Status: {self.scenario.ending_condition}",
                (0.02, 0.44), (255,255,0), 12
            )
            time = round(self.bot.time - self.scenario.start_time, 2)
            self.bot.client.debug_text_screen(
                f"Running {time} seconds of {self.scenario.max_runtime} seconds",
                (0.02, 0.46), (255,255,0), 12
            )
            self.bot.client.debug_text_screen(
                f"enemy behavior {self.scenario.options.get("enemy_behavior")}",
                (0.02, 0.48), (255,255,0), 12
            )
            self.bot.client.debug_text_screen(
                f"Runs endless: {self.config['endless']}",
                (0.02, 0.50), (255,255,0), 12
            )
            self.bot.client.debug_text_screen(
                f"Saves to File: {self.config['save_data']}",
                (0.02, 0.52), (255,255,0), 12
            )

    async def prepare_benchmarks(self):
        """RUN IN on_start() of your bot class !"""
        await self.clear_all()
        await self.bot.client.debug_control_enemy()
        await self.bot.client.debug_show_map()

    async def destroy_workers(self) -> None:
        """Destroy enemy workers"""
        workers: Units = \
            self.bot.workers
        if workers:
            await self.bot.client.debug_kill_unit(workers)
        enemy_workers: Units = \
            self.bot.enemy_units.filter(lambda unit: unit.type_id in WORKER_IDS)
        if enemy_workers:
            await self.bot.client.debug_kill_unit(enemy_workers)

    async def __call__(self) -> None:
        """ RUN IN on_step() of your bot class"""
        if self.config['verbose']:
            self.render_overlay()
        await self.destroy_workers()
        if not self.scenario_running:
            await self.build_scenario()

        for unit in self.bot.units.filter(lambda unit: unit.type_id in TOWNHALL_IDS):
            self.bot.client.debug_set_unit_value(unit,2,unit.health_max)
        for unit in self.bot.enemy_units.filter(lambda unit: unit.type_id in TOWNHALL_IDS):
            self.bot.client.debug_set_unit_value(unit,2,unit.health_max)

        if self.scenario_running:
            enemy_behavior:str = self.scenario.options.get('enemy_behavior')
            self.scenario.record_observation()
            self.scenario.record_pathing_grids()

            if self.scenario.end_condition():
                result:Result = await self.scenario.end()
                await self.end_benchmark(result)
            else:
                if self.bot.enemy_units:
                    match enemy_behavior:
                        case "attack_retreat":
                            await self.enemy_behavior.attack_retreat(self.bot.enemy_units)
                        case "attack_towards":
                            await self.enemy_behavior.attack_towards(self.bot.enemy_units)
                        case "attack_weakest":
                            await self.enemy_behavior.attack_weakest(self.bot.enemy_units)
                        case "attack_closest":
                            await self.enemy_behavior.attack_closest(self.bot.enemy_units)
                        case _:
                            await self.enemy_behavior.attack_towards(self.bot.enemy_units)

                if self.bot.units and self.bot.enemy_units:
                    cam_center: Point2 = self.bot.units.center\
                        .towards(self.bot.enemy_units.center, 2)
                    await self.bot.client.move_camera(cam_center)
                if self.bot.units and not self.bot.enemy_units:

                    await self.bot.client.move_camera(self.bot.units.center)

    async def clear_all(self, blind:bool=True):
        """clears all units and structures, beside the Townhalls """
        await self.destroy_workers()
        enemies:Units = self.bot.enemy_units
        own_units:Units = self.bot.units
        enemy_structure:Units = self.bot.enemy_structures.filter\
            (lambda struct: struct.type_id not in TOWNHALL_IDS)
        own_structures:Units = self.bot.structures.filter\
            (lambda struct: struct.type_id not in TOWNHALL_IDS)

        destroy_list:List = [enemies, own_units, \
            enemy_structure, own_structures]
        for units in destroy_list:
            if units:
                await self.bot.client.debug_kill_unit(units)
        return True

    async def build_scenario(self) -> None:
        """Build current scenario"""
        if not self.current_scenario:
            return

        await self.clear_all()

        engagement_title:str = self.current_scenario.get("title")
        comment:str = self.bot.benchmark_message
        position_name:str=self.current_scenario.get('position_name')
        enemy_position: Point2 = \
            self.current_scenario.get("enemy_position")
        own_position: Point2 = \
            self.current_scenario.get("position")
        enemy_units:List[Tuple[UnitTypeId,int]] = \
            self.current_scenario.get("enemy_units")
        own_units:List[Tuple[UnitTypeId, int]] = \
            self.current_scenario.get("own_units")
        options:Dict = self.current_scenario.get('options')

        self.scenario = Scenario(self.bot,engagement_title,comment,\
            position_name,enemy_position,\
                own_position,enemy_units,own_units,options,\
                    max_runtime=self.config['max_runtime'])
        try:
            await self.scenario.start_benchmark(False)
        # pylint: disable=W0718
        except Exception as e:
            logger.warning(e)

        for unit in self.bot.units:
            self.bot.army_groups[0].add_combat_unit(unit)

        self.scenario_running = True

    async def end_benchmark(self, result: Result) -> None:
        """ Ends the benchmarks run and writes the results to csv files"""
        if self.config['save_data']:
            path:str = self.record_path
            content:dict = result.as_dict()
            Utils.write_dict_to_csv(content, path)

        if self.current_index < len(self.scenarios) -1:
            self.current_index += 1
        else:
            if self.config['endless']:
                self.current_index = 0
            else:
                await self.bot.client.leave()
        self.scenario_running = False
