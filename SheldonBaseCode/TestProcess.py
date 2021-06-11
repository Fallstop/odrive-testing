
from __future__ import print_function
from tkinter import *
from tkinter.ttk import *
import odrive
from odrive.enums import *
import time
import math


window = Tk()
window.title("AndreisOdriveTestingWidget")
window.geometry('700x200')

lbl = Label(window, text="Waiting To connect To Odrive")
lbl.grid(column=0, row=0)

posOne = Entry(window,width=10)
posTwo = Entry(window,width=10)

CntrlVal = Label(window,text="ControlerValues P V I")
CntrlVal.grid(column = 0, row = 5)

kpBox =Entry(window,width=10)
kvBox =Entry(window,width=10)
kiBox =Entry(window,width=10)

kpBox.grid(column = 1, row = 5)
kvBox.grid(column = 2, row = 5)
kiBox.grid(column = 3, row = 5)

kpCurrent = Label(window,text = "wfc")
kvCurrent = Label(window,text = "wfc")
kiCurrent = Label(window,text = "wfc")

kpCurrent.grid(column = 1, row = 6)
kvCurrent.grid(column = 2, row = 6)
kiCurrent.grid(column = 3, row = 6)

posOne.grid(column =1,row =3)
posTwo.grid(column =3,row =3)

CurrentState = Label(window, text = "State waitingforconnect")
CurrentState.grid(column=0, row=1)

CtrlMode = Label(window, text = "waitingforconnect")
CtrlMode.grid(column=0, row=2)

comboCtrlMode = Combobox(window)
comboCtrlMode['values'] = ("Not Set","CTRL_MODE_VOLTAGE_CONTROL","CTRL_MODE_CURRENT_CONTROL","CTRL_MODE_VELOCITY_CONTROL","CTRL_MODE_POSITION_CONTROL","CTRL_MODE_TRAJECTORY_CONTROL")
comboCtrlMode.current(0)
comboCtrlMode.grid(column=1, row=2)


def clicked():
    print("connecting")
    global my_drive
    my_drive = odrive.find_any() #Connect ot Odrive
    con = "Connected to Odrive"
    lbl.configure(text= con)
    CurrentState.configure(text = con)
    comboCtrlMode.current(my_drive.axis0.controller.config.control_mode + 1)
    kpCurrent.configure(text =  my_drive.axis0.controller.config.pos_gain)
    kvCurrent.configure(text =  my_drive.axis0.controller.config.vel_gain)
    kiCurrent.configure(text =  my_drive.axis0.controller.config.vel_integrator_gain)


def setCalbttn():
    global my_drive
    print("Calibration")
    my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
    while my_drive.axis0.current_state != AXIS_STATE_IDLE:
        time.sleep(0.1)
    cal = "Calibrated"
    CurrentState.configure(text = cal)

def CLCClicked():
    global my_drive
    print("ClosedLoopControl")
    my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    while my_drive.axis0.current_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
        time.sleep(0.1)
    clc = "ClosedLoopControl"
    CurrentState.configure(text = clc)

def setModeClicked():
    global my_drive
    selected = comboCtrlMode.get()
    if selected == "Not Set":
        print("ctrlModeNotSet")
        noSet = "notSet"
        CtrlMode.configure(text = noSet)
    elif selected == "CTRL_MODE_VOLTAGE_CONTROL":
        print("Set Voltage Control")
        my_drive.axis0.controller.config.control_mode = CTRL_MODE_VOLTAGE_CONTROL
        while my_drive.axis0.controller.config.control_mode != CTRL_MODE_VOLTAGE_CONTROL:
            time.sleep(0.1)
        voltmode = "Voltage Control"
        CtrlMode.configure(text = voltmode)
    elif selected == "CTRL_MODE_TRAJECTORY_CONTROL":
        print("Set TrajControl")
        my_drive.axis0.controller.config.control_mode = CTRL_MODE_TRAJECTORY_CONTROL
        while my_drive.axis0.controller.config.control_mode != CTRL_MODE_TRAJECTORY_CONTROL:
            time.sleep(0.1)
        trajmode = "Trajectory Control"
        CtrlMode.configure(text = trajmode)
    elif selected == "CTRL_MODE_POSITION_CONTROL":
        print("Set Position Control")
        my_drive.axis0.controller.config.control_mode = CTRL_MODE_POSITION_CONTROL
        while my_drive.axis0.controller.config.control_mode != CTRL_MODE_POSITION_CONTROL:
            time.sleep(0.1)
        posMode = "Position Control"
        CtrlMode.configure(text = posMode)
    elif selected == "CTRL_MODE_VELOCITY_CONTROL":
        print("Set VelocityControl")
        my_drive.axis0.controller.config.control_mode = CTRL_MODE_VELOCITY_CONTROL
        while my_drive.axis0.controller.config.control_mode != CTRL_MODE_VELOCITY_CONTROL:
            time.sleep(0.1)
        Velmode = "VelocityControl"
        CtrlMode.configure(text = velmode)
    elif selected == "CTRL_MODE_CURRENT_CONTROL":
        print("Set Current Control")
        my_drive.axis0.controller.config.control_mode = CTRL_MODE_CURRENT_CONTROL
        while my_drive.axis0.controller.config.control_mode != CTRL_MODE_CURRENT_CONTROL:
            time.sleep(0.1)
        Currmode = "Current Control"
        CtrlMode.configure(text = Currmode)

def goSetpointOne():
    global my_drive
    setpoint = posOne.get()
    print("setpoint =" + setpoint)
    my_drive.axis0.controller.pos_setpoint = int(setpoint)

def goSetpointTwo():
    global my_drive
    setpoint = posTwo.get()
    print("setpoint =" + setpoint)
    my_drive.axis0.controller.pos_setpoint = int(setpoint)

def goTrajpointOne():
    global my_drive
    setpoint = posOne.get()
    print("Trajpoint =" + setpoint)
    my_drive.axis0.controller.move_to_pos(int(setpoint))

def goTrajpointTwo():
    global my_drive
    setpoint = posTwo.get()
    print("Trajpoint =" + setpoint)
    my_drive.axis0.controller.move_to_pos(int(setpoint))

def writeCntrlValues():
    global my_drive
    kpGain = float(kpBox.get())
    kvGain = float(kvBox.get())
    kiGain = float(kiBox.get())
    my_drive.axis0.controller.config.pos_gain = kpGain
    my_drive.axis0.controller.config.vel_gain = kvGain
    my_drive.axis0.controller.config.vel_integrator_gain = kiGain
    kpCurrent.configure(text =  my_drive.axis0.controller.config.pos_gain)
    kvCurrent.configure(text =  my_drive.axis0.controller.config.vel_gain)
    kiCurrent.configure(text =  my_drive.axis0.controller.config.vel_integrator_gain)

def SaveButton():
    global my_drive
    my_drive.save_configuration()
    print("configSaved")

btn = Button(window, text="Connect", command=clicked)
btn.grid(column=1, row=0)

setCalbttn = Button(window, text="FullCalibration", command=setCalbttn)
setCalbttn.grid(column=1,row=1)

setCLCbttn = Button(window, text="ClosedLoopControl", command=CLCClicked)
setCLCbttn.grid(column=2,row=1)

setTrajcontrol = Button(window,text = "Set Mode", command=setModeClicked)
setTrajcontrol.grid(column=2,row=2)

saveConfbttn = Button(window, text="SaveConfig", command=SaveButton)
saveConfbttn.grid(column=5,row=8)

thisSetpointOne = Button(window, text="<=SetPointHere", command=goSetpointOne)
thisSetpointOne.grid(column =2,row =3)

thisTrajOne = Button(window, text="<=TrajToHere", command=goTrajpointOne)
thisTrajOne.grid(column =2,row =4)

thisSetpointTwo = Button(window, text="<=SetPointHere", command=goSetpointTwo)
thisSetpointTwo.grid(column =4,row =3)

wrtCntrlVal = Button(window, text="Write Cntrl Values", command=writeCntrlValues)
wrtCntrlVal.grid(column =4,row =5)

thisTrajOne = Button(window, text="<=TrajToHere", command=goTrajpointTwo)
thisTrajOne.grid(column =4,row =4)


txt = Entry(window,width=10)
#txt.grid(column=1, row=0)


window.mainloop()
