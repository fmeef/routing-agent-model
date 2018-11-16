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
from realhoomin.agents  import Hoomin

class HoominWorld(Model):


    height = 50
    width = 50

    hoomin_level = 0

    initial_hoomins = 10

    verbose = False

    description = "A model of foot traffic and radio communication in an urban environment"

    def __init__(self, height=50, width=50, initial_hoomins=10):
        super().__init__()


        self.height = height
        self.width = width
        self.initial_hoomins = initial_hoomins
        self.schedule = RandomHoominActivation(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector({"Hoomin Level" : lambda m: m.hoomin_level})


        #initialize hoomins
        for i in range(self.initial_hoomins):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)

            hoomin = Hoomin(self.next_id(), (x,y), self)
            self.grid.place_agent(hoomin, (x,y))
            self.schedule.add(hoomin)


        self.running = True
        self.datacollector.collect(self)


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
