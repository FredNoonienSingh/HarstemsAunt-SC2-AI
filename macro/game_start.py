
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId
from actions.set_rally import set_nexus_rally, set_rally

async def game_start(bot:BotAI, worker) -> None:
    nexus = bot.structures(UnitTypeId.NEXUS).sorted(lambda nexus: nexus.age)
     
    if not bot.structures(UnitTypeId.PYLON):
        build_pos = bot.main_base_ramp.protoss_wall_pylon
        await bot.build(UnitTypeId.PYLON, build_worker=worker, near=build_pos)
        #await set_rally(bot, nexus, build_pos)
    
    if not bot.structures(UnitTypeId.GATEWAY):
        build_pos = list(bot.main_base_ramp.protoss_wall_buildings)[0]
        nexus = bot.structures(UnitTypeId.NEXUS)[0]
        minerals =  bot.expansion_locations_dict[nexus.position].mineral_field.sorted_by_distance_to(nexus)
        if bot.already_pending(UnitTypeId.PYLON) and worker.is_idle:
            worker.patrol(build_pos)
        else:
            await set_nexus_rally(bot, nexus, minerals.closest_to(nexus))
 
    if len(bot.structures(UnitTypeId.NEXUS)) == 1 and bot.minerals > 300:
        next_expantion = await bot.get_next_expansion()
        nexus_builder = bot.workers.closest_to(next_expantion)
        nexus_builder.move(next_expantion)
