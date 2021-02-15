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
    print("see wiki for commands")
    print("")

#===============main=====================
if os.name == 'nt':
    p = 'COM'
    i = '1'
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


ser.close();

print("fwhew! Is that all?")
