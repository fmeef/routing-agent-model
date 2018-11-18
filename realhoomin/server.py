from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from realhoomin.agents import Hoomin, Road, MeetHoomin, FindRoadHoomin, Home
from realhoomin.model import HoominWorld


def hoomin_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Hoomin:
        portrayal["Shape"] = "realhoomin/resources/base_hoomin.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Road:
        portrayal["Shape"] = "realhoomin/resources/road.png"
        portrayal["scale"] = 1.0
        portrayal["Layer"] = 0

    elif type(agent) is MeetHoomin:
        portrayal["Shape"] = "realhoomin/resources/base_hoomin.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is FindRoadHoomin:
        portrayal["Shape"] = "realhoomin/resources/base_hoomin.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Home:
        portrayal["Shape"] = "realhoomin/resources/home.png"
        portrayal["scale"] = 1.5
        portrayal["Layer"] = 0

    return portrayal

canvas_element = CanvasGrid(hoomin_portrayal, 50, 50, 500, 500)
chart_element = ChartModule([{"Label" : "Hoomin Level", "Color" : "#CACACA"}])

model_params = {}
server = ModularServer(HoominWorld, [canvas_element, chart_element], "Hoomin World", model_params)
server.port = 8083
