""" Holds Wrappers for Abilities"""
from typing import Union
from sc2.bot_ai import BotAI
from sc2.position import Point3, Point2
from sc2.unit import Unit
from sc2.ids.ability_id import AbilityId


"""Units"""

async def blink(bot:BotAI,stalker:Unit,target:Union[Point3, Unit]):
    bot.do(stalker(AbilityId.EFFECT_BLINK_STALKER,target))

async def prismaticaligment(bot:BotAI,voidray:Unit):
    bot.do(voidray(AbilityId.EFFECT_VOIDRAYPRISMATICALIGNMENT))

async def gravitonbeam(bot:BotAI,phoenix:Unit,target:Unit):
    bot.do(phoenix(AbilityId.GRAVITONBEAM_GRAVITONBEAM,target))

async def charge(bot:BotAI,zealot:Unit,target:Unit):
    bot.do(zealot(AbilityId.EFFECT_CHARGE,target))

async def strom(bot:BotAI,templar:Unit,target:Union[Unit, Point2]):
    bot.do(templar(AbilityId.PSISTORM_PSISTORM,target))

async def feedback(bot:BotAI,templar:Unit,target:Unit):
    bot.do(templar(AbilityId.FEEDBACK_FEEDBACK,target))

async def morph(bot:BotAI,templar:Unit,target:Unit):
    bot.do(templar(AbilityId.MORPH_ARCHON,target))


""" Prism """

async def load_prism(bot:BotAI, prism:Unit, target:Unit):
    bot.do(prism(AbilityId.LOAD_WARPPRISM, target))

async def unload_prism(bot:BotAI, prism:Unit, target:Point3):
    bot.do(prism(AbilityId.UNLOAD_WARPPRISM, target))

async def morph_phasing(bot:BotAI, prism:Unit):
    bot.do(prism(AbilityId.MORPH_WARPPRISMPHASINGMODE))

async def morph_transport(bot:BotAI, prism:Unit):
    bot.do(prism(AbilityId.MORPH_WARPPRISMTRANSPORTMODE))


"""Structures"""


async def shield_battery(bot:BotAI, battery:Unit, target:Unit):
    bot.do(battery(AbilityId.EFFECT_RESTORE, target))