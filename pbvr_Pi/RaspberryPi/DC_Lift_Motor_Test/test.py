#!/usr/bin/env python3

#this program just goes through the various inclines and makes a table for you

import serial
import time
import binascii
import sb_lib
import readline
import os
import sys


def common():
    print("addresses:")
    print(" x21 motor controller    x51 speed")
    print(" x27 accelerometer       x61 resistance")
    print(" x41 incline")
    print("")
    st = input("type an address to get available commands (e.g. 41): ")
    if(st == "41"):
        print("incline commands:")
        print(" x1 target       x8 actual (phys) max")
        print(" x2 current      x9 neg. offset")
        print(" x3 calibrate    xA OL up")
        print(" x4 stop         xB OL down")
        print(" x5 transmax     xC transZero")
        print(" x6 min          xD Use Time")
        print(" x7 max          x15 FB timeout")
        print("                 x16 OL speed")
        print("")
    elif(st == "61"):
        print("resistance commands:")
        print(" x1 OL up        x6 current")
        print(" x2 OL down      x7 min")
        print(" x3 stop         x8 max")
        print(" x4              x9 ")
        print(" x5 target       xA step loss (stepper mtr)")
        print("")
    elif(st == "51"):
        print("speeeed commands:")
        print(" x1 mph          x4 cadence")
        print(" x2 rpm          x5 pedal position")
        print(" x3 rpm*100      ")
        print("")
    elif(st == "27"):
        print("accelerometer commands:")
        print(" x1 device id    x6 arm len")
        print(" x2 axis data    x7 arc distance")
        print(" x3 slope data   x8 arc speed")
        print(" x4 axis config     ")
        print(" x5 state        ")
        print("")
    else:
        print("spencer was too lazy to type in that one")
    print("")


print("Welcome to the ShortBus Terminal")
print(" type a ShortBus command and hit enter and it will be sent")
print(" use format \"address command data\" for quicker entry")
print(" omit the 3rd argument (data) for a get, otherwise it")
print(" assumes its a set command")
print(" type 'q' to quit")


#a = [int(s) for s in st.replace(',',' ').split() if s.isdigit()]
st = ""
while st != 'q':
    print("")
    st = input("Next message (h for help, q to quit): ")
    if(st and st != 'q'):
        if(st == 'h'):
            common();
            continue
        m = bytearray(b"")
        m = sb_lib.sendMsg(ser,st)
        if(len(m)):
            sb_lib.printSBdata(m)



