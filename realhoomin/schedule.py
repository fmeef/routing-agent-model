from collections import defaultdict

from mesa.time import RandomActivation



class RandomHoominActivation(RandomActivation):

    def __init__(self, model):
        super().__init__(model)
        self.hoomintypes = defaultdict(dict)

    def add(self, agent):

        self._agents[agent.unique_id] = agent
        agent_class = type(agent)
        self.hoomintypes[agent_class][agent.unique_id] = agent

    def remove(self, agent):
        del self._agents[agent.unique_id]

        agent_class = type(agent)
        del self.hoomintypes[agent_class][agent.unique_id]

    def step(self, byhoomintype=True):
        if byhoomintype:
            for agent_class in self.hoomintypes:
                self.step_hoomintype(agent_class)
            self.steps += 1
        else:
            super().step()

    def step_hoomintype(self, hoomintype):
        agent_keys = list(self.hoomintypes[hoomintype].keys())
        self.model.random.shuffle(agent_keys)
        for key in agent_keys:
            self.hoomintypes[hoomintype][key].step()
            neighborhoomins = self.hoomintypes[hoomintype][key].get_neighbor_hoomins(50)
            

    def get_hoomin_count(self, hoomintype):
        return len(self.hoomintypes[hoomintype].values())

