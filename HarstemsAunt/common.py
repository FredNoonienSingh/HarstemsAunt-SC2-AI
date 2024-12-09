from sc2.data import Race
from sc2.ids.unit_typeid import UnitTypeId

MAP_LIST= [
    "Equilibrium512V2AIE", 
    "Goldenaura512V2AIE", 
    "Gresvan512AIEV2", 
    "HardLead512AIEV2",
    "Oceanborn512V2AIE",
    "SiteDelta512V2AIE"
]

TOWNHALL_IDS =  [
    UnitTypeId.HATCHERY,
    UnitTypeId.LAIR,
    UnitTypeId.HIVE,
    UnitTypeId.COMMANDCENTER,
    UnitTypeId.ORBITALCOMMAND,
    UnitTypeId.PLANETARYFORTRESS,
    UnitTypeId.NEXUS
    ]

RACES = [
    Race.Zerg,
    Race.Terran,
    Race.Protoss
]

GATEWAY_UNTIS = [
    UnitTypeId.ZEALOT,
    UnitTypeId.STALKER,
    UnitTypeId.SENTRY,
    UnitTypeId.ADEPT
]

WORKER_IDS = [
    UnitTypeId.PROBE,
    UnitTypeId.DRONE,
    UnitTypeId.DRONEBURROWED,
    UnitTypeId.SCV
]

SPEEDMINING_DISTANCE = 1.8