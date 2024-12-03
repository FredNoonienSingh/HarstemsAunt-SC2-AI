from typing import Union

from sc2.unit import Unit
from sc2.bot_ai import BotAI
from sc2.position import Point3, Point2
from sc2.ids.unit_typeid import UnitTypeId

from util.calculate_supply import calculate_enemy_supply

def draw_gameinfo(bot: BotAI, params:dict={"next_step":True,"supply":True,"income":True,"unit_count":True}): 
    
     text:str = ""
     
     if params.get("next_step"):
          next_step = bot.build_order[bot.step]
          text = text + (f"next: {next_step}\n")
     if params.get("supply"): 
        supply:int = bot.supply_army
        enemy_supply:int=calculate_enemy_supply(bot)
        text= text +(f"supply: {supply}\nenemy_supply: {enemy_supply}\n")
     if params.get("income"):
         minerals:int= bot.minerals
         gas:int = bot.vespene
         text = text +(f"\nIncome: {minerals, gas}\n")
     if params.get("\nunit_count"):     
         for unit_type in set([unit.type_id for unit in bot.units]):
              text = text +(f"{unit_type}: {len(bot.units(unit_type))}\n")

     bot.client.debug_text_screen(str(text), (0,.125), color=None, size=18)