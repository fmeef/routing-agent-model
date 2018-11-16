from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from realhoomin.agents import Hoomin
from realhoomin.model import HoominWorld


def hoomin_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Hoomin:
        portrayal["Shape"] = "realhoomin/resources/base_hoomin.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    return portrayal

canvas_element = CanvasGrid(hoomin_portrayal, 20, 20, 500, 500)
chart_element = ChartModule([{"Label" : "Hoomin Level", "Color" : "#FFFFFF"}])

model_params = {}
server = ModularServer(HoominWorld, [canvas_element, chart_element], "Hoomin World", model_params)
server.port = 8083

