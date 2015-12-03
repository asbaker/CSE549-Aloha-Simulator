#!/bin/python
import random
import numpy as np
import sys

FRAME_SIZE = 5
SIMULATION_LENGTH = 500
SIMULATIONS = 100

# OPTIMAL SIMULATION
SLOTTED_PROBABILITY = 0.75
PURE_PROBABILITY = 0.1

# SLOTTED THROUGHPUT
# SLOTTED_PROBABILITY = 0.75
# PURE_PROBABILITY = 0.75

# PURE THROUGHPUT
# SLOTTED_PROBABILITY = 0.1
# PURE_PROBABILITY = 0.1

class PureNode:
    def __init__(self, name, probabilityOfXmit):
        self.nextTransmit = 0
        self.transmitting = False
        self.name = name
        self.history = []
        self.probabilityOfXmit = probabilityOfXmit

    def transmit(self, t):
        if self.nextTransmit <= t:
            self.transmitting = random.uniform(0,1) < self.probabilityOfXmit

            if self.transmitting:
                self.nextTransmit = t + FRAME_SIZE
            else:
                self.nextTransmit = t + 1

        self.history.append(self.transmitting)

        return self.transmitting


class SlottedNode:
    def __init__(self, name, probabilityOfXmit):
        self.nextTransmit = 0
        self.transmitting = False
        self.name = name
        self.history = []
        self.probabilityOfXmit = probabilityOfXmit

    def transmit(self, t):
        if t % FRAME_SIZE == 0 and self.nextTransmit <= t:
            self.nextTransmit = t + FRAME_SIZE
            self.transmitting = random.uniform(0,1) < self.probabilityOfXmit

        self.history.append(self.transmitting)
        return self.transmitting


class Simulation:
    def repeatSim(self, iterations, func, *args):
        capacity = []
        for i in range(0, iterations):
            capacity.append(func(*args))
        return capacity

    def getNodes(self, nodetype, count, probabilityOfXmit, startChar=97):
        nodes = []
        for i in range(0, count):
            nodes.append(nodetype(chr(startChar+i), probabilityOfXmit))
        return nodes

    def __checkCollision(self, otherNodes, start, end):
        for node in otherNodes:
            for t in range(start, end):
                if node.history[t]:
                    return True
        return False

    def __getNodesSuccessfulFrames(self, nodes, node):
        successfulFrames = 0
        otherNodes = list(set(nodes) - set([node]))
        time = len(node.history)

        t = 0
        while t < time:
            if node.history[t]:
                start = t
                end = t + FRAME_SIZE
                if end < time: #packets after the end time do not count as successfull
                    collision = self.__checkCollision(otherNodes, start, end)
                    successfulFrames = successfulFrames + (0 if collision else 1)
                t = t + 5
            else:
                t = t + 1

        return successfulFrames

    def __calcCapacity(self, nodes):
        time = len(nodes[0].history)
        successfulFrames = 0
        possibleFrames = time/FRAME_SIZE*1.0

        for n in nodes:
            successfulFrames = successfulFrames + self.__getNodesSuccessfulFrames(nodes, n)

        return successfulFrames/possibleFrames

    def pureAloha(self, length, numNodes=4, output=False):
        nodes = self.getNodes(PureNode, numNodes, PURE_PROBABILITY)

        for t in range(0, length):
            xmit = []
            for node in nodes:
                xmit.append(node.transmit(t))

        capacity = self.__calcCapacity(nodes)
        if output:
            print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Pure ALOHA (" + "%0.3f" % capacity + ") ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
            self.__printHistory(nodes)

        return capacity

    def slottedAloha(self, length, numNodes=4, output=False):
        nodes = self.getNodes(SlottedNode, numNodes, SLOTTED_PROBABILITY)

        for t in range(0, length):
            xmit = []
            for node in nodes:
                xmit.append(node.transmit(t))

        capacity = self.__calcCapacity(nodes)
        if output:
            print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Slotted ALOHA (" + "%0.3f" % capacity + ") ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
            self.__printHistory(nodes, True)

        return capacity

    def slottedAlohaSelfish(self, length, numSlottedNodes=2, numSelfishNodes=2, output=False):
        nodes = []
        nodes = nodes + self.getNodes(SlottedNode, numSlottedNodes, SLOTTED_PROBABILITY)
        nodes = nodes + self.getNodes(PureNode, numSelfishNodes, SLOTTED_PROBABILITY, 97+numSlottedNodes)

        for t in range(0, length):
            xmit = []
            for node in nodes:
                xmit.append(node.transmit(t))

        capacity = self.__calcCapacity(nodes)
        if output:
            print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Slotted ALOHA With Selfish Nodes (" + "%0.3f" % capacity + ") ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
            self.__printHistory(nodes, True)

        return capacity

    def __printHistory(self, nodes, slots=False):
        time = len(nodes[0].history)
        self.__printTimeline(time, slots)
        self.__printNodelines(nodes, slots)

    def __printTimeline(self, time, slots):
        if slots:
            sys.stdout.write("t = |")
        else:
            sys.stdout.write("t =  ")

        for i in range(0, time):
            sys.stdout.write("%02d" % i)
            if slots and i % FRAME_SIZE == 0:
                sys.stdout.write("|")
            else:
                sys.stdout.write(" ")

        sys.stdout.write("\n")

    def __printNodelines(self, nodes, slots):
        for node in nodes:
            if slots:
                sys.stdout.write(node.name + " = |")
            else:
                sys.stdout.write(node.name + " =  ")

            for i, h in enumerate(node.history):
                sys.stdout.write("**" if h else "  ")
                if slots and (i+1) % FRAME_SIZE == 0:
                    sys.stdout.write("|")
                else:
                    sys.stdout.write(" ")
            sys.stdout.write("\n")




sim = Simulation()

print "Capacity numbers are computed using " + str(SIMULATIONS) + " simulations and " + str(SIMULATION_LENGTH) + " ticks with frame size of " + str(FRAME_SIZE) + " ticks"
print "Probabilities of transmit: Pure Node(" + str(PURE_PROBABILITY) + ") Slotted(" + str(SLOTTED_PROBABILITY) + ")\n"

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
# Capacity numbers are computed using 100 simulations and 500 ticks with frame size of 5 ticks
# Probabilities of transmit: Pure Node(0.1) Slotted(0.75)
#
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Pure ALOHA (0.375) ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# t =  00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39
# a =  ** ** ** ** ** ** ** ** ** **                                                                                     ** **
# b =                                ** ** ** ** **
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Pure Aloha Capacity for 2 Nodes:  0.2949
# Pure Aloha Capacity for 3 Nodes:  0.1939
# Pure Aloha Capacity for 4 Nodes:  0.1081
# Pure Aloha Capacity for 8 Nodes:  0.009
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Slotted ALOHA (0.750) ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# t = |00|01 02 03 04 05|06 07 08 09 10|11 12 13 14 15|16 17 18 19 20|21 22 23 24 25|26 27 28 29 30|31 32 33 34 35|36 37 38 39
# a = |              |** ** ** ** **|              |** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|
# b = |** ** ** ** **|              |** ** ** ** **|              |** ** ** ** **|              |              |** ** ** ** **|
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Slotted Aloha Capacity for 2 Nodes:  0.37
# Slotted Aloha Capacity for 3 Nodes:  0.1412
# Slotted Aloha Capacity for 4 Nodes:  0.0479
# Slotted Aloha Capacity for 8 Nodes:  0.0006
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Slotted ALOHA With Selfish Nodes (0.000) ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# t = |00|01 02 03 04 05|06 07 08 09 10|11 12 13 14 15|16 17 18 19 20|21 22 23 24 25|26 27 28 29 30|31 32 33 34 35|36 37 38 39
# a = |** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|              |** ** ** ** **|
# b = |** ** ** ** **|   ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Slotted Aloha - Selfish Node Capacity for 2 Nodes (1/1):  0.0966
# Slotted Aloha - Selfish Node Capacity for 3 Nodes (2/1):  0.0186
# Slotted Aloha - Selfish Node Capacity for 3 Nodes (1/2):  0.0001
# Slotted Aloha - Selfish Node Capacity for 4 Nodes (3/1):  0.0028
# Slotted Aloha - Selfish Node Capacity for 4 Nodes (2/2):  0.0
# Slotted Aloha - Selfish Node Capacity for 4 Nodes (1/3):  0.0
# Slotted Aloha - Selfish Node Capacity for 8 Nodes (7/1):  0.0
# Slotted Aloha - Selfish Node Capacity for 8 Nodes (6/2):  0.0
# Slotted Aloha - Selfish Node Capacity for 8 Nodes (5/3):  0.0
# Slotted Aloha - Selfish Node Capacity for 8 Nodes (4/4):  0.0
# Slotted Aloha - Selfish Node Capacity for 8 Nodes (3/5):  0.0
# Slotted Aloha - Selfish Node Capacity for 8 Nodes (2/6):  0.0
# Slotted Aloha - Selfish Node Capacity for 8 Nodes (1/7):  0.0
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


# Capacity numbers are computed using 100 simulations and 500 ticks with frame size of 5 ticks
# Probabilities of transmit: Pure Node(0.75) Slotted(0.75)
#
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Pure ALOHA (0.000) ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# t =  00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39
# a =     ** ** ** ** **    ** ** ** ** **       ** ** ** ** ** ** ** ** ** ** ** ** ** ** **    ** ** ** ** **    ** ** ** **
# b =  ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **    ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Pure Aloha Capacity for 2 Nodes:  0.0004
# Pure Aloha Capacity for 3 Nodes:  0.0
# Pure Aloha Capacity for 4 Nodes:  0.0
# Pure Aloha Capacity for 8 Nodes:  0.0
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Slotted ALOHA (0.000) ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# t = |00|01 02 03 04 05|06 07 08 09 10|11 12 13 14 15|16 17 18 19 20|21 22 23 24 25|26 27 28 29 30|31 32 33 34 35|36 37 38 39
# a = |              |** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|              |
# b = |              |** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Slotted Aloha Capacity for 2 Nodes:  0.3641
# Slotted Aloha Capacity for 3 Nodes:  0.1438
# Slotted Aloha Capacity for 4 Nodes:  0.0497
# Slotted Aloha Capacity for 8 Nodes:  0.0004
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Slotted ALOHA With Selfish Nodes (0.375) ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# t = |00|01 02 03 04 05|06 07 08 09 10|11 12 13 14 15|16 17 18 19 20|21 22 23 24 25|26 27 28 29 30|31 32 33 34 35|36 37 38 39
# a = |** ** ** ** **|** ** ** ** **|              |              |** ** ** ** **|              |** ** ** ** **|** ** ** ** **|
# b = |** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|   ** ** ** **|**    ** ** **|
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Slotted Aloha - Selfish Node Capacity for 2 Nodes (1/1):  0.0938
# Slotted Aloha - Selfish Node Capacity for 3 Nodes (2/1):  0.0173
# Slotted Aloha - Selfish Node Capacity for 3 Nodes (1/2):  0.0
# Slotted Aloha - Selfish Node Capacity for 4 Nodes (3/1):  0.0032
# Slotted Aloha - Selfish Node Capacity for 4 Nodes (2/2):  0.0
# Slotted Aloha - Selfish Node Capacity for 4 Nodes (1/3):  0.0
# Slotted Aloha - Selfish Node Capacity for 8 Nodes (7/1):  0.0
# Slotted Aloha - Selfish Node Capacity for 8 Nodes (6/2):  0.0
# Slotted Aloha - Selfish Node Capacity for 8 Nodes (5/3):  0.0
# Slotted Aloha - Selfish Node Capacity for 8 Nodes (4/4):  0.0
# Slotted Aloha - Selfish Node Capacity for 8 Nodes (3/5):  0.0
# Slotted Aloha - Selfish Node Capacity for 8 Nodes (2/6):  0.0
# Slotted Aloha - Selfish Node Capacity for 8 Nodes (1/7):  0.0
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



# Capacity numbers are computed using 100 simulations and 500 ticks with frame size of 5 ticks
# Probabilities of transmit: Pure Node(0.1) Slotted(0.1)
#
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Pure ALOHA (0.375) ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# t =  00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39
# a =                                   ** ** ** ** **    ** ** ** ** **                                  ** ** ** ** ** ** **
# b =     ** ** ** ** **                               ** ** ** ** **          ** ** ** ** **          ** ** ** ** **       **
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Pure Aloha Capacity for 2 Nodes:  0.2964
# Pure Aloha Capacity for 3 Nodes:  0.1978
# Pure Aloha Capacity for 4 Nodes:  0.1097
# Pure Aloha Capacity for 8 Nodes:  0.0067
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Slotted ALOHA (0.250) ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# t = |00|01 02 03 04 05|06 07 08 09 10|11 12 13 14 15|16 17 18 19 20|21 22 23 24 25|26 27 28 29 30|31 32 33 34 35|36 37 38 39
# a = |              |              |** ** ** ** **|              |              |              |              |              |
# b = |              |              |              |** ** ** ** **|              |              |              |              |
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Slotted Aloha Capacity for 2 Nodes:  0.1832
# Slotted Aloha Capacity for 3 Nodes:  0.2359
# Slotted Aloha Capacity for 4 Nodes:  0.2895
# Slotted Aloha Capacity for 8 Nodes:  0.3729
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Slotted ALOHA With Selfish Nodes (0.375) ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# t = |00|01 02 03 04 05|06 07 08 09 10|11 12 13 14 15|16 17 18 19 20|21 22 23 24 25|26 27 28 29 30|31 32 33 34 35|36 37 38 39
# a = |              |              |              |** ** ** ** **|              |              |              |              |
# b = |              |   ** ** ** **|**            |              |              |** ** ** ** **|              |              |
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Slotted Aloha - Selfish Node Capacity for 2 Nodes (1/1):  0.3339
# Slotted Aloha - Selfish Node Capacity for 3 Nodes (2/1):  0.3195
# Slotted Aloha - Selfish Node Capacity for 3 Nodes (1/2):  0.2696
# Slotted Aloha - Selfish Node Capacity for 4 Nodes (3/1):  0.3062
# Slotted Aloha - Selfish Node Capacity for 4 Nodes (2/2):  0.2326
# Slotted Aloha - Selfish Node Capacity for 4 Nodes (1/3):  0.1639
# Slotted Aloha - Selfish Node Capacity for 8 Nodes (7/1):  0.2543
# Slotted Aloha - Selfish Node Capacity for 8 Nodes (6/2):  0.1646
# Slotted Aloha - Selfish Node Capacity for 8 Nodes (5/3):  0.097
# Slotted Aloha - Selfish Node Capacity for 8 Nodes (4/4):  0.0609
# Slotted Aloha - Selfish Node Capacity for 8 Nodes (3/5):  0.0369
# Slotted Aloha - Selfish Node Capacity for 8 Nodes (2/6):  0.02
# Slotted Aloha - Selfish Node Capacity for 8 Nodes (1/7):  0.0125
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
