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

connected = False

tk = Tk()
Width = 1210
Height = 600

kpLbl = []
kvLbl = []
kiLbl = []
kpVal = []
kvVal = []
kiVal = []
trajVelLbl = []
trajAccelLbl = []
trajDecelLbl = []
CurrentLimLbl = []
trajVelVal = []
trajAccelVal = []
trajDecelVal = []
CurrentLimVal = []
kpBox = []
kvBox = []
kiBox = []
trajVelBox = []
trajAccelBox = []
trajDecelBox = []
CurrentLimBox = []
FirstPosLbl = []
SecondPosLbl = []
FirstPosBox = []
SecondPosBox = []
GoBtn = []
GoFunk = []

tk.geometry('1210x600')
canvas = Canvas(tk, width = Width, height = Height)
canvas.pack()
tk.title("Motor tuner")

Odrive0Lab = Label(tk, text="Odrive0").place(x=10, y=10)
Odrive1Lab = Label(tk, text="Odrive1").place(x=610, y=10)
Axis00 = Label(tk, text="Axis0").place(x=10, y=45)
Axis10 = Label(tk, text="Axis1").place(x=310, y=45)
Axis01 = Label(tk, text="Axis0").place(x=610, y=45)
Axis11 = Label(tk, text="Axis1").place(x=910, y=45)


def Drive1Sync():
    print("connecting")
    global odrv0
    odrv0 = odrive.find_any(serial_number = "208037743548") #Connect ot Odrive
    print("odrv0 connected")
    Drawing()
    # 208037743548 first odrive
    # 3762364A3137 new odrive


def Drive2Sync():
    print("connecting")
    global odrv1
    odrv1 = odrive.find_any(serial_number = "3762364A3137") #Connect ot Odrive
    print("odrv1 connected")
    Drawing()
    # 208037743548 first odrive
    # 3762364A3137 new odrive


def GoFunk0():
    global odrv0
    setpoint1 = FirstPosBox[0].get()
    setpoint2 = SecondPosBox[0].get()
    odrv0.axis0.controller.pos_setpoint = int(setpoint1)
    time.sleep(2)
    odrv0.axis0.controller.pos_setpoint = int(setpoint2)


def GoFunk1():
    global odrv0
    setpoint1 = FirstPosBox[1].get()
    setpoint2 = SecondPosBox[1].get()
    odrv0.axis1.controller.pos_setpoint = int(setpoint1)
    time.sleep(2)
    odrv0.axis1.controller.pos_setpoint = int(setpoint2)


def GoFunk2():
    global odrv1
    setpoint1 = FirstPosBox[2].get()
    setpoint2 = SecondPosBox[2].get()
    odrv1.axis0.controller.pos_setpoint = int(setpoint1)
    time.sleep(2)
    odrv1.axis0.controller.pos_setpoint = int(setpoint2)


def GoFunk3():
    global odrv1
    setpoint1 = FirstPosBox[3].get()
    setpoint2 = SecondPosBox[3].get()
    odrv1.axis1.controller.pos_setpoint = int(setpoint1)
    time.sleep(2)
    odrv1.axis1.controller.pos_setpoint = int(setpoint2)


a = 0
while a <=3:

    canvas.create_line(5, 38, 5, 332, fill = "black", width = 4)
    canvas.create_line(305, 40, 305, 330, fill = "black", width = 4)
    canvas.create_line(605, 40, 605, 330, fill = "black", width = 4)
    canvas.create_line(905, 40, 905, 330, fill = "black", width = 4)
    canvas.create_line(1205, 38, 1205, 332, fill = "black", width = 4)
    canvas.create_line(5, 40, 1205, 40, fill = "black", width = 4)
    canvas.create_line(5, 70, 1205, 70, fill = "black", width = 4)
    canvas.create_line(5, 330, 1205, 330, fill = "black", width = 4)

    canvas.pack()
    # canvas.create_line(656, 40, 806, 390, fill = "black", width = 5)

    kpLbl.append(Label(tk, text = "pos_gain"))
    kvLbl.append(Label(tk, text = "vel_gain"))
    kiLbl.append(Label(tk, text = "vel_integrator_gain"))
    kpVal.append(Label(tk, text = "wfc"))
    kvVal.append(Label(tk, text = "wfc"))
    kiVal.append(Label(tk, text = "wfc"))
    kpBox.append(Entry(tk, width=10))
    kvBox.append(Entry(tk, width=10))
    kiBox.append(Entry(tk, width=10))
    trajVelLbl.append(Label(tk, text = "traj vel_limit"))
    trajAccelLbl.append(Label(tk, text = "traj accel_limit"))
    trajDecelLbl.append(Label(tk, text = "traj decel_limit"))
    CurrentLimLbl.append(Label(tk, text = "current_lim"))
    trajVelVal.append(Label(tk, text = "wfc"))
    trajAccelVal.append(Label(tk, text = "wfc"))
    trajDecelVal.append(Label(tk, text = "wfc"))
    CurrentLimVal.append(Label(tk, text = "wfc"))
    trajVelBox.append(Entry(tk, width=10))
    trajAccelBox.append(Entry(tk, width=10))
    trajDecelBox.append(Entry(tk, width=10))
    CurrentLimBox.append(Entry(tk, width=10))
    FirstPosLbl.append(Label(tk, text = "First position"))
    SecondPosLbl.append(Label(tk, text = "Second position"))
    FirstPosBox.append(Entry(tk, width=10))
    SecondPosBox.append(Entry(tk, width=10))
    GoBtn.append(Button(tk, text="Go", command=GoFunk0))
    GoBtn.append(Button(tk, text="Go", command=GoFunk1))
    GoBtn.append(Button(tk, text="Go", command=GoFunk2))
    GoBtn.append(Button(tk, text="Go", command=GoFunk3))

    kpLbl[a].place(x=(10+(a*300)), y=80)
    kvLbl[a].place(x=(10+(a*300)), y=100)
    kiLbl[a].place(x=(10+(a*300)), y=120)
    kpVal[a].place(x=(150+(a*300)), y=80)
    kvVal[a].place(x=(150+(a*300)), y=100)
    kiVal[a].place(x=(150+(a*300)), y=120)
    kpBox[a].place(x=(200+(a*300)), y=80)
    kvBox[a].place(x=(200+(a*300)), y=100)
    kiBox[a].place(x=(200+(a*300)), y=120)
    trajVelLbl[a].place(x=(10+(a*300)), y=140)
    trajAccelLbl[a].place(x=(10+(a*300)), y=160)
    trajDecelLbl[a].place(x=(10+(a*300)), y=180)
    CurrentLimLbl[a].place(x=(10+(a*300)), y=200)
    trajVelVal[a].place(x=(150+(a*300)), y=140)
    trajAccelVal[a].place(x=(150+(a*300)), y=160)
    trajDecelVal[a].place(x=(150+(a*300)), y=180)
    CurrentLimVal[a].place(x=(150+(a*300)), y=200)
    trajVelBox[a].place(x=(200+(a*300)), y=140)
    trajAccelBox[a].place(x=(200+(a*300)), y=160)
    trajDecelBox[a].place(x=(200+(a*300)), y=180)
    CurrentLimBox[a].place(x=(200+(a*300)), y=200)
    FirstPosLbl[a].place(x=(10+(a*300)), y=240)
    SecondPosLbl[a].place(x=(10+(a*300)), y=260)
    FirstPosBox[a].place(x=(200+(a*300)), y=240)
    SecondPosBox[a].place(x=(200+(a*300)), y=260)
    GoBtn[a].place(x=(200+(a*300)), y=300)
    a = a + 1
    canvas.pack()


def draw():
    a = 0
    while a <=3:

        kpLbl.append(Label(tk, text = "pos_gain"))
        kvLbl.append(Label(tk, text = "vel_gain"))
        kiLbl.append(Label(tk, text = "vel_integrator_gain"))
        kpVal.append(Label(tk, text = "wfc"))
        kvVal.append(Label(tk, text = "wfc"))
        kiVal.append(Label(tk, text = "wfc"))
        kpBox.append(Entry(tk, width=10))
        kvBox.append(Entry(tk, width=10))
        kiBox.append(Entry(tk, width=10))
        trajVelLbl.append(Label(tk, text = "traj vel_limit"))
        trajAccelLbl.append(Label(tk, text = "traj accel_limit"))
        trajDecelLbl.append(Label(tk, text = "traj decel_limit"))
        CurrentLimLbl.append(Label(tk, text = "current_lim"))
        trajVelVal.append(Label(tk, text = "wfc"))
        trajAccelVal.append(Label(tk, text = "wfc"))
        trajDecelVal.append(Label(tk, text = "wfc"))
        CurrentLimVal.append(Label(tk, text = "wfc"))
        trajVelBox.append(Entry(tk, width=10))
        trajAccelBox.append(Entry(tk, width=10))
        trajDecelBox.append(Entry(tk, width=10))
        CurrentLimBox.append(Entry(tk, width=10))

        kpLbl[a].place(x=(10+(a*300)), y=80)
        kvLbl[a].place(x=(10+(a*300)), y=100)
        kiLbl[a].place(x=(10+(a*300)), y=120)
        kpVal[a].place(x=(150+(a*300)), y=80)
        kvVal[a].place(x=(150+(a*300)), y=100)
        kiVal[a].place(x=(150+(a*300)), y=120)
        kpBox[a].place(x=(200+(a*300)), y=80)
        kvBox[a].place(x=(200+(a*300)), y=100)
        kiBox[a].place(x=(200+(a*300)), y=120)
        trajVelLbl[a].place(x=(10+(a*300)), y=140)
        trajAccelLbl[a].place(x=(10+(a*300)), y=160)
        trajDecelLbl[a].place(x=(10+(a*300)), y=180)
        CurrentLimLbl[a].place(x=(10+(a*300)), y=200)
        trajVelVal[a].place(x=(150+(a*300)), y=140)
        trajAccelVal[a].place(x=(150+(a*300)), y=160)
        trajDecelVal[a].place(x=(150+(a*300)), y=180)
        CurrentLimVal[a].place(x=(150+(a*300)), y=200)
        trajVelBox[a].place(x=(200+(a*300)), y=140)
        trajAccelBox[a].place(x=(200+(a*300)), y=160)
        trajDecelBox[a].place(x=(200+(a*300)), y=180)
        CurrentLimBox[a].place(x=(200+(a*300)), y=200)

        a = a + 1


def OdrvParams():
    a = 0
    kpVal[a].configure(text = odrv0.axis0.controller.config.pos_gain)
    kvVal[a].configure(text = odrv0.axis0.controller.config.vel_gain)
    kiVal[a].configure(text = odrv0.axis0.controller.config.vel_integrator_gain)
    trajVelVal[a].configure(text = odrv0.axis0.trap_traj.config.vel_limit)
    trajAccelVal[a].configure(text = odrv0.axis0.trap_traj.config.accel_limit)
    trajDecelVal[a].configure(text = odrv0.axis0.trap_traj.config.decel_limit)
    CurrentLimVal[a].configure(text = odrv0.axis0.motor.config.current_lim)
    a = a +1
    kpVal[a].configure(text = odrv0.axis1.controller.config.pos_gain)
    kvVal[a].configure(text = odrv0.axis1.controller.config.vel_gain)
    kiVal[a].configure(text = odrv0.axis1.controller.config.vel_integrator_gain)
    trajVelVal[a].configure(text = odrv0.axis1.trap_traj.config.vel_limit)
    trajAccelVal[a].configure(text = odrv0.axis1.trap_traj.config.accel_limit)
    trajDecelVal[a].configure(text = odrv0.axis1.trap_traj.config.decel_limit)
    CurrentLimVal[a].configure(text = odrv0.axis1.motor.config.current_lim)
    a = a +1
    kpVal[a].configure(text = odrv1.axis0.controller.config.pos_gain)
    kvVal[a].configure(text = odrv1.axis0.controller.config.vel_gain)
    kiVal[a].configure(text = odrv1.axis0.controller.config.vel_integrator_gain)
    trajVelVal[a].configure(text = odrv1.axis0.trap_traj.config.vel_limit)
    trajAccelVal[a].configure(text = odrv1.axis0.trap_traj.config.accel_limit)
    trajDecelVal[a].configure(text = odrv1.axis0.trap_traj.config.decel_limit)
    CurrentLimVal[a].configure(text = odrv1.axis0.motor.config.current_lim)
    a = a +1
    kpVal[a].configure(text = odrv1.axis1.controller.config.pos_gain)
    kvVal[a].configure(text = odrv1.axis1.controller.config.vel_gain)
    kiVal[a].configure(text = odrv1.axis1.controller.config.vel_integrator_gain)
    trajVelVal[a].configure(text = odrv1.axis1.trap_traj.config.vel_limit)
    trajAccelVal[a].configure(text = odrv1.axis1.trap_traj.config.accel_limit)
    trajDecelVal[a].configure(text = odrv1.axis1.trap_traj.config.decel_limit)
    CurrentLimVal[a].configure(text = odrv1.axis1.motor.config.current_lim)

    canvas.create_line(5, 38, 5, 332, fill = "black", width = 4)
    canvas.create_line(305, 40, 305, 330, fill = "black", width = 4)
    canvas.create_line(605, 40, 605, 330, fill = "black", width = 4)
    canvas.create_line(905, 40, 905, 330, fill = "black", width = 4)
    canvas.create_line(1205, 38, 1205, 332, fill = "black", width = 4)
    canvas.create_line(5, 40, 1205, 40, fill = "black", width = 4)
    canvas.create_line(5, 70, 1205, 70, fill = "black", width = 4)
    canvas.create_line(5, 330, 1205, 330, fill = "black", width = 4)

    canvas.pack()


def Drawing():
    canvas.delete("all")
    # canvas.create_rectangle(500, 500, 200, 200, fill = "red")
    draw()
    OdrvParams()
    Entrys()
    canvas.pack()
    tk.update()


def KpNew1(kpGain):
    global odrv0
    kpGain = float(kpBox[0].get())
    odrv0.axis0.controller.config.pos_gain = kpGain
    kpVal[0].configure(text = odrv0.axis0.controller.config.pos_gain)


def KpNew2(kpGain):
    global odrv0
    kpGain = float(kpBox[1].get())
    odrv0.axis1.controller.config.pos_gain = kpGain
    kpVal[1].configure(text = odrv0.axis1.controller.config.pos_gain)


def KpNew3(kpGain):
    global odrv1
    kpGain = float(kpBox[2].get())
    odrv1.axis0.controller.config.pos_gain = kpGain
    kpVal[2].configure(text = odrv1.axis0.controller.config.pos_gain)


def KpNew4(kpGain):
    global odrv1
    kpGain = float(kpBox[3].get())
    odrv1.axis1.controller.config.pos_gain = kpGain
    kpVal[3].configure(text = odrv1.axis1.controller.config.pos_gain)


def KvNew1(kvGain):
    global odrv0
    kvGain = float(kvBox[0].get())
    odrv0.axis0.controller.config.vel_gain = kvGain
    kvVal[0].configure(text = odrv0.axis0.controller.config.vel_gain)


def KvNew2(kvGain):
    global odrv0
    kvGain = float(kvBox[1].get())
    odrv0.axis1.controller.config.vel_gain = kvGain
    kvVal[1].configure(text = odrv0.axis1.controller.config.vel_gain)


def KvNew3(kvGain):
    global odrv1
    kvGain = float(kvBox[2].get())
    odrv1.axis0.controller.config.vel_gain = kvGain
    kvVal[2].configure(text = odrv1.axis0.controller.config.vel_gain)


def KvNew4(kvGain):
    global odrv1
    kvGain = float(kvBox[3].get())
    odrv1.axis1.controller.config.vel_gain = kvGain
    kvVal[3].configure(text = odrv1.axis1.controller.config.vel_gain)


def KiNew1(kiGain):
    global odrv0
    kiGain = float(kiBox[0].get())
    odrv0.axis0.controller.config.vel_integrator_gain = kiGain
    kiVal[0].configure(text = odrv0.axis0.controller.config.vel_integrator_gain)


def KiNew2(kiGain):
    global odrv0
    kiGain = float(kiBox[1].get())
    odrv0.axis1.controller.config.vel_integrator_gain = kiGain
    kiVal[1].configure(text = odrv0.axis1.controller.config.vel_integrator_gain)


def KiNew3(kiGain):
    global odrv1
    kiGain = float(kiBox[2].get())
    odrv1.axis0.controller.config.vel_integrator_gain = kiGain
    kiVal[2].configure(text = odrv1.axis0.controller.config.vel_integrator_gain)


def KiNew4(kiGain):
    global odrv1
    kiGain = float(kiBox[3].get())
    odrv1.axis1.controller.config.vel_integrator_gain = kiGain
    kiVal[3].configure(text = odrv1.axis1.controller.config.vel_integrator_gain)


def trajVelNew1(trajVel):
    global odrv0
    trajVel = float(trajVelBox[0].get())
    odrv0.axis0.trap_traj.config.vel_limit = trajVel
    trajVelVal[0].configure(text = odrv0.axis0.trap_traj.config.vel_limit)


def trajVelNew2(trajVel):
    global odrv0
    trajVel = float(trajVelBox[1].get())
    odrv0.axis1.trap_traj.config.vel_limit = trajVel
    trajVelVal[1].configure(text = odrv0.axis1.trap_traj.config.vel_limit)


def trajVelNew3(trajVel):
    global odrv1
    trajVel = float(trajVelBox[2].get())
    odrv1.axis0.trap_traj.config.vel_limit = trajVel
    trajVelVal[2].configure(text = odrv1.axis0.trap_traj.config.vel_limit)


def trajVelNew4(trajVel):
    global odrv1
    trajVel = float(trajVelBox[3].get())
    odrv1.axis1.trap_traj.config.vel_limit = trajVel
    trajVelVal[3].configure(text = odrv1.axis1.trap_traj.config.vel_limit)


def trajAccelNew1(trajAccel):
    global odrv0
    trajAccel = float(trajAccelBox[0].get())
    odrv0.axis0.trap_traj.config.accel_limit = trajAccel
    trajAccelVal[0].configure(text = odrv0.axis0.trap_traj.config.accel_limit)


def trajAccelNew2(trajAccel):
    global odrv0
    trajAccel = float(trajAccelBox[1].get())
    odrv0.axis1.trap_traj.config.accel_limit = trajAccel
    trajAccelVal[1].configure(text = odrv0.axis1.trap_traj.config.accel_limit)


def trajAccelNew3(trajAccel):
    global odrv1
    trajAccel = float(trajAccelBox[2].get())
    odrv1.axis0.trap_traj.config.accel_limit = trajAccel
    trajAccelVal[2].configure(text = odrv1.axis0.trap_traj.config.accel_limit)


def trajAccelNew4(trajAccel):
    global odrv1
    trajAccel = float(trajAccelBox[3].get())
    odrv1.axis1.trap_traj.config.accel_limit = trajAccel
    trajAccelVal[3].configure(text = odrv1.axis1.trap_traj.config.accel_limit)


def trajDecelNew1(trajDecel):
    global odrv0
    trajDecel = float(trajDecelBox[0].get())
    odrv0.axis0.trap_traj.config.decel_limit = trajDecel
    trajDecelVal[0].configure(text = odrv0.axis0.trap_traj.config.decel_limit)


def trajDecelNew2(trajDecel):
    global odrv0
    trajDecel = float(trajDecelBox[1].get())
    odrv0.axis1.trap_traj.config.decel_limit = trajDecel
    trajDecelVal[1].configure(text = odrv0.axis1.trap_traj.config.decel_limit)


def trajDecelNew3(trajDecel):
    global odrv1
    trajDecel = float(trajDecelBox[2].get())
    odrv1.axis0.trap_traj.config.decel_limit = trajDecel
    trajDecelVal[2].configure(text = odrv1.axis0.trap_traj.config.decel_limit)


def trajDecelNew4(trajDecel):
    global odrv0
    trajDecel = float(trajDecelBox[3].get())
    odrv1.axis1.trap_traj.config.decel_limit = trajDecel
    trajDecelVal[3].configure(text = odrv1.axis1.trap_traj.config.decel_limit)


def CurrentLimBox1(CurrentLim):
    global odrv0
    CurrentLim = float(CurrentLimBox[0].get())
    odrv0.axis0.motor.config.current_lim = CurrentLim
    CurrentLimVal[0].configure(text = odrv0.axis0.motor.config.current_lim)


def CurrentLimBox2(CurrentLim):
    global odrv0
    CurrentLim = float(CurrentLimBox[1].get())
    odrv0.axis1.motor.config.current_lim = CurrentLim
    CurrentLimVal[1].configure(text = odrv0.axis1.motor.config.current_lim)


def CurrentLimBox3(CurrentLim):
    global odrv1
    CurrentLim = float(CurrentLimBox[2].get())
    odrv1.axis0.motor.config.current_lim = CurrentLim
    CurrentLimVal[2].configure(text = odrv1.axis0.motor.config.current_lim)


def CurrentLimBox4(CurrentLim):

    global odrv1
    CurrentLim = float(CurrentLimBox[3].get())
    odrv1.axis1.motor.config.current_lim = CurrentLim
    CurrentLimVal[3].configure(text = odrv1.axis1.motor.config.current_lim)


def Save0():

    global odrv0
    odrv0.save_configuration()


def Save1():

    global odrv1
    odrv1.save_configuration()


def Reboot0():

    global odrv0
    odrv0.reboot()


def Reboot1():
    global odrv1
    odrv1.reboot()


kpBox[0].bind('<Return>', KpNew1)
kpBox[1].bind('<Return>', KpNew2)
kpBox[2].bind('<Return>', KpNew3)
kpBox[3].bind('<Return>', KpNew4)
kvBox[0].bind('<Return>', KvNew1)
kvBox[1].bind('<Return>', KvNew2)
kvBox[2].bind('<Return>', KvNew3)
kvBox[3].bind('<Return>', KvNew4)
kiBox[0].bind('<Return>', KiNew1)
kiBox[1].bind('<Return>', KiNew2)
kiBox[2].bind('<Return>', KiNew3)
kiBox[3].bind('<Return>', KiNew4)
trajVelBox[0].bind('<Return>', trajVelNew1)
trajVelBox[1].bind('<Return>', trajVelNew2)
trajVelBox[2].bind('<Return>', trajVelNew3)
trajVelBox[3].bind('<Return>', trajVelNew4)
trajAccelBox[0].bind('<Return>', trajAccelNew1)
trajAccelBox[1].bind('<Return>', trajAccelNew2)
trajAccelBox[2].bind('<Return>', trajAccelNew3)
trajAccelBox[3].bind('<Return>', trajAccelNew4)
trajDecelBox[0].bind('<Return>', trajDecelNew1)
trajDecelBox[1].bind('<Return>', trajDecelNew2)
trajDecelBox[2].bind('<Return>', trajDecelNew3)
trajDecelBox[3].bind('<Return>', trajDecelNew4)
CurrentLimBox[0].bind('<Return>', CurrentLimBox1)
CurrentLimBox[1].bind('<Return>', CurrentLimBox2)
CurrentLimBox[2].bind('<Return>', CurrentLimBox3)
CurrentLimBox[3].bind('<Return>', CurrentLimBox4)


def XYMove():
    Drawing()


SyncButton0 = Button(tk, text="Connect odrv0", command=Drive1Sync).place(x=10, y=340)
SyncButton1 = Button(tk, text="Connect odrv1", command=Drive2Sync).place(x=610, y=340)
SaveButton0 = Button(tk, text="Save odrv0", command=Save0).place(x=10, y=370)
SaveButton1 = Button(tk, text="Save odrv1", command=Save1).place(x=610, y=370)
RebootButton0 = Button(tk, text="Reboot odrv0", command=Reboot0).place(x=10, y=400)
RebootButton1 = Button(tk, text="Reboot odrv1", command=Reboot1).place(x=610, y=400)

tk.mainloop()
