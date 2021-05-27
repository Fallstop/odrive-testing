#I used this file to test the speed at which we can communicate with and control the motor. 
#it just does a setup and then runs a move function with a one encoder count step size. How long to do a full rotation.
#The screen write slows it down (it is a blocking function) so take care not to print in the loop


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
#my_drive.axis0.controller.input_pos =0
#time.sleep(10)

t0 = time.perf_counter()
EndCounter = 0
stopper = False
while not stopper:
    EndCounter += 1
    if EndCounter > 1000:
        stopper = True

    setpoint = 10000.0 * math.sin((time.perf_counter() - t0)*0.5)
    print("goto " + str(int(setpoint)) ) 
    #print(time.perf_counter() - t0)
    my_drive.axis0.controller.input_pos = setpoint
    #time.sleep(0.001) #0.01

setpoint = my_drive.axis0.controller.input_pos
#my_drive.axis0.controller.input_pos = setpoint
EndCounter = 0
stopper = False
t0 = time.perf_counter()
print(time.perf_counter() - t0)
while EndCounter < 10001:
    EndCounter += 1
    #if EndCounter > 10000:
    #    stopper = True
    setpoint = setpoint + 1
    print("goto " + str(int(setpoint)) ) 
    #print(time.perf_counter() - t0)
    my_drive.axis0.controller.input_pos = setpoint
    time.sleep(0.000001) #0.01

print (time.perf_counter() - t0)

time.sleep(5)
my_drive.axis0.requested_state = AXIS_STATE_IDLE
time.sleep(15)
exit