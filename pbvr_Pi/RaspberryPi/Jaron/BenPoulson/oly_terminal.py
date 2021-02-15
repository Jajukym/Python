#!/usr/bin/env python3

#this program just goes through the various inclines and makes a table for you

import serial
import time
import binascii
import oly_lib
import readline
import os
import sys


def common():
    print("commands:")
    print("  Ir__ read param __")
    print("  Iw__xx write xx to param __")
    print(" ")
    print("params:")
    print("  di desired incl.")
    print("  ci current incl.")
    print("  si stop incl.")
    print("  tm transmax")
    print("  cv code version")
    print("  mi max incl.")
    print("  ai actual max")
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

print(p) 

#open port 
ser = serial.Serial(
    port=p,
    baudrate=38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

ser.isOpen();#just a safety check

print("Welcome to the Olympus Terminal")
print(" type an Olympus command and hit enter and it will be sent")
print(" (omit start, stop and xsum bytes)")
print(" you can also follow with a number that")
print(" will be appended to the message (e.g. Irtm 29)")
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
        m = oly_lib.sendMsg(ser,st)
        if(len(m)):
            v = oly_lib.getOlydata(m)
            print(" returned: ",v," (", hex(v),")")
    elif(st != 'q'):
        m = bytearray(b"")
        m = oly_lib.getReply(ser)
        if(len(m)):
            v = oly_lib.getOlydata(m)
            print(" returned: ",v," (", hex(v),")")


ser.close();

print("fwhew! Is that all?")
