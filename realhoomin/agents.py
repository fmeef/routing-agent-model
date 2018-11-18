from mesa import Agent
from realhoomin.generichoomin import GenericHoomin

class Hoomin(GenericHoomin):

    def step(self):
        self.hoomin_dance()


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

