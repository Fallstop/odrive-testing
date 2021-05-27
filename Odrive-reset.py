import odrive
from odrive.enums import *
from odrive.utils import  dump_errors
from fibre.protocol import ChannelBrokenException

print("finding an odrive...")
odrv0 = odrive.find_any()
dump_errors(odrv0,True)
print("starting to do settings on odrv0.axis0 ...")

try:
    odrv0.erase_configuration()
    print("Failed to reboot?")
except ChannelBrokenException:
    print("ODrive rebooted and configuration saved")

