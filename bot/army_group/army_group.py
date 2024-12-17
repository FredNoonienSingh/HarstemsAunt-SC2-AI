from __future__ import annotations
from typing import Union

from sc2.unit import Unit
from sc2.units import Units
from sc2.ids.unit_typeid import UnitTypeId
from sc2.bot_ai import BotAI
from sc2.position import Point2, Point3

class ArmyGroup:
    def __init__(self, bot:BotAI, unit_list:list):
        self.bot:BotAI = bot
        self.unit_list:list=unit_list

    @property
    def units(self) -> Units:
        return self.bot.units.filter(lambda unit: unit.tag in self.unit_list)

    @property
    def position(self) -> Point2:
        return self.units.center

    @property
    def ground_dps(self) -> float:
        return sum([unit.ground_dps for unit in self.units])

    @property
    def air_dps(self) -> float:
        return sum([unit.air_dps for unit in self.units])

    @property
    def average_health_percentage(self) -> float:
        return 1/len(self.units)*sum([unit.health_percentage for unit in self.units])

    @property
    def average_shield_precentage(self) -> float:
        return 1/len(self.units)*sum([unit.shield_percentage for unit in self.units])

    @property
    def has_detection(self) -> float:
        if self.units.filter(lambda unit: unit.is_detector):
            return True
        return False

    @property
    def attack_pos(self) -> Union[Point2,Point3,Unit]:
        return self.bot.enemy_start_locations[0]

    @attack_pos.setter
    def attack_pos(self, new_attack_pos:Union[Point2,Point3,Unit]):
        self.attack_pos = new_attack_pos

    @property
    def retreat_pos(self) -> Union[Point2,Point3,Unit]:
        return self.bot.game_info.map_center

    @retreat_pos.setter
    def retreat_pos(self, new_retreat_pos:Union[Point2,Point3,Unit]):
        self.retreat_pos = new_retreat_pos

    def request_unit(self) -> UnitTypeId:
        # Gets called when Production is Idle
        pass

    def remove_unit(self, unit_tag:str) -> bool:
        if unit_tag in self.unit_list:
            self.unit_list.remove(unit_tag)
            return True
        return False

    def merge_groups(self, army_group:ArmyGroup) -> bool:
        # Returns true if ArmyGroups were merged
        if army_group in self.bot.army_groups:
            self.unit_list.extend(army_group.unit_list)
            self.bot.army_groups.remove(army_group)
            return True
        return False

    def attack(self) -> None:
        pass

    def move(self) -> None:
        pass

    def retreat(self) -> None:
        pass

    def regroup(self) -> None:
        pass

    def defend(self, position:Union[Point2,Point3,Unit]) -> None:
        pass