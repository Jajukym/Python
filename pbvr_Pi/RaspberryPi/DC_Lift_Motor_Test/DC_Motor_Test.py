#!/usr/bin/evn python3

#this program just goes through the various inclines and makes a table for you

import serial
import time
import binascii
import sb_lib
import readline
import os
import sys
import subprocess
#import numpy as np


def common():
    print("see wiki for commands")
    print("")

#===============main=====================
if os.name == 'nt':
    p = 'COM'
    i = '0'
else:
    p = '/dev/ttyUSB'
    i = '0' 
if(len(sys.argv) > 1):
    i = str(sys.argv[1])
p += i

#open port 
ser = serial.Serial(
    port=p,
    baudrate=38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

ser.isOpen();#just a safety check

print("Welcome to the DC Motor Test")

#partnumber = ["419474", "415172", "415473", "415904", "423419"]
#transmax = np.array([2.48, 2.85, 4.25, 7.01, 6.35])
smpl = 0
cyc = 0
cont = ""
smpl = int(input("Sample Size:"))
sb_lib.transmax()
while cyc < smpl:
    print("\n\n----------------------------------------------------")#test
    print("                  DC Lift Test#: ", (cyc + 1))
    print("----------------------------------------------------")
    sb_lib.sendMsg(ser,"41 5 10")#set transmax to ~0
    #sb_lib.sendMsg(ser,"41 11")
    #loop 3 times
    sb_lib.sendMsg(ser,"41 a 1")#push
    time.sleep(2)
    sb_lib.sendMsg(ser,"41 4 1")#pause
    time.sleep(3)
    sb_lib.sendMsg(ser,"41 a 1")#push
    time.sleep(3)
    sb_lib.sendMsg(ser,"41 3 1")#calibrate
    #sb_lib.wait()
    time.sleep (50)#timer for calibration
    #sb_lib.sendMsg(ser,"41 5")
    print("\n---------------Transmax Verify----------------")

    st = "41 5"
    m = bytearray(b"")
    m = sb_lib.sendMsg(ser,st)
    print(m)
    if(len(m)):
        sb_lib.printSBdata(m)
    cyc += 1
    cont = input("Enter To Continue. 'n' To End")
    if cont == "n":
        print("Bye-Bye!")
        break
print("Test Complete")
print((cyc), "Samples Completed")
