from __init__ import logger

from typing import Set
from sc2.data import Race
from sc2.ids.unit_typeid import UnitTypeId

MAP_LIST:list = [
    "Equilibrium512V2AIE",
    "Goldenaura512V2AIE",
    "Gresvan512AIEV2",
    "HardLead512AIEV2",
    "Oceanborn512V2AIE",
    "SiteDelta512V2AIE"
]

TOWNHALL_IDS:Set[UnitTypeId] = {
    UnitTypeId.NEXUS,
    UnitTypeId.LAIR,
    UnitTypeId.HIVE,
    UnitTypeId.HATCHERY,
    UnitTypeId.COMMANDCENTER,
    UnitTypeId.ORBITALCOMMAND,
    UnitTypeId.PLANETARYFORTRESS,
    }

RACES:Set[Race] = {
    Race.Zerg,
    Race.Terran,
    Race.Protoss
    }

ATTACK_TARGET_IGNORE:Set[UnitTypeId] = {
    UnitTypeId.LARVA,
    UnitTypeId.EGG,
    UnitTypeId.CHANGELING,
    UnitTypeId.CHANGELINGMARINE,
    UnitTypeId.CHANGELINGMARINESHIELD,
    UnitTypeId.CHANGELINGZEALOT,
    UnitTypeId.CHANGELINGZERGLING,
    UnitTypeId.CHANGELINGZERGLINGWINGS,
    }

GATEWAY_UNTIS:Set[UnitTypeId] = {
    UnitTypeId.ZEALOT,
    UnitTypeId.STALKER,
    UnitTypeId.SENTRY,
    UnitTypeId.ADEPT,
    UnitTypeId.HIGHTEMPLAR,
    UnitTypeId.DARKTEMPLAR
    }

ROBO_UNITS:Set[UnitTypeId] = {
    UnitTypeId.OBSERVER,
    UnitTypeId.WARPPRISM,
    UnitTypeId.IMMORTAL,
    UnitTypeId.DISRUPTOR,
    UnitTypeId.COLOSSUS
    }

STARGATE_UNITS:Set[UnitTypeId] = {
    UnitTypeId.PHOENIX,
    UnitTypeId.VOIDRAY,
    UnitTypeId.ORACLE,
    UnitTypeId.CARRIER,
    UnitTypeId.TEMPEST
    }

WORKER_IDS:Set[UnitTypeId] = {
    UnitTypeId.PROBE,
    UnitTypeId.DRONE,
    UnitTypeId.DRONEBURROWED,
    UnitTypeId.SCV
    }

SECTORS:int = 3
SPEEDMINING_DISTANCE:float = 1.8