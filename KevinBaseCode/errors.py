from __future__ import print_function

import odrive
from odrive.tests import *
from odrive.utils import dump_errors
from odrive.enums import *
from odrive.utils import start_liveplotter
import time



print("finding an odrive...")
odrv = odrive.find_any()
#axis = odrv.axis0
dump_errors(odrv,True)
exit