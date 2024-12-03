
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId
from actions.set_rally import set_nexus_rally

async def game_start(bot:BotAI, worker, build_pos) -> None:
    if not bot.structures(UnitTypeId.PYLON) or not bot.structures(UnitTypeId.GATEWAY):
        nexus = bot.structures(UnitTypeId.NEXUS)[0]
        minerals =  bot.expansion_locations_dict[nexus.position].mineral_field.sorted_by_distance_to(nexus)
        if bot.already_pending(UnitTypeId.PYLON) and worker.is_idle:
            worker.patrol(build_pos)
        else:
            nexus = bot.structures(UnitTypeId.NEXUS).sorted(lambda nexus: nexus.age)
            await set_nexus_rally(bot, nexus[0], minerals.closest_to(nexus[0]))
 
        if len(bot.structures(UnitTypeId.NEXUS)) == 1 and bot.minerals > 300:
            next_expantion = await bot.get_next_expansion()
            nexus_builder = bot.workers.closest_to(next_expantion)
            nexus_builder.move(next_expantion)
