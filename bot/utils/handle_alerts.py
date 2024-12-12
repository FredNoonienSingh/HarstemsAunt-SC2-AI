
from sc2.bot_ai import BotAI
from sc2.data import Alert

""" Possible Alerts:
AlertError
AddOnComplete
BuildingComplete
BuildingUnderAttack
LarvaHatched
MergeComplete
MineralsExhausted
MorphComplete
MothershipComplete
MULEExpired
NuclearLaunchDetected
NukeComplete
NydusWormDetected
ResearchComplete
TrainError
TrainUnitComplete
TrainWorkerComplete
TransformationComplete
UnitUnderAttack
UpgradeComplete
VespeneExhausted
WarpInComplete
"""

def handle_alerts(bot: BotAI, alert) -> None:
    match alert:
        case Alert.VespeneExhausted:
            bot.gas_count += 1
            print(alert)
        case Alert.NuclearLaunchDetected:
            pass 
        case Alert.NydusWormDetected:
            pass