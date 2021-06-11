
from __future__ import print_function
from tkinter import *
from tkinter.ttk import *
import odrive
from odrive.enums import *
import time
import math
import threading

connected = False

window = Tk()
window.title("AndreisOdriveTestingWidget")
window.geometry('900x400')

lbl = Label(window, text="Waiting To connect To Odrive")
lbl.grid(column=0, row=0)

posOne = Entry(window,width=10)
posTwo = Entry(window,width=10)

CntrlVal = Label(window,text="===Control Values===")
CntrlVal.grid(column = 0, row = 5)

kpBox =Entry(window,width=10)
kvBox =Entry(window,width=10)
kiBox =Entry(window,width=10)

kpBox.grid(column = 2, row = 6)
kvBox.grid(column = 2, row = 7)
kiBox.grid(column = 2, row = 8)

kpCurrentLbl = Label(window,text = "axis0.controller.config.pos_gain")
kvCurrentLbl = Label(window,text = "axis0.controller.config.vel_gain")
kiCurrentLbl = Label(window,text = "axis0.controller.config.vel_integrator_gain")

kpCurrentLbl.grid(column = 0, row = 6)
kvCurrentLbl.grid(column = 0, row = 7)
kiCurrentLbl.grid(column = 0, row = 8)

kpCurrentVal = Label(window,text = "wfc")
kvCurrentVal = Label(window,text = "wfc")
kiCurrentVal = Label(window,text = "wfc")

kpCurrentVal.grid(column = 1, row = 6)
kvCurrentVal.grid(column = 1, row = 7)
kiCurrentVal.grid(column = 1, row = 8)

trajVelLbl = Label(window, text = "axis0.trap_traj.config.vel_limit")
trajAccelLbl = Label(window, text = "axis0.trap_traj.config.accel_limit")
trajDecelLbl = Label(window, text = "axis0.trap_traj.config.decel_limit")

trajVelVal =Label(window,text = "wfc")
trajAccelVal =Label(window,text = "wfc")
trajDecelVal =Label(window,text = "wfc")

trajVelLbl.grid(column = 0, row = 9)
trajAccelLbl.grid(column = 0, row = 10)
trajDecelLbl.grid(column = 0, row = 11)

trajVelVal.grid(column = 1, row = 9)
trajAccelVal.grid(column = 1, row = 10)
trajDecelVal.grid(column = 1, row = 11)

trajVelBox =Entry(window,width=10)
trajAccelBox =Entry(window,width=10)
trajDecelBox =Entry(window,width=10)

trajVelBox.grid(column = 2, row = 9)
trajAccelBox.grid(column = 2, row = 10)
trajDecelBox.grid(column = 2, row = 11)

#New MOtor Set UP
#axis0.motor.config.current_lim
#axis0.motor.config.pole_pairs
#axis0.encoder.config.cpr
#axis0.controller.config.vel_limit

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
    kpCurrentVal.configure(text =  my_drive.axis0.controller.config.pos_gain)
    kvCurrentVal.configure(text =  my_drive.axis0.controller.config.vel_gain)
    kiCurrentVal.configure(text =  my_drive.axis0.controller.config.vel_integrator_gain)


def setCalbttn():
    global my_drive
    global connected
    print("Calibration")
    my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
    while my_drive.axis0.current_state != AXIS_STATE_IDLE:
        time.sleep(0.1)
    connected = True
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

def writekp():
    global my_drive
    kpGain = float(kpBox.get())
    my_drive.axis0.controller.config.pos_gain = kpGain
    kpCurrentVal.configure(text =  my_drive.axis0.controller.config.pos_gain)

def writekv():
    global my_drive
    kvGain = float(kvBox.get())
    my_drive.axis0.controller.config.vel_gain = kvGain
    kvCurrentVal.configure(text =  my_drive.axis0.controller.config.vel_gain)

def writeki():
    kiGain = float(kiBox.get())
    my_drive.axis0.controller.config.vel_integrator_gain = kiGain
    kiCurrentVal.configure(text =  my_drive.axis0.controller.config.vel_integrator_gain)

def writeTrajVel():
    global my_drive
    trajVel = float(trajVelBox.get())
    my_drive.axis0.trap_traj.config.vel_limit = trajVel
    trajVelVal.configure(text =  my_drive.axis0.trap_traj.config.vel_limit)

def writeTrajAccel():
    global my_drive
    trajAccel = float(trajAccelBox.get())
    my_drive.axis0.trap_traj.config.accel_limit = trajAccel
    trajAccelVal.configure(text =  my_drive.axis0.trap_traj.config.accel_limit)

def writeTrajDecel():
    global my_drive
    trajDecel = float(trajDecelBox.get())
    my_drive.axis0.trap_traj.config.decel_limit = trajDecel
    trajDecelVal.configure(text =  my_drive.axis0.trap_traj.config.decel_limit)

def SaveButton():
    global my_drive
    my_drive.save_configuration()
    print("configSaved")

def RandomSheldCode():
    print("this is a section for sheldon to try random code")
    print("for eaxmple, go to position 2000 wait 2 second then go pos 0")
    my_drive.axis0.controller.move_to_pos(2000)
    time.sleep(2)
    my_drive.axis0.controller.move_to_pos(0)
    my_drive.axis1.trap_traj.config.vel_limit = 5000000
    my_drive.axis1.trap_traj.config.accel_limit = 1000000
    my_drive.axis1.controller.move_to_pos(2000)
    time.sleep(2)
    my_drive.axis1.trap_traj.config.vel_limit = 1000
    my_drive.axis1.trap_traj.config.accel_limit = 1000
    my_drive.axis1.controller.move_to_pos(0)
    print("Have fun dude")

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

wrtkp = Button(window, text="Write new kp", command=writekp)
wrtkp.grid(column =3,row =6)

wrtkv = Button(window, text="Write new kv", command=writekv)
wrtkv.grid(column =3,row =7)

wrtki = Button(window, text="Write new ki", command=writeki)
wrtki.grid(column =3,row =8)

wrtTrajVel = Button(window, text="Write new trajVel", command=writeTrajVel)
wrtTrajVel.grid(column =3,row =9)

wrtTrajAccel = Button(window, text="Write new trajAccel", command=writeTrajAccel)
wrtTrajAccel.grid(column =3,row =10)

wrtTrajDecel = Button(window, text="Write new trajdecel", command=writeTrajDecel)
wrtTrajDecel.grid(column =3,row =11)

thisTrajOne = Button(window, text="<=TrajToHere", command=goTrajpointTwo)
thisTrajOne.grid(column =4,row =4)

RndCodeButton = Button(window, text="Do Random Sheldon Code", command=RandomSheldCode)
RndCodeButton.grid(column =5,row =9)


def updateValues():
  threading.Timer(0.5, updateValues).start()
  global connected
  if connected:
      kpCurrentVal.configure(text =  my_drive.axis0.controller.config.pos_gain)
      kvCurrentVal.configure(text =  my_drive.axis0.controller.config.vel_gain)
      kiCurrentVal.configure(text =  my_drive.axis0.controller.config.vel_integrator_gain)
      trajVelVal.configure(text =  my_drive.axis0.trap_traj.config.vel_limit)
      trajAccelVal.configure(text =  my_drive.axis0.trap_traj.config.accel_limit)
      trajDecelVal.configure(text =  my_drive.axis0.trap_traj.config.decel_limit)


updateValues()

txt = Entry(window,width=10)
#txt.grid(column=1, row=0)


window.mainloop()
