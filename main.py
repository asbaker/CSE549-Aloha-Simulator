#!/bin/python
import random
import numpy as np

class PureNode:
    def transmit(self, t):
        return random.randint(1, 10) > 5

# This node adheres to the slot
# class SlottedStrictNode:
#     def transmit(self, t, slot):
#         return True


# This node does not adhere to the slot
# class SlottedSelfishNode:
#     def transmit(self, t, slot):
#         return True



class Simulation:
    def debug(*args):
        debug = False
        if debug: print(args[1::])

    def repeatSim(self, iterations, func, *args):
        capacity = []
        for i in range(0, iterations):
            capacity.append(func(*args))
        return capacity

    def pureAloha(self, length, numNodes=4):
        nodes = [PureNode()] * numNodes

        successfulTransmissions = 0

        for t in range(0, length):
            xmit = map(lambda n:n.transmit(t), nodes)
            if xmit.count(True) == 1:
                successfulTransmissions = successfulTransmissions + 1
            self.debug("t is ", t, xmit)
            self.debug("t is", t)


        self.debug("successfulTransmissions: ", successfulTransmissions)
        self.debug("capacity: ", 1.0*successfulTransmissions/length)

        return 1.0*successfulTransmissions/length



sim = Simulation()
print "Pure Aloha Capacity for 4 Nodes: ", np.mean(sim.repeatSim(100, sim.pureAloha, 400, 4))
print "Pure Aloha Capacity for 8 Nodes: ", np.mean(sim.repeatSim(100, sim.pureAloha, 400, 8))
