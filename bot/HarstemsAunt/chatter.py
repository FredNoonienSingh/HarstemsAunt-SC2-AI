"""Handles all chatter"""
# pylint: disable=E0401
from sc2.bot_ai import BotAI

class Chatter:
    """handles all bot chatter """

    @staticmethod
    async def greeting(bot:BotAI):
        """sends the greeting"""
        await bot.chat_send(bot.greeting)

    @staticmethod
    async def build_order_comments(bot:BotAI):
        """ Comments on the Build of the Opponent """
        if not bot.macro.build_order.opponent_builds_air:
            if [unit for unit in bot.seen_enemies if unit.is_flying and unit.can_attack]:
                bot.macro.build_order.opponent_builds_air = True
                await bot.chat_send("I see you got an AirForce, i can do that too")

        if not bot.macro.build_order.opponent_has_detection:
            if [unit for unit in bot.seen_enemies if unit.is_detector]:
                bot.macro.build_order.opponent_has_detection = True

        if not bot.macro.build_order.opponent_uses_cloak:
            if [unit for unit in bot.seen_enemies if (unit.is_cloaked and unit.can_attack) \
                or (unit.is_burrowed and unit.can_attack)]:
                bot.macro.build_order.opponent_uses_cloak = True
                await bot.chat_send("Stop hiding and fight like a honorable ... \
                        ähm... Robot?\ndo computers have honor ?")

    @staticmethod
    async def end_game_message(bot:BotAI) -> None:
        """ sends the the message before leaving """
        await bot.chat_send\
                (f"GG, you are probably a hackcheating smurf cheat hacker anyway also\
                {bot.enemy_race} is IMBA")