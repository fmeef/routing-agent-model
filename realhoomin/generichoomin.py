from mesa import Agent


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

