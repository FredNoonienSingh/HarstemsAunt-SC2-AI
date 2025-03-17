"""DOCSTRING to shut up the linter"""
# pylint: disable=E0611
from typing import Set

# pylint: disable=W0611
from __init__ import logger

from sc2.ids.unit_typeid import UnitTypeId

TOWNHALL_IDS: Set[UnitTypeId] = {
    UnitTypeId.NEXUS,
    UnitTypeId.LAIR,
    UnitTypeId.HIVE,
    UnitTypeId.HATCHERY,
    UnitTypeId.COMMANDCENTER,
    UnitTypeId.ORBITALCOMMAND,
    UnitTypeId.PLANETARYFORTRESS,
}

WORKER_IDS: Set[UnitTypeId] = {
    UnitTypeId.PROBE,
    UnitTypeId.DRONE,
    UnitTypeId.DRONEBURROWED,
    UnitTypeId.SCV
}
