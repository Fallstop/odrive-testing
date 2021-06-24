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


def PlixRead():
    global CupNumber
    with open('Plix.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            Plix.append([])
            Plix[line_count].append(row[0])
            Plix[line_count].append(row[1])
            Plix[line_count].append('0')
            line_count += 1
        CupNumber = line_count
        print(line_count)

PlixRead()
print(Plix)
