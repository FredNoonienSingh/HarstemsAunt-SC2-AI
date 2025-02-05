"""DOCSTRING to shut up the Linter """
from typing import Union

from sc2.data import Alert
from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.game_data import Cost
from sc2.ids.buff_id import BuffId
from sc2.position import Point2, Point3
from sc2.ids.ability_id import AbilityId
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.unit_typeid import UnitTypeId

# pylint: disable=E0402
from .utils import Utils
from .production_buffer import ProductionBuffer
from .common import GATEWAY_UNITS, ROBO_UNITS, STARGATE_UNITS
from .build_order import BuildOrder, BuildInstruction, InstructionType

class Macro:
    """ Class handling the Marco aspect of the Game """
    def __init__(self,bot:BotAI) -> None:
        self.bot = bot
        self.temp:list = []
        self.mined_out_bases: list = []
        self.build_order = BuildOrder(self.bot)
        self.production_buffer = ProductionBuffer(self.bot)

    async def __call__(self) -> None:
        """ makes the class callable, get's executed to every tick in BotClass  """
        if self.bot.alert:
            await self.handle_alerts(self.bot.alert)

        await self.chronoboost()
        self.get_upgrades()

        await self.handle_instructions()
        await self.build_order.update()

        if not self.build_order.is_performing_initial_build:
            await self.build_supply()
        self.build_probes()

    def get_build_worker(self) -> Unit:
        """ returns the build worker """
        return self.bot.workers.closest_n_units(self.build_order.get_build_pos(), 1)[0]

    def get_production_structure(self, unit_type: UnitTypeId) -> UnitTypeId:
        """ returns the appropriate production structure

        Args:
            unit_type (UnitTypeId): unit_type for which the production structure is needed

        Returns:
            UnitTypeId: appropriate productions structure
        """
        if unit_type in GATEWAY_UNITS:
            if not self.bot.structures(UnitTypeId.WARPGATE):
                return UnitTypeId.GATEWAY
            return UnitTypeId.WARPGATE
        if unit_type in ROBO_UNITS:
            return UnitTypeId.ROBOTICSFACILITY
        if unit_type in STARGATE_UNITS:
            return UnitTypeId.STARGATE
        return

    async def handle_instructions(self) -> None:
        """ gets build Instruction for self.build_order  """

        async def construct_building(next_step:BuildInstruction):
            """ Handles the construction of structures 

            Args:
                next_step (BuildInstruction): next instruction 
            """
            #TODO: #70 ADD a check if the next instruction is equal to the
            # current one so that building gets not delayed
            pending_check:bool = False
            following_instruction: UnitTypeId = None

            if self.build_order.step + 1 < len(self.build_order.instruction_list):
                following_instruction: BuildInstruction = \
                    self.build_order.instruction_list[self.build_order.step +1]

            if following_instruction == next_step.type_id:
                pending_check = False

            # Needs to be handled separably because it the special placement requirements
            if next_step.type_id == UnitTypeId.ASSIMILATOR:
                if Utils.can_build_structure(self.bot, next_step.type_id):
                    if not pending_check:
                        await self.build_gas(next_step.position)
                    else:
                        if not self.bot.already_pending(next_step.type_id):
                            await self.build_gas(next_step.position)

            # Needs to be handled here because, bot.get_next_expansion() is a coroutine
            if next_step.type_id == UnitTypeId.NEXUS:
                if Utils.can_build_structure(self.bot, next_step.type_id)and\
                    not self.bot.already_pending(next_step.type_id):
                    await self.expand()

            if Utils.can_build_structure(self.bot, next_step.type_id):
                if not pending_check:
                    await self.bot.build(next_step.type_id,near=next_step.position,\
                    max_distance=next_step.accuracy,build_worker=self.get_build_worker())
                else:
                    if not self.bot.already_pending(next_step.type_id):
                        await self.bot.build(next_step.type_id,near=next_step.position,\
                        max_distance=next_step.accuracy,build_worker=self.get_build_worker())

        # TODO: This should be reworked
        async def train_unit(next_step:BuildInstruction):
            """ handles the construction of Units

            Args:
                next_step (BuildInstruction): next instruction
            """

            async def warp_in_unit(bot: BotAI,unit:UnitTypeId,\
                warp_in_position:Union[Point2,Point3,Unit]) -> bool:
                pos:Point2= warp_in_position.position.to2.random_on_distance(4)
                placement = await bot.find_placement(AbilityId.WARPGATETRAIN_STALKER, \
                    pos, placement_step=1)

                for gate in bot.structures(UnitTypeId.WARPGATE).idle:
                    if Utils.can_build_unit(bot, unit):
                        gate.warp_in(unit, placement)

            async def build_gateway_units(bot:BotAI,unit_type:UnitTypeId):
                gate_aliases:list = [UnitTypeId.GATEWAY, UnitTypeId.WARPGATE]
                if Utils.can_build_unit(bot, unit_type):
                    for gate in bot.structures\
                        .filter(lambda struct: struct.type_id in gate_aliases):
                        if gate.is_idle and UpgradeId.WARPGATERESEARCH not in bot.researched:
                            gate.train(unit_type)
                            self.build_order.increment_step()
                        else:
                            warp_in_pos = Utils.get_warp_in_pos(bot)
                            await warp_in_unit(bot, unit_type, warp_in_pos)
                            self.build_order.increment_step()

            #TODO: ADD WARPPRISM LOGIC, SO REINFORCEMENTS CAN BE WARPED IN CLOSE TO FIGHT
            unit_type: UnitTypeId = next_step.type_id
            production_structure_type = self.get_production_structure(unit_type)
            production_structures: Units = self.bot.structures(production_structure_type)
            if Utils.can_build_unit(self.bot, next_step.type_id) and production_structures:
                if not production_structure_type in [UnitTypeId.WARPGATE, UnitTypeId.GATEWAY]:
                    for struct in production_structures:
                        if struct.is_idle and not self.bot.already_pending(unit_type):
                            production_structures[0].train(unit_type)
                            self.build_order.increment_step()
                            return
                await build_gateway_units(self.bot,unit_type)

        next_step: BuildInstruction = self.build_order.next_instruction()
        if not next_step and self.build_order.buffer:
            next_step = self.build_order.get_instruction_from_buffer()
        if not next_step and not self.build_order.buffer:
            return

        if not next_step.type_id == UnitTypeId.ASSIMILATOR \
            and self.build_order.is_performing_initial_build:
            structure_cost:Cost = self.bot.calculate_cost(next_step.type_id)
            if self.bot.minerals > (structure_cost.minerals*0.65):
                if not Utils.unittype_in_proximity_to_point(self.bot,\
                    UnitTypeId.PROBE, next_step.position):
                    worker: Unit = self.get_build_worker()
                    worker.move(next_step.position)

        match next_step.instruction_type:
            case InstructionType.BUILD_STRUCTURE:
                await construct_building(next_step)
            case InstructionType.UNIT_PRODUCTION:
                await train_unit(next_step)

    def get_upgrades(self) -> None:
        """ handles the research of upgrades """

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

        # THIS IS A INNER FUNCTION DON'T CHANGE THE INDENTATION \
            # AGAIN BECAUSE YOU GOT THE MEMORY OF A GOLDFISH
        def upgrade(bot:BotAI, upgrade_structure:UnitTypeId, upgrade_id:UpgradeId) -> None:
            if bot.structures(upgrade_structure).idle \
                and Utils.can_research_upgrade(bot,upgrade_id):
                bot.research(upgrade_id)

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

    async def handle_alerts(self, alert:Alert) -> None:
        """ Handles reaction to alerts

        Args:
            alert (Alert): Alert triggered on the current tick
        """
        #Possible Alerts:
        #    AlertError
        #    AddOnComplete
        #    BuildingComplete
        #    BuildingUnderAttack
        #    LarvaHatched
        #    MergeComplete
        #    MineralsExhausted
        #    MorphComplete
        #    MothershipComplete
        #    MULEExpired
        #    NuclearLaunchDetected
        #    NukeComplete
        #    NydusWormDetected
        #    ResearchComplete
        #    TrainError
        #    TrainUnitComplete
        #    TrainWorkerComplete
        #    TransformationComplete
        #    UnitUnderAttack
        #    UpgradeComplete
        #    VespeneExhausted
        #    WarpInComplete

        match alert:
            case Alert.VespeneExhausted:
                self.build_order.buffer.append(UnitTypeId.ASSIMILATOR)
            case Alert.NuclearLaunchDetected:
                await self.bot.chat_send("Nukes ?!? -> RUDE !!!")
            case Alert.NydusWormDetected:
                await self.bot.chat_send("You went into that thing ? DISGUSTING !!!")

    async def build_supply(self) -> None:
        """Builds supply structures """
        if not self.bot.can_afford(UnitTypeId.PYLON) or self.bot.supply_cap == 200:
            return
        if Utils.can_build_structure(self.bot,UnitTypeId.PYLON) and not \
            self.bot.already_pending(UnitTypeId.PYLON) and self.bot.supply_left < 8 \
                and len(self.bot.structures(UnitTypeId.NEXUS))>= 2 \
                    and self.bot.structures(UnitTypeId.CYBERNETICSCORE):
            worker:Unit = self.bot.workers.prefer_idle.closest_to(self.build_order.get_build_pos())
            await self.bot.build(UnitTypeId.PYLON, build_worker=worker, \
                                 near=self.build_order.get_build_pos())

    async def build_gas(self,position:Union[Point2,Point3,Unit]) -> None:
        """Handles the Building of Gas Structures """
        bot:BotAI = self.bot
        vespene: Units = bot.vespene_geyser.closest_to(position)
        if await bot.can_place_single(UnitTypeId.ASSIMILATOR, vespene.position):
            workers: Units = bot.workers.gathering
            if workers:
                worker: Unit = workers.closest_to(vespene)
                worker.build_gas(vespene)

    def check_mined_out(self) -> None:
        """ Check if Base is mined out -> needs to be reworked"""
        for townhall in self.bot.townhalls:
            minerals = self.bot.expansion_locations_dict[townhall.position].mineral_field

            if not minerals:
                if not townhall in self.bot.mined_out_bases:
                    self.bot.mined_out_bases.append(townhall)

            if not len(self.bot.mined_out_bases) == len(self.bot.temp):
                #self.base_count += 1
                self.temp = self.mined_out_bases

    def build_probes(self) -> None:
        """ Builds workers """
        probe_count:int = len(self.bot.structures(UnitTypeId.NEXUS))*16 \
            + len(self.bot.structures(UnitTypeId.ASSIMILATOR))*3
        if self.bot.structures(UnitTypeId.PYLON):
            for townhall in self.bot.townhalls.idle:
                if Utils.can_build_unit(self.bot, UnitTypeId.PROBE) \
                    and len(self.bot.workers) < probe_count:
                    townhall.train(UnitTypeId.PROBE)

    async def chronoboost(self) -> None:
        """ handles chronoboosting """
        prios:list = [
            [
                UnitTypeId.ROBOTICSBAY,
                UnitTypeId.FLEETBEACON,
                UnitTypeId.TWILIGHTCOUNCIL,
                UnitTypeId.FORGE,
                # WARPGATE SHOULD NOT BE CHRONOBOOSTED
                #UnitTypeId.CYBERNETICSCORE,
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
            # pylint: disable=W0640
            structures = self.bot.structures.filter(lambda struct: not struct.is_idle and \
                not struct.has_buff(BuffId.CHRONOBOOSTENERGYCOST) and struct.type_id in prio)\
                    .sorted(lambda struct: struct.orders[0].progress, reverse=True)

            for struct in structures:
                chrono_nexus = self.bot.structures(UnitTypeId.NEXUS)\
                    .filter(lambda nexus: nexus.energy > 50)
                if chrono_nexus:
                    chrono_nexus[0](AbilityId.EFFECT_CHRONOBOOSTENERGYCOST, struct)

    async def expand(self) -> None:
        """ Handles the building of new townhalls """
        location:Union[Point2,Point3] = await self.bot.get_next_expansion()
        if location:
            if not self.bot.enemy_units.filter(lambda unit: unit.distance_to(location) < 2.75):
                # Misplacing townhalls causes the Bot to crash, therefore it must be checked if the
                # Area is free to build
                # 2.75 is the radius of a nexus -
                # if a unit is closer than this a nexus would be build away from the location
                await self.bot.build(UnitTypeId.NEXUS, near=location, max_distance=0)
