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


ALL_STRUCTURES: Set[UnitTypeId] = {
    UnitTypeId.ARMORY,
    UnitTypeId.ASSIMILATOR,
    UnitTypeId.ASSIMILATORRICH,
    UnitTypeId.AUTOTURRET,
    UnitTypeId.BANELINGNEST,
    UnitTypeId.BARRACKS,
    UnitTypeId.BARRACKSFLYING,
    UnitTypeId.BARRACKSREACTOR,
    UnitTypeId.BARRACKSTECHLAB,
    UnitTypeId.BUNKER,
    UnitTypeId.BYPASSARMORDRONE,
    UnitTypeId.COMMANDCENTER,
    UnitTypeId.COMMANDCENTERFLYING,
    UnitTypeId.CREEPTUMOR,
    UnitTypeId.CREEPTUMORBURROWED,
    UnitTypeId.CREEPTUMORQUEEN,
    UnitTypeId.CYBERNETICSCORE,
    UnitTypeId.DARKSHRINE,
    UnitTypeId.ELSECARO_COLONIST_HUT,
    UnitTypeId.ENGINEERINGBAY,
    UnitTypeId.EVOLUTIONCHAMBER,
    UnitTypeId.EXTRACTOR,
    UnitTypeId.EXTRACTORRICH,
    UnitTypeId.FACTORY,
    UnitTypeId.FACTORYFLYING,
    UnitTypeId.FACTORYREACTOR,
    UnitTypeId.FACTORYTECHLAB,
    UnitTypeId.FLEETBEACON,
    UnitTypeId.FORGE,
    UnitTypeId.FUSIONCORE,
    UnitTypeId.GATEWAY,
    UnitTypeId.GHOSTACADEMY,
    UnitTypeId.GREATERSPIRE,
    UnitTypeId.HATCHERY,
    UnitTypeId.HIVE,
    UnitTypeId.HYDRALISKDEN,
    UnitTypeId.INFESTATIONPIT,
    UnitTypeId.LAIR,
    UnitTypeId.LURKERDENMP,
    UnitTypeId.MISSILETURRET,
    UnitTypeId.NEXUS,
    UnitTypeId.NYDUSCANAL,
    UnitTypeId.NYDUSCANALATTACKER,
    UnitTypeId.NYDUSCANALCREEPER,
    UnitTypeId.NYDUSNETWORK,
    UnitTypeId.ORACLESTASISTRAP,
    UnitTypeId.ORBITALCOMMAND,
    UnitTypeId.ORBITALCOMMANDFLYING,
    UnitTypeId.PHOTONCANNON,
    UnitTypeId.PLANETARYFORTRESS,
    UnitTypeId.POINTDEFENSEDRONE,
    UnitTypeId.PYLON,
    UnitTypeId.PYLONOVERCHARGED,
    UnitTypeId.RAVENREPAIRDRONE,
    UnitTypeId.REACTOR,
    UnitTypeId.REFINERY,
    UnitTypeId.REFINERYRICH,
    UnitTypeId.RESOURCEBLOCKER,
    UnitTypeId.ROACHWARREN,
    UnitTypeId.ROBOTICSBAY,
    UnitTypeId.ROBOTICSFACILITY,
    UnitTypeId.SENSORTOWER,
    UnitTypeId.SHIELDBATTERY,
    UnitTypeId.SPAWNINGPOOL,
    UnitTypeId.SPINECRAWLER,
    UnitTypeId.SPINECRAWLERUPROOTED,
    UnitTypeId.SPIRE,
    UnitTypeId.SPORECRAWLER,
    UnitTypeId.SPORECRAWLERUPROOTED,
    UnitTypeId.STARGATE,
    UnitTypeId.STARPORT,
    UnitTypeId.STARPORTFLYING,
    UnitTypeId.STARPORTREACTOR,
    UnitTypeId.STARPORTTECHLAB,
    UnitTypeId.SUPPLYDEPOT,
    UnitTypeId.SUPPLYDEPOTLOWERED,
    UnitTypeId.TECHLAB,
    UnitTypeId.TEMPLARARCHIVE,
    UnitTypeId.TWILIGHTCOUNCIL,
    UnitTypeId.ULTRALISKCAVERN,
    UnitTypeId.WARPGATE,
}


SECTORS:int = 3
SPEEDMINING_DISTANCE:float = 1.8