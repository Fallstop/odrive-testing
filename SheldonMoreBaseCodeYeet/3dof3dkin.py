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
import PlixLayouts as fl
from array import *
import csv

Plix = []

tk = Tk()
Width = 1000
Height = 1000
x =0
y =100
z =-5
Txy = 25
u = 0
a = True
OldAngle = 0
Begin = 0
tk.geometry('1000x1000')
canvas = Canvas(tk, width = Width, height = Height)
tk.title("3Dof Graphics")

xlab = Label(tk, text="x").place(x=0, y=0)
# xlab.grid(column=0, row=1)
ylab = Label(tk, text="y").place(x=0, y=30)
# ylab.grid(column=1, row=1)
zlab = Label(tk, text="z").place(x=0, y=60)
# zlab.grid(column=1, row=1)
xVal = Entry(tk, width=10)
xVal.place(x=20, y=0)
yVal = Entry(tk, width=10)
yVal.place(x=20, y=30)
zVal = Entry(tk, width=10)
zVal.place(x=20, y=60)
# xVal.grid(column=0, row=2)
# yVal.grid(column=1, row=2)
# zVal.grid(column=2, row=2)
PlixSizedd = Combobox(tk)
PlixSizedd['values'] = ("Not Set", "P22", "P25", "P27", "P30", "P33")
PlixSizedd.current(0)
PlixSizedd.place(x=20, y = 140)


def SetPlix():
    global CupNumber
    selected = PlixSizedd.get()
    if selected == "Not Set":
        print("No size")
    elif selected == "P22":
        print("P22")
        with open('Plix22.txt') as csv_file:
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
        global a
        while a:

            NewFruit()
            nexty = ((Plix[u][0]) + 60)
            nextx = ((Plix[u][1]) - 245)
            clicked()
            PutnPick()
            clicked()
            ZReset()
            clicked()
            newz = - 150
            newy = ((Plix[u][0]) + 60)
            newx = ((Plix[u][1]) - 245)
            u = u +1
            clicked()
            PutnPick()
            clicked()
            ZReset()
            clicked()
            if not a:
                break
            if u == 10:
                u = 0
            if not a:
                break

    thread = threading.Thread(target=run)
    thread.start()


def Drawing():
    global r1
    global theta_1
    global theta_2
    global theta_3
    global z
    global OldAngle
    global CupNumber
    global Txy
    global TopArm
    global Bicep
    global ForeArm
    global Tool
    global TopEnd
    global TopStart
    global ArmEnd
    global ArmStart
    global Begin
    basex = 120
    basey= 245
    shoulderx = 120
    shouldery = 500
    plixx = 180
    plixy = 10
    x_end = basex + (r1+25) * cos(deg2rad(OldAngle))
    y_end = basey + (r1+25) * sin(deg2rad(OldAngle))
    x_elbow = shoulderx - 150 * cos(deg2rad(theta_2))
    y_elbow = shouldery + 150 * sin(deg2rad(theta_2))
    x_wrist = x_elbow + 200 * cos(deg2rad(theta_3+theta_2))
    y_wrist = y_elbow + 200 * sin(deg2rad(theta_3+theta_2))

    if (Begin == 0):
        canvas.delete("all")
        i = 0
        canvas.create_rectangle(plixx, plixy, plixx+290, plixy+470, fill = "red")
        while i < CupNumber:
            canvas.create_oval((Plix[i][0])-20+180, Plix[i][1]-30, Plix[i][0]+20+180, Plix[i][1]+30, fill = 'blue')
            i = i + 1
            if i == CupNumber:
                break

        TopArm = canvas.create_line(basex, basey, x_end, y_end, fill = "green", width = 5)
        Bicep = canvas.create_line(shoulderx, shouldery, x_elbow, y_elbow, fill = "blue", width = 5)
        ForeArm = canvas.create_line(x_elbow, y_elbow, shoulderx + r1, shouldery - z+60, fill = "blue", width = 5)
        Tool = canvas.create_line(shoulderx + r1, shouldery - z+60, shoulderx + r1 +Txy, shouldery - z+60, fill = "blue", width = 5)
        TopEnd = canvas.create_oval(x_end-4, y_end-4, x_end+4, y_end+4, fill = "purple")
        TopStart = canvas.create_oval(basex-4, basey-4, basex+4, basey+4, fill = "red")
        ArmEnd = canvas.create_oval(shoulderx + r1-4+Txy, shouldery - z+60-4, shoulderx + r1+4+Txy, shouldery - z+60+4, fill = "purple")
        ArmStart = canvas.create_oval(shoulderx-4, shouldery-4, shoulderx+4, shouldery+4, fill = "red")
        Begin = Begin + 1
        canvas.pack()
        tk.update()

    canvas.coords(TopArm, basex, basey, x_end, y_end)
    canvas.coords(Bicep, shoulderx, shouldery, x_elbow, y_elbow)
    canvas.coords(ForeArm, x_elbow, y_elbow, shoulderx + r1, shouldery - z+60)
    canvas.coords(Tool, shoulderx + r1, shouldery - z+60, shoulderx + r1 +Txy, shouldery - z+60)
    canvas.coords(TopEnd, x_end-4, y_end-4, x_end+4, y_end+4)
    canvas.coords(TopStart, basex-4, basey-4, basex+4, basey+4)
    canvas.coords(ArmEnd, shoulderx + r1-4+Txy, shouldery - z+60-4, shoulderx + r1+4+Txy, shouldery - z+60+4)
    canvas.coords(ArmStart, shoulderx-4, shouldery-4, shoulderx+4, shouldery+4)


def clicked():
    global x
    global y
    global z
    global newx
    global newy
    global newz
    global r1
    global theta_1
    global theta_2
    global theta_3
    global OldAngle
    global nextx
    global nexty
    global Txy

    x = int(x)
    y = int(y)
    z = int(z)
    newx = int(newx)
    newy = int(newy)
    newz = int(newz)
    a1 = 60
    a2 = 150
    a3 = 230
    Resolution = 1
    Distance = sqrt(((x - newx)**2) + ((y - newy)**2))
    z1 = z

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

            if z == newz:
                z = z
            if(z > newz):
                z = z -Resolution
            if(z < newz):
                z = z +Resolution
        if (Distance > 0):
            CurrentDistance = sqrt(((x - newx)**2) + ((y - newy)**2))
            z = -150+((80)*sin((pi*CurrentDistance)/(Distance)))
            Resolution = 1+((int(CurrentDistance/10))*sin((pi*CurrentDistance)/(Distance)))
            Resolution = int(Resolution)

        theta_1 = rad2deg(arctan2(nextx, nexty))

        r1 = sqrt(y**2 + x**2) - Txy

        r2 = z - a1

        phi_2 = arctan2(r2, r1)

        r3 = sqrt(r1**2+r2**2)

        cat = (a3**2-a2**2-r3**2)

        dog = (-2*a2*r3)

        phi_1 = arccos(cat/dog)

        theta_2 = -rad2deg(phi_2 - phi_1)

        phi_3 = arccos((r3**2-a2**2-a3**2)/(-2*a2*a3))

        theta_3 = (180-rad2deg(phi_3))

        theta_2 = 180 - theta_2
        if OldAngle == theta_1:
            OldAngle = OldAngle
        if(OldAngle > theta_1):
            OldAngle = OldAngle -1
        if(OldAngle < theta_1):
            OldAngle = OldAngle +1

        # print((theta_1))
        # print((theta_2))
        # print((theta_3))
        Drawing()

        if (x == newx and y == newy and z == newz):
            break


def NewFruit():
    global newx
    global newy
    global newz
    newx = int(00)
    newy = int(0)
    newz = int(-150)


def PutnPick():
    global newz
    newz = int(-170)


def ZReset():
    global newz
    newz = int(-150)


def XYMove():

    global newx
    global newy
    global newz
    newx = xVal.get()
    newy = yVal.get()
    newz = zVal.get()
    clicked()


def Start():
    global a
    a = True
    PlixMovement()


def Stop():
    global a
    a = False


XYButton = Button(tk, text="X Y pos move", command=XYMove).place(x=20, y=90)
SetPlixSize = Button(tk, text="Set Size", command=SetPlix).place(x=20, y=170)
PlixButton = Button(tk, text="Plix Run", command=Start).place(x=20, y=200)
PlixButton1 = Button(tk, text="Plix Pause", command=Stop).place(x=20, y=230)
# XYButton.grid(column=4, row=2)


canvas.pack()

tk.mainloop()
