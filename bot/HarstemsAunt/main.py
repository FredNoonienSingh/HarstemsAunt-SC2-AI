"""MainClass of the Bot handling"""
import threading
from typing import List
from itertools import chain
from .common import GATEWAY_UNTIS,WORKER_IDS,SECTORS,\
    ATTACK_TARGET_IGNORE,logger

"""SC2 Imports"""
from sc2.unit import Unit
from sc2.data import Race
from sc2.bot_ai import BotAI
from sc2.position import Point2
from sc2.ids.unit_typeid import UnitTypeId

"""PATHING"""
from HarstemsAunt.pathing import Pathing

"""MAP VISION"""
from map_vision.map_sector import MapSector

"""Actions"""
from actions.set_rally import set_rally, set_nexus_rally
from actions.speedmining import get_speedmining_positions, \
    split_workers, micro_worker

"""Utils"""
from utils.get_build_pos import get_build_pos

"""Unit Classes"""
# Ground
from Unit_Classes.Archon import Archons
from Unit_Classes.Zealots import Zealot
from Unit_Classes.Stalkers import Stalkers
from Unit_Classes.Immortal import Immortals
from Unit_Classes.HighTemplar import HighTemplar
from Unit_Classes.DarkTemplar import DarkTemplar

"""Wrappers"""
from HarstemsAunt.macro import marco
from HarstemsAunt.micro import micro

DEBUG = True

class HarstemsAunt(BotAI):
    pathing: Pathing

    # Ground Units
    zealots: Zealot
    archons: Archons
    stalkers: Stalkers
    immortals: Immortals
    high_templar: HighTemplar
    dark_templar: DarkTemplar

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.name = "HarstemsAunt"
        self.version = "1.5.1"
        self.race:Race = Race.Protoss

        self.game_step = None
        self.speedmining_positions = None

        self.expand_locs:list = []
        self.temp:list = []
        self.mined_out_bases:list = []
        self.researched:list = []

        # Move in to one tuple
        self.base_count:int = 5
        self.gas_count:int = 1
        
        # Rework build order so that is not necessary anymore
        self.gateway_count:int = 1
        self.robo_count:int = 1
        self.stargate_count:int = 1
        
        self.seen_enemys:list = []
        self.enemy_supply:int = 0
        self.last_tick:int = 0
 
        self.scout_probe_tag:int = None
        self.fighting_probes:list = []
        self.map_sectors:list = []
        self.army_groups:list = []

    @property
    def greeting(self):
        return f"I am {self.name} on Version{self.version}"

    async def on_before_start(self) -> None:
        top_right = Point2((self.game_info.playable_area.right, self.game_info.playable_area.top))
        bottom_right = Point2((self.game_info.playable_area.right, 0))
        top_left = Point2((0, self.game_info.playable_area.top))

        # Create Map_sectors
        sector_width:int = abs(top_right.x - top_left.x)//SECTORS

        for x in range(SECTORS):
            for y in range(SECTORS):
                upper_left: Point2 = Point2((0+(sector_width*x), 0+bottom_right.y+(sector_width*(y))))
                lower_right: Point2 = Point2((0+(sector_width*(x+1)),0+bottom_right.y+(sector_width*(y+1))))
                logger.info(f"upper_left {upper_left} lower_right {lower_right}")
                sector: MapSector = MapSector(self, upper_left, lower_right)
                self.map_sectors.append(sector)

    async def on_start(self):
        self.pathing = Pathing(self, DEBUG)
        self.stalkers = Stalkers(self, self.pathing)
        self.zealots = Zealot(self, self.pathing)
        await self.chat_send(self.greeting)
        self.expand_locs = list(self.expansion_locations)
        self.client.game_step = self.game_step
        self.speedmining_positions = get_speedmining_positions(self)

        for sector in self.map_sectors:
            sector.build_sector()
        split_workers(self)
        
        self._client.debug_create_unit([[UnitTypeId.STALKER, 5, self._game_info.map_center, 1]])

    async def on_step(self, iteration):
        
        labels = ["min_step","avg_step","max_step","last_step"]

        for i, value in enumerate(self.step_time):
            if value > 34:
                color = (0, 0, 255)
            else:
                color = (0, 255, 0)
            self.client.debug_text_screen(f"{labels[i]}: {value}", (0, 0.025+(i*0.025)), color=color, size=20)
        
        
        threads: list = []
        for i, sector in enumerate(self.map_sectors):
            t_0 = threading.Thread(target=sector.update())
            threads.append(t_0)
            t_1 = threading.Thread(target=sector.render_sector())
            threads.append(t_1)
            t_0.start()
            t_1.start()
        for t in threads:
            t.join()

        self.pathing.update()

        if self.townhalls and self.units:
            self.transfer_from: List[Unit] = []
            self.transfer_to: List[Unit] = []
            self.transfer_from_gas: List[Unit] = []
            self.transfer_to_gas: List[Unit] = []
            self.resource_by_tag = {unit.tag: unit for unit in chain(self.mineral_field, self.gas_buildings)}

            #TODO: Write a cannon rush response, that actually works
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

            for worker in self.workers:
                micro_worker(self, worker)

            if self.scout_probe_tag:
                scout:Unit = self.units.find_by_tag(self.scout_probe_tag)
                if scout:
                    if scout.distance_to(self.enemy_start_locations[0])<5:
                        scout.move(self.structures(UnitTypeId.NEXUS).furthest_to(scout))
                        self.scout_probe_tag = 69420666
                    else:
                        scout.move(self.enemy_start_locations[0], queue=True)

            build_pos = get_build_pos(self)
            if self.workers:
                worker = self.workers.closest_to(build_pos)
            await self.distribute_workers()
            await marco(self, worker, build_pos)
            await micro(self)

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

    @property
    def get_attack_target(self) -> Point2:
        if self.time > 300.0:
            if enemy_units := self.enemy_units.filter(
                lambda u: u.type_id not in ATTACK_TARGET_IGNORE
                and not u.is_flying
                and not u.is_cloaked
                and not u.is_hallucination
            ):
                return enemy_units.closest_to(self.start_location).position
            elif enemy_structures := self.enemy_structures:
                return enemy_structures.closest_to(self.start_location).position

        return self.enemy_start_locations[0]

    async def on_building_construction_started(self,unit):
        if self.time < 60:
            if unit.type_id == UnitTypeId.PYLON:
                for nexus in self.structures(UnitTypeId.NEXUS):
                    minerals =  \
                        self.expansion_locations_dict[nexus.position].mineral_field.sorted_by_distance_to(nexus)
                    await set_nexus_rally(self, nexus, minerals.closest_to(nexus))

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
                    logger.info(f"can not set rally point due to {e} ")
            case "RoboticsFacility":
                try:
                    await set_rally(self,unit, self.structures(UnitTypeId.NEXUS).center)
                except Exception as e:
                    logger.info(f"can not set rally point due to {e} ")

    async def on_enemy_unit_entered_vision(self, unit):
        if not unit.tag in self.seen_enemys and unit.type_id not in WORKER_IDS:
            self.seen_enemys.append(unit.tag)
            self.enemy_supply += self.calculate_supply_cost(unit.type_id)

    async def on_enemy_unit_left_vision(self, unit_tag):
        unit = self.enemy_units.find_by_tag(unit_tag)
        logger.info(f"{unit} left vision")

    async def on_unit_created(self, unit):
        if unit in GATEWAY_UNTIS:
            print(unit)
            self.last_gateway_units.append(unit.type_id)
        logger.info(f"{unit} created")

    async def on_unit_type_changed(self, unit, previous_type):
        logger.info(f"{unit} morphed from {previous_type}")

    async def on_unit_took_damage(self, unit, amount_damage_taken):
        logger.info(f"{unit} took {amount_damage_taken} damage")

    async def on_unit_destroyed(self, unit_tag):
        unit = self.enemy_units.find_by_tag(unit_tag)
        if unit:
            self.enemy_supply -= self.calculate_supply_cost(unit.type_id)

    async def on_upgrade_complete(self, upgrade):
        logger.info(f"researched {upgrade}")
        self.researched.append(upgrade)

    async def on_end(self,game_result):
        logger.info(f"game ended with result {game_result}")
        await self.client.leave()