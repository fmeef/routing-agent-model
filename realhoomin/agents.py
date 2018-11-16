from mesa import Agent
from realhoomin.generichoomin import GenericHoomin

class Hoomin(GenericHoomin):

    def step(self):
        self.hoomin_dance()
