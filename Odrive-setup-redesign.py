import odrive
from odrive.enums import *
from odrive.utils import  dump_errors
from fibre.protocol import ChannelBrokenException

print("finding an odrive...")
odrv0 = odrive.find_any()
dump_errors(odrv0,True)
print("starting to do settings on odrv0.axis0 ...")

#motor type
odrv0.axis0.motor.config.motor_type = MOTOR_TYPE_HIGH_CURRENT
odrv0.axis0.motor.config.pole_pairs = 20

#current limit
odrv0.axis0.motor.config.current_lim = 10
odrv0.axis0.motor.config.calibration_current = 10

odrv0.axis0.controller.config.vel_limit = 3
odrv0.axis0.controller.config.vel_limit_tolerance = 3
odrv0.config.brake_resistance = 50


odrv0.axis0.controller.config.vel_gain = 0.2
odrv0.axis0.controller.config.pos_gain = 35



#encoder  (normal encoder set to high res is 2048 x4 = 8192)
odrv0.axis0.encoder.config.cpr = 8192

print ("Saving and rebooting")
#save and restart
odrv0.save_configuration()
try:
    odrv0.reboot()
    print("Failed to reboot?")
except ChannelBrokenException:
    print("ODrive rebooted and configuration saved")
exit