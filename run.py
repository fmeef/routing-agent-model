from realhoomin.server import server
from realhoomin.model import HoominWorld
import settings

if settings.runheadless:
    hworld = HoominWorld()
    hworld.run_model()
else:
    server.launch()
