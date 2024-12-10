from typing import Union

from sc2.unit import Unit
from sc2.bot_ai import BotAI
from sc2.position import Point3, Point2
from sc2.ids.unit_typeid import UnitTypeId

def unit_label(bot:BotAI, unit:Unit):
    text:str=f"Type: {unit.type_id}\nHealth: {unit.health}\nOrders: {unit.orders} \nPos {unit.position3d}"
    bot.client.debug_text_world(text,unit,color=(255,90,0),size=12)