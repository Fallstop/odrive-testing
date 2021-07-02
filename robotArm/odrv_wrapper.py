from typing import Dict
import odrive
from odrive.enums import *
from odrive.utils import dump_errors
from typing import Union,Any

import sys

class Odrive_Arm:
    odrv_X = None
    odrv_YZ = None
    axes: Union[Any,Dict[str,Any]] = None

    # Generates and Odrive Arm Object, that automatically connects to the odrive
    def __init__(self):
        self.connect_to_odrive()

    def connect_to_odrive(self):

        print("finding YZ odrive...")
        self.odrv_YZ = odrive.find_any(serial_number="208037743548")

        assert self.odrv_YZ != None
        assert not isinstance(self.odrv_YZ,list)
        

        print("finding X odrive...")
        self.odrv_X = odrive.find_any(serial_number="3762364A3137")

        assert self.odrv_X != None
        assert not isinstance(self.odrv_X,list)

        self.axes = {
            "X": self.odrv_X.axis0,
            "Y": self.odrv_YZ.axis1,
            "Z": self.odrv_YZ.axis0
        }
        print("Odrives are connected, dumping previous errors")
        print("YZ Odrive Errors:")
        dump_errors(self.odrv_YZ, True)
        print("X Odrive Errors:")
        dump_errors(self.odrv_X, True)
        print("\n\n")
        
    
    def check_connected(self):
        assert self.odrv_X != None
        assert not isinstance(self.odrv_X,list)

        assert self.odrv_YZ != None
        assert not isinstance(self.odrv_YZ,list)

        assert self.axes != None

    def check_errors(self):
        self.check_connected()
        for axis in self.axes.values():
            if axis.error != 0:
                print("ERROR:")
                dump_errors(self.odrv_YZ, True)
                dump_errors(self.odrv_X, True)

                print("Quiting due to error...")
                sys.exit()

    def move_axis(self, axis_id: str, location: float):
        self.check_errors()
        assert axis_id in self.axes
        self.axes[axis_id].controller.input_pos = 0
