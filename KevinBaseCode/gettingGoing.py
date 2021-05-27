#!/usr/bin/env python3
from __future__ import print_function

import odrive
from odrive.enums import *
from odrive.utils import start_liveplotter
import time
import math
import numpy

# Find a connected ODrive (this will block until you connect one)
print("finding an odrive...")
my_drive = odrive.find_any()

# Find an ODrive that is connected on the serial port /dev/ttyUSB0
#my_drive = odrive.find_any("serial:/dev/ttyUSB0")

#use the plotter to monitor the current and position
start_liveplotter(lambda: [(my_drive.axis0.motor.current_control.Iq_measured*100),my_drive.axis0.encoder.count_in_cpr])

# Calibrate motor and wait for it to finish
print("starting calibration...")
my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
while my_drive.axis0.current_state != AXIS_STATE_IDLE:
    time.sleep(0.1)

my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

# EXAMPLE
# Read and print the voltage property
print("Bus voltage is " + str(my_drive.vbus_voltage) + "V")

# EXAMPLE
# change a value, just assign to the property
my_drive.axis0.controller.input_pos = 3.14
print("Position setpoint is " + str(my_drive.axis0.controller.input_pos))

# And this is how function calls are done:
for i in [1,2,3,4]:
    print('voltage on GPIO{} is {} Volt'.format(i, my_drive.get_adc_voltage(i)))

# A sine wave to test
#t0 = time.monotonic()
t0 = time.perf_counter()
EndCounter = 0
stopper = False
while not stopper:
    EndCounter += 1
    if EndCounter > 5000:
        stopper = True

    setpoint = 10000.0 * math.sin((time.perf_counter() - t0)*3)
    print("goto " + str(int(setpoint)) ) 
    print(time.perf_counter() - t0)
    my_drive.axis0.controller.input_pos = setpoint
    #time.sleep(0.001) #0.01
    
my_drive.axis0.requested_state = AXIS_STATE_IDLE
#time.sleep(10.0)
exit
