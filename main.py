#!/bin/python
import random
import numpy as np

FRAME_SIZE = 5
SIMULATION_LENGTH = 500
SIMULATIONS = 100
BACKOFF_MEAN = 1.0/FRAME_SIZE

class PureNode:
    def __init__(self):
        self.nextTransmit = 0
        self.transmitting = False

    def transmit(self, t):
        if self.nextTransmit <= t:
            self.nextTransmit = t + random.randint(1,10)
            self.transmitting = random.randint(1, 10) > 5
        return self.transmitting

    def backoff(self, t):
        self.nextTransmit = t + random.expovariate(BACKOFF_MEAN)

class SlottedStrictNode:
    def __init__(self):
        self.nextTransmit = 0
        self.transmitting = False

    def transmit(self, t):
        if t % FRAME_SIZE == 0:
            self.transmitting = False

        if t % FRAME_SIZE == 0 and self.nextTransmit <= t:
            self.nextTransmit = t + random.randint(1,10)
            self.transmitting = random.randint(1, 10) > 5
        return self.transmitting

    def backoff(self, t):
        self.nextTransmit = t + random.expovariate(BACKOFF_MEAN)

class Simulation:
    def repeatSim(self, iterations, func, *args):
        capacity = []
        for i in range(0, iterations):
            capacity.append(func(*args))
        return capacity

    def getNodes(self, nodetype, count):
        nodes = []
        for i in range(0, count):
            nodes.append(nodetype())
        return nodes

    def pureAloha(self, length, numNodes=4):
        nodes = self.getNodes(PureNode, numNodes)
        successfulTransmissions = 0

        for t in range(0, length):
            xmit = map(lambda n:n.transmit(t), nodes)

            if xmit.count(True) == 1:
                successfulTransmissions = successfulTransmissions + 1
            elif xmit.count(True) > 1:
                for n in nodes:
                    n.backoff(t)

        return 1.0*successfulTransmissions/length

    def slottedAloha(self, length, numNodes=4):
        nodes = self.getNodes(SlottedStrictNode, numNodes)
        successfulTransmissions = 0

        for t in range(0, length):
            xmit = []
            for node in nodes:
                xmit.append(node.transmit(t))

            if xmit.count(True) == 1:
                successfulTransmissions = successfulTransmissions + 1
            elif xmit.count(True) > 1 and t % FRAME_SIZE == 0:
                for n in nodes:
                    n.backoff(t)

        return 1.0*successfulTransmissions/length

    def slottedAlohaRogue(self, length, numNodes=4):
        nodes = self.getNodes(SlottedStrictNode, numNodes-2)
        nodes.append(PureNode())
        nodes.append(PureNode())

        successfulTransmissions = 0

        for t in range(0, length):
            xmit = []
            for node in nodes:
                xmit.append(node.transmit(t))

            if xmit.count(True) == 1:
                successfulTransmissions = successfulTransmissions + 1
            elif xmit.count(True) > 1 and t % FRAME_SIZE == 0:
                for n in nodes:
                    n.backoff(t)

        return 1.0*successfulTransmissions/length



sim = Simulation()

print "*********"
print "Pure Aloha Capacity for 4 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.pureAloha, SIMULATION_LENGTH, 4))
print "Pure Aloha Capacity for 8 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.pureAloha, SIMULATION_LENGTH, 8))
print "Pure Aloha Capacity for 12 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.pureAloha, SIMULATION_LENGTH, 12))
print "Pure Aloha Capacity for 16 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.pureAloha, SIMULATION_LENGTH, 16))
print "*********\n"

print "*********"
print "Slotted Aloha Capacity for 4 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAloha, SIMULATION_LENGTH, 4))
print "Slotted Aloha Capacity for 8 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAloha, SIMULATION_LENGTH, 8))
print "Slotted Aloha Capacity for 12 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAloha, SIMULATION_LENGTH, 12))
print "Slotted Aloha Capacity for 16 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAloha, SIMULATION_LENGTH, 16))
print "*********\n"

print "**** With 2 Rogue Nodes ****"
print "Slotted Aloha - Rogue Node Capacity for 4 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAlohaRogue, SIMULATION_LENGTH, 4))
print "Slotted Aloha - Rogue Node Capacity for 8 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAlohaRogue, SIMULATION_LENGTH, 8))
print "Slotted Aloha - Rogue Node Capacity for 12 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAlohaRogue, SIMULATION_LENGTH, 12))
print "Slotted Aloha - Rogue Node Capacity for 16 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAlohaRogue, SIMULATION_LENGTH, 16))
print "*********\n"


# OUTPUT:
# Kora :: ~/Source/aloha » python main.py
# *********
# Pure Aloha Capacity for 4 Nodes:  0.26538
# Pure Aloha Capacity for 8 Nodes:  0.03284
# Pure Aloha Capacity for 12 Nodes:  0.00276
# Pure Aloha Capacity for 16 Nodes:  0.00044
# *********
#
# *********
# Slotted Aloha Capacity for 4 Nodes:  0.3964
# Slotted Aloha Capacity for 8 Nodes:  0.178
# Slotted Aloha Capacity for 12 Nodes:  0.0612
# Slotted Aloha Capacity for 16 Nodes:  0.0182
# *********
#
# **** With 2 Rogue Nodes ****
# Slotted Aloha - Rogue Node Capacity for 4 Nodes:  0.33702
# Slotted Aloha - Rogue Node Capacity for 8 Nodes:  0.12078
# Slotted Aloha - Rogue Node Capacity for 12 Nodes:  0.03966
# Slotted Aloha - Rogue Node Capacity for 16 Nodes:  0.00876
# *********
