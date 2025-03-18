""" scenario class for Benchmarks"""
from typing import Union, List, Tuple, Dict

import numpy as np

# pylint: disable=C0411
from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.position import Point2
from sc2.ids.unit_typeid import UnitTypeId

# pylint: disable=E0402
from .common import TOWNHALL_IDS
from .result import Result, EndCondition

class Scenario:

    def __init__(self,
                 bot:BotAI,
                 title:str,
                 comment:str,
                 position_name:str,
                 enemy_position:Union[Point2,Unit],
                 own_position: Union[Point2, Unit],
                 enemy_units: List[Tuple[UnitTypeId,int]],
                 own_units: List[Tuple[UnitTypeId,int]],
                 options:Dict,
                 initial_score:int,
                 initial_damage_dealt_life: float,
                 initial_damage_dealt_shield: float,
                 initial_damage_taken_life:float,
                 initial_damage_taken_shield:float,
                 engagement_radius:float = 5,
                 max_runtime: float = 30
                 ) ->None:
        self.bot = bot
        self.title = title
        self.comment = comment
        self.position_name = position_name
        self.enemy_position = enemy_position
        self.own_position = own_position
        self.enemy_units = enemy_units
        self.own_units = own_units
        self.options = options
        self.initial_score = initial_score,
        self.initial_damage_dealt_life = initial_damage_dealt_life,
        self.initial_damage_dealt_shield = initial_damage_dealt_shield,
        self.initial_damage_taken_life = initial_damage_taken_life,
        self.initial_damage_taken_shield = initial_damage_taken_shield,
        self.engagement_radius = engagement_radius
        self.max_runtime = max_runtime
        self.start_time = self.bot.time
        self.running = False
        self.ending_condition:EndCondition = EndCondition.PENDING
        self.damage_taken:float = 0
        self.observations:List = []
        self.pathing_grids:List[Tuple[np.ndarray,np.ndarray,\
            np.ndarray, np.ndarray]] = []

    def __repr__(self) -> None:
        return f"Scenario {self.title} playing at {self.position_name}"

    def record_observation(self) -> None:
        """records raw gamedata"""
        enemies = []
        for unit in self.bot.enemy_units:
            enemies.append(
                (unit.type_id, unit.health, unit.shield, \
                    unit.energy, unit.buffs, unit.tag, unit.position_tuple)
                )
        units = []
        for unit in self.bot.units:
            units.append(
                (unit.type_id, unit.health, unit.shield, \
                    unit.energy, unit.buffs, unit.tag, unit.position_tuple)
                )
        effects = []
        for effect in self.bot.state.effects:
            effects.append(
                (effect)
                )
        self.observations.append(
            {"enemies": enemies,
             "units": units, 
             "effects": effects}
            )

    def get_state_delta(self, states:Dict) -> Tuple[float, float, float, float, float]:
        current_score:float = states.get('score')
        current_damage_dealt_life:float = states.get('total_damage_dealt_life')
        current_damage_dealt_shield:float = states.get('total_damage_dealt_shields')
        current_damage_taken_life:float = states.get('total_damage_taken_life')
        current_damage_taken_shield:float = states.get('total_damage_taken_shields')
        
        benchmark_score:float = current_score - self.initial_score[0]
        benchmark_damage_dealt_life: float = current_damage_dealt_life- \
            self.initial_damage_dealt_life[0]
        benchmark_damage_dealt_shield: float = current_damage_dealt_shield -\
            self.initial_damage_dealt_shield[0]
        benchmark_damage_taken_life: float = current_damage_taken_life- \
            self.initial_damage_taken_life[0]
        benchmark_damage_taken_shield: float = current_damage_taken_shield -\
            self.initial_damage_taken_shield[0]
        
        return (benchmark_score,
                benchmark_damage_dealt_life,
                benchmark_damage_dealt_shield,
                benchmark_damage_taken_life,
                benchmark_damage_taken_shield)

    def record_pathing_grids(self) -> None:
        ground_grid:np.ndarray = self.bot.pathing.ground_grid
        air_grid:np.ndarray = self.bot.pathing.air_grid
        detection_grid:np.ndarray = self.bot.pathing.detection_grid
        climber_grid: np.ndarray = self.bot.pathing.climber_grid

        self.pathing_grids.append(
            (ground_grid, air_grid, detection_grid, climber_grid)
            )

    async def generate_creep(self) -> None:
        distance:float = self.enemy_position.distance_to(self.own_position)
        await self.bot.client.debug_create_unit([[UnitTypeId.CREEPTUMOR, 1,\
            self.enemy_position.towards_with_random_angle(self.own_position,1),2]])
        await self.bot.client.debug_create_unit([[UnitTypeId.CREEPTUMOR, 1,\
            self.own_position.towards_with_random_angle(self.enemy_position,1),2]])
        await self.bot.client.debug_create_unit([[UnitTypeId.CREEPTUMOR, 1,\
            self.own_position.towards(self.enemy_position,distance/2),2]])

    async def clear_all(self, blind:bool=True):
        """clears all units and structures, beside the Townhalls """

        enemies:Units = self.bot.enemy_units
        own_units:Units = self.bot.units
        enemy_structure:Units = self.bot.enemy_structures.filter\
            (lambda struct: struct.type_id not in TOWNHALL_IDS)
        own_structures:Units = self.bot.structures.filter\
            (lambda struct: struct.type_id not in TOWNHALL_IDS)

        destroy_list:List = [enemies, own_units, enemy_structure, own_structures]
        for units in destroy_list:
            if units:
                await self.bot.client.debug_kill_unit(units)
        return True

    async def start_benchmark(self, blind:bool=True) -> None:
        """Starts the time for the benchmark"""

        if await self.clear_all(blind):
            current_time:int = self.bot.time
            self.start_time = current_time
            if self.options['has_creep']:
               await self.generate_creep()
            for instruction in self.enemy_units:
                await self.bot.client.debug_create_unit(
                    [[instruction[0], instruction[1],
                    self.enemy_position.\
                          towards(self.bot.enemy_start_locations[0],self.engagement_radius),2]]
                )
            for instruction in self.own_units:
                await self.bot.client.debug_create_unit(
                    [[instruction[0], instruction[1],
                    self.own_position.\
                          towards(self.bot.start_location,self.engagement_radius),1]]
                )

    def calculate_destroyed_units(self) -> Tuple[int, int]:
        """ calculates how many units got destroyed

        Returns:
            Tuple[int, int]: destroyed enemies, destroyed friendlies
        """
        destroyed_enemies:int = 0
        destroyed_units: int = 0

        for unit in self.enemy_units:
            unit_type:UnitTypeId = unit[0]
            initial_unit_count:int = unit[1]
            current_unit_count:int = len(self.bot.enemy_units(unit_type))
            destroyed_enemies += (initial_unit_count-current_unit_count)

        for unit in self.own_units:
            unit_type = unit[0]
            initial_unit_count = unit[1]
            current_unit_count = len(self.bot.units(unit_type))
            destroyed_units += (initial_unit_count-current_unit_count)

        return (destroyed_enemies, destroyed_units)

    def end_condition(self) -> bool:
        """Overwritten in SuBclasses """
        current_time:int = self.bot.time
        runtime = current_time - self.start_time
        under_runtime:bool = current_time >= self.start_time+self.max_runtime

        if not self.bot.enemy_units.filter(lambda unit: unit.type_id not in TOWNHALL_IDS)\
            and runtime > 2:
            self.ending_condition = EndCondition.VICTORY
            return True
        if not self.bot.units.filter(lambda unit: unit.type_id not in TOWNHALL_IDS)\
            and runtime > 2:
            self.ending_condition = EndCondition.DEFEAT
            return True
        if under_runtime:
            self.ending_condition = EndCondition.TIME_OUT
            return True
        return False

    async def end(self, state_dict:Dict) -> Result:
        """returns data on end"""
        time:float = self.bot.time - self.start_time
        bot_version: str = self.bot.version
        map_name:str = self.bot.game_info.map_name
        has_creep = self.options['has_creep']
        enemy_behavior = self.options['enemy_behavior']
        destroyed, lost = self.calculate_destroyed_units()
        states = self.get_state_delta(state_dict)
        
        return Result(self.title,
                      bot_version,
                      self.comment,
                      map_name,
                      self.position_name,
                      enemy_behavior,
                      has_creep,
                      self.enemy_units,
                      self.own_units,
                      time,
                      states[0],
                      states[1],
                      states[2],
                      states[3],
                      states[4],
                      destroyed,
                      lost,
                      self.observations,
                      self.pathing_grids,
                      self.ending_condition
                      )
