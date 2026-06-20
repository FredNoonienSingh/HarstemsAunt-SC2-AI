"""DocString"""
#pylint: disable=W0611
#pylint: disable=C0411
#pylint: disable=W0212
#pylint: disable=C0116
from typing import List, Union

from sc2.unit import Unit
from sc2.units import Units
from sc2.position import Point2
from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId

from s2clientprotocol import ui_pb2 as ui_pb
from s2clientprotocol import raw_pb2 as raw_pb
from s2clientprotocol import sc2api_pb2 as sc_pb

# pylint: disable=E0402
from bot.HarstemsAunt.utils import Utils
from bot.HarstemsAunt.common import logger
from bot.HarstemsAunt.Army.Units.combat_unit import FightStatus
from bot.HarstemsAunt.Army.Units.combat_flyer import CombatFlyer



PRIORY_TARGETS: List[UnitTypeId] = [
    UnitTypeId.IMMORTAL,
    UnitTypeId.COLOSSUS,
    UnitTypeId.DISRUPTOR,
    UnitTypeId.HIGHTEMPLAR
]

class Warpprism(CombatFlyer):
    """Child class of combat unit"""

    @property
    def has_passengers(self) -> bool:
        """returns True if the holds any cargo """
        if self.unit:
            return bool(self.unit.passengers)

    @property
    def cargo_left(self) -> int:
        """remaining cargo space """
        if self.unit:
            return self.unit.cargo_left

    @property
    def closest_friendly(self) -> Unit:
        """returns the closest enemy unit"""
        if self.unit:
            return self.bot.units.filter(lambda unit: unit.tag not in \
                self.unit.passengers_tags and not unit.tag == self.tag)\
                .closest_to(self.unit)
            #return self.friendlies_in_proximity.closest_to(self.unit)

    @property
    def pickup_target(self) -> Unit:
        """returns the next_pickup target"""
        if self.unit:
            units:Units = self.bot.units.filter(lambda unit: unit.tag not in \
                self.unit.passengers_tags and not unit.tag == self.tag)\
                    .filter(lambda unit: unit.weapon_cooldown > 5)
            if units:
                if self.enemies_in_proximity:
                    return units.closest_to(self.enemies_in_proximity.center)
                else:
                    return None

    def pick_up(self, target:Unit) -> None:
        if self.can_cast(AbilityId.LOAD_WARPPRISM, self.pickup_target):
            self.unit(ability=AbilityId.LOAD_WARPPRISM, target=target)

    def drop_unit_at(self, target_position:Point2) -> None:
        if Utils.in_proximity_to_point(self.unit, target_position, 5):
            self.unit(AbilityId.UNLOADALLAT_WARPPRISM, target_position)
        else:
            self.unit.move(self.get_retreat_pos())

    async def unload_unit(self, transporter_unit: Unit, unload_unit: Union[int, Unit]):
        assert isinstance(unload_unit, (int, Unit))
        assert hasattr(self.bot, "raw_affects_selection") and self.bot.raw_affects_selection is True
        assert hasattr(self.bot, "enable_feature_layer") and self.bot.enable_feature_layer is True
        if isinstance(unload_unit, Unit):
            unload_unit_tag = unload_unit.tag
        else:
            unload_unit_tag = unload_unit

        unload_unit_index = next(
            (index for index, unit in enumerate(list(self.unit.passengers)) \
                if unit.tag == unload_unit_tag),
            None
        )

        if unload_unit_index is None:
            logger.info(f"Unable to find unit {unload_unit} in transporter {transporter_unit}")
            return

        logger.info(f"Unloading unit at index: {unload_unit_index}")
        await self.bot.client._execute(
            action=sc_pb.RequestAction(
                actions=[
                    sc_pb.Action(
                        action_raw=raw_pb.ActionRaw(
                            unit_command=raw_pb.ActionRawUnitCommand\
                                (ability_id=0, unit_tags=[transporter_unit.tag])
                        )
                    ),
                    sc_pb.Action(
                        action_ui=ui_pb.ActionUI(
                            cargo_panel=ui_pb.ActionCargoPanelUnload(unit_index=unload_unit_index)
                        )
                    ),
                ]
            )
        )

    async def unload_specific_unit(self, transporter: Unit, unload_target: Union[Unit, int]):
        assert isinstance(transporter, Unit)
        assert isinstance(unload_target, (Unit, int))

        unload_tag = unload_target.tag if isinstance(unload_target, Unit) else unload_target

        unload_index = next(
            (i for i, passenger in enumerate(transporter._proto.passengers) \
                if passenger.tag == unload_tag),
            None,
        )
        if unload_index is None:
            self.bot._client.debug_text_screen\
                (f"Unit {unload_tag} not found in {transporter.tag}", pos=(0.1, 0.1), size=16)
            return False

        return await self.bot._client._execute(
            action=sc_pb.RequestAction(
                actions=[
                    sc_pb.Action(
                        action_raw=raw_pb.ActionRaw(
                            unit_command=raw_pb.ActionRawUnitCommand(
                                ability_id=912,
                                unit_tags=[transporter.tag],
                            )
                        )
                 ),
                    sc_pb.Action(
                        action_ui=ui_pb.ActionUI(
                            cargo_panel=ui_pb.ActionCargoPanelUnload(unit_index=unload_index)
                        )
                    ),
                ]
            )
        )

    def morph(self) -> None:
        """Changes the Mode of the Unit """
        if self.unit.type_id == UnitTypeId.WARPPRISM:
            self.unit(AbilityId.MORPH_WARPPRISMPHASINGMODE)
            return
        if self.unit.type_id == UnitTypeId.WARPPRISMPHASING:
            self.unit(AbilityId.MORPH_WARPPRISMTRANSPORTMODE)
            return

    async def engage(self, attack_target:Union[Point2, Unit]) -> None:
        """Engagement Method """
        if self.unit:

            if not self.has_passengers:
                self.pick_up(self.pickup_target)

            if self.closest_friend:
                if self.closest_enemy:
                    target_pos = self.safe_spot
                else:
                    target_pos = self.closest_friendly.position
            elif self.enemies_in_proximity:
                target_pos = self.bot.pathing.find_closest_safe_spot(self.unit.position,
                                                                     self.pathing_grid)
            else:
                target_pos = attack_target

            if self.has_passengers:
                if self.bot.pathing.is_position_safe(self.pathing_grid,self.unit.position):
                    self.drop_unit_at(self.unit.position)

                else:
                    self.unit.move(self.bot.pathing.find_closest_safe_spot(
                            self.unit.position,
                            self.pathing_grid
                        ))
            else:
                self.move(target_pos)

            if self.bot.debug:
                self.bot.debug_tools.draw_line_from_to(self.unit, target_pos)
                self.bot.client.debug_text_world(f"is safe: {self.is_safe}",
                                                self.unit, color=(0,255,0), size=20)
