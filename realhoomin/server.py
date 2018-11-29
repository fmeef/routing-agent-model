from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, NetworkModule
from mesa.visualization.UserParam import UserSettableParameter

from realhoomin.agents import Hoomin, Road, MeetHoomin, FindRoadHoomin, Home, SocialHoomin
from realhoomin.model import HoominWorld
import settings


def friendgraph_portrayal(G):
    # The model ensures there is always 1 agent per node

    def node_color(agent):
        return '#008000'

    def edge_color(agent1, agent2):
            return '#000000'

    def edge_width(agent1, agent2):
        return 2

    def get_agents(source, target):
        return G.node[source]['agent'][0], G.node[target]['agent'][0]

    portrayal = dict()
    portrayal['nodes'] = [{'size': 6,
                           'color': node_color(agents[0]),
                           'tooltip': "id: {}<br>state: {}".format(agents[0].unique_id, agents[0].state.name),
                           }
                          for (_, agents) in G.nodes.data('agent')]

    portrayal['edges'] = [{'source': source,
                           'target': target,
                           'color': edge_color(*get_agents(source, target)),
                           'width': edge_width(*get_agents(source, target)),
                           }
                          for (source, target) in G.edges]

    return portrayal





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

    elif type(agent) is FindRoadHoomin or type(agent) is SocialHoomin:
        portrayal["Shape"] = "realhoomin/resources/base_hoomin.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Home:
        portrayal["Shape"] = "realhoomin/resources/home.png"
        portrayal["scale"] = 1.5
        portrayal["Layer"] = 0

    return portrayal

canvas_element = CanvasGrid(hoomin_portrayal, settings.width, settings.height, 500, 500)
chart_element = ChartModule([{"Label" : "Messages Exchanged", "Color" : "#CACACA"}])

friendgraph = NetworkModule(friendgraph_portrayal, 300, 300, library='d3')

model_params = {}
server = ModularServer(HoominWorld, [canvas_element, chart_element, friendgraph], "Hoomin World", model_params)
server.port = 8083
