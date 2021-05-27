from __future__ import print_function
import odrive
from odrive.enums import *
from odrive.utils import start_liveplotter
import time
import math
import numpy
import key_input    #so we can interupt   (need to have: pip3 install pynput)


#Standard startup
print("finding an odrive...")
drive = odrive.find_any()
axis0 = drive.axis0
#print(axis0)

#use the plotter to monitor the current and position
start_liveplotter(lambda: [(axis0.motor.current_control.Iq_measured*100),axis0.encoder.count_in_cpr])

# Calibrate motor and wait for it to finish
print("starting calibration...")
# axis0.encoder.is_ready = False
axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
while axis0.encoder.is_ready != True:
    #Dont do anything
    #time.sleep(0.1)
    if axis0.encoder.is_ready: 
        print("Encoder Ready")

#save that 
#axis0.motor.config.pre_calibrated = True
#axis0.save_configuration()
#print(axis0)

#Manualy move the arm till the encoder is count is Zero then press d (for done)

keep_looping = True
with key_input.KeyPoller() as keyPoller:
    while keep_looping == True:
        print("Encoder count = ", axis0.encoder.count_in_cpr)
        time.sleep(0.01)
        keypress = keyPoller.poll()
        if not keypress is None:
            if keypress == "d":
                keep_looping = False
                #break
                print ("Done.  Encoder count is now at ", axis0.encoder.count_in_cpr)
        
# while axis0.encoder.count_in_cpr != AXIS_STATE_IDLE:
#     # with keyboard.Listener(
# #         on_press=on_press,
# #         on_release=on_release) as listener:
# #     listener.join()
#     time.sleep(0.1)
# axis0.requested_state = AXIS_STATE_IDLE

# while axis0.current_state != AXIS_STATE_IDLE:
#     print()
#     time.sleep(0.01)

# do a full calibration sequence then save it.

# turn the motor by hand until encoder count is at zero. (encoder.phase should be almost zero as well, but I recall this wasn’t always the case not so sure why).

# now read the absolute encoder’s position and write it down somewhere. lets call this ‘zero_angle’.

# assuming motor has been rotated randomly and ODrive has just been reset, read the absolute encoder position. lets call this ‘current_angle’.
# offset_angle = zero_angle - current_angle

# if offset_angle < 0; offset_angle += encoder_cpr  // not strictly necessary

# write this offset: odrv0.axis0.encoder.config.offset = offset_angle
# set is_ready prop: odrv0.axis0.encoder.is_ready = True
# (is_ready might be readonly in older firmware, if so make it regular property)

# now you are ready to enter closed loop control. (I am doing step 5 using a custom CAN command added to the firmware)