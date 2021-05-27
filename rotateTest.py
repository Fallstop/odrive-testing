import odrive
from odrive.enums import *
from odrive.utils import start_liveplotter, dump_errors
import time
import math
import numpy
import time

# Find a connected ODrive (this will block until you connect one)
print("finding an odrive...")
my_drive = odrive.find_any()
dump_errors(my_drive,True)

# Find an ODrive that is connected on the serial port /dev/ttyUSB0
#my_drive = odrive.find_any("serial:/dev/ttyUSB0")

#use the plotter to monitor the current and position
# start_liveplotter(lambda: [(my_drive.axis0.motor.current_control.Iq_measured*100),my_drive.axis0.encoder.count_in_cpr])
start_liveplotter(lambda: [(my_drive.axis0.controller.input_pos),my_drive.axis0.encoder.pos_estimate])


# Calibrate motor and wait for it to finish
print("starting calibration...")
my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
while my_drive.axis0.current_state != AXIS_STATE_IDLE:
    time.sleep(0.1)

my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
time.sleep(5)
# EXAMPLE
# Read and print the voltage property
print("Bus voltage is " + str(my_drive.vbus_voltage) + "V")



# EXAMPLE
# change a value, just assign to the property
my_drive.axis0.controller.input_pos = 0
print("Position setpoint is " + str(my_drive.axis0.encoder.pos_estimate))
time.sleep(2)
my_drive.axis0.controller.input_pos = 0.25
print("Position setpoint is " + str(my_drive.axis0.encoder.pos_estimate))
time.sleep(2)
my_drive.axis0.controller.input_pos = 0

