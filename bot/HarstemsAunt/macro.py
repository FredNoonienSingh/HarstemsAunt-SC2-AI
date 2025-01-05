from typing import Union

from sc2.data import Alert
from sc2.unit import Unit
from sc2.data import Race
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.ids.buff_id import BuffId
from sc2.position import Point2, Point3
from sc2.ids.ability_id import AbilityId
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.unit_typeid import UnitTypeId

from .utils import Utils
from .common import INITIAL_TECH,UNIT_COMPOSIOTION

async def warp_in_unit(bot: BotAI,unit:UnitTypeId,warp_in_position:Union[Point2,Point3,Unit]) -> bool:
    pos:Point2= warp_in_position.position.to2.random_on_distance(4)
    placement = await bot.find_placement(AbilityId.WARPGATETRAIN_STALKER, pos, placement_step=1)

    for gate in bot.structures(UnitTypeId.WARPGATE).idle:
        if Utils.can_build_unit(bot, unit):
            gate.warp_in(unit, placement)

async def build_gateway_units(bot:BotAI,unit_type:UnitTypeId):
    gate_aliases:list = [UnitTypeId.GATEWAY, UnitTypeId.WARPGATE]
    if Utils.can_build_unit(bot, unit_type):
        for gate in bot.structures.filter(lambda struct: struct.type_id in gate_aliases):
            if gate.is_idle and UpgradeId.WARPGATERESEARCH not in bot.researched:
                gate.train(unit_type)
            else:
                warp_in_pos = Utils.get_warp_in_pos(bot)
                await warp_in_unit(bot, unit_type, warp_in_pos)

async def build_stargate_units(bot:BotAI, unit_type:UnitTypeId):
    if Utils.can_build_unit(bot, unit_type):
        for gate in bot.structures(UnitTypeId.STARGATE):
            if gate.is_idle:
                gate.train(unit_type)

async def build_robo_units(bot:BotAI, unit_type:UnitTypeId):
    if Utils.can_build_unit(bot, unit_type):
        for robo in bot.structures(UnitTypeId.ROBOTICSFACILITY):
            if robo.is_idle:
                robo.train(unit_type)

class Macro:

    def __init__(self,bot:BotAI) -> None:
        self.bot = bot
        self.temp:list = []
        self.mined_out_bases: list = []

    @property
    def unit_composition(self) -> list:
        return UNIT_COMPOSIOTION.get(self.bot.race)

    @property
    def gas_count(self) -> int:
        return 0

    @property
    def base_count(self) -> int:
        return 0

    async def __call__(self):
        await self.chronoboost()
        self.get_upgrades()
        if self.bot.alert:
            self.handle_alerts(self.bot.alert)
        if self.bot.units(UnitTypeId.CYBERNETICSCORE) or self.bot.already_pending(UnitTypeId.CYBERNETICSCORE):
            await expand(self.bot)
        self.build_probes()

    def get_build_pos(self) -> Union[Point2, Point3, Unit]:
        return Point2((0,0))

    def get_build_worker(self) -> Unit:
        return self.bot.workers.closest_to(self.get_build_pos())

    async def build_infrastructure(self):
        enemy_race: Race = self.bot.enemy_race
        tech_buildings: list = INITIAL_TECH.get(enemy_race)
        tech_0: UnitTypeId = tech_buildings[0]
        tech_1: UnitTypeId = tech_buildings[1]

        build_pos = self.get_build_pos()
        worker = self.get_build_worker()
        bot = self.bot

        if not bot.structures(UnitTypeId.PYLON) and can_build_structure(bot, UnitTypeId.PYLON):
            await bot.build(UnitTypeId.PYLON, build_worker=worker, near=build_pos, max_distance=0)
        if not bot.structures(UnitTypeId.GATEWAY) and not bot.structures(UnitTypeId.WARPGATE) \
            and can_build_structure(bot, UnitTypeId.GATEWAY):
                await bot.build(UnitTypeId.GATEWAY, build_worker=worker, near=build_pos)
                return
        if not bot.structures(UnitTypeId.CYBERNETICSCORE) and can_build_structure(bot, UnitTypeId.CYBERNETICSCORE) \
            and not bot.already_pending(UnitTypeId.CYBERNETICSCORE):
            await bot.build(UnitTypeId.CYBERNETICSCORE, build_worker=worker, near=build_pos)
            return
        if (len(bot.structures(UnitTypeId.GATEWAY)) + len(bot.structures(UnitTypeId.WARPGATE))) < 2 and can_build_structure(bot, UnitTypeId.GATEWAY)\
            and bot.structures(tech_0):
            await bot.build(UnitTypeId.GATEWAY, build_worker=worker, near=build_pos)
        if not bot.structures(tech_0) and can_build_structure(bot, tech_0) and not bot.already_pending(tech_0):
            await bot.build(tech_0, build_worker=worker, near=build_pos)
        if bot.structures(tech_0) and can_build_structure(bot, tech_1) and not bot.structures(tech_1):
            await bot.build(tech_1, build_worker=worker, near=build_pos)
        if (len(bot.structures(UnitTypeId.GATEWAY)) + len(bot.structures(UnitTypeId.WARPGATE))) < 2 and can_build_structure(bot, UnitTypeId.GATEWAY)\
            and bot.structures(tech_1):
            await bot.build(UnitTypeId.GATEWAY, build_worker=worker, near=build_pos)

    def get_upgrades(self) -> None:
        attack = [
                UpgradeId.PROTOSSGROUNDWEAPONSLEVEL1,
                UpgradeId.PROTOSSGROUNDWEAPONSLEVEL2,
                UpgradeId.PROTOSSGROUNDWEAPONSLEVEL3,
            ]
    
        amor = [
                UpgradeId.PROTOSSGROUNDARMORSLEVEL1,
                UpgradeId.PROTOSSGROUNDARMORSLEVEL2,
                UpgradeId.PROTOSSGROUNDARMORSLEVEL3
            ]

        def upgrade(bot:BotAI, Upgrade_structure:UnitTypeId, Upgrade_id:UpgradeId) -> None:
            if bot.structures(Upgrade_structure).idle and can_research_upgrade(bot,Upgrade_id):
                bot.research(Upgrade_id)

        for forge in self.bot.structures(UnitTypeId.FORGE):
                for upgrades in attack:
                    if upgrades not in self.bot.researched:
                       upgrade(self.bot, UnitTypeId.FORGE, upgrades)
                for upgrades in amor:
                    if upgrades not in self.bot.researched:
                        upgrade(self.bot, UnitTypeId.FORGE, upgrades)

        if self.bot.structures(UnitTypeId.CYBERNETICSCORE):
            if not UpgradeId.WARPGATERESEARCH in self.bot.researched:
                upgrade(self.bot, UnitTypeId.CYBERNETICSCORE, UpgradeId.WARPGATERESEARCH)
        if self.bot.structures(UnitTypeId.TWILIGHTCOUNCIL):
            if not UpgradeId.CHARGE in self.bot.researched:
                upgrade(self.bot, UnitTypeId.TWILIGHTCOUNCIL, UpgradeId.CHARGE)

    def handle_alerts(self, alert:Alert) -> None:
        """ Possible Alerts:
            AlertError
            AddOnComplete
            BuildingComplete
            BuildingUnderAttack
            LarvaHatched
            MergeComplete
            MineralsExhausted
            MorphComplete
            MothershipComplete
            MULEExpired
            NuclearLaunchDetected
            NukeComplete
            NydusWormDetected
            ResearchComplete
            TrainError
            TrainUnitComplete
            TrainWorkerComplete
            TransformationComplete
            UnitUnderAttack
            UpgradeComplete
            VespeneExhausted
            WarpInComplete
        """
        match alert:
            case Alert.VespeneExhausted:
                self.gas_count += 1
            case Alert.NuclearLaunchDetected:
                pass 
            case Alert.NydusWormDetected:
                pass

    async def build_army(self) -> None:
        #TODO: #53 Find a better way to control Army composition
        #TODO: #54 Implement a Check for detectors in Enemy Comp, if not at DTs

        stalkers:int = len(self.bot.units(UnitTypeId.STALKER))
        # +1 to avoid ZeroDivision exception
        zealots:int = len(self.bot.units(UnitTypeId.ZEALOT)) +1
    
        if not stalkers or stalkers/zealots < 3:
            await build_gateway_units(self.bot, UnitTypeId.STALKER)
        else:
            await build_gateway_units(self.bot, UnitTypeId.ZEALOT)
        # await build_stargate_units(bot, UnitTypeId.PHOENIX)

        if not self.bot.units(UnitTypeId.OBSERVER):
            await build_robo_units(self.bot, UnitTypeId.OBSERVER)
        else:
            await build_robo_units(self.bot, UnitTypeId.IMMORTAL)

    async def build_supply(self) -> None:
        if not self.bot.can_afford(UnitTypeId.PYLON) or self.bot.supply_cap == 200:
            return
        if can_build_structure(self.bot,UnitTypeId.PYLON) and not \
            self.bot.already_pending(UnitTypeId.PYLON) and self.bot.supply_left < 8 \
                and len(self.bot.structures(UnitTypeId.NEXUS))>= 2 and self.bot.structures(UnitTypeId.CYBERNETICSCORE):
            worker:Unit = self.bot.workers.prefer_idle.closest_to(self.get_build_pos())
            await self.bot.build(UnitTypeId.PYLON, build_worker=worker, near=self.get_build_pos())

    async def build_structure(self,structure:UnitTypeId,build_pos:Union[Point2,Point3,Unit],worker:Unit) -> None:
        bot:BotAI = self.bot
        if can_build_structure(bot, structure):
            await bot.build(structure,near=build_pos,build_worker=worker)

    async def build_gas(self,nexus:Unit) -> None:
        bot:BotAI = self.bot
        vespene: Units = bot.vespene_geyser.closer_than(12, nexus)[0]
        if await bot.can_place_single(UnitTypeId.ASSIMILATOR, vespene.position):
            workers: Units = bot.workers.gathering
            if workers:
                worker: Unit = workers.closest_to(vespene)
                worker.build_gas(vespene)

    async def take_gas(self) -> None:
        if self.bot.townhall.is_ready and self.bot.structures(UnitTypeId.PYLON) \
            and self.bot.structures(UnitTypeId.GATEWAY) and\
            len(self.bot.structures(UnitTypeId.ASSIMILATOR)) < len(self.bot.structures(UnitTypeId.NEXUS).ready)*2 \
            and not self.bot.already_pending(UnitTypeId.ASSIMILATOR):
                await build_gas(self.bot, self.townhall)

    def check_mined_out(self) -> None:
        for townhall in self.bot.townhalls:
            minerals = self.bot.expansion_locations_dict[townhall.position].mineral_field

            if not minerals:
                if not townhall in self.bot.mined_out_bases:
                    self.bot.mined_out_bases.append(townhall)

            if not len(self.bot.mined_out_bases) == len(self.bot.temp):
                self.base_count += 1
                self.temp = self.mined_out_bases

    def build_probes(self) -> None:
        probe_count:int = len(self.bot.structures(UnitTypeId.NEXUS))*16 + len(self.bot.structures(UnitTypeId.ASSIMILATOR))*3
        if self.bot.structures(UnitTypeId.PYLON):
            for townhall in self.bot.townhalls.is_idle:
                if can_build_unit(self.bot, UnitTypeId.PROBE) and len(self.bot.workers) < probe_count:
                    townhall.train(UnitTypeId.PROBE)

    async def chronoboost(self) -> None:
        prios:list = [
            [
                UnitTypeId.ROBOTICSBAY,
                UnitTypeId.FLEETBEACON,
                UnitTypeId.TWILIGHTCOUNCIL,
                UnitTypeId.FORGE,
                UnitTypeId.CYBERNETICSCORE,
                UnitTypeId.DARKSHRINE,
                UnitTypeId.TEMPLARARCHIVE,
            ],
            [
                UnitTypeId.GATEWAY,
                UnitTypeId.ROBOTICSFACILITY,
                UnitTypeId.STARGATE,
            ],
            [
                UnitTypeId.NEXUS
            ]
        ]
        for prio in prios:
            structures = self.bot.structures.filter(lambda struct: not struct.is_idle and \
                not struct.has_buff(BuffId.CHRONOBOOSTENERGYCOST) and struct.type_id in prio)\
                    .sorted(lambda struct: struct.orders[0].progress, reverse=True)

            for struct in structures:
                chrono_nexus = self.bot.structures(UnitTypeId.NEXUS).filter(lambda nexus: nexus.energy > 50)
                if chrono_nexus:
                    chrono_nexus[0](AbilityId.EFFECT_CHRONOBOOSTENERGYCOST, struct)

    async def expand(self) -> None:
        bot:BotAI = self.bot
        if not bot.already_pending(UnitTypeId.NEXUS) and len(bot.structures(UnitTypeId.NEXUS))<bot.base_count:
            location:Union[Point2,Point3] = await bot.get_next_expansion()
            if location:
                if not bot.enemy_units.filter(lambda unit: unit.distance_to(location) < 2.75):
                    # Misplacing townhalls causes the Bot to crash, therefore it must be checked if the
                    # Area is free to build
                    # 2.75 is the radius of a nexus -
                    # if a unit is closer than this a nexus would be build away from the location
                    await bot.build(UnitTypeId.NEXUS, near=location, max_distance=0)