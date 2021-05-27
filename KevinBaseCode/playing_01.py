from __future__ import print_function

import odrive
from odrive.enums import *
from odrive.utils import start_liveplotter
import time
import math
import numpy

print("finding an odrive...")
my_drive = odrive.find_any()
#use the plotter to monitor the current and position
start_liveplotter(lambda: [(my_drive.axis0.motor.current_control.Iq_measured*100),my_drive.axis0.encoder.count_in_cpr])
# Calibrate motor and wait for it to finish
print("starting calibration...")
my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
while my_drive.axis0.current_state != AXIS_STATE_IDLE:
    time.sleep(0.1)

my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
#my_drive.axis0.controller.pos_setpoint =0
#time.sleep(10)

t0 = time.perf_counter()
EndCounter = 0
stopper = False
while not stopper:
    EndCounter += 1
    if EndCounter > 10000:
        stopper = True

    setpoint = 10000.0 * math.sin((time.perf_counter() - t0)*1)
    print("goto " + str(int(setpoint)) ) 
    print(time.perf_counter() - t0)
    my_drive.axis0.controller.pos_setpoint = setpoint
    #time.sleep(0.001) #0.01
time.sleep(10)

# my_drive.axis0.controller.pos_setpoint =0
# EndCounter = 0
# stopper = False
# while not stopper:
#     EndCounter += 1
#     if EndCounter > 10000:
#         stopper = True
#     setpoint = setpoint + 1
#     print("goto " + str(int(setpoint)) ) 
#     print(time.perf_counter() - t0)
#     my_drive.axis0.controller.pos_setpoint = setpoint
#     time.sleep(0.1) #0.01


my_drive.axis0.requested_state = AXIS_STATE_IDLE
time.sleep(10)
exit