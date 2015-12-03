import random
import SETTINGS

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
                self.nextTransmit = t + SETTINGS.FRAME_SIZE
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
        if t % SETTINGS.FRAME_SIZE == 0 and self.nextTransmit <= t:
            self.nextTransmit = t + SETTINGS.FRAME_SIZE
            self.transmitting = random.uniform(0,1) < self.probabilityOfXmit

        self.history.append(self.transmitting)
        return self.transmitting
