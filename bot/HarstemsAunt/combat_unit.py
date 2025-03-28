"""Replacement for UnitClass"""
from enum import Enum
from typing import Union, List

import numpy as np

# pylint: disable=E0402
# from .utils import Utils
from .unitmarker import UnitMarker
from .common import MIN_SHIELD_AMOUNT, RANGE_BUFFER,\
    PROXIMITY,PRIO_ATTACK_TARGET, ALL_STRUCTURES,UNIT_LABEL_FONT_SIZE, logger

# pylint: disable=C0411
from sc2.unit import Unit
from sc2.units import Units
from sc2.bot_ai import BotAI
from sc2.position import Point2,Point3
from sc2.ids.ability_id import AbilityId

# pylint: disable=E0401
from map_analyzer import MapData, Region

class FightStatus(Enum):
    """Could be named better, will be used to report to the 
        Group if the unit is ready to engage
    """
    FIGHTING = 1
    RETREATING = 2
    DESTROYED = 3

class CombatUnit:
    """Base Class for new UnitClass, controls a single unit not all units of a type
        will replace the old UnitClasses

        IMPORTANT CURRENTLY JUST CARES ABOUT GROUND UNITS
    """
    def __init__(self,bot:BotAI ,unit_tag:int,pathing_grid:np.ndarray) -> None:
        # I NEED TO BE REMOVED, WHEN I GET DESTROYED
        self.bot = bot
        self.unit_tag = unit_tag
        self.pathing_grid = pathing_grid

    def __call__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"combat unit {self.unit.type_id} at \
            {self.unit.position} currently {self.fight_status}"

    @property
    def unit(self) -> Unit:
        """The unit property."""
        return self.bot.units.find_by_tag(self.unit_tag)

    @property
    def tag(self) -> int:
        """unique identifier for unit"""
        return self.unit.tag

    @property
    def safe_spot(self) -> Point2:
        """ Returns the closest safe spot to the unit """
        return self.bot.pathing.find_closest_safe_spot(
                self.unit.position, self.pathing_grid)

    @property
    def position3d(self) -> Point3:
        """position of the unit as Point3"""
        return self.unit.position3d

    @property
    def friendlies_in_proximity(self) -> Units:
        """ friendly Units in proyimity to self, 
            PROXIMITY value is specified in HarstemsAunt.common

        Returns:
            Units: Units close to self
        """
        return self.bot.units.closer_than(PROXIMITY,self.unit)

    @property
    def markers_in_proximity(self) -> List[UnitMarker]:
        """The markers_in_proximity property."""
        if self.bot.unitmarkers and self.unit:
            return [marker for marker in self.bot.unitmarkers if\
                    self.unit.position.distance_to(marker.position) >\
                    self.unit.sight_range + 1]
        return

    @property
    def enemies_in_proximity(self) -> Units:
        """The enemies_in_proximity property."""
        if self.bot.enemy_units and self.unit:
            return self.bot.enemy_units.closer_than(25, self.unit)\
                .filter(lambda unit: unit.type_id not in ALL_STRUCTURES)
        return

    @property
    def in_attack_range_of(self) -> Units:
        """returns all enemies that currently can attack the unit
                i just saw, there is a implementation of this 

                I should benchmark both to test if i want to keep this
        """
        if self.enemies_in_proximity:
            if self.unit.is_flying:
                return self.enemies_in_proximity\
                        .filter(lambda enemy: enemy.can_attack_air \
                        and enemy.distance_to(self.unit) + RANGE_BUFFER <= enemy.air_range)
            if self.bot.enemy_units:
                return self.enemies_in_proximity.filter(lambda enemy: enemy.can_attack_ground \
                    and enemy.distance_to(self.unit) + RANGE_BUFFER <= enemy.ground_range)
        return None

    @property
    def potential_damage_taken(self) -> float:
        """returns the amount of damage the unit may take at the current position """
        if self.in_attack_range_of:
            if self.unit.is_flying:
                return sum([unit.air_dps for unit in list(self.in_attack_range_of)])
            if self.in_attack_range_of:
                return sum([unit.ground_dps for unit in list(self.in_attack_range_of)])
        return 0.0

    @property
    def potential_damage_given(self) -> float:
        """The potential_damage_give property."""
        if self.enemies_in_proximity:
            # pylint: disable=W0108
            sorted_enemies = self.enemies_in_proximity\
                    .sort(lambda enemy: self.unit.calculate_dps_vs_target(enemy))
            return self.unit.calculate_dps_vs_target(sorted_enemies[0])
        return 0.0

    @property
    def can_survive_fleeing(self) -> bool:
        """ Returns true, 
            if unit will not be destroyed in current fight and transit to safe spot
        """
        # More readable then just a massive oneliner
        if self.potential_damage_taken:
            movement_speed:float = self.unit.movement_speed
            distance_to_safety:float = self.unit.distance_to(self.safe_spot)
            time_in_danger:float = distance_to_safety/movement_speed
            damage_over_time:float = self.potential_damage_taken*time_in_danger

            #does not account for the fact that the potential damage is /
            # probally spread out over multiple units
            # could be improved by dividing the damage by own units in proximity
            return self.unit.health > damage_over_time\
                /len(self.friendlies_in_proximity)/2
                # assuming that on average half of the units are closer to the enemies
        return True

    @property
    def fight_status(self) -> FightStatus:
        """Returns the current fighting status of the Unit """
        if self.unit:
            if self.unit.shield_percentage >= MIN_SHIELD_AMOUNT:# or not self.can_survive_fleeing:
                return FightStatus.FIGHTING
            return FightStatus.RETREATING
        return FightStatus.DESTROYED

    @property
    def region(self) -> Region:
        """returns the current region"""
        if self.unit:
            try:
                position:Point2 = self.unit.position
                return self.bot.map_data.where_all(position)[0]
            except IndexError as e:
                logger.error(e)
                return None
        return None

    @property
    def retreat_region(self) -> Region:
        """ point that sets the angle for retreating"""
        map_data:MapData = self.bot.map_data
        start_location:Point2 = self.bot.start_location
        start_region:Region = map_data.where_all(start_location)[0]

        connections:List[Region] \
            = map_data.region_connectivity_all_paths(self.region, start_region)

        if connections:
            return connections[0]
        return None

    @property
    def unit_label(self) -> str:
        """creates a string for use as unit_label """
        if self.unit:
            # This line needs to be so fucking long to be rendered correctly
            return f"{self.unit.type_id}\nweapon cooldown: {self.unit.weapon_cooldown}\nfight status: {self.fight_status}\nin region: {self.region}\norders: {self.unit.orders}"
        return None

    # TODO: breaks a bit on Bases !!! -> needs to be fixxed 
    def get_retreat_pos(self) -> Point2:
        """returns the positions to retreat to """
        if not self.retreat_region or self.retreat_region[0] == self.region:
            if self.enemies_in_proximity:
                closest_enemy:Unit = self.enemies_in_proximity.closest_to(self.unit)
                position_away_from_enemy:Point2 = self.unit.position.towards(closest_enemy,-self.unit.distance_to_weapon_ready/2)
                return self.bot.pathing.find_path_next_point(self.unit.position,position_away_from_enemy,self.pathing_grid)
            else:
                return self.bot.start_location

        next_region_center:Point2 = self.retreat_region[0].center
        return self.bot.pathing.find_path_next_point(self.unit.position,next_region_center,self.pathing_grid)

    def cast_influence(self) -> np.ndarray:
        """ returns an np.array to influence the pathing Grid
            -> goal of this function is to get Units to create formations and
                stopping them from blocking each other

            # Maybe a whole map is not necessary ... 

        Returns:
            np.ndarray: influence grid
        """
        pass

    async def can_cast(self, ability:AbilityId, target: Union[Point2, Point3, Unit]) -> bool:
        """Checks if the Unit can use a certain ability"""
        abilities = await self.bot.get_available_abilities(self.unit)
        return await self.bot.can_cast(self.unit, ability,
                    target,
                    cached_abilities_of_unit=abilities)

    async def move(self, target_position:Union[Point2, Point3, Unit]) -> None:
        """ moves the unit to a given point """
        self.unit.move(
                   self.bot.pathing.find_path_next_point(
                       self.unit.position, target_position, self.pathing_grid
                    )
                )

    async def engage(self, attack_target:Union[Unit, Point2]) -> None:
        """replacement for handle_attackers """
        if not self.unit:
            return

        if self.unit and self.bot.debug:
            self.bot.client.debug_text_world(self.unit_label, \
                self.unit, size=UNIT_LABEL_FONT_SIZE)

        try:
            if self.enemies_in_proximity:
                prio_targets:Unit = \
                    self.enemies_in_proximity.filter(lambda unit: unit.type_id in PRIO_ATTACK_TARGET and\
                        unit.distance_to(self.unit) <= self.unit.ground_range+RANGE_BUFFER
                        )
                if prio_targets:
                    target = prio_targets.closest_to(self.unit)
                else:
                    target = self.enemies_in_proximity.closest_to(self.unit.position)

            else:
                target:Union[Unit, Point2] = attack_target
            if self.bot.debug and self.unit:
                try:
                    self.bot.debug_tools.debug_targeting(self, target)
                # pylint: disable=W0718
                except Exception as e:
                    logger.warning(f"can't run debug method for {self.unit} due to {e}")


            if not self.unit.distance_to(target) <= self.unit.ground_range+RANGE_BUFFER:
                if isinstance(target,Union[Unit, UnitMarker]):
                    target = target.position

                move_to:Point2 = self.bot.pathing.find_path_next_point(
                            self.unit.position, target, self.pathing_grid
                        )
                self.unit.move(move_to)

            if self.unit.weapon_cooldown <= 5:
                self.unit.attack(target)

            else:
                position:Point2 = self.get_retreat_pos()
                self.unit.move(position)

        except Exception as e:
            logger.warning(e)

    async def disengage(self, retreat_position: Point2) -> None:
        """ replacement for move to safety
            -> This should contain stutter stepping, for ranged Units
        """
        if not self.unit:
            if self.bot.debug:
                logger.warning("Unit not existing")
            return
        self.bot.client.debug_text_world(self.unit_label,\
            self.unit, size=UNIT_LABEL_FONT_SIZE)
        move_to: Point2 = self.bot.pathing.find_path_next_point(
            self.unit.position, retreat_position, self.pathing_grid
        )
        self.unit.move(move_to)

