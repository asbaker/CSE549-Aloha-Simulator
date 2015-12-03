import sys
import SETTINGS
from nodes import PureNode
from nodes import SlottedNode

class Simulation:
    def repeatSim(self, iterations, func, *args):
        throughput = []
        for i in range(0, iterations):
            throughput.append(func(*args))
        return throughput

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
                end = t + SETTINGS.FRAME_SIZE
                if end < time: #packets after the end time do not count as successfull
                    collision = self.__checkCollision(otherNodes, start, end)
                    successfulFrames = successfulFrames + (0 if collision else 1)
                t = t + 5
            else:
                t = t + 1

        return successfulFrames

    def __calcThroughput(self, nodes):
        time = len(nodes[0].history)
        successfulFrames = 0
        possibleFrames = time/SETTINGS.FRAME_SIZE*1.0

        for n in nodes:
            successfulFrames = successfulFrames + self.__getNodesSuccessfulFrames(nodes, n)

        return successfulFrames/possibleFrames

    def pureAloha(self, length, numNodes=4, output=False):
        nodes = self.getNodes(PureNode, numNodes, SETTINGS.PURE_PROBABILITY)

        for t in range(0, length):
            xmit = []
            for node in nodes:
                xmit.append(node.transmit(t))

        throughput = self.__calcThroughput(nodes)
        if output:
            print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Pure ALOHA (" + "%0.3f" % throughput + ") ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
            self.__printHistory(nodes)

        return throughput

    def slottedAloha(self, length, numNodes=4, output=False):
        nodes = self.getNodes(SlottedNode, numNodes, SETTINGS.SLOTTED_PROBABILITY)

        for t in range(0, length):
            xmit = []
            for node in nodes:
                xmit.append(node.transmit(t))

        throughput = self.__calcThroughput(nodes)
        if output:
            print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Slotted ALOHA (" + "%0.3f" % throughput + ") ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
            self.__printHistory(nodes, True)

        return throughput

    def slottedAlohaSelfish(self, length, numSlottedNodes=2, numSelfishNodes=2, output=False):
        nodes = []
        nodes = nodes + self.getNodes(SlottedNode, numSlottedNodes, SETTINGS.SLOTTED_PROBABILITY)
        nodes = nodes + self.getNodes(PureNode, numSelfishNodes, SETTINGS.SLOTTED_PROBABILITY, 97+numSlottedNodes)

        for t in range(0, length):
            xmit = []
            for node in nodes:
                xmit.append(node.transmit(t))

        throughput = self.__calcThroughput(nodes)
        if output:
            print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Slotted ALOHA With Selfish Nodes (" + "%0.3f" % throughput + ") ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"
            self.__printHistory(nodes, True)

        return throughput

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
            if slots and i % SETTINGS.FRAME_SIZE == 0:
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
                if slots and (i+1) % SETTINGS.FRAME_SIZE == 0:
                    sys.stdout.write("|")
                else:
                    sys.stdout.write(" ")
            sys.stdout.write("\n")

