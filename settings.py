## tunable settings for model

exampleval = "blob"

#grid options
height = 50
width = 50

#hoomin generation tuning options
initial_hoomins = 10

# road generation tuning
straightweight = 0.9
leftweight = 0.05
rightweight = 0.05
initial_roads = 80
initial_road_seeds = 4
gridspacing = 7

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
    self.model.total_scattermessages += counter


def hoomin_init(self):
    True

hoomininit = hoomin_init
scatterfucntion = send_blockdata
