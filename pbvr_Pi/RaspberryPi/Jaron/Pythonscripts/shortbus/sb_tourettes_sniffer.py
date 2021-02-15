#!/usr/bin/env python3

#this program just goes through the various inclines and makes a table for you

import serial
import sb_lib
import os
import sys

#===============main=====================
if os.name == 'nt':
    pr = 'COM'
    i = '1'
else:
    pr = '/dev/ttyUSB'
    i = '0' 
if(len(sys.argv) > 1):
    i = str(sys.argv[1])
pt = pr
pr += i
i = str(int(i)+1)
if(len(sys.argv) > 2):
    i = str(sys.argv[2])
pt += i

#open port 
serRx = serial.Serial(
    port=pr,
    baudrate=38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)
serTx = serial.Serial(
    port=pt,
    baudrate=38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

serRx.isOpen();#just a safety check
serTx.isOpen();#just a safety check

print("Welcome to the ShortBus Tourettes Mode Sniffer")
print(" you know, that kid in the back that always had the funny smile?")
print(" sit back and relax as the messages come through")
print(" type 'ctl+c' to quit")


nmr = bytearray(b"")
nmt = bytearray(b"")
while 1:
    nmr += sb_lib.recieve(serRx) 
    if(len(nmr)):
        i = sb_lib.findmsg(nmr,True)
        nmr = nmr[i:]
    nmt += sb_lib.recieve(serTx) 
    if(len(nmt)):
        i = sb_lib.findmsg(nmt,True)
        nmt = nmt[i:]
ser.close();

