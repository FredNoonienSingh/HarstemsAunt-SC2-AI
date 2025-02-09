"""DOCSTRING to shut up the linter"""
# pylint: disable=E0611
from typing import Dict, Set, List

# pylint: disable=W0611
from __init__ import logger
from sc2.data import Race
from sc2.ids.unit_typeid import UnitTypeId

SECTORS: int = 10
DEBUG: bool = True
RUN_BY_SIZE: int = 4
DT_TIMING: float = 480
DEBUG_FONT_SIZE: int = 7
MIN_SHIELD_AMOUNT: float = 0.5
SPEEDMINING_DISTANCE: float = 1.8

UNIT_COMPOSITION: Dict = {
    Race.Protoss: [UnitTypeId.STALKER,
                   UnitTypeId.ZEALOT,
                   UnitTypeId.IMMORTAL
                   ],
    Race.Terran: [UnitTypeId.ZEALOT,
                  UnitTypeId.STALKER,
                  UnitTypeId.HIGHTEMPLAR,
                  ],
    Race.Zerg: [UnitTypeId.ZEALOT,
                UnitTypeId.IMMORTAL,
                UnitTypeId.ARCHON
                ]
}

INITIAL_TECH: Dict = {
    Race.Protoss: [UnitTypeId.TWILIGHTCOUNCIL, UnitTypeId.ROBOTICSFACILITY],
    Race.Terran: [UnitTypeId.TWILIGHTCOUNCIL, UnitTypeId.ROBOTICSFACILITY],
    # [UnitTypeId.TWILIGHTCOUNCIL, UnitTypeId.TEMPLARARCHIVE], -> Terran tech change back later
    Race.Zerg: [UnitTypeId.TWILIGHTCOUNCIL, UnitTypeId.ROBOTICSFACILITY]
}

MAP_LIST: list = [
    "AbyssalReefAIE",
    "AcropolisAIE",
    "AutomatonAIE",
    "EphemeronAIE",
    "InterloperAIE",
    "ThunderbirdAIE"
]

TOWNHALL_IDS: Set[UnitTypeId] = {
    UnitTypeId.NEXUS,
    UnitTypeId.LAIR,
    UnitTypeId.HIVE,
    UnitTypeId.HATCHERY,
    UnitTypeId.COMMANDCENTER,
    UnitTypeId.ORBITALCOMMAND,
    UnitTypeId.PLANETARYFORTRESS,
}

RACES: Set[Race] = {
    Race.Zerg,
    Race.Terran,
    Race.Protoss
}

ATTACK_TARGET_IGNORE: Set[UnitTypeId] = {
    UnitTypeId.LARVA,
    UnitTypeId.EGG,
    UnitTypeId.CHANGELING,
    UnitTypeId.CHANGELINGMARINE,
    UnitTypeId.CHANGELINGMARINESHIELD,
    UnitTypeId.CHANGELINGZEALOT,
    UnitTypeId.CHANGELINGZERGLING,
    UnitTypeId.CHANGELINGZERGLINGWINGS,
}

PRIO_ATTACK_TARGET: Set[UnitTypeId] = {
    # Terran
    UnitTypeId.GHOST,
    UnitTypeId.SIEGETANK,
    UnitTypeId.SIEGETANKSIEGED,
    UnitTypeId.BATTLECRUISER,

    # Zerg
    UnitTypeId.QUEEN,
    UnitTypeId.LURKER,
    UnitTypeId.LURKERBURROWED,
    UnitTypeId.NYDUSCANAL,

    # Protoss
    UnitTypeId.COLOSSUS,
    UnitTypeId.CARRIER,
    UnitTypeId.ARCHON,
}

GATEWAY_UNITS: Set[UnitTypeId] = {
    UnitTypeId.ZEALOT,
    UnitTypeId.STALKER,
    UnitTypeId.SENTRY,
    UnitTypeId.ADEPT,
    UnitTypeId.HIGHTEMPLAR,
    UnitTypeId.DARKTEMPLAR
}

ROBO_UNITS: Set[UnitTypeId] = {
    UnitTypeId.OBSERVER,
    UnitTypeId.WARPPRISM,
    UnitTypeId.IMMORTAL,
    UnitTypeId.DISRUPTOR,
    UnitTypeId.COLOSSUS
}

STARGATE_UNITS: Set[UnitTypeId] = {
    UnitTypeId.PHOENIX,
    UnitTypeId.VOIDRAY,
    UnitTypeId.ORACLE,
    UnitTypeId.CARRIER,
    UnitTypeId.TEMPEST
}

WORKER_IDS: Set[UnitTypeId] = {
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

COUNTER_DICT: Dict[UnitTypeId, List] = {
    # Zerg Units
    UnitTypeId.ZERGLING: [UnitTypeId.ZEALOT, UnitTypeId.STALKER, UnitTypeId.SENTRY, UnitTypeId.ARCHON],
    UnitTypeId.HYDRALISK:[UnitTypeId.STALKER, UnitTypeId.ARCHON, UnitTypeId.IMMORTAL],
    UnitTypeId.MUTALISK:[UnitTypeId.PHOENIX, UnitTypeId.ARCHON, UnitTypeId.CARRIER],
    UnitTypeId.BANELING: [UnitTypeId.STALKER, UnitTypeId.IMMORTAL, UnitTypeId.COLOSSUS],
    UnitTypeId.ROACH: [UnitTypeId.ZEALOT, UnitTypeId.IMMORTAL, UnitTypeId.COLOSSUS],
    UnitTypeId.ULTRALISK:[UnitTypeId.IMMORTAL, UnitTypeId.COLOSSUS, UnitTypeId.TEMPEST],
    UnitTypeId.INFESTOR: [UnitTypeId.STALKER, UnitTypeId.HIGHTEMPLAR, UnitTypeId.DISRUPTOR],
    UnitTypeId.LURKER: [UnitTypeId.OBSERVER, UnitTypeId.STALKER, UnitTypeId.DISRUPTOR],
    UnitTypeId.BROODLORD:[UnitTypeId.VOIDRAY, UnitTypeId.TEMPEST, UnitTypeId.CARRIER],
    UnitTypeId.CORRUPTOR:[UnitTypeId.PHOENIX, UnitTypeId.STALKER, UnitTypeId.CARRIER],
    UnitTypeId.QUEEN:[UnitTypeId.ZEALOT, UnitTypeId.STALKER],
    UnitTypeId.OVERLORD: [UnitTypeId.PHOENIX, UnitTypeId.STALKER],
    # Terran Units
    UnitTypeId.MARINE: [UnitTypeId.ZEALOT, UnitTypeId.STALKER, UnitTypeId.ARCHON],
    UnitTypeId.MARAUDER:[UnitTypeId.IMMORTAL, UnitTypeId.COLOSSUS, UnitTypeId.ARCHON],
    UnitTypeId.REAPER: [UnitTypeId.STALKER, UnitTypeId.PHOENIX],
    UnitTypeId.GHOST:[UnitTypeId.STALKER, UnitTypeId.HIGHTEMPLAR, UnitTypeId.DISRUPTOR],
    UnitTypeId.SIEGETANK:[UnitTypeId.STALKER, UnitTypeId.VOIDRAY, UnitTypeId.TEMPEST],
    UnitTypeId.HELLION: [UnitTypeId.STALKER],
    UnitTypeId.THOR:[UnitTypeId.VOIDRAY, UnitTypeId.TEMPEST, UnitTypeId.CARRIER],
    UnitTypeId.VIKING: [UnitTypeId.STALKER, UnitTypeId.PHOENIX, UnitTypeId.ARCHON],
    UnitTypeId.BATTLECRUISER:[UnitTypeId.VOIDRAY, UnitTypeId.TEMPEST, UnitTypeId.CARRIER],
    UnitTypeId.RAVEN: [UnitTypeId.STALKER, UnitTypeId.PHOENIX, UnitTypeId.ARCHON],
    UnitTypeId.BANSHEE: [UnitTypeId.STALKER, UnitTypeId.PHOENIX, UnitTypeId.ARCHON],
    UnitTypeId.LIBERATOR:[UnitTypeId.STALKER, UnitTypeId.PHOENIX, UnitTypeId.ARCHON],
    UnitTypeId.WIDOWMINE:[UnitTypeId.OBSERVER, UnitTypeId.STALKER, UnitTypeId.DISRUPTOR],
    # Protoss Units
    UnitTypeId.ZEALOT: [UnitTypeId.ZEALOT, UnitTypeId.STALKER, UnitTypeId.SENTRY, UnitTypeId.IMMORTAL],
    UnitTypeId.STALKER:[UnitTypeId.STALKER, UnitTypeId.ARCHON, UnitTypeId.DISRUPTOR, UnitTypeId.IMMORTAL],
    UnitTypeId.SENTRY: [UnitTypeId.SENTRY, UnitTypeId.STALKER, UnitTypeId.HIGHTEMPLAR],
    UnitTypeId.HIGHTEMPLAR: [UnitTypeId.HIGHTEMPLAR, UnitTypeId.ARCHON, UnitTypeId.STALKER],
    UnitTypeId.DARKTEMPLAR: [UnitTypeId.DARKTEMPLAR, UnitTypeId.STALKER, UnitTypeId.ARCHON],
    UnitTypeId.ARCHON: [UnitTypeId.ARCHON, UnitTypeId.TEMPEST, UnitTypeId.CARRIER, UnitTypeId.IMMORTAL],
    UnitTypeId.IMMORTAL:[UnitTypeId.IMMORTAL, UnitTypeId.COLOSSUS, UnitTypeId.ARCHON],
    UnitTypeId.COLOSSUS:[UnitTypeId.COLOSSUS, UnitTypeId.TEMPEST, UnitTypeId.CARRIER],
    UnitTypeId.VOIDRAY: [UnitTypeId.VOIDRAY, UnitTypeId.PHOENIX, UnitTypeId.CARRIER], 
    UnitTypeId.CARRIER:[UnitTypeId.CARRIER, UnitTypeId.TEMPEST, UnitTypeId.VOIDRAY],
    UnitTypeId.PHOENIX: [UnitTypeId.PHOENIX, UnitTypeId.STALKER, UnitTypeId.ARCHON],
    UnitTypeId.TEMPEST: [UnitTypeId.TEMPEST, UnitTypeId.CARRIER],
    UnitTypeId.DISRUPTOR: [UnitTypeId.DISRUPTOR, UnitTypeId.STALKER, UnitTypeId.ARCHON],
    UnitTypeId.MOTHERSHIP:[UnitTypeId.MOTHERSHIP, UnitTypeId.CARRIER, UnitTypeId.TEMPEST], 
}

INFLUENCE_COSTS: Dict[UnitTypeId, Dict] = {
    UnitTypeId.ADEPT: {
        "AirCost": 0,
        "GroundCost": 9,
        "AirRange": 0,
        "GroundRange": 5
    },
    UnitTypeId.ADEPTPHASESHIFT: {
        "AirCost": 0,
        "GroundCost": 9,
        "AirRange": 0,
        "GroundRange": 5,
    },
    UnitTypeId.AUTOTURRET: {
        "AirCost": 31,
        "GroundCost": 31,
        "AirRange": 7,
        "GroundRange": 7,
    },
    UnitTypeId.ARCHON: {
        "AirCost": 40,
        "GroundCost": 40,
        "AirRange": 3,
        "GroundRange": 3,
    },
    UnitTypeId.BANELING: {
        "AirCost": 0,
        "GroundCost": 20,
        "AirRange": 0,
        "GroundRange": 3,
    },
    UnitTypeId.BANSHEE: {
        "AirCost": 0,
        "GroundCost": 12,
        "AirRange": 0,
        "GroundRange": 6,
    },
    UnitTypeId.BATTLECRUISER: {
        "AirCost": 31,
        "GroundCost": 50,
        "AirRange": 6,
        "GroundRange": 6,
    },
    UnitTypeId.BUNKER: {
        "AirCost": 22,
        "GroundCost": 22,
        "AirRange": 6,
        "GroundRange": 6,
    },
    UnitTypeId.CARRIER: {
        "AirCost": 20,
        "GroundCost": 20,
        "AirRange": 11,
        "GroundRange": 11,
    },
    UnitTypeId.CORRUPTOR: {
        "AirCost": 10,
        "GroundCost": 0,
        "AirRange": 6,
        "GroundRange": 0,
    },
    UnitTypeId.CYCLONE: {
        "AirCost": 27,
        "GroundCost": 27,
        "AirRange": 7,
        "GroundRange": 7,
    },
    UnitTypeId.GHOST: {
        "AirCost": 10,
        "GroundCost": 10,
        "AirRange": 6,
        "GroundRange": 6,
    },
    UnitTypeId.HELLION: {
        "AirCost": 0,
        "GroundCost": 8,
        "AirRange": 0,
        "GroundRange": 8,
    },
    UnitTypeId.HYDRALISK: {
        "AirCost": 20,
        "GroundCost": 20,
        "AirRange": 6,
        "GroundRange": 6,
    },
    UnitTypeId.INFESTOR: {
        "AirCost": 30,
        "GroundCost": 30,
        "AirRange": 10,
        "GroundRange": 10,
    },
    UnitTypeId.LIBERATOR: {
        "AirCost": 10,
        "GroundCost": 0,
        "AirRange": 5,
        "GroundRange": 0,
    },
    UnitTypeId.MARINE: {
        "AirCost": 10,
        "GroundCost": 10,
        "AirRange": 5,
        "GroundRange": 5,
    },
    UnitTypeId.MOTHERSHIP: {
        "AirCost": 23,
        "GroundCost": 23,
        "AirRange": 7,
        "GroundRange": 7,
    },
    UnitTypeId.MUTALISK: {
        "AirCost": 8,
        "GroundCost": 8,
        "AirRange": 3,
        "GroundRange": 3,
    },
    UnitTypeId.ORACLE: {
        "AirCost": 0,
        "GroundCost": 24,
        "AirRange": 0,
        "GroundRange": 4,
    },
    UnitTypeId.PHOENIX: {
        "AirCost": 15,
        "GroundCost": 0,
        "AirRange": 7,
        "GroundRange": 0,
    },
    UnitTypeId.PHOTONCANNON: {
        "AirCost": 22,
        "GroundCost": 22,
        "AirRange": 7,
        "GroundRange": 7,
    },
    UnitTypeId.QUEEN: {
        "AirCost": 12.6,
        "GroundCost": 11.2,
        "AirRange": 7,
        "GroundRange": 5,
    },
    UnitTypeId.SENTRY: {
        "AirCost": 8.4,
        "GroundCost": 8.4,
        "AirRange": 5,
        "GroundRange": 5,
    },
    UnitTypeId.SPINECRAWLER: {
        "AirCost": 0,
        "GroundCost": 15,
        "AirRange": 0,
        "GroundRange": 7,
    },
    UnitTypeId.STALKER: {
        "AirCost": 10,
        "GroundCost": 10,
        "AirRange": 6,
        "GroundRange": 6,
    },
    UnitTypeId.TEMPEST: {
        "AirCost": 17,
        "GroundCost": 17,
        "AirRange": 14,
        "GroundRange": 10,
    },
    UnitTypeId.THOR: {
        "AirCost": 28,
        "GroundCost": 28,
        "AirRange": 11,
        "GroundRange": 7,
    },
    UnitTypeId.VIKINGASSAULT: {
        "AirCost": 0,
        "GroundCost": 17,
        "AirRange": 0,
        "GroundRange": 6,
    },
    UnitTypeId.VIKINGFIGHTER: {
        "AirCost": 14,
        "GroundCost": 0,
        "AirRange": 9,
        "GroundRange": 0,
    },
    UnitTypeId.VOIDRAY: {
        "AirCost": 20,
        "GroundCost": 20,
        "AirRange": 6,
        "GroundRange": 6,
    },
    UnitTypeId.WIDOWMINEBURROWED: {
        "AirCost": 150,
        "GroundCost": 150,
        "AirRange": 5.5,
        "GroundRange": 5.5,
    },
}
