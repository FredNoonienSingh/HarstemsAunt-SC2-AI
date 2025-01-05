"""MainClass of the Bot handling"""

#TODO: #51 NEEDS to be cleaned up !

import os
import csv
import threading
from datetime import datetime
from typing import List
from itertools import chain

from sc2.unit import Unit
from sc2.data import Race
from sc2.bot_ai import BotAI
from sc2.position import Point2
from sc2.ids.unit_typeid import UnitTypeId

from map_analyzer import MapData
from map_vision.map_sector import MapSector

from .speedmining import get_speedmining_positions, \
    split_workers, micro_worker
from .pathing import Pathing
from .macro import Macro
from .army_group import ArmyGroup
from .common import GATEWAY_UNTIS,WORKER_IDS,SECTORS,\
    ATTACK_TARGET_IGNORE,logger

from Unit_Classes.Archon import Archons
from Unit_Classes.Zealots import Zealot
from Unit_Classes.Stalkers import Stalkers
from Unit_Classes.Immortal import Immortals
from Unit_Classes.observer import Observer
from Unit_Classes.HighTemplar import HighTemplar
from Unit_Classes.DarkTemplar import DarkTemplar


DEBUG = True

class HarstemsAunt(BotAI):
    macro: Macro
    pathing: Pathing
    map_data: MapData

    # Ground Units
    zealots: Zealot
    archons: Archons
    stalkers: Stalkers
    immortals: Immortals
    high_templar: HighTemplar
    dark_templar: DarkTemplar

    # Scouting Units
    observer : Observer

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.name = "HarstemsAunt"
        self.version = "1.6 alpha"
        self.race:Race = Race.Protoss

        self.start_time = None
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
        self.enemies_lt_list: list = []     #Units in the last tick
        self.enemy_supply:int = 0
        self.last_tick:int = 0

        self.scout_probe_tag:int = None
        self.fighting_probes:list = []
        self.map_sectors:list = []
        self.army_groups:list = []

    @property
    def greeting(self):
        return f"Hey {self.opponent_id}\n \
            i am {self.name} on Version {self.version}\n\
                GL HF"

    @property
    def match_id(self):
        map_name:str = self.game_info.map_name
        return f"{self.start_time}_{self.name}_{self.opponent_id}_{map_name}"

    @property
    def data_path(self):
        return f"data/match/{self.match_id}/"

    @property
    def map_data_path(self):
        map_name:str = self.game_info.map_name
        return f"data/map_data/{map_name}"

    @property
    def opponent_data_path(self):
        opponent:str = self.opponent_id
        return f"data/opponent/{opponent}"

    @property
    def get_attack_target(self) -> Point2:
        # Why the 5 Minute wait time
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

    def create_folders(self):
        for path in [self.data_path,self.map_data_path, self.opponent_data_path]:
            if not os.path.exists(path):
                os.makedirs(path)

    async def on_before_start(self) -> None:
        self.start_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Create Folders to save data for analysis
        self.create_folders()

        # set Edge Points
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
        self.macro = Macro(self)
        self.stalkers = Stalkers(self, self.pathing)
        self.zealots = Zealot(self, self.pathing)
        self.observers = Observer(self, self.pathing)

        self.expand_locs = list(self.expansion_locations)
        self.client.game_step = self.game_step
        self.speedmining_positions = get_speedmining_positions(self)

        await self.chat_send(self.greeting)

        for sector in self.map_sectors:
            sector.build_sector()
        split_workers(self)

        initial_army_group:ArmyGroup = ArmyGroup(self, [],[],self.pathing)
        self.army_groups.append(initial_army_group)

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
            t_0.start()
        for t in threads:
            t.join()

        self.pathing.update(iteration)

        for group in self.army_groups:
            await group.update(self.get_attack_target)
            self.client.debug_text_screen(f"{group.name}: {group.attack_pos}", \
                (.25, 0.025), color=(255,255,255), size=20)
            self.client.debug_text_screen(f"Supply:{group.supply} \
                Enemysupply:{group.enemy_supply_in_proximity}", \
                    (.25, 0.05), color=(255,255,255), size=20)

        if self.townhalls and self.units:
            self.transfer_from: List[Unit] = []
            self.transfer_to: List[Unit] = []
            self.transfer_from_gas: List[Unit] = []
            self.transfer_to_gas: List[Unit] = []
            self.resource_by_tag = {unit.tag: unit for unit in \
                chain(self.mineral_field, self.gas_buildings)}

            #TODO: #33 Write a cannon rush response, that actually works
            for townhall in self.townhalls:
                workers_in_base = self.enemy_units.closer_than(15, townhall)\
                    .filter(lambda unit: unit.type_id in WORKER_IDS)
                for worker in workers_in_base:
                    close_worker = self.workers.prefer_idle.closest_to(worker)
                    close_worker.attack(worker)

            for worker in self.workers:
                micro_worker(self, worker)
            await self.distribute_workers()
            await self.macro()

            # tie_breaker
            if self.units.closer_than(10, self.enemy_start_locations[0])\
                and not self.enemy_units and not self.enemy_structures:
                for loc in self.expand_locs:
                    worker = self.workers.closest_to(loc)
                    worker.move(loc)

            return

        # If the Game is lost, but i want to insult the Opponent before i leave
        if self.last_tick == 0:
            await self.chat_send(f"GG, you are probably a hackcheating smurf cheat hacker anyway also \
                {self.enemy_race} is IMBA")
            self.last_tick = iteration
        elif self.last_tick == iteration - 120:
            await self.client.leave()

    async def on_building_construction_started(self,unit):
        pass

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

    async def on_enemy_unit_entered_vision(self, unit):
        if not unit.tag in self.seen_enemys and unit.type_id not in WORKER_IDS:
            self.seen_enemys.append(unit.tag)
            self.enemy_supply += self.calculate_supply_cost(unit.type_id)

    async def on_enemy_unit_left_vision(self, unit_tag):
        pass

    async def on_unit_created(self, unit):
        if unit.type_id in GATEWAY_UNTIS:
            self.army_groups[0].units_in_transit.append(unit.tag)
        if unit.type_id == UnitTypeId.OBSERVER or unit.type_id == UnitTypeId.IMMORTAL:
            self.army_groups[0].units_in_transit.append(unit.tag)

    async def on_unit_type_changed(self, unit, previous_type):
        pass

    async def on_unit_took_damage(self, unit, amount_damage_taken):
        pass

    async def on_unit_destroyed(self, unit_tag):
        # Keeps the List as short as possible
        if unit_tag in self.seen_enemys:
            self.seen_enemys.remove(unit_tag)

        unit = self.enemy_units.find_by_tag(unit_tag)
        if unit:
            self.enemy_supply -= self.calculate_supply_cost(unit.type_id)

    async def on_upgrade_complete(self, upgrade):
        self.researched.append(upgrade)

    async def on_end(self,game_result):
        data:list = [self.match_id, game_result, self.version, self.time]
        filename = f"{self.opponent_data_path}/results.csv"

        if not os.path.exists(filename):
            with open(filename, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(data)
        else:
            with open(filename, 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(data)

        await self.client.leave()