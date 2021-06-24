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


def SendMove(Step_List):
    #print("SendMove")
    global odrv0
    global odrv1
    #print("Axis 0 steps = ", Step_List[0])
    #print("Axis 1 steps = ", Step_List[1])
    #print("Axis 2 steps = ", Step_List[2])
    odrv1.axis0.controller.pos_setpoint = (int(Step_List[0]))
    odrv0.axis0.controller.pos_setpoint = (int(Step_List[1]))
    odrv0.axis1.controller.pos_setpoint = (int(Step_List[2]))


def PlixLoader():
    #print("PlixLoader")
    Plix = []
    with open('Full30.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            Step_List = [int(row[0]), int(row[1]), int(row[2])]
            SendMove(Step_List)
            PositionWait(Step_List)
            line_count += 1
        CupNumber = line_count
    return Plix


def PositionWait(Step_List):
    #print("PositionWait")
    global odrv0
    global odrv1
    Accuracy = 400

    Base = odrv1.axis0.encoder.shadow_count
    Shoulder = odrv0.axis0.encoder.shadow_count
    Elbow = odrv0.axis1.encoder.shadow_count
    Base = int(Base)
    Shoulder = int(Shoulder)
    Elbow = int(Elbow)
    #print("Read = ", Shoulder)
    #print("Sent = ", Step_List[1])

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


def RunMovement(Position_List):
    print("hello")


def Main():
    global u
    while True:
        PlixLoader()
        u = u + 1


print("connecting")
odrv0 = odrive.find_any(serial_number = "208037743548") #Connect ot Odrive0
print("odrv0 connected")
odrv1 = odrive.find_any() #Connect ot Odrive1
print(odrv1)
input()
Main()
