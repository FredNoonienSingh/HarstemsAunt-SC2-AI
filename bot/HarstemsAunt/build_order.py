"""DOCSTRING to shut up the Linter """
from __future__ import annotations

from enum import Enum
from typing import Union, List
from functools import cached_property

from sc2.unit import Unit
from sc2.data import Race
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.position import Point2, Point3
from sc2.unit_command import UnitCommand
from sc2.ids.unit_typeid import UnitTypeId

# pylint: disable=E0402
from .army_group import ArmyGroup
from .common import ALL_STRUCTURES,INITIAL_TECH,DT_TIMING

class InstructionType(Enum):
    """Enumeration containing InstructionTypes """
    UNIT_PRODUCTION = 1
    BUILD_STRUCTURE = 2

class Build(Enum):
    """Enumeration containing BuildOrders """
    CANNON_RUSH = 1
    FOUR_GATE = 2

#TODO: #74 Add worker instruction to BuildInstruction
class BuildInstruction:
    """ class representing a Build Instruction """

    def __new__(cls,type_id:UnitTypeId,position:Union[Point2,Point3,Unit]=None,\
        accuracy:int=0, worker_command:UnitCommand=None) -> BuildInstruction:
        """ Creates new instance of BuildInstruction

        Args:
            type_id (UnitTypeId): type of structure or unit that needs to be build
            position (Union[Point2,Point3,Unit], optional): position on which the structure will be build. Defaults to None.
            worker_command (UnitCommand, optional): Worker Command after finishing the structure. Defaults to None.

        Returns:
            _type_: BuildInstruction
        """
        instance = super().__new__(cls)
        instance.type_id = type_id
        instance.position = position
        instance.accuracy = accuracy
        instance.worker_command = worker_command
        return instance

    def __init__(self,type_id:UnitTypeId, position:Union[Point2,Point3,Unit],\
        accuracy:int=0,worker_command:UnitCommand=None) -> None:
        """ instantiate a instance of the class

        Args:
            type_id (UnitTypeId): type of unit or structure
            position (Union[Point2,Point3,Unit]): position on which the structure will be build
            worker_command (UnitCommand, optional): Worker Command after finishing the structure. Defaults to None.
        """
        self.type_id = type_id
        self.position = position
        self.accuracy = accuracy
        self.worker_command = worker_command

    @property
    def instruction_type(self) -> InstructionType:
        """ types of the instruction either, BUILD_STRUCTURE or UNIT_PRODUCTION 

        Returns:
            InstructionType: type of the instruction
        """
        if self.type_id in ALL_STRUCTURES:
            return InstructionType.BUILD_STRUCTURE
        return InstructionType.UNIT_PRODUCTION

    def __repr__(self) -> str:
        """returns a string representation of the class

        Returns:
            _type_: string representation of class
        """
        if self.instruction_type == InstructionType.BUILD_STRUCTURE:
            return f"build {self.type_id} at {self.position}"
        if self.instruction_type == InstructionType.UNIT_PRODUCTION:
            return f"train {self.type_id}"

class BuildOrder:
    """ Class containing the build order and methods connected with it
    """
    
    def __init__(self, bot:BotAI, build:Build=Build.FOUR_GATE):
        self.bot = bot
        self.build = build
        self.step = 0
        self.buffer = []
        self.army_groups:List[ArmyGroup] = bot.army_groups

    @cached_property
    def enemy_race(self) -> Race:
        """ Race of the enemy"""
        return self.bot.enemy_race

    @cached_property
    def instruction_list(self) -> List[BuildInstruction]:
        """ list of initial Build Instructions """

        tech:List[UnitTypeId] = INITIAL_TECH.get(self.enemy_race)

        start_pos: Point2 = self.bot.start_location
        minerals:Units = self.bot.expansion_locations_dict[self.bot.start_location].mineral_field
        wall_buildings:list = list(self.bot.main_base_ramp.protoss_wall_buildings)
        wall_pylon_pos:Point2 = self.bot.main_base_ramp.protoss_wall_pylon
        tech_pylon_pos:Point2 = self.bot.start_location.towards(self.bot.start_location.furthest(minerals).position, 10)
        angle_pylon_pos:Point2 = self.bot.start_location.towards(self.bot.game_info.map_center,10)
        vespene_position_0:Point2 = self.bot.vespene_geyser.closer_than(12, start_pos)[0]
        vespene_position_1:Point2 = self.bot.vespene_geyser.closer_than(12, start_pos)[1]

        cannon_pylon_0: Point2 = self.bot.enemy_start_locations[0].towards(self.bot.game_info.map_center, 5)

        FOUR_GATE = [
            BuildInstruction(UnitTypeId.PYLON,wall_pylon_pos),
            BuildInstruction(UnitTypeId.GATEWAY,wall_buildings[0]),
            BuildInstruction(UnitTypeId.ASSIMILATOR,vespene_position_0),
            BuildInstruction(UnitTypeId.PYLON,tech_pylon_pos),
            BuildInstruction(UnitTypeId.ASSIMILATOR,vespene_position_1),
            BuildInstruction(UnitTypeId.CYBERNETICSCORE,wall_buildings[1]),
            BuildInstruction(UnitTypeId.NEXUS, start_pos),
            BuildInstruction(UnitTypeId.GATEWAY, wall_pylon_pos,5),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.PYLON, angle_pylon_pos, 1),
            BuildInstruction(tech[0],tech_pylon_pos,5),
            BuildInstruction(UnitTypeId.GATEWAY, angle_pylon_pos,5),
            BuildInstruction(tech[1],wall_pylon_pos.towards(self.bot.game_info.map_center),5),
            BuildInstruction(UnitTypeId.GATEWAY, angle_pylon_pos,5),
            BuildInstruction(UnitTypeId.PYLON, angle_pylon_pos.towards(wall_pylon_pos,-6),5),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
            BuildInstruction(UnitTypeId.STALKER, start_pos),
        ]

        CANNON_RUSH = [
            BuildInstruction(UnitTypeId.PYLON,wall_pylon_pos),
            BuildInstruction(UnitTypeId.FORGE,wall_buildings[0]),
            BuildInstruction(UnitTypeId.PYLON, cannon_pylon_0, 5),
            BuildInstruction(UnitTypeId.PHOTONCANNON, cannon_pylon_0, 5),
            BuildInstruction(UnitTypeId.PHOTONCANNON, cannon_pylon_0, 5),
            BuildInstruction(UnitTypeId.PYLON, cannon_pylon_0, 5),
            BuildInstruction(UnitTypeId.PYLON, cannon_pylon_0, 5),
            BuildInstruction(UnitTypeId.PHOTONCANNON, cannon_pylon_0, 5),
            BuildInstruction(UnitTypeId.PHOTONCANNON, cannon_pylon_0, 5),
            BuildInstruction(UnitTypeId.PYLON, cannon_pylon_0, 5),
        ]

        match self.build:
            case Build.CANNON_RUSH:
                return CANNON_RUSH
            case Build.FOUR_GATE:
                return FOUR_GATE

    @property
    def constructed_structures(self) -> List[UnitTypeId]:
        """ List of Structures that have been constructed  """
        return []

    @property
    def opponent_builds_air(self) -> bool:
        """ Returns True if the opponent is building an Airforce """
        return False

    @opponent_builds_air.setter
    def opponent_builds_air(self, status:bool) -> None:
        """sets the Value of opponent_builds_air """
        self.opponent_builds_air = status

    @property
    def opponent_uses_cloak(self) -> bool:
        """ Returns true if the opponent has cloak """
        return False

    @opponent_uses_cloak.setter
    def opponent_uses_cloak(self, status:bool) -> None:
        """ setter for opponent uses cloak """
        self.opponent_uses_cloak = status

    @property
    def opponent_has_detection(self) -> bool:
        """ Is set to True once, when the enemy builds a detector """
        return False

    @opponent_has_detection.setter
    def opponent_has_detection(self, status:bool) -> None:
        """ sets opponent_has_detection to the parsed status"""
        # for some reason is this causing max iter-depth issues
        self.opponent_has_detection = status

    @property
    def is_performing_initial_build(self) -> bool:
        """ is True, when the bot is still performing predefined actions  """
        return len(self.instruction_list) > self.step

    def increment_step(self) -> None:
        """ increments the current build step"""
        self.step = self.step + 1

    #TODO: Decide if this can be removed
    def add_constructed_structure(self, structure:UnitTypeId) -> None:
        """ appends structure to constructed structures currently not in use """
        self.constructed_structures.append(structure)

    #TODO: Make this structure dependent -> return the last pylon not in Vision Pylons for any structure and a different pos for pylons
    def get_build_pos(self) -> Union[Point2, Point3, Unit]:
        """ returns build pos

        Returns:
            Union[Point2, Point3, Unit]: position on which the next structure will be build
        """
        if len(self.instruction_list) > self.step:
            return self.instruction_list[self.step].position
        last_pylon:Unit = self.bot.structures(UnitTypeId.PYLON).sorted(lambda struct: struct.age)[0]
        return last_pylon.position.towards_with_random_angle(self.bot.game_info.map_center)

    async def update(self):
        """ Updates the the Instance, bases on game_state -> gets called once per tick in Macro class"""
        # CODE FOR THE CANNON RUSH
        if self.build == Build.CANNON_RUSH:
            if self.bot.structures(UnitTypeId.PYLON)\
                .filter(lambda struct: struct.distance_to(self.bot.enemy_start_locations[0]) < 12):
                self.buffer.append(UnitTypeId.PYLON)
            else:
                self.buffer.append(UnitTypeId.PHOTONCANNON)
            return

        #TODO: ADD Conditions under which more Economy gets added to the Build
        #TODO: #66 ADD Conditions for advanced Tech -> such as fleet beacon ...
        if self.opponent_builds_air and not self.bot.structures(UnitTypeId.STARGATE):
            self.buffer.append(UnitTypeId.STARGATE)

        if self.bot.time > DT_TIMING:
            if not self.opponent_has_detection and not self.bot.structures(UnitTypeId.DARKSHRINE)\
                and UnitTypeId.DARKSHRINE not in self.buffer:
                self.buffer.append(UnitTypeId.DARKSHRINE)

        # THIS RUNS EVERY TICK
        for group in self.army_groups:
            if group.requested_units:
                requested_unit:UnitTypeId = group.requested_units[0]
                if not requested_unit in self.buffer:
                    self.buffer.append(requested_unit)
                    group.requested_units.remove(requested_unit)

        self.bot.client.debug_text_screen(f"{self.next_instruction()} instruction {self.step}", \
            (0.01, 0.15), color=(255,255,255), size=15)
        self.bot.client.debug_text_screen(f"next struct in Buffer: {self.get_next_in_buffer()}", \
            (0.01, 0.20), color=(255,255,255), size=15)

    def debug_build_pos(self, pos:Union[Point2, Point3]):
        """debug methode to show the current build pos """
        z = self.bot.get_terrain_z_height(pos)+1
        x,y = pos.x, pos.y
        pos_3d = Point3((x,y,z))
        self.bot.client.debug_sphere_out(pos_3d ,1, (255,255,0))

    #TODO: rework so into separate unit and structure buffers
    def get_next_in_buffer(self) -> UnitTypeId:
        """returns the next structure or unit in buffer """
        if self.buffer:
            return self.buffer[0]

    def get_instruction_from_buffer(self) -> BuildInstruction:
        """ creates BuildInstruction from Units in Buffer

        Returns:
            BuildInstruction: new BuildInstruction from data in Buffer
        """
        structure_type:UnitTypeId = self.buffer[0]
        build_pos:Point2 = self.get_build_pos()
        accuracy:int = 10
        instruction:BuildInstruction = BuildInstruction(structure_type,build_pos,accuracy)
        return instruction

    def remove_from_buffer(self,structure:UnitTypeId) -> None:
        """ remove structure type from buffer

        Args:
            structure (UnitTypeId): type that is to will be removed from buffer
        """
        self.buffer.remove(structure)

    def next_instruction(self) -> BuildInstruction:
        """ returns next instruction when there a still instructions left

        Returns:
            BuildInstruction: next_step instruction
        """
        if self.is_performing_initial_build:
            return self.instruction_list[self.step]
