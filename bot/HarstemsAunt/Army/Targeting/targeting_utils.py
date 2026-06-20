""" keep the Target Allocator concise """
from math import pi, inf
from typing import  Union, Optional,Dict

from sc2.unit import Unit

from bot.HarstemsAunt.enums.fight_status import FightStatus
from bot.HarstemsAunt.misc.unitmarker import UnitMarker
from bot.HarstemsAunt.Army.Units.combat_unit import CombatUnit
from bot.HarstemsAunt.Army.Units.combat_flyer import CombatFlyer
from bot.HarstemsAunt.common import TRASH_UNITS, DROPSHIPS, TIME_MULTIPLIER

class TargetingUtils:

    @staticmethod
    def target_allocation_score(enemy:Union[Unit, UnitMarker],
                            enemy_cost:Dict,
                            unit:Union[CombatUnit, CombatFlyer]
                            ) -> float:
        """ calculates TAS for ground units 

        Args:
            enemy (Unit): Unit
            unit (Unit): Unit

        Returns:
            float: Target Allocation Score
        """

        if not unit.can_attack(enemy) or enemy.is_hallucination:
            return -inf

        potential_damage: float = unit.calculate_damage_vs_target(enemy)
        cost: float = enemy_cost.minerals + (2.85 * enemy_cost.vespene)

        # can you kill it right now kill it
        if unit.target_in_range(enemy) \
            and enemy.health < potential_damage:
            # if it is worth killing
            if not enemy.type_id in TRASH_UNITS:
                return 100000 + cost

        damage_scalar: float = potential_damage/10
        vulnerability:float = (enemy.health_max/(enemy.health+0.001)) +\
            (enemy.shield_max/(enemy.shield+0.001))

        tte = TargetingUtils.get_tte(enemy, unit)
        if not tte:
            tte = (unit.distance_to(enemy)/pi) + 1

        if unit.is_flying:
            dps = TargetingUtils.get_dps(enemy, True)
        else:
            dps = TargetingUtils.get_dps(enemy,False)

        tas: float = (pow(dps,3) + pow(vulnerability,2) + cost) / tte
        final_score: float = damage_scalar*tas

        if enemy.type_id in TRASH_UNITS:
            return final_score * 0.5
        return final_score


    @staticmethod
    def get_dps(enemy:Unit, flyer_score:bool) -> float:
        """ returns dps based on the requesting UnitType   """
        if enemy.type_id in DROPSHIPS:
            dps: float = 220 + (enemy.energy /4)
            return dps
        if flyer_score:
            dps: float = enemy.air_dps + (enemy.ground_dps/2) + (enemy.energy / 4)
        else:
            dps: float = enemy.ground_dps + (enemy.air_dps/2) + (enemy.energy / 4)
        return dps


    @staticmethod
    def get_tte(enemy:Union[Unit, UnitMarker],
                unit:Union[CombatUnit, CombatFlyer]
                ) -> Optional[float]:
        """ calculates the time to be engaged or to engage based depending on the situation"""
        distance = unit.distance_to(enemy)
        # just in case as defensive as possible
        speed:float = 0.001
        gap:float = inf

        if unit.fight_status == FightStatus.FIGHTING:
            if isinstance(unit, CombatUnit):
                gap: float = max(0, (distance-unit.ground_range))
            else: # Expected is a CombatFlyer
                gap: float = max(0, distance-unit.air_range)
            speed += unit.movement_speed

        if unit.fight_status in [FightStatus.DEFENDING, FightStatus.RETREATING]:
            gap:float = max(0, distance - \
                (enemy.air_range if unit.is_flying else enemy.ground_range))
            speed += enemy.movement_speed

        tte:float = gap/(speed*TIME_MULTIPLIER)
        return tte