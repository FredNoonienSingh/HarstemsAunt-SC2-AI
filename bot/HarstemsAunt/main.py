"""MainClass of the Bot handling"""
# pylint: disable=W0201
import os
import csv
import threading
from typing import List
from itertools import chain
from datetime import datetime

from sc2.unit import Unit
from sc2.bot_ai import BotAI
from sc2.position import Point2
from sc2.data import Race, Result
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.unit_typeid import UnitTypeId

# pylint: disable=E0401
#from Unit_Classes.Archon import Archons
from Unit_Classes.Zealots import Zealot
from Unit_Classes.Stalkers import Stalkers
#from Unit_Classes.Immortal import Immortals
from Unit_Classes.observer import Observer
#from Unit_Classes.HighTemplar import HighTemplar
#from Unit_Classes.DarkTemplar import DarkTemplar

from map_analyzer import MapData

# pylint: disable=E0402
from .macro import Macro
from .pathing import Pathing
from .army_group import ArmyGroup
from .map_sector import MapSector
from .common import WORKER_IDS,SECTORS,ATTACK_TARGET_IGNORE,logger
from .speedmining import get_speedmining_positions,split_workers, micro_worker


DEBUG = True

class HarstemsAunt(BotAI):
    """ Main class of the Bot"""
    macro: Macro
    pathing: Pathing
    map_data: MapData

    # Ground Units
    zealots: Zealot
    stalkers: Stalkers

    # Scouting Units
    observer : Observer

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.name = "HarstemsAunt"
        self.version = "1.1 alpha"
        self.race:Race = Race.Protoss

        self.base_count = 0

        self.start_time = None
        self.game_step = None
        self.speedmining_positions = None

        self.expand_locs:list = []
        self.researched:list = []

        self.seen_enemies:list = []
        self.enemies_lt_list: list = []
        self.enemy_supply:int = 0
        self.last_tick:int = 0

        self.map_sectors:list = []
        self.army_groups:list = []

    @property
    def greeting(self) -> str:
        """ Message that is supposed to be send at start"""
        return f"Hey {self.opponent_id}\n \
            i am {self.name} on Version {self.version}\n\
                GL HF"

    @property
    def match_id(self) -> str:
        """unique identifier of the game"""
        map_name:str = self.game_info.map_name
        return f"{self.start_time}_{self.name}_{self.opponent_id}_{map_name}"

    @property
    def data_path(self) -> str:
        """ path where information about the match will be stored"""
        return f"data/match/{self.match_id}/"

    @property
    def map_data_path(self) -> str:
        """ path to where data about the map can be stored"""
        map_name:str = self.game_info.map_name
        return f"data/map_data/{map_name}"

    @property
    def opponent_data_path(self):
        """ path to where data about the opponent can be stored"""
        opponent:str = self.opponent_id
        return f"data/opponent/{opponent}"

    @property
    def get_attack_target(self) -> Point2:
        """ Target of the main army group """
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

    def create_folders(self) -> None:
        """creates folders for data_path, map_data_path, opponent_data_path"""
        for path in [self.data_path,self.map_data_path,self.opponent_data_path]:
            if not os.path.exists(path):
                os.makedirs(path)

    async def on_before_start(self) -> None:
        """ coroutine called before the game starts """
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

    async def on_start(self) -> None:
        """ coroutine called on game_start """
        self.pathing = Pathing(self, DEBUG)
        self.macro:Macro = Macro(self)
        self.stalkers:Stalkers = Stalkers(self, self.pathing)
        self.zealots:Zealot = Zealot(self, self.pathing)
        self.observers:Observer = Observer(self, self.pathing)

        self.expand_locs = list(self.expansion_locations)
        self.client.game_step = self.game_step
        self.speedmining_positions = get_speedmining_positions(self)

        await self.chat_send(self.greeting)

        for sector in self.map_sectors:
            sector.build_sector()
        split_workers(self)

        initial_army_group:ArmyGroup = ArmyGroup(self, [],[],self.pathing)
        #run_by_group:ArmyGroup = ArmyGroup(self, [], [], self.pathing, GroupTypeId.RUN_BY)
        self.army_groups.append(initial_army_group)
        #self.army_groups.append(run_by_group)

    async def on_step(self, iteration:int):
        """ Coroutine running every game tick

        Args:
            iteration (_type_): current tick
        """
        labels = ["min_step","avg_step","max_step","last_step"]
        for i, value in enumerate(self.step_time):
            if value > 34:
                color = (0, 0, 255)
            else:
                color = (0, 255, 0)
            self.client.debug_text_screen(f"{labels[i]}: {value}", \
                (0, 0.025+(i*0.025)), color=color, size=20)

        threads: list = []
        for i, sector in enumerate(self.map_sectors):
            t_0 = threading.Thread(target=sector.update())
            threads.append(t_0)
            t_0.start()
        for t in threads:
            t.join()

        if not self.macro.build_order.opponent_builds_air:
            if [unit for unit in self.seen_enemies if unit.is_flying and unit.can_attack]:
                self.macro.build_order.opponent_builds_air = True
                await self.chat_send("I see you got an AirForce, i can do that too")

        if not self.macro.build_order.opponent_has_detection:
            if [unit for unit in self.seen_enemies if unit.is_flying and unit.can_attack]:
                self.macro.build_order.opponent_has_detection = True

        if not self.macro.build_order.opponent_uses_cloak:
            if [unit for unit in self.seen_enemies if (unit.is_cloaked and unit.can_attack) \
                or (unit.is_burrowed and unit.can_attack)]:
                self.macro.build_order.opponent_uses_cloak = True
                await self.chat_send("Stop hiding and fight like a honorable ... \
                        ähm... Robot?\ndo computers have honor ?")


        self.pathing.update(iteration)

        for j, group in enumerate(self.army_groups):
            await group.update(self.get_attack_target)
            self.client.debug_text_screen(f"{group.GroupTypeId}: {group.attack_target}",\
                (.25+(j*0.25), 0.025), color=(255,255,255), size=20)
            self.client.debug_text_screen(f"Supply:{group.supply}\
                Enemysupply:{group.enemy_supply_in_proximity}",\
                    (.25+(j*0.27), 0.05), color=(255,255,255), size=20)
            self.client.debug_text_screen(f"requested:{group.requested_units}",\
                    (.25+(j*0.27), 0.075), color=(255,255,255), size=20)

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
            # TODO: #69 write on distrubute workers coroutine
            await self.distribute_workers(1.22)
            await self.macro()

            # tie_breaker
            if self.units.closer_than(10, self.enemy_start_locations[0])\
                and not self.enemy_units and not self.enemy_structures:
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

    async def on_building_construction_started(self,unit:Unit) -> None:
        """ Coroutine called when the construction of a building starts 

        Args:
            unit (Unit): completed Structure
        """
        logger.info(f"construction of {unit} started")
        self.macro.build_order.increment_step()
        if unit.type_id in self.macro.build_order.buffer:
            self.macro.build_order.remove_from_buffer(unit.type_id)

    async def on_building_construction_complete(self, unit:Unit) -> None:
        """ Coroutine getting called upon the completion of a structure

        Args:
            unit (Unit): completed Structure
        """
        self.macro.build_order.constructed_structures.append(unit.type_id)

    async def on_enemy_unit_entered_vision(self, unit:Unit) -> None:
        """ Coroutine called when unit enters vision:
            -> sets Values for build order:
                - opponent_builds_air
                - opponent_has_detection 
                - opponent_uses_cloak
            creates a list of unit.tags for seen_enemies
        Args:
            unit (Unit): Unit
        """
        if not unit in self.seen_enemies and unit.type_id not in WORKER_IDS:
            self.seen_enemies.append(unit)
            self.enemy_supply += self.calculate_supply_cost(unit.type_id)

    #TODO: #73 Implement on_enemy_unit_left_vision logic
    async def on_enemy_unit_left_vision(self, unit_tag:int):
        """ Coroutine gets called when enemy left vision

        Args:
            unit_tag (int): unit_tag
        """
        pass

    async def on_unit_created(self, unit:Unit) -> None:
        """ Coroutine that gets called when Unit is created
            - adds created Units to the ArmyGroup

        Args:
            unit (Unit): Unit that gets created 
        """
        if not unit.type_id == UnitTypeId.PROBE:
            self.army_groups[0].units_in_transit.append(unit.tag)

        for group in self.army_groups:
            if unit.type_id in group.requested_units:
                self.macro.build_order.buffer.remove(unit.type_id)
                logger.info(f"{unit.type_id} got removed from {group}")

    async def on_unit_type_changed(self, unit:Unit, previous_type:UnitTypeId) -> None:
        """ Coroutine that gets called when a unit changes type:
            useful for warprism and Archon

        Args:
            unit (Unit): _description_
            previous_type (UnitTypeId): _description_
        """
        pass

    async def on_unit_took_damage(self, unit:Unit, amount_damage_taken:float) -> None:
        """ Coroutine that gets called when unit takes damage

        Args:
            unit (Unit): Unit that took damage 
            amount_damage_taken (float): amount of damage taken
        """
        pass

    async def on_unit_destroyed(self, unit_tag: int) -> None:
        """ Coroutine called when unit gets destroyed
            !!! IMPORTANT DOES NOT CONTAIN THE UNIT -> JUST THE TAG !!!

            adjusts enemy supply 
            
        Args:
            unit_tag (int): tag of destroyed unit
        """
        
        # Keeps the List as short as possible
        if unit_tag in self.seen_enemies:
            self.seen_enemies.remove(unit_tag)

        unit = self.enemy_units.find_by_tag(unit_tag)
        if unit:
            self.enemy_supply -= self.calculate_supply_cost(unit.type_id)

    async def on_upgrade_complete(self, upgrade:UpgradeId):
        """ Coroutine gets called on when upgrade is complete 

        Args:
            upgrade (UpgradeId): _description_
        """
        self.researched.append(upgrade)

    async def on_end(self,game_result:Result):
        """ Coroutine gets called on game end

            writes data to csv, before closing the connection
            
        Args:
            game_result (Result): Result of the game
        """
        data:list = [self.match_id, game_result, self.version, self.time]
        filename = f"{self.opponent_data_path}/results.csv"

        if not os.path.exists(filename):
            with open(filename, 'w', newline='', encoding='uft-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(data)
        else:
            with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(data)

        await self.client.leave()
