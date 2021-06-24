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


def SendMove(passed_list):
    print("Axis 0 steps = ", passed_list[0])
    print("Axis 1 steps = ", passed_list[1])
    print("Axis 2 steps = ", passed_list[2])

    # alao need to get newx,x and next x from the plix layout and load the plix array
def NewFruit():# these need to be done next, add their position to the pos list
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


def NextPosition(Position_List):
    x = Position_List[0]
    y = Position_List[1]
    z = Position_List[2]
    Newx = Position_List[3]
    Newy = Position_List[4]
    Newz = Position_List[5]
    # Position_List = [x, y, z, Newx, Newy, Newz]
    Distance = sqrt(((x - Newx)**2) + ((y - Newy)**2))
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
        Resolution = 1+((int(CurrentDistance/10))*sin((pi*CurrentDistance)/(Distance)))
        Resolution = int(Resolution)

    Position_List = [x, y, z, Newx, Newy, Newz]
    return Position_List


def Kinematics(Position_List):
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

    BaseSteps = (Angle_List[0] * 22.755) - 920 # top motor
    ShoulderSteps = -((Angle_List[1] * 22.755) - 870)  # this zeros to have the arms up flat at 90 angle have a look at this maths
    ElbowSteps = (Angle_List[2] * 45.511) - (5040 - ((Angle_List[1] * 22.755)))# elbow which is adjusted with the steps of the shoulder
    BaseSteps = int(BaseSteps)
    ShoulderSteps = int(ShoulderSteps)
    ElbowSteps = int(ElbowSteps)
    Step_List = [BaseSteps, ShoulderSteps, ElbowSteps]
    return Step_List


def PositionWait(Step_List):
    Accuracy = 400

    Base = odrv1.axis0.encoder.shadow_count
    Shoulder = odrv0.axis0.encoder.shadow_count
    Elbow = odrv0.axis1.encoder.shadow_count
    Base = int(Base)
    Shoulder = int(Shoulder)
    Elbow = int(Elbow)

    BaseLower = Step_List[0] - Accuracy
    BaseUpper = Step_List[0] + Accuracy
    ShoulderLower = Step_List[1] - Accuracy
    ShoulderUpper = Step_List[1] + Accuracy
    ElbowLower = Step_List[2] - Accuracy
    ElbowUpper = Step_List[2] + Accuracy

    while ((BaseUpper < Base) or (BaseLower > Base)):
        Base = odrv1.axis0.encoder.shadow_count
        Base = int(Base)
    while ((ShoulderUpper < Shoulder) or (ShoulderLower > Shoulder)):
        Shoulder = odrv0.axis0.encoder.shadow_count
        Shoulder = int(Shoulder)
    while ((ElbowUpper < Elbow) or (ElbowLower > Elbow)):
        Elbow = odrv0.axis1.encoder.shadow_count
        Elbow = int(Elbow)


def Main():
    Position_List = [1, 2, 3, 0, 0, 0, 1, 1]
    NextPosition(Position_List)
    Angle_List = Kinematics(Position_List)
    # passed_list inside useTheList is set to what is returned from defineAList
    Step_List = AngleToStep(Angle_List)
    print(Step_List)


Main()
