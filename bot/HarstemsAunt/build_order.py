from typing import Union, List, Enum

from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.position import Point2, Point3
from sc2.ids.unit_typeid import UnitTypeId

from .common import ALL_STRUCTURES, logger

class InstructionType(Enum):
    UNIT_PRODUCTION = 1
    BUILD_STRUCTURE = 2

class BuildInstruction:
    """ Instruction for the Bot to build a structure, not sure yet how to add upgrades, and multiple instructions at once
    and how to take unit production into account, i already got a set of all Structures in .common maybe i just add every instruction
    including upgrades and unit production. 
    """

    def __init__(self, type_id:UnitTypeId, position:Union[Point2,Point3,Unit], accuracy:float) -> None:
        self.type_id = type_id
        self.position = position
        self.accuracy = accuracy

    @property
    def instruction_type(self) -> InstructionType:
        if self.type_id in ALL_STRUCTURES:
            return InstructionType.BUILD_STRUCTURE
        return InstructionType.UNIT_PRODUCTION

    def __repr__(self):
        if self.instruction_type == InstructionType.BUILD_STRUCTURE:
            return f"build {self.type_id} at {self.position}"
        if self.instruction_type == InstructionType.UNIT_PRODUCTION:
            return f"train {self.type_id}"

class BuildOrder:

    def __init__(self, bot:BotAI):
        self.bot = bot

    @property
    def step(self) -> int:
        return 0

    @property
    def constructed_structures(self) -> List[UnitTypeId]:
        return []

    @property
    def opponent_builds_air(self) -> bool:
        return False

    @opponent_builds_air.setter
    def opponent_builds_air(self, status:bool) -> None:
        self.opponent_builds_air = status

    @property
    def opponent_uses_cloak(self) -> bool:
        return False

    @opponent_uses_cloak.setter
    def opponent_uses_cloak(self, status:bool) -> None:
        self.opponent_uses_cloak = status

    def increment_step(self) -> None:
        self.step += 1

    def add_constructed_structure(self, structure:UnitTypeId) -> None:
        self.constructed_structures.append(structure)

    def get_build_pos(self) -> Union[Point2, Point3, Unit]:
        # First Pylon Position
        if not self.bot.structures(UnitTypeId.PYLON):
            return self.bot.main_base_ramp.protoss_wall_pylon
        if self.bot.structures(UnitTypeId.PYLON):
            minerals:Units = self.bot.expansion_locations_dict[self.bot.start_location].mineral_field
            return self.bot.start_location.towards(self.bot.start_location.furthest(minerals).position, 10)
        return self.bot.start_location.towards(self.bot.game_info.map_center,2)

    async def update(self):
        # Does only be set once
        if not self.opponent_builds_air:
            if self.bot.enemy_units.filter(lambda unit: unit.is_flying \
                and not unit.can_attack):
                self.opponent_builds_air = True
                await self.bot.chat_send("I see you got an AirForce, i can do that too")

        # Does only be set once
        if not self.opponent_uses_cloak:
            if self.bot.enemy_units\
                .filter(lambda unit: unit.is_cloaked and unit.can_attack \
                    or unit.is_burrowed and unit.can_attack):
                self.opponent_uses_cloak = True
                await self.bot.chat_send("Stop hiding and fight like a honorable ... ähm... Robot?\ndo computers have honor ?")

        self.debug_build_pos(self.get_build_pos())

    def debug_build_pos(self, pos:Union[Point2, Point3]):
        z = self.bot.get_terrain_z_height(pos)+1
        x,y = pos.x, pos.y
        pos_3d = Point3((x,y,z))
        self.bot.client.debug_sphere_out(pos_3d ,2, (255,255,0))

    def next_instruction(self) -> BuildInstruction:
        return BuildInstruction(UnitTypeId.PYLON, self.get_build_pos())