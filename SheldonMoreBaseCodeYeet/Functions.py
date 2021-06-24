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
import csv

Plix = []

x = 0
y = 100
z = -5
OldAngle = 0
tk = Tk()
Width = 1210
Height = 600
tk.geometry('1210x600')# size of the window
canvas = Canvas(tk, width = Width, height = Height) # size of the drawing window
canvas.pack()
tk.title("Man Arm") # title of page
PlixSizedd = Combobox(tk)
PlixSizedd['values'] = ("Not Set", "P22", "P25", "P27", "P30", "P33")
PlixSizedd.current(0)
PlixSizedd.place(x=10, y = 100)


def SetPlix():
    global CupNumber
    selected = PlixSizedd.get()
    if selected == "Not Set":
        print("No size")
    elif selected == "P22":
        print("Line")
        with open('Line.txt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                Plix.append([])
                Plix[line_count].append(int(row[0]))
                Plix[line_count].append(int(row[1]))
                Plix[line_count].append(int(0))
                line_count += 1
            CupNumber = line_count
    elif selected == "P25":
        print("P25")
        with open('Plix25.txt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                Plix.append([])
                Plix[line_count].append(int(row[0]))
                Plix[line_count].append(int(row[1]))
                Plix[line_count].append(int(0))
                line_count += 1
            CupNumber = line_count
    elif selected == "P27":
        print("P27")
        with open('Plix27.txt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                Plix.append([])
                Plix[line_count].append(int(row[0]))
                Plix[line_count].append(int(row[1]))
                Plix[line_count].append(int(0))
                line_count += 1
            CupNumber = line_count
    elif selected == "P30":
        print("P30")
        with open('Plix30.txt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                Plix.append([])
                Plix[line_count].append(int(row[0]))
                Plix[line_count].append(int(row[1]))
                Plix[line_count].append(int(0))
                line_count += 1
            CupNumber = line_count
    elif selected == "P33":
        print("P33")
        with open('Plix33.txt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                Plix.append([])
                Plix[line_count].append(int(row[0]))
                Plix[line_count].append(int(row[1]))
                Plix[line_count].append(int(0))
                line_count += 1
            CupNumber = line_count


def PlixMovement():
    def run():
        global CupNumber
        global newx
        global newy
        global newz
        global nextx
        global nexty
        global u
        u = 0
        global a
        while a:
            while u < CupNumber:
                if not a:
                    break
                newz = - 150
                NewFruit()
                nexty = ((Plix[u][0]) + 60)
                nextx = ((Plix[u][1]) - 235)
                ThreeDoF()
                if not a:
                    break
                PutnPick()
                ThreeDoF()
                if not a:
                    break
                ZReset()
                ThreeDoF()
                if not a:
                    break
                newz = - 150
                newy = (((Plix[u][0]) + 60))
                newx = (((Plix[u][1]) - 235))
                u = u +1
                ThreeDoF()
                if not a:
                    break
                PutnPick()
                ThreeDoF()
                if not a:
                    break
                ZReset()
                ThreeDoF()
                if not a:
                    break
                if u == 10:
                    u = 0
            if not a:
                break

    thread = threading.Thread(target=run)
    thread.start()


def NewFruit():
    global newx
    global newy
    global newz
    newx = int(00)
    newy = int(0)
    newz = int(-150)


def PutnPick():
    global newz
    newz = int(-200)


def ZReset():
    global newz
    newz = int(-150)


def DriveSync():
    print("connecting")
    global odrv0
    global odrv1
    odrv0 = odrive.find_any(serial_number = "208037743548") #Connect ot Odrive0
    print("odrv0 connected")
    odrv1 = odrive.find_any(serial_number = "3762364A3137") #Connect ot Odrive1
    print("odrv1 connected")
    # 208037743548 first odrive
    # 3762364A3137 new odrive


def PickUp():
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


def ThreeDoF():

    global odrv0
    global odrv1
    global newx
    global newy
    global newz
    global x
    global y
    global z
    global nextx
    global nexty
    global Distance
    global OldAngle
    newx = int(newx)
    newy = int(newy)
    newz = int(newz)
    Distance = sqrt(((x - newx)**2) + ((y - newy)**2))

    Resolution = 1

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
        if (Distance == 0):
            if z == newz: #might have to get rid of this or keep and rename z as we wont know the current distance
                z = z      # other option would be to ignore z all together and just use xy for distance and have it seperate from ramp
            if(z > newz):
                z = z -Resolution
            if(z < newz):
                z = z +Resolution
        if (Distance > 0):
            CurrentDistance = sqrt(((x - newx)**2) + ((y - newy)**2))
            z = -150+((80)*sin((pi*CurrentDistance)/(Distance)))
            Resolution = 1+((int(CurrentDistance/10))*sin((pi*CurrentDistance)/(Distance)))
            Resolution = int(Resolution)
            print(Resolution)
        a1 = 60
        a2 = 150
        a3 = 200
        Txy = 25
        # Ramp()

        theta_1 = rad2deg(arctan2(nextx, nexty))

        #xa = int(x - 25 * sin((theta_1)))
        #ya = int(y - 25 * cos((theta_1)))
        #print(ya)
        #r1 = sqrt(ya**2 + xa**2) # dont dunderstand why it wont do the tool of
        r1 = sqrt(y**2 + x**2) -Txy
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
        if OldAngle == theta_1:
            OldAngle = OldAngle
        if(OldAngle > theta_1):
            OldAngle = OldAngle -Resolution
        if(OldAngle < theta_1):
            OldAngle = OldAngle +Resolution
        j1c = OldAngle * 22.755
        j2c = theta_2 * 22.755
        j3c = theta_3 * 45.511
        j1 = j1c - 920 # top motor
        j2 = -(j2c - 870)  # this zeros to have the arms up flat at 90 angle have a look at this maths
        j3 = j3c - (5040 - (j2c))# elbow
        j1 = int(j1)
        j2 = int(j2)
        j3 = int(j3)
        odrv0.axis0.controller.pos_setpoint = (int(j2))
        odrv0.axis1.controller.pos_setpoint = (int(j3))
        odrv1.axis0.controller.pos_setpoint = (int(j1))
        val = odrv0.axis0.encoder.shadow_count
        val1 = odrv0.axis1.encoder.shadow_count
        val2 = odrv1.axis0.encoder.shadow_count
        val2 = int(val2)
        val1 = int(val1)
        val = int(val)

        # print(val2)
        Accuracy = 400

        j4 = j1 - Accuracy
        jj4 = j1 + Accuracy
        j = j2 - Accuracy
        jj = j2 + Accuracy
        j0 = j3 - Accuracy
        jj0 = j3 + Accuracy
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
    MaxAccel = 4500
    MinAccel = 1
    Amplitude = MaxAccel - MinAccel
    CurrentDistance = sqrt(((x - newx)**2) + ((y - newy)**2) + ((z - newz)**2))
    Acceleration = MinAccel + (Amplitude)*sin((pi*CurrentDistance)/(Distance))
    Acceleration = (MaxAccel - (Acceleration))
    print(Acceleration)
    # time.sleep(0.5)

    odrv0.axis1.controller.vel_setpoint = Acceleration
    odrv0.axis0.controller.vel_setpoint = Acceleration
    # odrv1.axis0.controller.vel_setpoint = Acceleration
    # odrv0.axis0.controller.current_setpoint = (Acceleration/10)
    # odrv0.axis1.controller.current_setpoint = (Acceleration/10)
    # odrv1.axis0.controller.current_setpoint = (Acceleration/10)
    # print(Acceleration)


def Start():
    global a
    a = True
    PlixMovement()


def Stop():
    global a
    a = False


SyncButton = Button(tk, text="Connect odrives", command=DriveSync).place(x=10, y=10)

StartButton = Button(tk, text="Start", command=Start).place(x=10, y=40)

StopButton = Button(tk, text="Stop", command=Stop).place(x=10, y=70)

SetPlixSize = Button(tk, text="Set Size", command=SetPlix).place(x=10, y=130)

tk.mainloop()
