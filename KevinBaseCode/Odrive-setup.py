#!/usr/bin/env python3
from __future__ import print_function

import odrive
from odrive.enums import *
from odrive.utils import  dump_errors

# Find a connected ODrive (this will block until you connect one)
print("finding an odrive...")
odrv0 = odrive.find_any()
dump_errors(odrv0,True)
print("starting to do settings on odrv0.axis0 ...")

#motor limits
odrv0.axis0.controller.config.vel_gain = 0.0019
odrv0.axis0.controller.config.vel_integrator_gain = 0.0799
odrv0.axis0.controller.config.pos_gain= 20
#current limit
odrv0.axis0.motor.config.current_lim =20
#motor type
odrv0.axis0.motor.config.motor_type = MOTOR_TYPE_HIGH_CURRENT
odrv0.axis0.motor.config.pole_pairs = 20
#velocity limit
odrv0.axis0.controller.config.vel_limit = 1000000
#encoder  (normal encoder set to high res is 2048 x4 = 8192)
odrv0.axis0.encoder.config.cpr = 8192
#Brake resistance 
odrv0.config.brake_resistance=  0.469

#save and restart
odrv0.save_configuration() 
odrv0.reboot()
exit

