#!/usr/bin/env python3

#this program just goes through the various inclines and makes a table for you

import serial
import oly_lib
import os
import sys

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

print("Welcome to the Olympus Sniffer")
print(" sit back and relax as the messages come through")
print(" type 'ctl+c' to quit")


nm = bytearray(b"")
while 1:
    nm += oly_lib.recieve(ser) 
    if(len(nm)):
        i = oly_lib.findmsg(nm,1)
        nm = nm[i:]
ser.close();

