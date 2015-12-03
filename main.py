#!/bin/python
import random
import numpy as np

FRAME_SIZE = 5
SIMULATION_LENGTH = 500
SIMULATIONS = 100
BACKOFF_MEAN = 1.0/FRAME_SIZE

class PureNode:
    def __init__(self, name):
        self.nextTransmit = 0
        self.transmitting = False
        self.name = name
        self.history = []

    def transmit(self, t):
        if self.nextTransmit <= t:
            self.nextTransmit = t + random.randint(1,10)
            self.transmitting = random.randint(1, 10) > 5
        self.history.append(self.transmitting)
        return self.transmitting

    def backoff(self, t):
        self.nextTransmit = t + random.expovariate(BACKOFF_MEAN)




class SlottedStrictNode:
    def __init__(self, name):
        self.nextTransmit = 0
        self.transmitting = False
        self.name = name
        self.history = []

    def transmit(self, t):
        if t % FRAME_SIZE == 0:
            self.transmitting = False

        if t % FRAME_SIZE == 0 and self.nextTransmit <= t:
            self.nextTransmit = t + random.randint(1,10)
            self.transmitting = random.randint(1, 10) > 5
        self.history.append(self.transmitting)
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
            nodes.append(nodetype(chr(97+i)))
        return nodes

    def pureAloha(self, length, numNodes=4, output=False):
        nodes = self.getNodes(PureNode, numNodes)
        successfulTransmissions = 0

        for t in range(0, length):
            xmit = map(lambda n:n.transmit(t), nodes)# convert this to a foreach

            if xmit.count(True) == 1:
                successfulTransmissions = successfulTransmissions + 1
            elif xmit.count(True) > 1:
                for n in nodes:
                    n.backoff(t)

        capacity = 1.0*successfulTransmissions/length

        if output:
            print "**************** Pure ALOHA (" + str(capacity) + ") ************** "
            self.printHistory(nodes)

        return capacity

    def slottedAloha(self, length, numNodes=4, output=False):
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

        capacity = 1.0*successfulTransmissions/length

        if output:
            print "**************** Slotted ALOHA (" + str(capacity) + ") ************** "
            self.printHistory(nodes)

        return capacity

    def slottedAlohaSelfish(self, length, numNodes=4, output=False):
        nodes = self.getNodes(SlottedStrictNode, numNodes-2)
        nodes.append(PureNode("s"))
        nodes.append(PureNode("s"))

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

        capacity = 1.0*successfulTransmissions/length

        if output:
            print "**************** Slotted ALOHA With Selfish Nodes (" + str(capacity) + ") ************** "
            self.printHistory(nodes)

        return capacity

    def printHistory(self, nodes):
        time = len(nodes[0].history)
        print "t =",

        for i in range(1, time+1):
            print "%02d" % i,

        print "\n"
        for node in nodes:
            print node.name + " =",
            for h in node.history:
                print ("**" if h else "  "),
            print "\n"




sim = Simulation()

print "(Capacity numbers are computed using " + str(SIMULATIONS) + " simulations and " + str(SIMULATION_LENGTH) + " ticks)"

sim.pureAloha(40, 4, True)
print "Pure Aloha Capacity for 4 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.pureAloha, SIMULATION_LENGTH, 4))
print "Pure Aloha Capacity for 8 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.pureAloha, SIMULATION_LENGTH, 8))
print "Pure Aloha Capacity for 12 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.pureAloha, SIMULATION_LENGTH, 12))
print "Pure Aloha Capacity for 16 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.pureAloha, SIMULATION_LENGTH, 16))
print "***********************\n"

sim.slottedAloha(40, 4, True)
print "Slotted Aloha Capacity for 4 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAloha, SIMULATION_LENGTH, 4))
print "Slotted Aloha Capacity for 8 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAloha, SIMULATION_LENGTH, 8))
print "Slotted Aloha Capacity for 12 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAloha, SIMULATION_LENGTH, 12))
print "Slotted Aloha Capacity for 16 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAloha, SIMULATION_LENGTH, 16))
print "***********************\n"

sim.slottedAlohaSelfish(40, 4, True)
print "Slotted Aloha - Selfish Node Capacity for 4 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAlohaSelfish, SIMULATION_LENGTH, 4))
print "Slotted Aloha - Selfish Node Capacity for 8 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAlohaSelfish, SIMULATION_LENGTH, 8))
print "Slotted Aloha - Selfish Node Capacity for 12 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAlohaSelfish, SIMULATION_LENGTH, 12))
print "Slotted Aloha - Selfish Node Capacity for 16 Nodes: ", np.mean(sim.repeatSim(SIMULATIONS, sim.slottedAlohaSelfish, SIMULATION_LENGTH, 16))
print "***********************\n"





# OUTPUT:
# (Capacity numbers are computed using 100 simulations and 500 ticks)
# **************** Pure ALOHA (0.15) **************
# t = 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40
#
# a =                         ** ** ** ** ** ** **                      ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **
#
# b =                                  ** ** ** ** ** ** ** ** **    ** **                      ** ** ** ** ** ** ** ** ** **
#
# c = ** ** ** ** **                      ** ** ** ** ** **                      ** ** ** ** ** ** ** ** ** ** ** ** ** ** **
#
# d = ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **                            ** ** ** ** ** ** ** ** ** ** **
#
# Pure Aloha Capacity for 4 Nodes:  0.27386
# Pure Aloha Capacity for 8 Nodes:  0.03328
# Pure Aloha Capacity for 12 Nodes:  0.00348
# Pure Aloha Capacity for 16 Nodes:  0.00012
# ***********************
#
# **************** Slotted ALOHA (0.625) **************
# t = 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40
#
# a = ** ** ** ** **                                              ** ** ** ** ** ** ** ** ** ** ** ** ** ** **
#
# b =                ** ** ** ** **
#
# c = ** ** ** ** **                               ** ** ** ** **
#
# d =                                                             ** ** ** ** **                               ** ** ** ** **
#
# Slotted Aloha Capacity for 4 Nodes:  0.4095
# Slotted Aloha Capacity for 8 Nodes:  0.1825
# Slotted Aloha Capacity for 12 Nodes:  0.0571
# Slotted Aloha Capacity for 16 Nodes:  0.0179
# ***********************
#
# **************** Slotted ALOHA With Selfish Nodes (0.25) **************
# t = 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40
#
# a =                ** ** ** ** **                               ** ** ** ** **                ** ** ** ** ** ** ** ** ** **
#
# b =                               ** ** ** ** **
#
# s = ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **                            ** ** ** ** ** ** ** ** ** ** ** ** ** **
#
# s = ** ** ** ** ** ** ** ** ** ** **                                                    ** ** ** ** **
#
# Slotted Aloha - Selfish Node Capacity for 4 Nodes:  0.34124
# Slotted Aloha - Selfish Node Capacity for 8 Nodes:  0.1244
# Slotted Aloha - Selfish Node Capacity for 12 Nodes:  0.03618
# Slotted Aloha - Selfish Node Capacity for 16 Nodes:  0.01008
# ***********************
