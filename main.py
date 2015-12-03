#!/bin/python
import random
import numpy as np
import sys

FRAME_SIZE = 5
SIMULATION_LENGTH = 500
SIMULATIONS = 100

class PureNode:
    def __init__(self, name):
        self.nextTransmit = 0
        self.transmitting = False
        self.name = name
        self.history = []
        self.probabilityXmit = 0.5

    def transmit(self, t):
        if self.nextTransmit <= t:
            self.transmitting = random.uniform(0,1) < self.probabilityXmit

            if self.transmitting:
                self.nextTransmit = t + FRAME_SIZE
            else:
                self.nextTransmit = t + 1

        self.history.append(self.transmitting)

        return self.transmitting


class SlottedNode:
    def __init__(self, name):
        self.nextTransmit = 0
        self.transmitting = False
        self.name = name
        self.history = []
        self.probabilityXmit = 0.75

    def transmit(self, t):
        if t % FRAME_SIZE == 0 and self.nextTransmit <= t:
            self.nextTransmit = t + FRAME_SIZE
            self.transmitting = random.uniform(0,1) < self.probabilityXmit

        self.history.append(self.transmitting)
        return self.transmitting


class Simulation:
    def repeatSim(self, iterations, func, *args):
        capacity = []
        for i in range(0, iterations):
            capacity.append(func(*args))
        return capacity

    def getNodes(self, nodetype, count, startChar=97):
        nodes = []
        for i in range(0, count):
            nodes.append(nodetype(chr(startChar+i)))
        return nodes

    def pureAloha(self, length, numNodes=4, output=False):
        nodes = self.getNodes(PureNode, numNodes)
        successfulTransmissions = 0

        for t in range(0, length):
            xmit = map(lambda n:n.transmit(t), nodes)# convert this to a foreach

            if xmit.count(True) == 1:
                successfulTransmissions = successfulTransmissions + 1

        capacity = 1.0*successfulTransmissions/length

        if output:
            print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Pure ALOHA (" + str(capacity) + ") ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
            self.printHistory(nodes)

        return capacity

    def slottedAloha(self, length, numNodes=4, output=False):
        nodes = self.getNodes(SlottedNode, numNodes)
        successfulTransmissions = 0

        for t in range(0, length):
            xmit = []
            for node in nodes:
                xmit.append(node.transmit(t))

            if xmit.count(True) == 1:
                successfulTransmissions = successfulTransmissions + 1

        capacity = 1.0*successfulTransmissions/length

        if output:
            print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Slotted ALOHA (" + str(capacity) + ") ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
            self.printHistory(nodes, True)

        return capacity

    def slottedAlohaSelfish(self, length, numSlottedNodes=2, numSelfishNodes=2, output=False):
        nodes = []
        nodes = nodes + self.getNodes(SlottedNode, numSlottedNodes)
        nodes = nodes + self.getNodes(PureNode, numSelfishNodes, 97+numSlottedNodes)

        successfulTransmissions = 0

        for t in range(0, length):
            xmit = []
            for node in nodes:
                xmit.append(node.transmit(t))

            if xmit.count(True) == 1:
                successfulTransmissions = successfulTransmissions + 1

        capacity = 1.0*successfulTransmissions/length

        if output:
            print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Slotted ALOHA With Selfish Nodes (" + str(capacity) + ") ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
            self.printHistory(nodes, True)

        return capacity

    def printHistory(self, nodes, slots=False):
        time = len(nodes[0].history)
        print "t = ",

        for i in range(1, time+1):
            sys.stdout.write("%02d" % i)
            if slots and i % FRAME_SIZE == 0:
                sys.stdout.write("|")
            else:
                sys.stdout.write(" ")

        sys.stdout.write("\n")
        for node in nodes:
            print node.name + " = ",
            for i, h in enumerate(node.history):
                sys.stdout.write("**" if h else "  ")
                if slots and (i+1) % FRAME_SIZE == 0:
                    sys.stdout.write("|")
                else:
                    sys.stdout.write(" ")
            sys.stdout.write("\n")




sim = Simulation()

print "(Capacity numbers are computed using " + str(SIMULATIONS) + " simulations and " + str(SIMULATION_LENGTH) + " ticks)"

sim.pureAloha(40, 2, True)
print "^" * 125
print "Pure Aloha Capacity for 2 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.pureAloha, SIMULATION_LENGTH, 2))
print "Pure Aloha Capacity for 3 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.pureAloha, SIMULATION_LENGTH, 3))
print "Pure Aloha Capacity for 4 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.pureAloha, SIMULATION_LENGTH, 4))
print "Pure Aloha Capacity for 8 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.pureAloha, SIMULATION_LENGTH, 8))
print "^" * 125 + "\n"

sim.slottedAloha(40, 2, True)
print "^" * 125
print "Slotted Aloha Capacity for 2 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAloha, SIMULATION_LENGTH, 2))
print "Slotted Aloha Capacity for 3 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAloha, SIMULATION_LENGTH, 3))
print "Slotted Aloha Capacity for 4 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAloha, SIMULATION_LENGTH, 4))
print "Slotted Aloha Capacity for 8 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAloha, SIMULATION_LENGTH, 8))
print "^" * 125 + "\n"

sim.slottedAlohaSelfish(40, 1, 1, True)
print "^" * 125
print "Slotted Aloha - Selfish Node Capacity for 2 Nodes (1/1): ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAlohaSelfish, SIMULATION_LENGTH, 1, 1))
print "Slotted Aloha - Selfish Node Capacity for 3 Nodes (2/1): ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAlohaSelfish, SIMULATION_LENGTH, 2, 1))
print "Slotted Aloha - Selfish Node Capacity for 3 Nodes (1/2): ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAlohaSelfish, SIMULATION_LENGTH, 1, 2))
print "Slotted Aloha - Selfish Node Capacity for 4 Nodes (3/1): ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAlohaSelfish, SIMULATION_LENGTH, 3, 1))
print "Slotted Aloha - Selfish Node Capacity for 4 Nodes (2/2): ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAlohaSelfish, SIMULATION_LENGTH, 2, 2))
print "Slotted Aloha - Selfish Node Capacity for 4 Nodes (1/3): ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAlohaSelfish, SIMULATION_LENGTH, 1, 3))
print "Slotted Aloha - Selfish Node Capacity for 8 Nodes (7/1): ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAlohaSelfish, SIMULATION_LENGTH, 7, 1))
print "Slotted Aloha - Selfish Node Capacity for 8 Nodes (6/2): ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAlohaSelfish, SIMULATION_LENGTH, 6, 2))
print "Slotted Aloha - Selfish Node Capacity for 8 Nodes (5/3): ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAlohaSelfish, SIMULATION_LENGTH, 5, 3))
print "Slotted Aloha - Selfish Node Capacity for 8 Nodes (4/4): ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAlohaSelfish, SIMULATION_LENGTH, 4, 4))
print "Slotted Aloha - Selfish Node Capacity for 8 Nodes (3/5): ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAlohaSelfish, SIMULATION_LENGTH, 3, 5))
print "Slotted Aloha - Selfish Node Capacity for 8 Nodes (2/6): ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAlohaSelfish, SIMULATION_LENGTH, 2, 6))
print "Slotted Aloha - Selfish Node Capacity for 8 Nodes (1/7): ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAlohaSelfish, SIMULATION_LENGTH, 1, 7))
print "^" * 125 + "\n"






# OUTPUT:
# (Capacity numbers are computed using 100 simulations and 500 ticks)
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Pure ALOHA (0.2) ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# t = 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40
# a = ** ** ** ** **       ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **             ** ** ** ** ** ** ** ** **
# b = ** ** ** ** ** ** ** ** ** **    ** ** ** ** **    ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Pure Aloha Capacity for 2 Nodes:  0.28332
# Pure Aloha Capacity for 3 Nodes:  0.0726
# Pure Aloha Capacity for 4 Nodes:  0.01528
# Pure Aloha Capacity for 8 Nodes:  0.0001
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Slotted ALOHA (0.375) ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# t = 01 02 03 04 05|06 07 08 09 10|11 12 13 14 15|16 17 18 19 20|21 22 23 24 25|26 27 28 29 30|31 32 33 34 35|36 37 38 39 40|
# a = ** ** ** ** **|              |** ** ** ** **|** ** ** ** **|              |** ** ** ** **|** ** ** ** **|** ** ** ** **|
# b = ** ** ** ** **|** ** ** ** **|              |** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Slotted Aloha Capacity for 2 Nodes:  0.375
# Slotted Aloha Capacity for 3 Nodes:  0.1454
# Slotted Aloha Capacity for 4 Nodes:  0.0453
# Slotted Aloha Capacity for 8 Nodes:  0.0004
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Slotted ALOHA With Selfish Nodes (0.225) ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# t = 01 02 03 04 05|06 07 08 09 10|11 12 13 14 15|16 17 18 19 20|21 22 23 24 25|26 27 28 29 30|31 32 33 34 35|36 37 38 39 40|
# a = ** ** ** ** **|** ** ** ** **|              |** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|              |
# b = ** ** ** ** **|   ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|**    ** ** **|** ** ** ** **|** **         |
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Slotted Aloha - Selfish Node Capacity for 2 Nodes (1/1):  0.33436
# Slotted Aloha - Selfish Node Capacity for 3 Nodes (2/1):  0.11298
# Slotted Aloha - Selfish Node Capacity for 3 Nodes (1/2):  0.08884
# Slotted Aloha - Selfish Node Capacity for 4 Nodes (3/1):  0.03674
# Slotted Aloha - Selfish Node Capacity for 4 Nodes (2/2):  0.02818
# Slotted Aloha - Selfish Node Capacity for 4 Nodes (1/3):  0.02164
# Slotted Aloha - Selfish Node Capacity for 8 Nodes (7/1):  0.00042
# Slotted Aloha - Selfish Node Capacity for 8 Nodes (6/2):  0.00016
# Slotted Aloha - Selfish Node Capacity for 8 Nodes (5/3):  0.0002
# Slotted Aloha - Selfish Node Capacity for 8 Nodes (4/4):  8e-05
# Slotted Aloha - Selfish Node Capacity for 8 Nodes (3/5):  2e-05
# Slotted Aloha - Selfish Node Capacity for 8 Nodes (2/6):  4e-05
# Slotted Aloha - Selfish Node Capacity for 8 Nodes (1/7):  2e-05
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
