'''
Basic behavioral model of an urban environment,
for testing routing algorithms in delay-tolerant
networks.

**very much a work in progress**
'''



from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from realhoomin.schedule import RandomHoominActivation
from realhoomin.agents  import Hoomin, Road
import numpy as np


class HoominWorld(Model):

    LEFT = 0
    RIGHT = 1
    STRAIGHT = 2


    verbose = False
    description = "A model of foot traffic and radio communication in an urban environment"

    def roadplace(self, direction=0):

        if direction is HoominWorld.STRAIGHT:
            True
        elif direction is HoominWorld.LEFT:
            self.roaddir = np.array((-1 * self.roaddir[1], self.roaddir[0]))
        elif direction is HoominWorld.RIGHT:
            self.roaddir = np.array((self.roaddir[1], -1 * self.roaddir[0]))
        else:
            self.roaddir = np.array((0,0))


        newcoord = self.roadcurrentcoord + self.roaddir
        if newcoord[0] >= self.width or newcoord[0] < 0:
            return None
        if newcoord[1] >= self.height or newcoord[0] < 0:
            return None

        self.roadcurrentcoord += self.roaddir

        road = Road(self.next_id(), tuple(self.roadcurrentcoord), self)
        print("placing road, direction ", direction, " coord: ", self.roadcurrentcoord)
        self.grid.place_agent(road, tuple(self.roadcurrentcoord))

        return road


    def singleroad(self, initialcoord=(0,0)):
        #initialize roads
        roaddir = self.random.randrange(4)
        roadseedx = self.random.randrange(self.width)
        roadseedy = self.random.randrange(self.height)
        road = Road(self.next_id(), (roadseedx, roadseedy), self)
        self.grid.place_agent(road, (roadseedx, roadseedy))

        #note: roads are not scheduled because they do nothing

        for i in range(self.initial_roads):
            val = self.random.random()
            print("val: " , val)
            if val <= self.straightweight:
                self.roadplace(HoominWorld.STRAIGHT)
            elif val > self.straightweight and val <= self.leftweight + self.straightweight:
                self.roadplace(HoominWorld.LEFT)
            elif val > self.leftweight + self.straightweight:
                self.roadplace(HoominWorld.RIGHT)


    def __init__(self, height=50, width=50, initial_hoomins=10):
        super().__init__()

        #map height and width
        self.height = height
        self.width = width

        #ignore this. it does nothing
        self.hoomin_level = 0

        #road generation tuning
        self.straightweight = 0.7
        self.leftweight = 0.15
        self.rightweight = 0.15
        self.initial_roads = 70
        self.initial_road_seeds = 20
        self.roadcurrentcoord = np.array((0,0))
        self.roaddir = np.array((1,0))
        self.roadset = None

        #hoomin tuning values
        self.initial_hoomins = initial_hoomins
        self.schedule = RandomHoominActivation(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector({"Hoomin Level" : lambda m: m.get_hoomin_level()})

        #initialize hoomins
        for i in range(self.initial_hoomins):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)

            hoomin = Hoomin(self.next_id(), (x,y), self)
            self.grid.place_agent(hoomin, (x,y))
            self.schedule.add(hoomin)

        #initialize roads
        for i in range(self.initial_road_seeds):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)

            self.singleroad((x,y))

        self.running = True
        self.datacollector.collect(self)


    def get_hoomin_level(self):
        return self.hoomin_level

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        self.hoomin_level += 1
        if self.verbose:
            print([self.schedule.time,
                   "nothing yet"])

    def run_model(self, step_count=200):
        if self.verbose:
            print("Initializing hoomins" ,
                  self.schedule.get_hoomin_count(Hoomin))

            for i in range(step_count):
                self.step()
