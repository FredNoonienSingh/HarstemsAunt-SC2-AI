from __init__ import logger

from typing import Set, Dict
from sc2.data import Race
from sc2.ids.unit_typeid import UnitTypeId

UNIT_COMPOSIOTION:Dict = {
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
                UnitTypeId.ARCHON]
}

INITIAL_TECH:Dict = {
    Race.Protoss: [UnitTypeId.TWILIGHTCOUNCIL, UnitTypeId.ROBOTICSFACILITY],
    Race.Terran: [UnitTypeId.TWILIGHTCOUNCIL, UnitTypeId.TEMPLARARCHIVE],
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
    UnitTypeId.SIEGETANK,
    UnitTypeId.SIEGETANKSIEGED,
    UnitTypeId.BATTLECRUISER,

    # Zerg
    UnitTypeId.QUEEN,

    # Protoss
    UnitTypeId.COLOSSUS,
    UnitTypeId.CARRIER
}

GATEWAY_UNTIS: Set[UnitTypeId] = {
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

SECTORS: int = 10
MIN_SHIELD_AMOUNT: float = 0.5
SPEEDMINING_DISTANCE: float = 1.8