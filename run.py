from realhoomin.server import server
from realhoomin.model import HoominWorld
import settings


#assumes settings from git 2b07649
def trial_social():
    settings.socialswitchprobability = 0.01
    settings.randomswitchprobability = 0.05

    hworld = HoominWorld()
    
if settings.runheadless:
    hworld = HoominWorld()
    hworld.run_model()
else:
    server.launch()
