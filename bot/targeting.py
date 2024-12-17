from typing import Dict

from sc2.bot_ai import BotAI

class Targeting:

    def __init__(self, bot:BotAI):
        self.bot:BotAI = bot
        self.targeting_dict: Dict = {}

    def remove_from_targeting(self,unit_tag:str):
        self.targeting_dict.pop(unit_tag, None)

    def add_enemy_to_target(self, unit_tag:str):
        attackers: list = []
        self.targeting_dict[unit_tag] = attackers

    