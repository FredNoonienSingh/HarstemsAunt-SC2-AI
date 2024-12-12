
from sc2.bot_ai import BotAI
from sc2.unit import Unit

def structure_in_proximity(bot:BotAI, checked_structure, structure, max_distance)-> bool:
    structures = bot.structures.ready.closer_than(max_distance,structure)
    structure_names = [structures[x].name for x in range(len(structures))]
    return checked_structure in structure_names
   
def unit_in_proximity(bot:BotAI, checked_unit:str, unit, max_distance) ->bool:
    units = bot.units.closer_than(max_distance, unit)
    unit_names = [units[x].name for x in range(len(units))]
    return checked_unit in unit_names

def in_proximity_to_point(bot:BotAI, checked_unit, point, max_distance) -> bool:
    return checked_unit.distance_to(point) < max_distance

def is_close_to_unit(unit_1:Unit, unit_2:Unit, max_distance:int=12) -> bool:
    return unit_1.distance_to(unit_2) <= max_distance