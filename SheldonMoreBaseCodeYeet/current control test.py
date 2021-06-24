from __future__ import print_function
import tkinter
from tkinter import *
from tkinter.ttk import *
import odrive
from odrive.enums import *
import time
import math
import threading
from numpy import *

global odrv0
print("odrv0 connecting")
odrv0 = odrive.find_any(serial_number = "208037743548") #Connect ot Odrive
print("odrv0 connected")

# 208037743548 first odrive

odrv0.axis0.controller.config.control_mode = CTRL_MODE_CURRENT_CONTROL

while True:

    odrv0.axis0.controller.current_setpoint = 6
    time.sleep(3)
    odrv0.axis0.controller.current_setpoint = -6
    time.sleep(3)
