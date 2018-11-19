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
from realhoomin.agents  import Hoomin, Road, MeetHoomin, FindRoadHoomin, Home
import numpy as np


class HoominWorld(Model):

    LEFT = 0
    RIGHT = 1
    STRAIGHT = 2


    verbose = False
    description = "A model of foot traffic and radio communication in an urban environment"

    def roadplace_grid(self):
        for h in range(self.height):
            if h % self.gridspacing is 0:
                for w in range(self.width):
                    road = Road(self.next_id(), (w,h), self)
                    self.grid.place_agent(road, (w,h))

        for w in range(self.width):
            if w % self.gridspacing is 0:
                for h in range(self.height):
                    road = Road(self.next_id(), (w,h), self)
                    self.grid.place_agent(road, (w,h))




    def roadplace_random(self, direction=0):

        if direction is HoominWorld.STRAIGHT:
            True
        elif direction is HoominWorld.LEFT:
            self.roaddir = np.array((-1 * self.roaddir[1], self.roaddir[0]))
        elif direction is HoominWorld.RIGHT:
            self.roaddir = np.array((self.roaddir[1], -1 * self.roaddir[0]))
        else:
            self.roaddir = np.array((0,0))
            print("bad bad bad")
        print("placing road, direction ", direction, " coord: ", self.roadcurrentcoord)


        newcoord = self.roadcurrentcoord + self.roaddir
        if newcoord[0] >= self.width or newcoord[0] < 0:
            return None
        if newcoord[1] >= self.height or newcoord[1] < 0:
            return None

        self.roadcurrentcoord += self.roaddir

        road = Road(self.next_id(), tuple(self.roadcurrentcoord), self)
        self.grid.place_agent(road, tuple(self.roadcurrentcoord))

        return road


    def singleroad(self, initialcoord=(0,0)):
        #initialize roads
        print("placing road seed: ", initialcoord)
        roaddir = self.random.randrange(4)
        roadseedx = self.random.randrange(self.width)
        roadseedy = self.random.randrange(self.height)
        road = Road(self.next_id(), (roadseedx, roadseedy), self)
        self.roadcurrentcoord = (roadseedx, roadseedy)
        self.grid.place_agent(road, (roadseedx, roadseedy))

        #note: roads are not scheduled because they do nothing
        road = None
        counter = 0
        roadlist = []
        for i in range(self.initial_roads):
            while road is None:
                val = self.random.random()
                #print("val: " , val)
                if val <= self.straightweight:
                    road = self.roadplace_random(HoominWorld.STRAIGHT)
                elif val > self.straightweight and val <= self.leftweight + self.straightweight:
                    road = self.roadplace_random(HoominWorld.LEFT)
                elif val > self.leftweight + self.straightweight:
                    road = self.roadplace_random(HoominWorld.RIGHT)
                if road is None:
                    print("err: road is none")

                roadlist.append(road);
            road = None
            counter += 1
        print("initialized ", counter, " road tiles")
        self.roadset = self.roadset.union(set(roadlist))
        del roadlist


    def __init__(self, height=50, width=50, initial_hoomins=10):
        super().__init__()

        print("initializing ", width, height)
        #map height and width
        self.height = height
        self.width = width

        #ignore this. it does nothing
        self.hoomin_level = 0

        #road generation tuning
        self.straightweight = 0.9
        self.leftweight = 0.05
        self.rightweight = 0.05
        self.initial_roads = 80
        self.initial_road_seeds = 4
        self.gridspacing = 7
        self.roadcurrentcoord = np.array((0,0))
        self.roaddir = np.array((1,0))
        self.roadset = set()


        #home tuning options
        self.homes_per_hoomins = 1
        self.initial_homes = self.homes_per_hoomins * initial_hoomins
        self.homeset = set()


        #scatterbrain metrics
        self.total_scattermessages = 0


        #hoomin tuning values
        self.initial_hoomins = initial_hoomins
        self.schedule = RandomHoominActivation(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector({"Messages Exchanged" : lambda m: m.total_scattermessages})

        #initialize roads
        for i in range(self.initial_road_seeds):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)

            self.singleroad((x,y))


        homelist = []

        #initialize homes
        for i in range(self.initial_homes):
            road = self.random.sample(self.roadset, 1)
            #TODO get neighbors and put home
            if len(road) > 0 and road[0] is not None:
                neighbors = self.grid.get_neighborhood(road[0].pos, False, True)
            for neighbor in neighbors:
                n = []
                if len(self.grid.get_cell_list_contents(neighbor)) is 0:
                    n.append(neighbor)
                if len(n) > 0:
                    homeblock = self.random.sample(n, 1)
                    home = Home(self.next_id(), homeblock[0], self)
                    homelist.append(home)
                    self.grid.place_agent(home, homeblock[0])

        self.homeset = self.homeset.union(set(homelist))

        #initialize hoomins
        for i in range(self.initial_hoomins):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            hoomin = FindRoadHoomin(self.next_id(), (x,y), self)
            possiblehomes = self.homeset.difference(Home.claimedhomes)
            myhome = self.random.sample(possiblehomes, 1)
            if len(myhome) > 0:
                myhome[0].claim(hoomin)
            self.grid.place_agent(hoomin, (x,y))
            self.schedule.add(hoomin)

        self.roadplace_grid()
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
