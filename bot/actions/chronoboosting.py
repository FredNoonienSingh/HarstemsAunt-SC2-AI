
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.ids.buff_id import BuffId
from actions.abilliies import chronoboost

async def chronoboosting(bot:BotAI) -> None:

    prios:list = [
        [UnitTypeId.ROBOTICSBAY,
                  UnitTypeId.FLEETBEACON,
                  UnitTypeId.TWILIGHTCOUNCIL,
                  UnitTypeId.FORGE,
                  UnitTypeId.CYBERNETICSCORE,
                  UnitTypeId.DARKSHRINE,
                  UnitTypeId.TEMPLARARCHIVE,
                  ],
        [UnitTypeId.GATEWAY,
                  UnitTypeId.ROBOTICSFACILITY,
                  UnitTypeId.STARGATE,
                  ],
        [UnitTypeId.NEXUS]
    ]

    for prio in prios:
        structures = bot.structures.filter(lambda struct: not struct.is_idle and \
            not struct.has_buff(BuffId.CHRONOBOOSTENERGYCOST) and struct.type_id in prio)\
                .sorted(lambda struct: struct.orders[0].progress, reverse=True)

        chrono_nexus = bot.structures(UnitTypeId.NEXUS).filter(lambda nexus: nexus.energy > 50)
        for struct in structures:
            if chrono_nexus:
                await chronoboost(bot, chrono_nexus[0],struct)