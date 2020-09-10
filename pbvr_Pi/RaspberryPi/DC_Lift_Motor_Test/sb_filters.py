#!/usr/bin/env python3

#this program just goes through the various inclines and makes a table for you

import serial
import sb_lib
import os
import sys
import time
import math

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

print("Welcome to the ShortBus Sniffer")
print(" you know, that kid in the back that always had the funny smile?")
print(" sit back and relax as the messages come through")
print(" type 'ctl+c' to quit")

time.sleep(1)

nm = bytearray(b"")
deadline = 4
while 1:
    sb_lib.send(ser,sb_lib.sbifyst("27 3"))
    m = bytearray(b"")
    timeout = 0
    while m.find(b"\n") < 0 and timeout < deadline:
        timeout += 1
        m += sb_lib.recieve(ser)
    if m.find(b"\n") > 0 and m.find(b":") >=0:
        accel = sb_lib.breakupSBdata(m) 
        acc = [accel[0], accel[1], accel[2], accel[3]]
        if(acc[0] > 0x7fff):
            acc[0] = acc[0]-0x10000
        if(accel[1] > 0x7fff):
            acc[1] = acc[1]-0x10000
        if(acc[2] > 0x7fff):
            acc[2] = acc[2]-0x10000
        if(acc[3] > 0x7fff):
            acc[3] = acc[3]-0x10000

        print(acc[0],acc[1],acc[2],acc[3])
    else:
        print("timeout ", m)
ser.close();

