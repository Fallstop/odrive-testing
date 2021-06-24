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

OldAngle = 0
u = 0


def PlixLoader():
    #print("PlixLoader")
    global CupNumber
    Plix = []
    with open('Plix30.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            Plix.append([])
            Plix[line_count].append(int(row[0]))
            Plix[line_count].append(int(row[1]))
            line_count += 1
        CupNumber = line_count
    return Plix


def NewFruit(Position_List):
    #print("NewFruit")
    x = Position_List[0]
    y = Position_List[1]
    z = Position_List[2]
    Newx = Position_List[3]
    Newy = Position_List[4]
    Newz = Position_List[5]
    Nextx = Position_List[6]
    Nexty = Position_List[7]
    Newx = int(00)
    Newy = int(0)
    Newz = int(-150)
    Position_List = [x, y, z, Newx, Newy, Newz, Nextx, Nexty]
    return Position_List


def PutnPick(Position_List):
    #print("PutnPick")
    x = Position_List[0]
    y = Position_List[1]
    z = Position_List[2]
    Newx = Position_List[3]
    Newy = Position_List[4]
    Newz = Position_List[5]
    Nextx = Position_List[6]
    Nexty = Position_List[7]
    Newz = int(-200)
    Position_List = [x, y, z, Newx, Newy, Newz, Nextx, Nexty]
    return Position_List


def ZReset(Position_List):
    #print("ZReset")
    x = Position_List[0]
    y = Position_List[1]
    z = Position_List[2]
    Newx = Position_List[3]
    Newy = Position_List[4]
    Newz = Position_List[5]
    Nextx = Position_List[6]
    Nexty = Position_List[7]
    Newz = int(-150)
    Position_List = [x, y, z, Newx, Newy, Newz, Nextx, Nexty]
    return Position_List


def NextPosition(Position_List, Distance):
    x = Position_List[0]
    y = Position_List[1]
    z = Position_List[2]
    Newx = Position_List[3]
    Newy = Position_List[4]
    Newz = Position_List[5]
    Nextx = Position_List[6]
    Nexty = Position_List[7]
    Resolution = 1

    if x == Newx:
        x = x
    if(x > Newx):
        x = x -Resolution
    if(x < Newx):
        x = x +Resolution
    if y == Newy:
        y = y
    if(y > Newy):
        y = y -Resolution
    if(y < Newy):
        y = y +Resolution
    if (Distance == 0):
        if z == Newz: #might have to get rid of this or keep and rename z as we wont know the current distance
            z = z      # other option would be to ignore z all together and just use xy for distance and have it seperate from ramp
        if(z > Newz):
            z = z -Resolution
        if(z < Newz):
            z = z +Resolution
    if (Distance > 0):
        CurrentDistance = sqrt(((x - Newx)**2) + ((y - Newy)**2))
        z = -150+((80)*sin((pi*CurrentDistance)/(Distance)))

    x = int(x)
    y = int(y)
    z = int(z)
    #print("x ", x)
    #print("y ", y)
    #print("z ", z)
    Position_List = [x, y, z, Newx, Newy, Newz, Nextx, Nexty]
    return Position_List


def Kinematics(Position_List):
    #print("Kinematics")
    global OldAngle
    Resolution = 1
    x = Position_List[0]
    y = Position_List[1]
    z = Position_List[2]
    Nextx = Position_List[6]
    Nexty = Position_List[7]
    # firstly the robot dimentions are defined
    a1 = 60 # mount to shoulder mm
    a2 = 150 # upper arm length, pivot to pivot mm
    a3 = 200 # eblow legnth, pivot to pivot mm
    Txy = 25 # tool legth from the write pivot to tool center (only in xy direction)

    theta_1 = rad2deg(arctan2(Nextx, Nexty))
    r1 = sqrt(y**2 + x**2) -Txy
    r2 = z - a1
    phi_2 = arctan2(r2, r1)
    r3 = sqrt(r1**2+r2**2)
    phi_1 = arccos((a3**2-a2**2-r3**2)/(-2*a2*r3))
    theta_2 = -rad2deg(phi_2 - phi_1)
    phi_3 = arccos((r3**2-a2**2-a3**2)/(-2*a2*a3))
    theta_3 = (180-rad2deg(phi_3))
    theta_2 = 180 - theta_2

    if OldAngle == theta_1:
        OldAngle = OldAngle
    if(OldAngle > theta_1):
        OldAngle = OldAngle -Resolution
    if(OldAngle < theta_1):
        OldAngle = OldAngle +Resolution
    Angle_List = [OldAngle, theta_2, theta_3]
    return Angle_List


def AngleToStep(Angle_List):
    #print("AngleToStep")

    BaseSteps = (Angle_List[0] * 22.755) - 920 # top motor
    ShoulderSteps = -((Angle_List[1] * 22.755) - 870)  # this zeros to have the arms up flat at 90 angle have a look at this maths
    ElbowSteps = (Angle_List[2] * 45.511) - (5040 - ((Angle_List[1] * 22.755)))# elbow which is adjusted with the steps of the shoulder
    BaseSteps = int(BaseSteps)
    ShoulderSteps = int(ShoulderSteps)
    ElbowSteps = int(ElbowSteps)
    Step_List = [BaseSteps, ShoulderSteps, ElbowSteps]
    return Step_List


def RunMovement(Position_List):
    #print("RunMovement")

    x = Position_List[0]
    y = Position_List[1]
    z = Position_List[2]
    Newx = Position_List[3]
    Newy = Position_List[4]
    Newz = Position_List[5]
    Nextx = Position_List[6]
    Nexty = Position_List[7]
    Distance = sqrt(((x - Newx)**2) + ((y - Newy)**2))
    while (x != Newx or y != Newy or z != Newz):
        Position_List = NextPosition(Position_List, Distance)
        Angle_List = Kinematics(Position_List)
        # passed_list inside useTheList is set to what is returned from defineAList
        Step_List = AngleToStep(Angle_List)
        #SendMove(Step_List)
        #time.sleep(0.1)
        #PositionWait(Step_List)
        x = Position_List[0]
        y = Position_List[1]
        z = Position_List[2]
        Newx = Position_List[3]
        Newy = Position_List[4]
        Newz = Position_List[5]
        Nextx = Position_List[6]
        Nexty = Position_List[7]
        with open(r'Full30', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(Step_List)

    return Position_List


def Main():
    global u
    global CupNumber
    Plix = PlixLoader()
    Position_List = [0, 100, -150, 0, 0, 0, 0, 0]
    #Position_List = PlixToCoord(Plix, Position_List)
    Distance = sqrt(((Position_List[0] - Position_List[3])**2) + ((Position_List[1] - Position_List[4])**2))
    Position_List = NextPosition(Position_List, Distance)
    Angle_List = Kinematics(Position_List)
    # passed_list inside useTheList is set to what is returned from defineAList
    Step_List = AngleToStep(Angle_List)

    while u <10:
        Position_List = NewFruit(Position_List)
        Position_List = NextPoint(Plix, Position_List)
        Position_List = RunMovement(Position_List)
        Position_List = PutnPick(Position_List)
        Position_List = RunMovement(Position_List)
        Position_List = ZReset(Position_List)
        Position_List = RunMovement(Position_List)
        Position_List = NewPoint(Plix, Position_List)
        Position_List = RunMovement(Position_List)
        Position_List = PutnPick(Position_List)
        Position_List = RunMovement(Position_List)
        Position_List = ZReset(Position_List)
        Position_List = RunMovement(Position_List)


def NewPoint(Plix, Position_List):
    #print("NewPoint")
    global u
    #print(u)
    x = Position_List[0]
    y = Position_List[1]
    z = Position_List[2]
    Newx = Position_List[3]
    Newy = Position_List[4]
    Newz = Position_List[5]
    Nextx = Position_List[6]
    Nexty = Position_List[7]

    #Newz = - 150
    Newy = (((Plix[u][0]) + 60))
    Newx = (((Plix[u][1]) - 235))
    print(u)
    u = u + 1
    if u ==30:# change to cup number in the future and end program here
        print("end")
        sleep.time(5)
    Position_List = [x, y, z, Newx, Newy, Newz, Nextx, Nexty]
    return Position_List


def NextPoint(Plix, Position_List):
    #print("NextPoint")
    global u

    x = Position_List[0]
    y = Position_List[1]
    z = Position_List[2]
    Newx = Position_List[3]
    Newy = Position_List[4]
    Newz = Position_List[5]
    Nextx = Position_List[6]
    Nexty = Position_List[7]
    #Newz = - 150
    Nexty = ((Plix[u][0]) + 60)
    Nextx = ((Plix[u][1]) - 235)

    Position_List = [x, y, z, Newx, Newy, Newz, Nextx, Nexty]
    return Position_List



Main()
