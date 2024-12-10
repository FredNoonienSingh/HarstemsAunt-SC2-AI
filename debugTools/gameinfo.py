from typing import Union

from sc2.unit import Unit
from sc2.bot_ai import BotAI
from sc2.position import Point3, Point2
from sc2.ids.unit_typeid import UnitTypeId


def draw_gameinfo(bot: BotAI):
     text:str = ""
     supply:int = bot.supply_army
     enemy_supply:int=bot.enemy_supply
     text = text +(f"supply: {supply}\nenemy_supply: {enemy_supply}\n")
     minerals:int= bot.minerals
     gas:int = bot.vespene
     text = text +(f"\nIncome: {minerals, gas}\n")
     bot.client.debug_text_screen(str(text), (0,.125), color=None, size=14)