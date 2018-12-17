from realhoomin.server import server
from realhoomin.model import HoominWorld
import settings
import sys

height = settings.height
width = settings.width

def trial_highrange(start, end):
    settings.bluetooth_range = 8
    settings.socialswitchprobability = 0.1
    settings.randomswitchprobability = 0.03

    for x in range(start, end):
        hworld = HoominWorld(logtag="highrange"+str(x), height=height, width=width)
        hworld.run_model()
        del hworld

def trial_lowrange(start, end):
    settings.bluetooth_range = 4
    settings.socialswitchprobability = 0.1
    settings.randomswitchprobability = 0.03

    for x in range(start, end):
        hworld = HoominWorld(logtag="lowrange"+str(x), height=height, width=width)
        hworld.run_model()
        del hworld

if settings.runheadless:
    print("running lowrange model")
    trial_lowrange(int(sys.argv[1]), int(sys.argv[2]))
    print("running highrange model")
    trial_highrange(int(sys.argv[1]), int(sys.argv[2]))
    print("DONE")
else:
    server.launch()
