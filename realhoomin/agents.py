from mesa import Agent
import numpy as np

class GenericHoomin(Agent):


    grid = None
    x = None
    y = None

    startingpos = None

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos
        self.startingpos = pos


    def hoomin_dance(self):
        if self.pos is self.startingpos:
            next_moves = self.model.grid.get_neighborhood(self.pos, False, True)
            next_move = self.random.choice(next_moves)
            self.model.grid.move_agent(self, next_move)
        else:
            self.model.grid.move_agent(self, self.startingpos)


class Hoomin(GenericHoomin):
    ROADHOOMIN = 1
    FLIRTHOOMIN = 2
    BUYHOOMIN = 3
    RESTHOOMIN = 4
    WORKHOOMIN = 5

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, pos, model)
        self.modes = (Hoomin.ROADHOOMIN,
                      Hoomin.FLIRTHOOMIN,
                      Hoomin.BUYHOOMIN,
                      Hoomin.RESTHOOMIN,
                      Hoomin.WORKHOOMIN)

        self.mode = Hoomin.ROADHOOMIN


    def find_nearest_road(self):
        start = np.array(self.pos)
        road = None
        counter = 0
        searchwidth = 3
        mod = np.array((0,-1))
        while searchwidth < self.model.width:
            pstart = start + 1
            for x in range(4):
                for y in range(searchwidth):
                    cells = self.model.get_cell_list_contents([pstart])
                    for item in cells:
                        if type(item) is Road:
                            return item
                    pstart += mod
                mod = np.array((mod[1], -1*mod[0]))

        return None

    def random_road(self):
        True

    def step(self):
        if self.mode is Hoomin.ROADHOOMIN:
            self.random_road()

    def set_mode(self, mode):
        if mode in self.modes:
            self.mode = mode

    def get_mode(self):
        return self.mode

class Road(Agent):
    '''
    A road tile. Roads do nothing on their own, but hoomins can
    interact with them in various ways (mainly following them
    between locations)
    '''
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)

    def step(self):
        True

