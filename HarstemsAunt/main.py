"""MainClass of the Bot handling"""
import csv
from __init__ import logger
from random import choice
from .common import MAP_LIST

"""SC2 Imports"""
from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.main import run_game
from sc2.position import Point2, Point3
from sc2.data import Race, Difficulty
from sc2.ids.unit_typeid import UnitTypeId
from sc2.player import Bot, Computer, Human

"""MACRO"""
from macro.upgrade import get_upgrades
from macro.game_start import game_start
from macro.build_army import build_army
from macro.infrastructure import build_infrastructure

"""Actions"""
from actions.expand import expand
from actions.set_rally import set_rally, set_nexus_rally
from actions.build_structure import build_gas
from actions.build_supply import build_supply
from actions.chronoboosting import chronoboosting
from actions.unit_controll import control_stalkers, control_phoenix, control_zealots

"""Utils"""
from utils.can_build import can_build_unit
from utils.handle_alerts import handle_alerts
from utils.get_build_pos import get_build_pos
from utils.get_army_target import get_army_target, check_position

class HarstemsAunt(BotAI):

    def __init__(self, debug:bool=False) -> None:
        super().__init__()
        self.race:Race = Race.Protoss
        self.name:str = "HarstemsAunt"
        self.version:str = "0.1"
        self.greeting:str = " "
        self.debug:bool = debug
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
        self.enemy_supply = 12
        self.chatter_counts = [1, 1, 1]
        self.last_tick = 0
        self.logger = logger
 
    async def on_before_start(self) -> None:
        top_right = Point2((self.game_info.playable_area.right, self.game_info.playable_area.top))
        bottom_right = Point2((self.game_info.playable_area.right, 0))
        bottom_left = Point2((0, 0))
        top_left = Point2((0, self.game_info.playable_area.top))
        self.map_corners = [top_right, bottom_right, bottom_left, top_left]
        self.map_ramps = self.game_info.map_ramps
 
    async def on_start(self):
        self.expand_locs = list(self.expansion_locations)

    async def on_step(self, iteration):
        if self.townhalls and self.units:
            await chronoboosting(self)

            for townhall in self.townhalls:

                # maybe not sorting the minerals does not create this issue
                minerals = self.expansion_locations_dict[townhall.position].mineral_field

                if not minerals:
                    if not townhall in self.mined_out_bases:
                        self.mined_out_bases.append(townhall)

                if townhall.is_ready and self.structures(UnitTypeId.PYLON) \
                    and self.structures(UnitTypeId.GATEWAY) and\
                        len(self.structures(UnitTypeId.ASSIMILATOR)) < self.gas_count \
                        and not self.already_pending(UnitTypeId.ASSIMILATOR):
                    await build_gas(self, townhall)

                # Build_Probes
                probe_count:int = len(self.structures(UnitTypeId.NEXUS))*16 + len(self.structures(UnitTypeId.ASSIMILATOR))*3
                if townhall.is_idle and can_build_unit(self, UnitTypeId.PROBE) and len(self.workers) < probe_count:
                    townhall.train(UnitTypeId.PROBE)
                await self.distribute_workers(resource_ratio=2)

            # Needs improvement
            build_pos = get_build_pos(self)
            if self.workers:
                worker = self.workers.closest_to(build_pos)
            else:
                return
            if self.time < 180:
                await game_start(self, worker)
  
            await build_infrastructure(self,worker, build_pos)
            get_upgrades(self)
            await build_army(self)
            await build_supply(self, build_pos)
            await expand(self)

            handle_alerts(self, self.alert)

            if not len(self.mined_out_bases) == len(self.temp):
                self.base_count += 1
                self.temp = self.mined_out_bases

            #### Will get moved to Micro as soon as i get there ####
            army_target = get_army_target(self)
            z = self.get_terrain_z_height(army_target)+1
            x,y = army_target.x, army_target.y
            pos_3d = Point3((x,y,z))

            self.client.debug_sphere_out(pos_3d, 5, (255,255,255))
            

            
            await control_zealots(self)
            await control_stalkers(self, army_target)
            await control_phoenix(self)
            
            self.pos_checked = check_position(self)
            return

        if self.last_tick == 0:
            await self.chat_send(f"GG, you are probably a hackcheating smurf cheat hacker anyway also \
                {self.enemy_race} is IMBA")
            self.last_tick = iteration
        elif self.last_tick == iteration - 120:
            await self.client.leave()

    async def on_building_construction_started(self,unit):
        if unit.type_id == UnitTypeId.PYLON and self.time < 60:
            for nexus in self.structures(UnitTypeId.NEXUS):
                minerals =  \
                    self.expansion_locations_dict[nexus.position].mineral_field.sorted_by_distance_to(nexus)
                await set_nexus_rally(self, nexus, minerals.closest_to(nexus))

    async def on_building_construction_complete(self, unit):
        match unit.name:
            case "Nexus":
                self.gateway_count += 3
                if len(self.structures(UnitTypeId.NEXUS)) > 3:
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
        if not unit.tag in self.seen_enemys:
            self.seen_enemys.append(unit.tag)
            self.enemy_supply += self.calculate_supply_cost(unit.type_id)

    async def on_enemy_unit_left_vision(self, unit_tag):
        unit = self.enemy_units.find_by_tag(unit_tag)
        self.logger.info(f"{unit} left vision")
        if unit:
            self.last_enemy_army_pos = unit.position3d
            self.pos_checked = False

    async def on_unit_created(self, unit):
        self.logger.info(f"{unit} created")

    async def on_unit_type_changed(self, unit, previous_type):
        self.logger.info(f"{unit} morphed from {previous_type}")

    async def on_unit_took_damage(self, unit, amount_damage_taken):
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
