#!/bin/python
import numpy as np

from nodes import PureNode
from nodes import SlottedNode
from simulation import Simulation

import SETTINGS
SETTINGS.init()
sim = Simulation()

print "Throughput numbers are computed using " + str(SETTINGS.SIMULATIONS) + " simulations and " + str(SETTINGS.SIMULATION_LENGTH) + " ticks with frame size of " + str(SETTINGS.FRAME_SIZE) + " ticks"
print "Probabilities of transmit: Pure Node(" + str(SETTINGS.PURE_PROBABILITY) + ") Slotted(" + str(SETTINGS.SLOTTED_PROBABILITY) + ")\n"

sim.pureAloha(40, 2, True)
print "^" * 125
print "Pure Aloha Throughput for 2 Nodes: ", np.mean(sim.repeatSim(SETTINGS.SIMULATIONS, sim.pureAloha, SETTINGS.SIMULATION_LENGTH, 2))
print "Pure Aloha Throughput for 3 Nodes: ", np.mean(sim.repeatSim(SETTINGS.SIMULATIONS, sim.pureAloha, SETTINGS.SIMULATION_LENGTH, 3))
print "Pure Aloha Throughput for 4 Nodes: ", np.mean(sim.repeatSim(SETTINGS.SIMULATIONS, sim.pureAloha, SETTINGS.SIMULATION_LENGTH, 4))
print "Pure Aloha Throughput for 8 Nodes: ", np.mean(sim.repeatSim(SETTINGS.SIMULATIONS, sim.pureAloha, SETTINGS.SIMULATION_LENGTH, 8))
print "^" * 125 + "\n"

sim.slottedAloha(40, 2, True)
print "^" * 125
print "Slotted Aloha Throughput for 2 Nodes: ", np.mean(sim.repeatSim(SETTINGS.SIMULATIONS, sim.slottedAloha, SETTINGS.SIMULATION_LENGTH, 2))
print "Slotted Aloha Throughput for 3 Nodes: ", np.mean(sim.repeatSim(SETTINGS.SIMULATIONS, sim.slottedAloha, SETTINGS.SIMULATION_LENGTH, 3))
print "Slotted Aloha Throughput for 4 Nodes: ", np.mean(sim.repeatSim(SETTINGS.SIMULATIONS, sim.slottedAloha, SETTINGS.SIMULATION_LENGTH, 4))
print "Slotted Aloha Throughput for 8 Nodes: ", np.mean(sim.repeatSim(SETTINGS.SIMULATIONS, sim.slottedAloha, SETTINGS.SIMULATION_LENGTH, 8))
print "^" * 125 + "\n"

sim.slottedAlohaSelfish(40, 1, 1, True)
print "^" * 125
print "Slotted Aloha - Selfish Node Throughput for 2 Nodes (1/1): ", np.mean(sim.repeatSim(SETTINGS.SIMULATIONS, sim.slottedAlohaSelfish, SETTINGS.SIMULATION_LENGTH, 1, 1))
print "Slotted Aloha - Selfish Node Throughput for 3 Nodes (2/1): ", np.mean(sim.repeatSim(SETTINGS.SIMULATIONS, sim.slottedAlohaSelfish, SETTINGS.SIMULATION_LENGTH, 2, 1))
print "Slotted Aloha - Selfish Node Throughput for 3 Nodes (1/2): ", np.mean(sim.repeatSim(SETTINGS.SIMULATIONS, sim.slottedAlohaSelfish, SETTINGS.SIMULATION_LENGTH, 1, 2))
print "Slotted Aloha - Selfish Node Throughput for 4 Nodes (3/1): ", np.mean(sim.repeatSim(SETTINGS.SIMULATIONS, sim.slottedAlohaSelfish, SETTINGS.SIMULATION_LENGTH, 3, 1))
print "Slotted Aloha - Selfish Node Throughput for 4 Nodes (2/2): ", np.mean(sim.repeatSim(SETTINGS.SIMULATIONS, sim.slottedAlohaSelfish, SETTINGS.SIMULATION_LENGTH, 2, 2))
print "Slotted Aloha - Selfish Node Throughput for 4 Nodes (1/3): ", np.mean(sim.repeatSim(SETTINGS.SIMULATIONS, sim.slottedAlohaSelfish, SETTINGS.SIMULATION_LENGTH, 1, 3))
print "Slotted Aloha - Selfish Node Throughput for 8 Nodes (7/1): ", np.mean(sim.repeatSim(SETTINGS.SIMULATIONS, sim.slottedAlohaSelfish, SETTINGS.SIMULATION_LENGTH, 7, 1))
print "Slotted Aloha - Selfish Node Throughput for 8 Nodes (6/2): ", np.mean(sim.repeatSim(SETTINGS.SIMULATIONS, sim.slottedAlohaSelfish, SETTINGS.SIMULATION_LENGTH, 6, 2))
print "Slotted Aloha - Selfish Node Throughput for 8 Nodes (5/3): ", np.mean(sim.repeatSim(SETTINGS.SIMULATIONS, sim.slottedAlohaSelfish, SETTINGS.SIMULATION_LENGTH, 5, 3))
print "Slotted Aloha - Selfish Node Throughput for 8 Nodes (4/4): ", np.mean(sim.repeatSim(SETTINGS.SIMULATIONS, sim.slottedAlohaSelfish, SETTINGS.SIMULATION_LENGTH, 4, 4))
print "Slotted Aloha - Selfish Node Throughput for 8 Nodes (3/5): ", np.mean(sim.repeatSim(SETTINGS.SIMULATIONS, sim.slottedAlohaSelfish, SETTINGS.SIMULATION_LENGTH, 3, 5))
print "Slotted Aloha - Selfish Node Throughput for 8 Nodes (2/6): ", np.mean(sim.repeatSim(SETTINGS.SIMULATIONS, sim.slottedAlohaSelfish, SETTINGS.SIMULATION_LENGTH, 2, 6))
print "Slotted Aloha - Selfish Node Throughput for 8 Nodes (1/7): ", np.mean(sim.repeatSim(SETTINGS.SIMULATIONS, sim.slottedAlohaSelfish, SETTINGS.SIMULATION_LENGTH, 1, 7))
print "^" * 125 + "\n"




# Find below the output from various runs
# The different probabilities greatly effect what the channel throughput is

# Throughput numbers are computed using 100 simulations and 500 ticks with frame size of 5 ticks
# Probabilities of transmit: Pure Node(0.1) Slotted(0.75)
#
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Pure ALOHA (0.375) ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# t =  00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39
# a =  ** ** ** ** ** ** ** ** ** **                                                                                     ** **
# b =                                ** ** ** ** **
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Pure Aloha Throughput for 2 Nodes:  0.2949
# Pure Aloha Throughput for 3 Nodes:  0.1939
# Pure Aloha Throughput for 4 Nodes:  0.1081
# Pure Aloha Throughput for 8 Nodes:  0.009
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Slotted ALOHA (0.750) ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# t = |00|01 02 03 04 05|06 07 08 09 10|11 12 13 14 15|16 17 18 19 20|21 22 23 24 25|26 27 28 29 30|31 32 33 34 35|36 37 38 39
# a = |              |** ** ** ** **|              |** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|
# b = |** ** ** ** **|              |** ** ** ** **|              |** ** ** ** **|              |              |** ** ** ** **|
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Slotted Aloha Throughput for 2 Nodes:  0.37
# Slotted Aloha Throughput for 3 Nodes:  0.1412
# Slotted Aloha Throughput for 4 Nodes:  0.0479
# Slotted Aloha Throughput for 8 Nodes:  0.0006
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Slotted ALOHA With Selfish Nodes (0.000) ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# t = |00|01 02 03 04 05|06 07 08 09 10|11 12 13 14 15|16 17 18 19 20|21 22 23 24 25|26 27 28 29 30|31 32 33 34 35|36 37 38 39
# a = |** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|              |** ** ** ** **|
# b = |** ** ** ** **|   ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Slotted Aloha - Selfish Node Throughput for 2 Nodes (1/1):  0.0966
# Slotted Aloha - Selfish Node Throughput for 3 Nodes (2/1):  0.0186
# Slotted Aloha - Selfish Node Throughput for 3 Nodes (1/2):  0.0001
# Slotted Aloha - Selfish Node Throughput for 4 Nodes (3/1):  0.0028
# Slotted Aloha - Selfish Node Throughput for 4 Nodes (2/2):  0.0
# Slotted Aloha - Selfish Node Throughput for 4 Nodes (1/3):  0.0
# Slotted Aloha - Selfish Node Throughput for 8 Nodes (7/1):  0.0
# Slotted Aloha - Selfish Node Throughput for 8 Nodes (6/2):  0.0
# Slotted Aloha - Selfish Node Throughput for 8 Nodes (5/3):  0.0
# Slotted Aloha - Selfish Node Throughput for 8 Nodes (4/4):  0.0
# Slotted Aloha - Selfish Node Throughput for 8 Nodes (3/5):  0.0
# Slotted Aloha - Selfish Node Throughput for 8 Nodes (2/6):  0.0
# Slotted Aloha - Selfish Node Throughput for 8 Nodes (1/7):  0.0
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


# Throughput numbers are computed using 100 simulations and 500 ticks with frame size of 5 ticks
# Probabilities of transmit: Pure Node(0.75) Slotted(0.75)
#
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Pure ALOHA (0.000) ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# t =  00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39
# a =     ** ** ** ** **    ** ** ** ** **       ** ** ** ** ** ** ** ** ** ** ** ** ** ** **    ** ** ** ** **    ** ** ** **
# b =  ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **    ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** **
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Pure Aloha Throughput for 2 Nodes:  0.0004
# Pure Aloha Throughput for 3 Nodes:  0.0
# Pure Aloha Throughput for 4 Nodes:  0.0
# Pure Aloha Throughput for 8 Nodes:  0.0
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Slotted ALOHA (0.000) ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# t = |00|01 02 03 04 05|06 07 08 09 10|11 12 13 14 15|16 17 18 19 20|21 22 23 24 25|26 27 28 29 30|31 32 33 34 35|36 37 38 39
# a = |              |** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|              |
# b = |              |** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Slotted Aloha Throughput for 2 Nodes:  0.3641
# Slotted Aloha Throughput for 3 Nodes:  0.1438
# Slotted Aloha Throughput for 4 Nodes:  0.0497
# Slotted Aloha Throughput for 8 Nodes:  0.0004
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Slotted ALOHA With Selfish Nodes (0.375) ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# t = |00|01 02 03 04 05|06 07 08 09 10|11 12 13 14 15|16 17 18 19 20|21 22 23 24 25|26 27 28 29 30|31 32 33 34 35|36 37 38 39
# a = |** ** ** ** **|** ** ** ** **|              |              |** ** ** ** **|              |** ** ** ** **|** ** ** ** **|
# b = |** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|** ** ** ** **|   ** ** ** **|**    ** ** **|
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Slotted Aloha - Selfish Node Throughput for 2 Nodes (1/1):  0.0938
# Slotted Aloha - Selfish Node Throughput for 3 Nodes (2/1):  0.0173
# Slotted Aloha - Selfish Node Throughput for 3 Nodes (1/2):  0.0
# Slotted Aloha - Selfish Node Throughput for 4 Nodes (3/1):  0.0032
# Slotted Aloha - Selfish Node Throughput for 4 Nodes (2/2):  0.0
# Slotted Aloha - Selfish Node Throughput for 4 Nodes (1/3):  0.0
# Slotted Aloha - Selfish Node Throughput for 8 Nodes (7/1):  0.0
# Slotted Aloha - Selfish Node Throughput for 8 Nodes (6/2):  0.0
# Slotted Aloha - Selfish Node Throughput for 8 Nodes (5/3):  0.0
# Slotted Aloha - Selfish Node Throughput for 8 Nodes (4/4):  0.0
# Slotted Aloha - Selfish Node Throughput for 8 Nodes (3/5):  0.0
# Slotted Aloha - Selfish Node Throughput for 8 Nodes (2/6):  0.0
# Slotted Aloha - Selfish Node Throughput for 8 Nodes (1/7):  0.0
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



# Throughput numbers are computed using 100 simulations and 500 ticks with frame size of 5 ticks
# Probabilities of transmit: Pure Node(0.1) Slotted(0.1)
#
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Pure ALOHA (0.375) ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# t =  00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39
# a =                                   ** ** ** ** **    ** ** ** ** **                                  ** ** ** ** ** ** **
# b =     ** ** ** ** **                               ** ** ** ** **          ** ** ** ** **          ** ** ** ** **       **
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Pure Aloha Throughput for 2 Nodes:  0.2964
# Pure Aloha Throughput for 3 Nodes:  0.1978
# Pure Aloha Throughput for 4 Nodes:  0.1097
# Pure Aloha Throughput for 8 Nodes:  0.0067
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Slotted ALOHA (0.250) ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# t = |00|01 02 03 04 05|06 07 08 09 10|11 12 13 14 15|16 17 18 19 20|21 22 23 24 25|26 27 28 29 30|31 32 33 34 35|36 37 38 39
# a = |              |              |** ** ** ** **|              |              |              |              |              |
# b = |              |              |              |** ** ** ** **|              |              |              |              |
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Slotted Aloha Throughput for 2 Nodes:  0.1832
# Slotted Aloha Throughput for 3 Nodes:  0.2359
# Slotted Aloha Throughput for 4 Nodes:  0.2895
# Slotted Aloha Throughput for 8 Nodes:  0.3729
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Slotted ALOHA With Selfish Nodes (0.375) ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# t = |00|01 02 03 04 05|06 07 08 09 10|11 12 13 14 15|16 17 18 19 20|21 22 23 24 25|26 27 28 29 30|31 32 33 34 35|36 37 38 39
# a = |              |              |              |** ** ** ** **|              |              |              |              |
# b = |              |   ** ** ** **|**            |              |              |** ** ** ** **|              |              |
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Slotted Aloha - Selfish Node Throughput for 2 Nodes (1/1):  0.3339
# Slotted Aloha - Selfish Node Throughput for 3 Nodes (2/1):  0.3195
# Slotted Aloha - Selfish Node Throughput for 3 Nodes (1/2):  0.2696
# Slotted Aloha - Selfish Node Throughput for 4 Nodes (3/1):  0.3062
# Slotted Aloha - Selfish Node Throughput for 4 Nodes (2/2):  0.2326
# Slotted Aloha - Selfish Node Throughput for 4 Nodes (1/3):  0.1639
# Slotted Aloha - Selfish Node Throughput for 8 Nodes (7/1):  0.2543
# Slotted Aloha - Selfish Node Throughput for 8 Nodes (6/2):  0.1646
# Slotted Aloha - Selfish Node Throughput for 8 Nodes (5/3):  0.097
# Slotted Aloha - Selfish Node Throughput for 8 Nodes (4/4):  0.0609
# Slotted Aloha - Selfish Node Throughput for 8 Nodes (3/5):  0.0369
# Slotted Aloha - Selfish Node Throughput for 8 Nodes (2/6):  0.02
# Slotted Aloha - Selfish Node Throughput for 8 Nodes (1/7):  0.0125
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
