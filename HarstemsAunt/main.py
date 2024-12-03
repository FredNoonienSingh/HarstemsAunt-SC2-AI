"""MainClass of the Bot handling"""
import csv
from common import MAP_LIST
from random import choice
from datetime import datetime

"""SC2 Imports"""
from sc2 import maps
from sc2.unit import Unit
from sc2.data import Alert
from sc2.position import Point2
from sc2.bot_ai import BotAI
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.unit_typeid import UnitTypeId
from sc2.player import Bot, Computer, Human

"""MACRO"""
from macro.game_start import game_start
from macro.infrastructure import build_infrastructure

"""Actions"""
from actions.expand import expand
from actions.chronoboosting import chronoboosting
from actions.set_rally import set_nexus_rally
from actions.build_supply import build_supply
from actions.unit_controll import control_stalkers, control_phoenix, control_zealots
from actions.build_structure import build_structure, build_gas
from actions.build_army import build_gateway_units, build_stargate_units, build_robo_units

"""Utils"""
from utils.get_build_pos import get_build_pos
from utils.in_proximity import unit_in_proximity
from utils.can_build import can_build_unit, can_build_structure, can_research_upgrade

class HarstemsAunt(BotAI):

    def __init__(self, debug:bool=False) -> None:
        super().__init__()
        self.race:Race = Race.Protoss
        self.name:str = "HarstemsAunt"
        self.version:str = "0.1"
        self.debug:bool = debug
        self.expand_locs = []
        self.temp = []
        self.mined_out_bases = []
        self.tick_data = []
        self.map_corners = []
        
        """ECO COUNTER"""
        self.base_count = 5
        self.gas_count = 1
        
        """INFRA COUNTER"""
        self.gateway_count = 1
        self.robo_count = 0
        self.stargate_count = 1

        """ENEMY DATA"""
        self.seen_enemys = []
        self.enemy_supply = 12
        
        self.chatter_counts = [1, 1, 1]
        self.last_tick = 0

    async def writetocsv(self,path):
        with open(path, mode='w') as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerows(self.tick_data)
 
    async def on_before_start(self) -> None:
        top_right = Point2((self.game_info.playable_area.right, self.game_info.playable_area.top))
        bottom_right = Point2((self.game_info.playable_area.right, 0))
        bottom_left = Point2((0, 0))
        top_left = Point2((0, self.game_info.playable_area.top))
        self.map_corners = [top_right, bottom_right, bottom_left, top_left]
 
    async def on_start(self):
        await self.chat_send("GL HF")
        self.expand_locs = list(self.expansion_locations)

    async def on_step(self, iteration):
        if self.townhalls and self.units:
            """CAMERA CONTROL"""
            pos = self.units.closest_n_units(self.enemy_start_locations[0], 1)[0] \
                if not self.enemy_units else self.units.closest_to(self.enemy_units.center)
            await self.client.move_camera(pos)

            """CHRONOBOOSTING"""
            await chronoboosting(self)
            
            for townhall in self.townhalls:
                """THIS DOES NOT SEEM TO WORK"""
                minerals =  self.expansion_locations_dict[townhall.position].mineral_field.sorted_by_distance_to(townhall)
                if not minerals:
                    if not townhall in self.mined_out_bases:
                        self.mined_out_bases.append(townhall)

                if townhall.is_ready and self.structures(UnitTypeId.PYLON) \
                    and self.structures(UnitTypeId.GATEWAY) and len(self.structures(UnitTypeId.ASSIMILATOR)) < self.gas_count \
                        and not self.already_pending(UnitTypeId.ASSIMILATOR):
                    await build_gas(self, townhall)
                if townhall.is_idle and can_build_unit(self, UnitTypeId.PROBE):
                    townhall.train(UnitTypeId.PROBE)
                await self.distribute_workers(resource_ratio=2)

            build_pos = get_build_pos(self)             # THIS NEEDS TO IMPROVED
            worker = self.workers.closest_to(build_pos)
            if self.time < 180:
                await game_start(self, worker, build_pos)

            """INFRASTRUCTURE"""
            await build_infrastructure(self,worker, build_pos)

            """UPGRADES"""
            if self.structures(UnitTypeId.TWILIGHTCOUNCIL) and self.can_afford(UpgradeId.BLINKTECH):
                self.research(UpgradeId.BLINKTECH)

            if self.units(UnitTypeId.ZEALOT):
                if self.structures(UnitTypeId.TWILIGHTCOUNCIL) and self.can_afford(UpgradeId.CHARGE):
                    self.research(UpgradeId.CHARGE)

            """ARMY"""
            if len(self.units(UnitTypeId.STALKER)) > 20:
                await build_gateway_units(self, UnitTypeId.ZEALOT)
            await build_gateway_units(self, UnitTypeId.STALKER)
            await build_stargate_units(self, UnitTypeId.PHOENIX)

            await build_supply(self, build_pos)
            await expand(self)
            
            """Handling Alerts & Mined out Bases"""
            if self.alert(Alert.VespeneExhausted):
                self.gas_count += 1
            if not len(self.mined_out_bases) == len(self.temp):
                self.base_count += 1
                self.temp = self.mined_out_bases

            """UNIT CONTROL"""
            await control_zealots(self)
            await control_stalkers(self)
            await control_phoenix(self)

            return

        """IF GAME IS LOST"""
        if self.last_tick == 0:
            await self.chat_send(f"GG, you are probably a hackcheating smurf cheat hacker anyway also {self.enemy_race} is IMBA")
            self.last_tick = iteration
        elif self.last_tick == iteration - 120:
            await self.client.leave()

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
            #case "Gateway":
             #   await set_nexus_rally(self, self.structures(UnitTypeId.NEXUS)[0], self.structures(UnitTypeId.NEXUS)[0].position.towards(self.game_info.map_center, -5))

    async def on_enemy_unit_entered_vision(self, unit):
        if not unit.tag in self.seen_enemys:
            self.seen_enemys.append(unit.tag)
            self.enemy_supply += self.calculate_supply_cost(unit.type_id)

    async def on_unit_destroyed(self, unit_tag):
        unit = self.enemy_units.find_by_tag(unit_tag)
        if unit:
            self.enemy_supply -= self.calculate_supply_cost(unit.type_id)
        elif not unit and self.chatter_counts[0] == 1:
            self.chatter_counts[0] = 0
            await self.chat_send("RUDE !!!")

    async def on_end(self,game_result):
       # path = f'data/{self.name}_{self.version}_vs{self.enemy_race}_at_{datetime.now()}_{game_result}.csv'
        #await self.writetocsv(path)
        await self.client.leave()

def run_ai(race, diffiicultiy, time):
    AiPlayer = HarstemsAunt()
    run_game(maps.get(choice(MAP_LIST)),
             [
                Bot(AiPlayer.race, HarstemsAunt(debug=True)),
                Computer(race, difficulty=(diffiicultiy))
             ],
             realtime=time
        )

def play_against_ai(race):
    AiPlayer = HarstemsAunt()
    run_game(maps.get(choice(MAP_LIST)),
             [
                 Bot(AiPlayer.race, HarstemsAunt(debug=True)),
                 Human(race, "NoonienSingh", False)
             ],
             realtime=True
        )

if __name__ == "__main__":
    races:list = [
        Race.Terran,
        Race.Zerg,
        Race.Protoss
        ]
    enemy:Race = Race.Zerg
    
    #play_against_ai(Race.Protoss)
    run_ai(enemy,Difficulty.Hard, False)