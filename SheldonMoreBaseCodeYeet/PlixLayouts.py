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


P25 = [[200, 98, 0], [200, 175, 0], [180, 254, 0], [170, 332, 0],[150,20,0],[10,20,0],[10,20,0],[10,20,0],[10,20,0],[10,20,0],[10,20,0],[10,20,0],[10,20,0],[10,20,0],[10,20,0],[10,20,0],[10,20,0],]

print(P25[0][0])
