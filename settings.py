import networkx as nx


## tunable settings for model

exampleval = "blob"
runheadless = True

#grid options
height = 60
width = 60

#hoomin generation tuning options
initial_hoomins = 10
initial_scattermessages = 10

# road generation tuning
straightweight = 0.98
leftweight = 0.01
rightweight = 0.01
initial_roads = 140
initial_road_seeds = 10
gridspacing = 15

#home generation tuning options
homes_per_hoomins = 1
initial_homes = homes_per_hoomins * initial_hoomins


#radio tuning options
bluetooth_range = 5

'''
Function called when exchanging scatterdata between two hoomins.

Self is hoomin initiating the exchange, hoomin is hoomin that self is
exchanging with
'''
def send_blockdata(self, hoomin):
    packets = self.random.sample(self.scatterbuffer, min(5,len(self.scatterbuffer)))
    counter = 0
    for packet in packets:
        if packet not in hoomin.scatterbuffer:
            hoomin.scatterbuffer.append(packet)
            counter += 1
    if hoomin.unique_id == self.model.final_hoomin_id:
        self.model.total_scattermessages += counter

    self.model.global_scattermessages += counter
    self.friendgraph.add_node(hoomin)
    for x in hoomin.friendlist:
        h = self.model.schedule._agents[x]
        self.friendgraph.add_node(h)
        self.friendgraph.add_edge(hoomin, h)

    if self.unique_id == self.model.hoomin_zero_id:
            self.model.hoominzero_nodecount = self.friendgraph.number_of_nodes()

    if nx.is_isomorphic(self.friendgraph, self.model.G):
        self.complete = True
        print("we made it! hoomin ", self.unique_id, " has discovered true friendship!")

    #TODO: visualize adjanency list in webui


def hoomin_init(self):
    self.friendgraph = nx.Graph()
    self.complete = False

hoomininit = hoomin_init
scatterfucntion = send_blockdata


#visualization / performance options
displayfriendgraph = True
graphrefreshfreq = 10


#social hoomin tuning options
socialswitchprobability = 0.01
randomswitchprobability = 0.05
friendsperhoomin = 3
