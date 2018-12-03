from realhoomin.server import server
from realhoomin.model import HoominWorld
import settings


#assumes settings from git 2b07649
def trial_social(num_trials):
    settings.socialswitchprobability = 0.01
    settings.randomswitchprobability = 0.05

    for x in range(num_trials):
        hworld = HoominWorld(logtag="social"+str(x))
        hworld.run_model()
        del hworld

#assumes settings from git 2b07649
def trial_neet(num_trials):
    settings.socialswitchprobability = 0.00
    settings.randomswitchprobability = 1.0

    for x in range(num_trials):
        hworld = HoominWorld(logtag="neet"+str(x))
        hworld.run_model()
        del hworld

if settings.runheadless:
    print("running social model")
    trial_social(200)
    print("running NEET model")
    trial_neet(200)
    print("DONE")
else:
    server.launch()
