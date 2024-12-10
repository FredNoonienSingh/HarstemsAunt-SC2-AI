"""MainClass of the Bot handling"""
from __init__ import logger
from .common import MAP_LIST, GATEWAY_UNTIS, WORKER_IDS
from typing import List
from itertools import chain

"""SC2 Imports"""
from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.unit import Unit
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.position import Point2, Point3
from sc2.ids.unit_typeid import UnitTypeId
from sc2.player import Bot, Computer, Human

from HarstemsAunt.macro import marco


"""DEBUG TOOLS"""
from debugTools.gameinfo import draw_gameinfo
from debugTools.unit_lable import unit_label

"""Actions"""
from actions.set_rally import set_rally, set_nexus_rally
from actions.unit_controll import control_stalkers, control_phoenix, control_zealots
from actions.speedmining import get_speedmining_positions, split_workers, micro_worker

"""Utils"""
from utils.get_build_pos import get_build_pos
from utils.get_army_target import get_army_target, check_position
from utils.in_proximity import in_proximity_to_point

class HarstemsAunt(BotAI):

    def __init__(self, debug:bool=False) -> None:
        super().__init__()
        self.race:Race = Race.Protoss
        self.name:str = "HarstemsAunt"
        self.version:str = "1.5"
        self.greeting:str = " "
        self.debug:bool = debug
        self.game_step = None
        self.speedmining_positions = None
        self.last_enemy_army_pos = Point3((0,0,0))
        self.pos_checked = False
        self.expand_locs = []
        self.temp = []
        self.mined_out_bases = []
        self.tick_data = []
        self.map_corners = []
        self.map_ramps = []
        self.researched = []
        self.base_count = 5
        self.gas_count = 1
        self.gateway_count = 1
        self.robo_count = 0
        self.stargate_count = 1
        self.seen_enemys = []
        self.enemy_supply = 0
        self.chatter_counts = [1, 1, 1]
        self.last_tick = 0
        self.logger = logger
        self.scout_probe_tag = None
        self.last_gateway_units = []
        self.fighting_probes = []
 
    async def on_before_start(self) -> None:
        top_right = Point2((self.game_info.playable_area.right, self.game_info.playable_area.top))
        bottom_right = Point2((self.game_info.playable_area.right, 0))
        bottom_left = Point2((0, 0))
        top_left = Point2((0, self.game_info.playable_area.top))
        self.map_corners = [top_right, bottom_right, bottom_left, top_left]
        self.map_ramps = self.game_info.map_ramps
 
    async def on_start(self):
        self.expand_locs = list(self.expansion_locations)
        self.client.game_step = self.game_step
        self.speedmining_positions = get_speedmining_positions(self)
        split_workers(self)

    async def on_step(self, iteration):
        draw_gameinfo(self)
        
        for unit in self.units:
            unit_label(self, unit)
        
        if self.townhalls and self.units:
            self.transfer_from: List[Unit] = []
            self.transfer_to: List[Unit] = list()
            self.transfer_from_gas: List[Unit] = list()
            self.transfer_to_gas: List[Unit] = list()
            self.resource_by_tag = {unit.tag: unit for unit in chain(self.mineral_field, self.gas_buildings)}



            """
                THIS NEED TO BE REWORKED 
            """
            # Deal with Cannon rushes
            if self.time < 300:
                for th in self.townhalls:
                    if self.enemy_structures.closer_than(30, th):
                        for struct in self.enemy_structures.closer_than(30, th):
                            workers = self.workers.filter(lambda unit: unit not in self.fighting_probes).closest_n_units(struct.position,4)
                            for worker in workers:
                                self.fighting_probes.append(worker)
                                worker.attack(struct)
                            if self.enemy_units.closer_than(30, th):
                                enemy_builders = self.enemy_units.closer_than(30, th)
                                for builder in enemy_builders:
                                    attack_workers = self.workers.filter(lambda unit: unit not in self.fighting_probes).closest_n_units(builder,2)
                                    for aw in attack_workers:
                                        self.fighting_probes.append(aw)
                                        aw.attack(builder)

            for el in self.last_gateway_units:
                self.client.debug_text_simple(str(el))

            for worker in self.workers:
                micro_worker(self, worker)
            await self.distribute_workers(resource_ratio=2)

            if self.scout_probe_tag:
                scout:Unit = self.units.find_by_tag(self.scout_probe_tag)
                if scout:
                    if scout.distance_to(self.enemy_start_locations[0])<5:
                        scout.move(self.structures(UnitTypeId.NEXUS).furthest_to(scout))
                        self.scout_probe_tag = 69420666
                    else:
                        scout.move(self.enemy_start_locations[0], queue=True)

            # Needs improvement
            build_pos = get_build_pos(self)
            if self.workers:
                worker = self.workers.closest_to(build_pos)
            await marco(self, worker, build_pos)
  
            #### Will get moved to Micro as soon as i get there ####
            army_target = get_army_target(self)
            z = self.get_terrain_z_height(army_target)+1
            x,y = army_target.x, army_target.y
            pos_3d = Point3((x,y,z))

            self.client.debug_sphere_out(pos_3d, 3, (255,200,255))

            for zealot in self.units(UnitTypeId.ZEALOT):
                await control_zealots(self, zealot,army_target)
            await control_stalkers(self, army_target)
            await control_phoenix(self)

            self.pos_checked = check_position(self)

            # tie_breaker
            if self.units.closer_than(10, self.enemy_start_locations[0]) and not self.enemy_units and not self.enemy_structures:
                for loc in self.expand_locs:
                    worker = self.workers.closest_to(loc)
                    worker.move(loc)

            return

        if self.last_tick == 0:
            await self.chat_send(f"GG, you are probably a hackcheating smurf cheat hacker anyway also \
                {self.enemy_race} is IMBA")
            self.last_tick = iteration
        elif self.last_tick == iteration - 120:
            await self.client.leave()

    async def on_building_construction_started(self,unit):
        if self.time < 60:
            if unit.type_id == UnitTypeId.PYLON:
                for nexus in self.structures(UnitTypeId.NEXUS):
                    minerals =  \
                        self.expansion_locations_dict[nexus.position].mineral_field.sorted_by_distance_to(nexus)
                    await set_nexus_rally(self, nexus, minerals.closest_to(nexus))
        await self.client.move_camera(unit)

    async def on_building_construction_complete(self, unit):
        match unit.name:
            case "Nexus":
                self.gateway_count += 3
                if len(self.structures(UnitTypeId.NEXUS)) >= 3:
                    self.gas_count += 2
            case "Cyberneticscore":
                self.gateway_count += 1
            case "Assimilator":
                if self.gas_count < 2:
                    self.gas_count += 1
            case "Gateway":
                try:
                    await set_rally(self,unit, self.structures(UnitTypeId.NEXUS).center)
                except Exception as e:
                    self.logger.info(f"can not set rally point due to {e} ")
            case "RoboticsFacility":
                try:
                    await set_rally(self,unit, self.structures(UnitTypeId.NEXUS).center)
                except Exception as e:
                    self.logger.info(f"can not set rally point due to {e} ")

    async def on_enemy_unit_entered_vision(self, unit):
        if not unit.tag in self.seen_enemys and unit.type_id not in WORKER_IDS:
            self.seen_enemys.append(unit.tag)
            self.enemy_supply += self.calculate_supply_cost(unit.type_id)
            await self.client.move_camera(unit)

    async def on_enemy_unit_left_vision(self, unit_tag):
        unit = self.enemy_units.find_by_tag(unit_tag)
        self.logger.info(f"{unit} left vision")
        if unit:
            self.last_enemy_army_pos = unit.position3d
            self.pos_checked = False

    async def on_unit_created(self, unit):
        if unit in GATEWAY_UNTIS:
            print(unit)
            self.last_gateway_units.append(unit.type_id)
        self.logger.info(f"{unit} created")
        await self.client.move_camera(unit)

    async def on_unit_type_changed(self, unit, previous_type):
        self.logger.info(f"{unit} morphed from {previous_type}")

    async def on_unit_took_damage(self, unit, amount_damage_taken):
        await self.client.move_camera(unit)
        self.logger.info(f"{unit} took {amount_damage_taken} damage")

    async def on_unit_destroyed(self, unit_tag):
        unit = self.enemy_units.find_by_tag(unit_tag)
        if unit:
            self.enemy_supply -= self.calculate_supply_cost(unit.type_id)

    async def on_upgrade_complete(self, upgrade):
        self.logger.info(f"researched {upgrade}")
        self.researched.append(upgrade)

    async def on_end(self,game_result):
        self.logger.info(f"game ended with result {game_result}")
        await self.client.leave()
