#!/usr/bin/env python3

#this program just goes through the various inclines and makes a table for you

import serial
import time
import binascii
import delta_lib
import readline
import os
import sys


def common():
    print("Register:")
    print("2000 Function -x11 stop, x12 start")
    print("2001 Frequency")
    print("2002 Reset")
    print("2100 Error Code")
    print("2104 Output Current")

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

print("Welcome to the Delta Terminal")
print(" type a Delta command and hit enter and it will be sent")
print(" use format \"address data\" for quicker entry")
print(" omit the 2nd argument (data) for a get, otherwise it")
print(" assumes it's a set command")
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
        m = delta_lib.sendMsg(ser,st)
        #if(len(m)):
        #    delta_lib.printDeltadata(m)


ser.close();

print("fwhew! Is that all?")
