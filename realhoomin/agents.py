from mesa import Agent
import numpy as np


class ScatterMessage():
    """
    represents a message that moves between hoomans using a DTN
    """
    _currentid = 0

    @staticmethod
    def nextID():
        currentid += 1
        return currentid

    def __init__(self, message):
        self.id = ScatterMessage.nextID()
        self.num_hops = 0
        self.message = message

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

    def __init__(self, unique_id, pos, model, scatterrange=7):
        super().__init__(unique_id, pos, model)
        self.modes = (Hoomin.ROADHOOMIN,
                      Hoomin.FLIRTHOOMIN,
                      Hoomin.BUYHOOMIN,
                      Hoomin.RESTHOOMIN,
                      Hoomin.WORKHOOMIN)

        self.mode = Hoomin.ROADHOOMIN
        self.dst = None
        self.seekingroad = False
        self.home = None
        self.previous_road = None
        self.scatterbuffer = []
        self.scatterrange = scatterrange

    #checks the new destination for bounds and sets it as this hooman's destination
    def setdst(self, newdst):
        if newdst[0] < 0 or newdst[0] > self.model.width:
            return False
        if newdst[1] < 0 or newdst[1] > self.model.height:
            return False

        self.dst = np.array(newdst)
        return True




    #searches for the nearest road tile and returns it
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
                    if pstart[0] >= 0 and pstart[0] < self.model.width:
                        if pstart[1] >= 0 and pstart[1] < self.model.height:
                            cells = self.model.grid.get_cell_list_contents([pstart])
                            for item in cells:
                                if type(item) is Road:
                                    return item
                    pstart += mod
                mod = np.array((mod[1], -1*mod[0]))
            searchwidth += 1

        return None

    def get_neighbor_hoomins(self, radius):
        neighbors = self.model.grid.iter_neighborhood(self.pos, False, include_center=False, radius=radius)
        result = []
        for x in neighbors:
            cellcontents = self.model.grid.get_cell_list_contents(x)
            for val in cellcontents:
                if type(val) is Hoomin or issubclass(type(val), Hoomin):
                    result.append(val)

        return result


    #### REALLY IMPORTANT. Should make a lambda function to customize
    #### behaviour of scatterbrain blockdata. Right now we just edit here though
    def send_blockdata(self, hoomin):
        packets = self.random.sample(self.scatterbuffer, min(5,len(self.scatterbuffer)))
        for packet in packets:
            hoomin.scatterbuffer.append(packet)


    def store_scattermessage(self, message):
        self.scatterbuffer.append(ScatterMessage(message))

    #walks in a straight path to the hoomin's destination, ignoring roads.
    def straightwalk_to_dest(self):
        if self.dst is None:
            return False

        tovect = np.array((np.sign(self.dst[0] - self.pos[0])
                           ,np.sign(self.dst[1] - self.pos[1])))
        if (tovect[0] != 0) and (tovect[1] != 0):
            self.model.grid.move_agent(self, tuple(self.pos + tovect))
            return False

        return True

    #moves to the nearest road and stops
    def random_road(self):
        if self.seekingroad is False:
            road = self.find_nearest_road()
            print("hoomin ", self.unique_id, " found road ", road.pos)
            if road is None:
                return False
            else:
                self.seekingroad = True
                self.dst = np.array(road.pos)
        else:
            if self.straightwalk_to_dest() is True:
                self.seekingroad = False
                return True
        return False

    #move to a point following roads
    def pathfind_to_point_direct(self):
        if self.seekingroad is True:
            return False
        if self.dst is None:
            return False


        print('hooming ',self.unique_id, " pathfinding to ", self.dst )
        tovect = np.array((np.sign(self.dst[0] - self.pos[0])
                           ,np.sign(self.dst[1] - self.pos[1])))

        next = self.model.grid.get_neighbors(self.pos, False, True)
        mindist = np.sqrt(pow(self.model.height,2.0) + pow(self.model.width,2.0))
        minroad = None
        for x in next:
            if type(x) is Road:
                rdist = np.linalg.norm(self.dst - x.pos)
                if rdist < mindist:
                    mindist = rdist
                    minroad = x
        if minroad is not None:
            print("moving to road ", minroad.pos)
            self.model.grid.move_agent(self, minroad.pos)
            return True
        else:
            return False


    def random_pathfind(self):
        if self.seekingroad is True:
            return False

        print('hoomin ', self.unique_id, " random moving")

        next = self.model.grid.get_neighbors(self.pos, False, True)

        roadchoices = []
        for x in next:
            if type(x) is Road:
                roadchoices.append(x)

        roadchoices = set(roadchoices)
        if self.previous_road is not None:
            roadchoices.difference(set([self.previous_road]))

        self.previous_road = self.pos

        if len(roadchoices) > 0:
            road = self.random.sample(roadchoices, 1)
            self.model.grid.move_agent(self, road[0].pos)



    def sync_scatterbuffer(self):
        True
        #TODO:


    def step(self):
        if self.mode is Hoomin.ROADHOOMIN:
            self.random_road()



    def set_mode(self, mode):
        if mode in self.modes:
            self.mode = mode

    def get_mode(self):
        return self.mode

class Home(Agent):

    claimedhomes = set()

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.occupants = set()
    def step(self):
        return True

    def claim(self, hoomin:Hoomin):
        Home.claimedhomes = Home.claimedhomes.union(set([self]))
        self.occupants = self.occupants.union(set([hoomin]))
        hoomin.home = self



class MeetHoomin(Hoomin):

    def __init__(self, unique_id, pos, model, meettarget):
        super().__init__(unique_id, pos, model)

        self.dst = np.array(meettarget)

    def step(self):
        self.straightwalk_to_dest()

class FindRoadHoomin(Hoomin):

    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, pos, model)
        self.onroad = False
    def step(self):
        if self.onroad:
            self.dst = np.array(self.home.pos)
            self.random_pathfind()
        else:
            if self.random_road() is True:
                print("starting onroad hoomin ", self.unique_id)
                self.onroad = True


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
