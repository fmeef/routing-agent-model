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
            hoomin = self.hoomintypes[hoomintype][key]
            hoomin.step()
            neighborhoomins = hoomin.get_neighbor_hoomins(hoomin.scatterrange)
            for n in neighborhoomins:
                hoomin.send_blockdata(n)

    def get_hoomin_count(self, hoomintype):
        return len(self.hoomintypes[hoomintype].values())
