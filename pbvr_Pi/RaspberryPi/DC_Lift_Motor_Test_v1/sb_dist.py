#!/usr/bin/env python3

#this program just goes through the various inclines and makes a table for you

import serial
import sb_lib
import os
import sys
import time

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

nm = bytearray(b"")
deadline = 4
while 1:

    sb_lib.send(ser,sb_lib.sbifyst("27 7"))
    m = bytearray(b"")
    timeout = 0
    while m.find(b"\n") < 0 and timeout < deadline:
        timeout += 1
        m += sb_lib.recieve(ser)
    if m.find(b"\n") > 0 and m.find(b":") >=0:
        dist = sb_lib.breakupSBdata(m) 
    else:
        print("timeout ", m)

    sb_lib.send(ser,sb_lib.sbifyst("27 8"))
    m = bytearray(b"")
    timeout = 0
    while m.find(b"\n") < 0 and timeout < deadline:
        timeout += 1
        m += sb_lib.recieve(ser)
    if m.find(b"\n") > 0 and m.find(b":") >=0:
        spd = sb_lib.breakupSBdata(m) 
        print(spd[0]/100,"kph",dist[0],"m")
    else:
        print("timeout ", m)
ser.close();

