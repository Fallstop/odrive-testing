from __future__ import print_function
import tkinter
from tkinter import *
import sys
from tkinter.ttk import *
import odrive
from odrive.enums import *
import time
import math
import threading
from numpy import *

connected = False


class YourApp(Tk):
    def quit_and_close(self):
        window.destroy()
        sys.exit()


window = YourApp()
window.title("AndreisOdriveTestingWidget")
window.geometry('1200x600')
x = 0
y = 100
z = -100
lbl = Label(window, text="Waiting To connect To Odrive")
lbl.grid(column=0, row=0)

posOne = Entry(window, width=10)
posTwo = Entry(window, width=10)


xlab = Label(window, text="-x- -30 to 30")
xlab.grid(column=0, row=10)
ylab = Label(window, text="-y- 0 to 30")
ylab.grid(column=1, row=10)

xVal = Entry(window, width=10)
yVal = Entry(window, width=10)
zVal = Entry(window, width=10)

CntrlVal = Label(window, text="===Control Values===")
CntrlVal.grid(column=0, row=5)

# New MOtor Set UP
# axis0.motor.config.current_lim
# axis0.motor.config.pole_pairs
# axis0.encoder.config.cpr
# axis0.controller.config.vel_limit

posOne.grid(column=1, row=3)
posTwo.grid(column=3, row=3)

xVal.grid(column=0, row=11)
yVal.grid(column=1, row=11)
zVal.grid(column=2, row=11)

CurrentState = Label(window, text="State waitingforconnect")
CurrentState.grid(column=0, row=1)

CtrlMode = Label(window, text="waitingforconnect")
CtrlMode.grid(column=0, row=2)

comboCtrlMode = Combobox(window)
comboCtrlMode['values'] = ("Not Set", "CTRL_MODE_VOLTAGE_CONTROL", "CTRL_MODE_CURRENT_CONTROL", "CTRL_MODE_VELOCITY_CONTROL", "CTRL_MODE_POSITION_CONTROL", "CTRL_MODE_TRAJECTORY_CONTROL")
comboCtrlMode.current(0)
comboCtrlMode.grid(column=1, row=2)


def clicked():
    print("connecting")
    global odrv0
    global odrv1
    odrv0 = odrive.find_any(serial_number = "208037743548") #Connect ot Odrive
    print("odrv0 connected")
    odrv1 = odrive.find_any(serial_number = "3762364A3137") #Connect ot Odrive
    print("odrv1 connected")
    # 208037743548 first odrive
    # 3762364A3137 new odrive
    con = "Connected to Odrive"
    lbl.configure(text= con)
    CurrentState.configure(text = con)
    comboCtrlMode.current(odrv0.axis0.controller.config.control_mode + 1)


def setCalbttn():
    global odrv0
    global connected
    print("Calibration")
    odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
    while odrv0.axis0.current_state != AXIS_STATE_IDLE:
        time.sleep(0.1)
    connected = True
    cal = "Calibrated"
    CurrentState.configure(text = cal)


def CLCClicked():
    global odrv0
    print("ClosedLoopControl")
    odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    while odrv0.axis0.current_state != AXIS_STATE_CLOSED_LOOP_CONTROL:
        time.sleep(0.1)
    clc = "ClosedLoopControl"
    CurrentState.configure(text = clc)


def setModeClicked():
    global odrv0
    selected = comboCtrlMode.get()
    if selected == "Not Set":
        print("ctrlModeNotSet")
        noSet = "notSet"
        CtrlMode.configure(text = noSet)
    elif selected == "CTRL_MODE_VOLTAGE_CONTROL":
        print("Set Voltage Control")
        odrv0.axis0.controller.config.control_mode = CTRL_MODE_VOLTAGE_CONTROL
        while odrv0.axis0.controller.config.control_mode != CTRL_MODE_VOLTAGE_CONTROL:
            time.sleep(0.1)
        voltmode = "Voltage Control"
        CtrlMode.configure(text = voltmode)
    elif selected == "CTRL_MODE_TRAJECTORY_CONTROL":
        print("Set TrajControl")
        odrv0.axis0.controller.config.control_mode = CTRL_MODE_TRAJECTORY_CONTROL
        while odrv0.axis0.controller.config.control_mode != CTRL_MODE_TRAJECTORY_CONTROL:
            time.sleep(0.1)
        trajmode = "Trajectory Control"
        CtrlMode.configure(text = trajmode)
    elif selected == "CTRL_MODE_POSITION_CONTROL":
        print("Set Position Control")
        odrv0.axis0.controller.config.control_mode = CTRL_MODE_POSITION_CONTROL
        while odrv0.axis0.controller.config.control_mode != CTRL_MODE_POSITION_CONTROL:
            time.sleep(0.1)
        posMode = "Position Control"
        CtrlMode.configure(text = posMode)
    elif selected == "CTRL_MODE_VELOCITY_CONTROL":
        print("Set VelocityControl")
        odrv0.axis0.controller.config.control_mode = CTRL_MODE_VELOCITY_CONTROL
        while odrv0.axis0.controller.config.control_mode != CTRL_MODE_VELOCITY_CONTROL:
            time.sleep(0.1)
        Velmode = "VelocityControl"
        CtrlMode.configure(text = velmode)
    elif selected == "CTRL_MODE_CURRENT_CONTROL":
        print("Set Current Control")
        odrv0.axis0.controller.config.control_mode = CTRL_MODE_CURRENT_CONTROL
        while odrv0.axis0.controller.config.control_mode != CTRL_MODE_CURRENT_CONTROL:
            time.sleep(0.1)
        Currmode = "Current Control"
        CtrlMode.configure(text = Currmode)


def goSetpointOne():
    global odrv0
    setpoint = posOne.get()
    print("setpoint =" + setpoint)
    odrv0.axis0.controller.pos_setpoint = int(setpoint)


def goSetpointTwo():
    global odrv0
    setpoint = posTwo.get()
    print("setpoint =" + setpoint)
    odrv0.axis1.controller.pos_setpoint = int(setpoint)


def goTrajpointOne():
    global odrv0
    setpoint = posOne.get()
    print("Trajpoint =" + setpoint)
    odrv0.axis0.controller.move_to_pos(int(setpoint))


def goTrajpointTwo():
    global odrv0
    setpoint = posTwo.get()
    print("Trajpoint =" + setpoint)
    odrv0.axis1.controller.move_to_pos(int(setpoint))


def PickUp2():
    def run():
        global newx
        global newy
        global newz
        global a
        while a:
            newz = -120
            newy = 0
            newx = 0
            ThreeDoF()
            newz = -200
            ThreeDoF()
            newz = -120
            ThreeDoF()
            # newy = 50
            # ThreeDoF()
            newy = 200
            # newx = 100
            ThreeDoF()
            newz = -200
            ThreeDoF()
            newz = -120
            ThreeDoF()
            if not a:
                break
    thread = threading.Thread(target=run)
    thread.start()


def goKinmatic():
    global odrv0
    global odrv1
    global newx
    global newy
    # newx = yVal.get()
    # newy = xVal.get()
    newx = int(newx)
    newy = int(newy)
    global x
    global y
    global decel
    oldx = x
    #   oldy = y
    txdist = abs(newx - oldx)
    #   tydist = abs(newy - oldy)

    while (x != newx or y != newy):
        if x == newx:
            x = x
        elif(x > newx):
            x = x -5
        elif(x < newx):
            x = x +5
        if y == newy:
            y = y
        elif(y > newy):
            y = y -5
        elif(y < newy):
            y = y +5

        if y < 0:
            y = 0
    #    if x <10
        xdist = abs(newx - x)
        #   ydist = abs(newy - y)
        a2 = 150  # length of link a2 in cm

        a4 = 150  # length of link a4 in cm
        # Desired Position of End effector

        # Equations for Inverse kinematics
        r1 = sqrt(y**2+x**2)  # eqn 1
        phi_1 = arccos((a4**2-a2**2-r1**2)/(-2*a2*r1))  # eqn 2
        phi_2 = arctan2(x, y)  # eqn 3
        theta_1 = rad2deg(phi_2-phi_1)  # eqn 4 converted to degrees

        phi_3 = arccos((r1**2-a2**2-a4**2)/(-2*a2*a4))
        theta_2 = 180-rad2deg(phi_3)

        j1c = theta_1 * 22.755
        j2c = theta_2 * 45.511

        j1 = -(j1c - 900)  # this zeros to have the arms up flat at 90 angle
        j2 = j2c - (5000 - (j1c))

        j1 = int(j1)
        j2 = int(j2)

        if (txdist/4)>xdist:
            decel = decel -10000
            odrv0.axis1.trap_traj.config.decel_limit = decel
            odrv0.axis0.trap_traj.config.decel_limit = decel

        odrv0.axis0.controller.move_to_pos(j1)
        odrv0.axis1.controller.move_to_pos(j2)

        val = odrv0.axis0.encoder.shadow_count
        val1 = odrv0.axis1.encoder.shadow_count
        val1 = int(val1)
        val = int(val)

        j = j1 - 200
        jj = j1 + 200
        j0 = j2 - 200
        jj0 = j2 + 200
        while (((jj0) < val1) or ((j0) > val1)):
            val1 = odrv0.axis1.encoder.shadow_count
            val1 = int(val1)
        while (((jj) < val)) or (((j) > val)):
            val = odrv0.axis0.encoder.shadow_count
            val = int(val)


def ThreeDoF():

    global odrv0
    global odrv1
    global newx
    global newy
    global newz
    global x
    global y
    global z
    global Distance
    newx = int(newx)
    newy = int(newy)
    newz = int(newz)
    Distance = sqrt(((x - newx)**2) + ((y - newy)**2) + ((z - newz)**2))
    # CurrentDistance = sqrt(((x - newx)**2) + ((y - newy)**2) + ((z - newz)**2))
    Resolution = 10

    while (x != newx or y != newy or z != newz):
        if x == newx:
            x = x
        if(x > newx):
            x = x -Resolution
        if(x < newx):
            x = x +Resolution
        if y == newy:
            y = y
        if(y > newy):
            y = y -Resolution
        if(y < newy):
            y = y +Resolution
        if z == newz:
            z = z
        if(z > newz):
            z = z -Resolution
        if(z < newz):
            z = z +Resolution

        a1 = 60
        a2 = 150
        a3 = 230
        #Ramp()
        theta_1 = rad2deg(arctan2(x, y))

        r1 = sqrt(y**2 + x**2)

        r2 = z - a1

        phi_2 = arctan2(r2, r1)

        r3 = sqrt(r1**2+r2**2)

        cat = (a3**2-a2**2-r3**2)

        dog = (-2*a2*r3)

        phi_1 = arccos(cat/dog)

        theta_2 = -rad2deg(phi_2 - phi_1)

        phi_3 = arccos((r3**2-a2**2-a3**2)/(-2*a2*a3))

        theta_3 = (180-rad2deg(phi_3))

        # print(theta_1)
        # print(theta_2)
        # print(theta_3)

        theta_2 = 180 - theta_2

        j1c = theta_1 * 22.755
        j2c = theta_2 * 22.755
        j3c = (theta_3) * 45.511
        j1 = j1c - 970 # wrong
        j2 = -(j2c - 900)  # this zeros to have the arms up flat at 90 angle have a look at this maths
        j3 = j3c - (5000 - (j2c))
        j1 = int(j1)
        j2 = int(j2)
        j3 = int(j3)

        odrv0.axis0.controller.config.control_mode = CTRL_MODE_POSITION_CONTROL
        odrv0.axis1.controller.config.control_mode = CTRL_MODE_POSITION_CONTROL
        odrv1.axis0.controller.config.control_mode = CTRL_MODE_POSITION_CONTROL
        odrv0.axis0.controller.pos_setpoint = j2
        odrv0.axis1.controller.pos_setpoint = j3
        print(j1)
        # odrv1.axis0.controller.pos_setpoint = j1
        val = odrv0.axis0.encoder.shadow_count
        val1 = odrv0.axis1.encoder.shadow_count
        val2 = odrv1.axis0.encoder.shadow_count
        val2 = int(val2)
        val1 = int(val1)
        val = int(val)

        print(val2)

        j4 = j1 - 200
        jj4 = j1 + 200
        j = j2 - 200
        jj = j2 + 200
        j0 = j3 - 200
        jj0 = j3 + 200
        while (((jj0) < val1) or ((j0) > val1)):
            val1 = odrv0.axis1.encoder.shadow_count
            val1 = int(val1)
        while (((jj) < val)) or (((j) > val)):
            val = odrv0.axis0.encoder.shadow_count
            val = int(val)
        while (((jj4) < val2)) or (((j4) > val2)):
            val2 = odrv1.axis0.encoder.shadow_count
            val2 = int(val2)


def Ramp():
    global odrv0
    global odrv1
    global newx
    global newy
    global newz
    global x
    global y
    global z
    global Distance
    MaxAccel = 3800
    MinAccel = 0.01
    Amplitude = MaxAccel - MinAccel
    CurrentDistance = sqrt(((x - newx)**2) + ((y - newy)**2) + ((z - newz)**2))
    Acceleration = MinAccel + (Amplitude)*sin((pi*CurrentDistance)/Distance)
    Acceleration = MaxAccel - (Acceleration)
    # time.sleep(0.5)

    odrv0.axis1.controller.vel_setpoint = Acceleration
    odrv0.axis0.controller.vel_setpoint = Acceleration
    # odrv1.axis0.controller.vel_setpoint = Acceleration
    # odrv0.axis0.controller.current_setpoint = (Acceleration/10)
    # odrv0.axis1.controller.current_setpoint = (Acceleration/10)
    # odrv1.axis0.controller.current_setpoint = (Acceleration/10)
    # print(Acceleration)


def SaveButton():

    global odrv0
    odrv0.save_configuration()
    print("configSaved")


def OpenAxis0():
    window = Tk()
    window.title("Axis0 Config")
    window.geometry('800x300')

    kpBox =Entry(window, width=10)
    kvBox =Entry(window, width=10)
    kiBox =Entry(window, width=10)

    kpBox.grid(column = 2, row = 6)
    kvBox.grid(column = 2, row = 7)
    kiBox.grid(column = 2, row = 8)

    kpCurrentLbl = Label(window, text = "axis0.controller.config.pos_gain")
    kvCurrentLbl = Label(window, text = "axis0.controller.config.vel_gain")
    kiCurrentLbl = Label(window, text = "axis0.controller.config.vel_integrator_gain")

    kpCurrentLbl.grid(column = 0, row = 6)
    kvCurrentLbl.grid(column = 0, row = 7)
    kiCurrentLbl.grid(column = 0, row = 8)

    kpCurrentVal = Label(window, text = "wfc")
    kvCurrentVal = Label(window, text = "wfc")
    kiCurrentVal = Label(window, text = "wfc")

    kpCurrentVal.grid(column = 1, row = 6)
    kvCurrentVal.grid(column = 1, row = 7)
    kiCurrentVal.grid(column = 1, row = 8)

    trajVelLbl = Label(window, text = "axis0.trap_traj.config.vel_limit")
    trajAccelLbl = Label(window, text = "axis0.trap_traj.config.accel_limit")
    trajDecelLbl = Label(window, text = "axis0.trap_traj.config.decel_limit")
    CurrentLimLbl = Label(window, text = "axis0.motor.config.current_lim")

    trajVelVal =Label(window, text = "wfc")
    trajAccelVal =Label(window, text = "wfc")
    trajDecelVal =Label(window, text = "wfc")
    CurrentLimVal =Label(window, text = "wfc")

    trajVelLbl.grid(column = 0, row = 9)
    trajAccelLbl.grid(column = 0, row = 10)
    trajDecelLbl.grid(column = 0, row = 11)
    CurrentLimLbl.grid(column = 0, row = 12)

    trajVelVal.grid(column = 1, row = 9)
    trajAccelVal.grid(column = 1, row = 10)
    trajDecelVal.grid(column = 1, row = 11)
    CurrentLimVal.grid(column = 1, row = 12)

    trajVelBox =Entry(window, width=10)
    trajAccelBox =Entry(window, width=10)
    trajDecelBox =Entry(window, width=10)
    CurrentLimBox =Entry(window, width=10)

    trajVelBox.grid(column = 2, row = 9)
    trajAccelBox.grid(column = 2, row = 10)
    trajDecelBox.grid(column = 2, row = 11)
    CurrentLimBox.grid(column = 2, row = 12)

    kpCurrentVal.configure(text = odrv0.axis0.controller.config.pos_gain)
    kvCurrentVal.configure(text = odrv0.axis0.controller.config.vel_gain)
    kiCurrentVal.configure(text = odrv0.axis0.controller.config.vel_integrator_gain)
    trajVelVal.configure(text = odrv0.axis0.trap_traj.config.vel_limit)
    trajAccelVal.configure(text = odrv0.axis0.trap_traj.config.accel_limit)
    trajDecelVal.configure(text = odrv0.axis0.trap_traj.config.decel_limit)
    CurrentLimVal.configure(text = odrv0.axis0.motor.config.current_lim)

    def writekp():
        global odrv0
        kpGain = float(kpBox.get())
        odrv0.axis0.controller.config.pos_gain = kpGain
        kpCurrentVal.configure(text = odrv0.axis0.controller.config.pos_gain)

    def writekv():
        global odrv0
        kvGain = float(kvBox.get())
        odrv0.axis0.controller.config.vel_gain = kvGain
        kvCurrentVal.configure(text = odrv0.axis0.controller.config.vel_gain)

    def writeki():
        kiGain = float(kiBox.get())
        odrv0.axis0.controller.config.vel_integrator_gain = kiGain
        kiCurrentVal.configure(text = odrv0.axis0.controller.config.vel_integrator_gain)

    def writeTrajVel():
        global odrv0
        trajVel = float(trajVelBox.get())
        odrv0.axis0.trap_traj.config.vel_limit = trajVel
        trajVelVal.configure(text = odrv0.axis0.trap_traj.config.vel_limit)

    def writeTrajAccel():
        global odrv0
        trajAccel = float(trajAccelBox.get())
        odrv0.axis0.trap_traj.config.accel_limit = trajAccel
        trajAccelVal.configure(text = odrv0.axis0.trap_traj.config.accel_limit)

    def writeTrajDecel():
        global odrv0
        trajDecel = float(trajDecelBox.get())
        odrv0.axis0.trap_traj.config.decel_limit = trajDecel
        trajDecelVal.configure(text = odrv0.axis0.trap_traj.config.decel_limit)

    def writeCurrentLim():
        global odrv0
        CurrentLim = float(CurrentLimBox.get())
        odrv0.axis0.motor.config.current_lim = CurrentLim
        CurrentLimVal.configure(text = odrv0.axis0.motor.config.current_lim)

    wrtkp = Button(window, text="Write new kp", command=writekp)
    wrtkp.grid(column =3, row =6)

    wrtkv = Button(window, text="Write new kv", command=writekv)
    wrtkv.grid(column =3, row =7)

    wrtki = Button(window, text="Write new ki", command=writeki)
    wrtki.grid(column =3, row =8)

    wrtTrajVel = Button(window, text="Write new trajVel", command=writeTrajVel)
    wrtTrajVel.grid(column =3, row =9)

    wrtTrajAccel = Button(window, text="Write new trajAccel", command=writeTrajAccel)
    wrtTrajAccel.grid(column =3, row =10)

    wrtTrajDecel = Button(window, text="Write new trajdecel", command=writeTrajDecel)
    wrtTrajDecel.grid(column =3, row =11)

    wrtCurrentLim = Button(window, text="Write new Current lim", command=writeCurrentLim)
    wrtCurrentLim.grid(column =3, row =12)

    updateValues()


def OpenAxis1():
    window = Tk()
    window.title("Axis1 Config")
    window.geometry('800x300')

    kpBox1 =Entry(window, width=10)
    kvBox1 =Entry(window, width=10)
    kiBox1 =Entry(window, width=10)

    kpBox1.grid(column = 2, row = 6)
    kvBox1.grid(column = 2, row = 7)
    kiBox1.grid(column = 2, row = 8)

    kpCurrentLbl1 = Label(window, text = "axis1.controller.config.pos_gain")
    kvCurrentLbl1 = Label(window, text = "axis1.controller.config.vel_gain")
    kiCurrentLbl1 = Label(window, text = "axis1.controller.config.vel_integrator_gain")

    kpCurrentLbl1.grid(column = 0, row = 6)
    kvCurrentLbl1.grid(column = 0, row = 7)
    kiCurrentLbl1.grid(column = 0, row = 8)

    kpCurrentVal1 = Label(window, text = "wfc")
    kvCurrentVal1 = Label(window, text = "wfc")
    kiCurrentVal1 = Label(window, text = "wfc")

    kpCurrentVal1.grid(column = 1, row = 6)
    kvCurrentVal1.grid(column = 1, row = 7)
    kiCurrentVal1.grid(column = 1, row = 8)

    trajVelLbl1 = Label(window, text = "axis1.trap_traj.config.vel_limit")
    trajAccelLbl1 = Label(window, text = "axis1.trap_traj.config.accel_limit")
    trajDecelLbl1 = Label(window, text = "axis1.trap_traj.config.decel_limit")
    CurrentLimLbl1 = Label(window, text = "axis1.motor.config.current_lim")

    trajVelVal1 =Label(window, text = "wfc")
    trajAccelVal1 =Label(window, text = "wfc")
    trajDecelVal1 =Label(window, text = "wfc")
    CurrentLimVal1 =Label(window, text = "wfc")

    trajVelLbl1.grid(column = 0, row = 9)
    trajAccelLbl1.grid(column = 0, row = 10)
    trajDecelLbl1.grid(column = 0, row = 11)
    CurrentLimLbl1.grid(column = 0, row = 12)

    trajVelVal1.grid(column = 1, row = 9)
    trajAccelVal1.grid(column = 1, row = 10)
    trajDecelVal1.grid(column = 1, row = 11)
    CurrentLimVal1.grid(column = 1, row = 12)

    trajVelBox1 =Entry(window, width=10)
    trajAccelBox1 =Entry(window, width=10)
    trajDecelBox1 =Entry(window, width=10)
    CurrentLimBox1 =Entry(window, width=10)

    trajVelBox1.grid(column = 2, row = 9)
    trajAccelBox1.grid(column = 2, row = 10)
    trajDecelBox1.grid(column = 2, row = 11)
    CurrentLimBox1.grid(column = 2, row = 12)

    kpCurrentVal1.configure(text = odrv0.axis1.controller.config.pos_gain)
    kvCurrentVal1.configure(text = odrv0.axis1.controller.config.vel_gain)
    kiCurrentVal1.configure(text = odrv0.axis1.controller.config.vel_integrator_gain)
    trajVelVal1.configure(text = odrv0.axis1.trap_traj.config.vel_limit)
    trajAccelVal1.configure(text = odrv0.axis1.trap_traj.config.accel_limit)
    trajDecelVal1.configure(text = odrv0.axis1.trap_traj.config.decel_limit)
    CurrentLimVal1.configure(text = odrv0.axis1.motor.config.current_lim)

    def writekp1():
        global odrv0
        kpGain1 = float(kpBox1.get())
        odrv0.axis1.controller.config.pos_gain = kpGain1
        kpCurrentVal1.configure(text = odrv0.axis1.controller.config.pos_gain)

    def writekv1():
        global odrv0
        kvGain1 = float(kvBox1.get())
        odrv0.axis1.controller.config.vel_gain = kvGain1
        kvCurrentVal1.configure(text = odrv0.axis1.controller.config.vel_gain)

    def writeki1():
        kiGain1 = float(kiBox1.get())
        odrv0.axis1.controller.config.vel_integrator_gain = kiGain1
        kiCurrentVal1.configure(text = odrv0.axis1.controller.config.vel_integrator_gain)

    def writeTrajVel1():
        global odrv0
        trajVel1 = float(trajVelBox1.get())
        odrv0.axis1.trap_traj.config.vel_limit = trajVel1
        trajVelVal1.configure(text = odrv0.axis1.trap_traj.config.vel_limit)

    def writeTrajAccel1():
        global odrv0
        trajAccel1 = float(trajAccelBox1.get())
        odrv0.axis1.trap_traj.config.accel_limit = trajAccel1
        trajAccelVal1.configure(text = odrv0.axis1.trap_traj.config.accel_limit)

    def writeTrajDecel1():
        global odrv0
        trajDecel1 = float(trajDecelBox1.get())
        odrv0.axis1.trap_traj.config.decel_limit = trajDecel1
        trajDecelVal1.configure(text = odrv0.axis1.trap_traj.config.decel_limit)

    def writeCurrentLim1():
        global odrv0
        CurrentLim1 = float(CurrentLimBox1.get())
        odrv0.axis1.motor.config.current_lim = CurrentLim1
        CurrentLimVal1.configure(text = odrv0.axis1.motor.config.current_lim)

    wrtkp1 = Button(window, text="Write new kp", command=writekp1)
    wrtkp1.grid(column =3, row =6)

    wrtkv1 = Button(window, text="Write new kv", command=writekv1)
    wrtkv1.grid(column =3, row =7)

    wrtki1 = Button(window, text="Write new ki", command=writeki1)
    wrtki1.grid(column =3, row =8)

    wrtTrajVel1 = Button(window, text="Write new trajVel", command=writeTrajVel1)
    wrtTrajVel1.grid(column =3, row =9)

    wrtTrajAccel1 = Button(window, text="Write new trajAccel", command=writeTrajAccel1)
    wrtTrajAccel1.grid(column =3, row =10)

    wrtTrajDecel1 = Button(window, text="Write new trajdecel", command=writeTrajDecel1)
    wrtTrajDecel1.grid(column =3, row =11)

    wrtCurrentLim1 = Button(window, text="Write new Current lim", command=writeCurrentLim1)
    wrtCurrentLim1.grid(column =3, row =12)

    updateValues()


def Reboot():
    global odrv0
    odrv0.reboot()
    print("Rebooting")


def Start():
    global a
    a = True
    PickUp2()


def Stop():
    global a
    a = False


def XYMove():
    global a
    global newx
    global newy
    global newz
    newx = xVal.get()
    newy = yVal.get()
    newz = zVal.get()
    ThreeDoF()


btn = Button(window, text="Connect", command=clicked)
btn.grid(column=1, row=0)

setCalbttn = Button(window, text="FullCalibration", command=setCalbttn)
setCalbttn.grid(column=1, row=1)

setCLCbttn = Button(window, text="ClosedLoopControl", command=CLCClicked)
setCLCbttn.grid(column=2, row=1)

setTrajcontrol = Button(window, text = "Set Mode", command=setModeClicked)
setTrajcontrol.grid(column=2, row=2)

saveConfbttn = Button(window, text="SaveConfig", command=SaveButton)
saveConfbttn.grid(column=5, row=8)

thisSetpointOne = Button(window, text="<=SetPointHere", command=goSetpointOne)
thisSetpointOne.grid(column =2, row =3)

thisTrajOne = Button(window, text="<=TrajToHere", command=goTrajpointOne)
thisTrajOne.grid(column =2, row =4)

thisSetpointTwo = Button(window, text="<=SetPointHere", command=goSetpointTwo)
thisSetpointTwo.grid(column =4, row =3)

thisTrajOne = Button(window, text="<=TrajToHere", command=goTrajpointTwo)
thisTrajOne.grid(column =4, row =4)

StartButton = Button(window, text="Start", command=Start)
StartButton.grid(column =5, row =9)

StopButton = Button(window, text="Stop", command=Stop)
StopButton.grid(column =5, row =10)

Axis0Window = Button(window, text="Axis0 Config", command=OpenAxis0)
Axis0Window.grid(column =0, row =9)

Axis1Window = Button(window, text="Axis1 Config", command=OpenAxis1)
Axis1Window.grid(column =1, row =9)

RebootButton = Button(window, text="Reboot", command=Reboot)
RebootButton.grid(column =5, row =7)

XYButton = Button(window, text="X Y pos move", command=XYMove)
XYButton.grid(column=4, row=11)

killbutton = Button(window, text = "EXIT", command = window.quit_and_close)
killbutton.grid(column=9, row=12)


def updateValues():
    threading.Timer(0.5, updateValues).start()
    global connected
    if connected:
        kpCurrentVal.configure(text = odrv0.axis0.controller.config.pos_gain)
        kvCurrentVal.configure(text = odrv0.axis0.controller.config.vel_gain)
        kiCurrentVal.configure(text = odrv0.axis0.controller.config.vel_integrator_gain)
        trajVelVal.configure(text = odrv0.axis0.trap_traj.config.vel_limit)
        trajAccelVal.configure(text = odrv0.axis0.trap_traj.config.accel_limit)
        trajDecelVal.configure(text = odrv0.axis0.trap_traj.config.decel_limit)
        CurrentLimVal.configure(text = odrv0.axis1.motor.config.current_lim)

        kpCurrentVal1.configure(text = odrv0.axis1.controller.config.pos_gain)
        kvCurrentVal1.configure(text = odrv0.axis1.controller.config.vel_gain)
        kiCurrentVal1.configure(text = odrv0.axis1.controller.config.vel_integrator_gain)
        trajVelVal1.configure(text = odrv0.axis1.trap_traj.config.vel_limit)
        trajAccelVal1.configure(text = odrv0.axis1.trap_traj.config.accel_limit)
        trajDecelVal1.configure(text = odrv0.axis1.trap_traj.config.decel_limit)
        CurrentLimVal1.configure(text = odrv0.axis1.motor.config.current_lim)


updateValues()

txt = Entry(window, width=10)
# txt.grid(column=1, row=0)


window.mainloop()
