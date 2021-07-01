import odrive
from odrive.enums import *
from odrive.utils import start_liveplotter, dump_errors
import time

print("connecting")
# odrv1 = odrive.find_any(serial_number = "3762364A3137") #Connect ot Odrive1
print("odrv1 connected")
odrv0 = odrive.find_any(serial_number = "208037743548") #Connect ot Odrive0
print("odrv0 connected")



# Find a connected ODrive (this will block until you connect one)
# print("finding an odrive...")
# odrv0 = odrive.find_any()
dump_errors(odrv0,False)

# Find an ODrive that is connected on the serial port /dev/ttyUSB0
#odrv0 = odrive.find_any("serial:/dev/ttyUSB0")

#use the plotter to monitor the current and position
# start_liveplotter(lambda: [(odrv0.axis0.motor.current_control.Iq_measured*100),odrv0.axis0.encoder.count_in_cpr])
# start_liveplotter(lambda: [(odrv0.axis0.controller.input_pos),odrv0.axis0.encoder.pos_estimate])


time.sleep(2)
# EXAMPLE
# Read and print the voltage property
print("Bus voltage is " + str(odrv0.vbus_voltage) + "V")



# EXAMPLE
# change a value, just assign to the property
while True:
    odrv0.axis0.controller.pos_setpoint = int(input("Input 0: "))
    odrv0.axis1.controller.pos_setpoint = int(input("Input 1: "))

# odrv0.axis0.controller.input_pos = 0
# print("Position setpoint is " + str(odrv0.axis0.encoder.pos_estimate))
# time.sleep(2)
# odrv0.axis0.controller.input_pos = 0.25
# print("Position setpoint is " + str(odrv0.axis0.encoder.pos_estimate))
# time.sleep(2)
# odrv0.axis0.controller.input_pos = 0