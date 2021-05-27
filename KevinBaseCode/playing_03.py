#This file is to collect data from the motor current and look at how quickly we can detect and respond to hitting something.

import pandas as pd
import numpy as np
import os
import time
import datetime 
#from datetime import timedelta
#from __future__ import print_function
import odrive
from odrive.enums import *
from odrive.utils import start_liveplotter
import time
import math
import key_input    #so we can interupt   (need to have: pip3 install pynput)


print("finding an odrive...")
my_drive = odrive.find_any()
#use the plotter to monitor the current and position
start_liveplotter(lambda: [(my_drive.axis0.motor.current_control.Iq_measured*100),my_drive.axis0.encoder.count_in_cpr])
# Calibrate motor and wait for it to finish

print("starting calibration...")
my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
while my_drive.axis0.current_state != AXIS_STATE_IDLE:
    time.sleep(0.1)

#Before doing the next bit, bring the arm up to the tube/end point
#The task is to move away from it and while logging data come back up to it and touch it
#So manually move arm up to tube/endpoint and press the s key (s for start)
keep_looping = True
with key_input.KeyPoller() as keyPoll:
    while keep_looping == True:
        print("Encoder count = ", my_drive.axis0.encoder.count_in_cpr)
        time.sleep(0.01)
        keypress = keyPoll.poll()
        if not keypress is None:
            if keypress == "s":
                keep_looping = False
                #break
                print ("Done.  Encoder count is at ", my_drive.axis0.encoder.count_in_cpr, "  and the setpoint is at ", my_drive.axis0.controller.pos_setpoint)
                my_drive.axis0.controller.pos_setpoint = my_drive.axis0.encoder.count_in_cpr
                print ("and is now reset to ", my_drive.axis0.controller.pos_setpoint)

print("Creating data output table...")





# my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
# #my_drive.axis0.controller.pos_setpoint =0
# #time.sleep(10)

# t0 = time.perf_counter()
# EndCounter = 0
# stopper = False
# while not stopper:
#     EndCounter += 1
#     if EndCounter > 1000:
#         stopper = True

#     setpoint = 10000.0 * math.sin((time.perf_counter() - t0)*0.5)
#     print("goto " + str(int(setpoint)) ) 
#     #print(time.perf_counter() - t0)
#     my_drive.axis0.controller.pos_setpoint = setpoint
#     #time.sleep(0.001) #0.01

# setpoint = my_drive.axis0.controller.pos_setpoint
# #my_drive.axis0.controller.pos_setpoint = setpoint
# EndCounter = 0
# stopper = False
# t0 = time.perf_counter()
# print(time.perf_counter() - t0)
# while EndCounter < 10001:
#     EndCounter += 1
#     #if EndCounter > 10000:
#     #    stopper = True
#     setpoint = setpoint + 1
#     print("goto " + str(int(setpoint)) ) 
#     #print(time.perf_counter() - t0)
#     my_drive.axis0.controller.pos_setpoint = setpoint
#     time.sleep(0.000001) #0.01

# print (time.perf_counter() - t0)

# time.sleep(5)
# my_drive.axis0.requested_state = AXIS_STATE_IDLE
# time.sleep(15)
exit()