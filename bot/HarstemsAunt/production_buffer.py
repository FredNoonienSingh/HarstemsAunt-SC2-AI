"""DOCSTRING to shut up the Linter """
from __future__ import annotations

from typing import List

from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId


class ProductionRequest:
    """ Class Representing the a Production Request """

    def __new__(cls, requested_unit:UnitTypeId,army_group_id:int,build_structure_tag:int) -> ProductionRequest:
        """ Creates new instance of Production Request

        Args:
            requested_unit (UnitTypeId): type of requested Unit
            army_group_tag (int): identifier of the ArmyGroup requesting the Unit

        Returns:
            ProductionRequest: Request for a Unit (gets called in ArmyGroup)
        """
        instance = super().__new__(cls)
        instance.requested_unit = requested_unit
        instance.army_group = army_group_id
        instance.build_structure_tag = build_structure_tag

        return instance

    def __init__(self, requested_unit:UnitTypeId,army_group_id:int,build_structure_tag:int) -> None:
        self.requested_unit:UnitTypeId = requested_unit
        self.army_group_tag:int = army_group_id
        self.build_structure_tag = build_structure_tag

    def __repr__(self) -> str:
        return f"Unit: {self.requested_unit} requested by {self.army_group_tag}"

    @property
    def handled(self) -> bool:
        return False

    @handled.setter
    def handled(self, new_status) -> None:
        self.handled = new_status


class ProductionBuffer:
    """ Buffer for Production Requests before they are full filled"""

    def __init__(self,bot:BotAI) -> None:
        self.bot:BotAI = bot
        self.requests:List[ProductionRequest] = []

    @property
    def gateways(self) -> Units:
       return self.bot.units.filter(lambda struct: struct.type_id \
           in [UnitTypeId.WARPGATE, UnitTypeId.GATEWAY] and struct.is_idle)

    @property
    def stargates(self) -> Units:
        return self.bot.units(UnitTypeId.STARGATE).idle

    @property
    def robofacilities(self) -> Units:
        return self.bot.units(UnitTypeId.ROBOTICSFACILITY).idle

    def add_request(self, request:ProductionRequest) -> None:
        self.requests.append(request)

    def remove_request(self, request:ProductionRequest):
        self.requests.remove(request)

    def update(self) -> None:
        for request in self.requests:
            if request.handled:
                self.remove_request(request)
