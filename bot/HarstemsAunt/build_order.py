from enum import Enum
from typing import Union, List
from functools import cached_property

from .common import ALL_STRUCTURES, INITIAL_TECH, logger

from sc2.unit import Unit
from sc2.data import Race
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.position import Point2, Point3
from sc2.ids.unit_typeid import UnitTypeId


class InstructionType(Enum):
    UNIT_PRODUCTION = 1
    BUILD_STRUCTURE = 2

class BuildInstruction:
    """ Instruction for the Bot to build a structure, not sure yet how to add upgrades, and multiple instructions at once
    and how to take unit production into account, i already got a set of all Structures in .common maybe i just add every instruction
    including upgrades and unit production. """

    def __init__(self, type_id:UnitTypeId, position:Union[Point2,Point3,Unit], accuracy:float=0) -> None:
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
        self.step = 0
        self.buffer = []

    @cached_property
    def enemy_race(self) -> Race:
        return self.bot.enemy_race

    @property
    def instruction_list(self) -> List[BuildInstruction]:

        tech:List[UnitTypeId] = INITIAL_TECH.get(self.enemy_race)

        start_pos: Point2 = self.bot.start_location
        minerals:Units = self.bot.expansion_locations_dict[self.bot.start_location].mineral_field
        wall_buildings:list = list(self.bot.main_base_ramp.protoss_wall_buildings)
        wall_pylon_pos:Point2 = self.bot.main_base_ramp.protoss_wall_pylon
        tech_pylon_pos:Point2 = self.bot.start_location.towards(self.bot.start_location.furthest(minerals).position, 10)
        angle_pylon_pos:Point2 = self.bot.start_location.towards(self.bot.game_info.map_center,10)

        instructions = [
            BuildInstruction(UnitTypeId.PYLON,wall_pylon_pos),
            BuildInstruction(UnitTypeId.GATEWAY,wall_buildings[0]),
            BuildInstruction(UnitTypeId.CYBERNETICSCORE,wall_buildings[1]),
            BuildInstruction(UnitTypeId.PYLON,tech_pylon_pos),
            BuildInstruction(tech[0],tech_pylon_pos,5),
            BuildInstruction(UnitTypeId.PYLON, angle_pylon_pos, 1),
            BuildInstruction(UnitTypeId.GATEWAY, angle_pylon_pos,5),
            BuildInstruction(UnitTypeId.GATEWAY, angle_pylon_pos,5),
            BuildInstruction(tech[1],wall_pylon_pos.towards(self.bot.game_info.map_center),5),
            BuildInstruction(UnitTypeId.GATEWAY, angle_pylon_pos,5),
            BuildInstruction(UnitTypeId.PYLON, angle_pylon_pos.towards(wall_pylon_pos,-6),5)
        ]
        return instructions

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

    @property
    def opponent_has_detection(self) -> bool:
        return False

    @opponent_has_detection.setter
    def opponent_has_detection(self, status:bool) -> None:
        self.opponent_has_detection = status 

    def increment_step(self) -> None:
        self.step = self.step + 1

    def add_constructed_structure(self, structure:UnitTypeId) -> None:
        self.constructed_structures.append(structure)

    def get_build_pos(self) -> Union[Point2, Point3, Unit]:
        if len(self.instruction_list) > self.step:
            return self.instruction_list[self.step].position
        return self.bot.start_location.towards(self.bot.game_info.map_center, 4)

    async def update(self):

        if self.opponent_builds_air and not self.bot.structures(UnitTypeId.STARGATE):
            self.instruction_list.append(BuildInstruction(UnitTypeId.STARGATE,self.get_build_pos()))

        if self.bot.time > 35:
            if not self.opponent_has_detection and not self.bot.structures(UnitTypeId.DARKSHRINE)\
                and UnitTypeId.DARKSHRINE not in self.buffer:
                self.buffer.append(UnitTypeId.DARKSHRINE)

        self.debug_build_pos(self.get_build_pos())
        self.bot.client.debug_text_screen(f"{self.next_instruction()} instruction {self.step}", \
            (0.01, 0.15), color=(255,255,255), size=15)
        self.bot.client.debug_text_screen(f"next struct in Buffer: {self.get_next_in_buffer()}", \
            (0.01, 0.20), color=(255,255,255), size=15)

    def debug_build_pos(self, pos:Union[Point2, Point3]):
        z = self.bot.get_terrain_z_height(pos)+1
        x,y = pos.x, pos.y
        pos_3d = Point3((x,y,z))
        self.bot.client.debug_sphere_out(pos_3d ,1, (255,255,0))

    def get_next_in_buffer(self) -> UnitTypeId:
        if self.buffer:
            return self.buffer[0]

    def create_instruction_from_buffer(self) -> BuildInstruction:
        structure_type:UnitTypeId = self.buffer.pop(0)
        build_pos:Point2 = self.get_build_pos()
        accuracy:float = 10.0
        instruction:BuildInstruction = BuildInstruction(structure_type,build_pos,accuracy)
        return instruction

    def next_instruction(self) -> BuildInstruction:
        if len(self.instruction_list) > self.step:
            return self.instruction_list[self.step]
        if self.buffer:
            instruction:BuildInstruction = self.create_instruction_from_buffer()
            logger.info(instruction)
            return instruction