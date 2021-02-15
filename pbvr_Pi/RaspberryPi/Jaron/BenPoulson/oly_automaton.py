#!/usr/bin/env python3

#this program just alternates between various incline positions

import serial
import time
import binascii
import oly_lib

#===============main=====================

#open port 
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

ser.isOpen();#just a safety check

#ask rhymebus what the transmax is 
a = oly_lib.sendMsg(ser,"Irtm")
maxIncl = oly_lib.getOlydata(a)
print("here's your transmax:",maxIncl,"(",hex(maxIncl),")")

if not maxIncl:
    print("calibrating...")
    oly_lib.sendMsg(ser,"Iwca")
    input("enter when done calibrating ")
    print("here's your transmax:")
    a = oly_lib.sendMsg(ser,"Irtm")
    maxIncl = oly_lib.getOlydata(a)
    print("here's your transmax:",maxIncl,"(",hex(maxIncl),")")

maxIncl = 36 #hardcoded to the treadmill

#send the olympus to the bottom and wait 5 seconds
oly_lib.sendMsg(ser,"Iwdi 0")
time.sleep(5)

#should alternate between 1% and 7% grade indefinitely
while 1:
    oly_lib.sendMsg(ser,"Iwdi 8")
    time.sleep(15)

    oly_lib.sendMsg(ser,"Iwdi 20")
    time.sleep(10)
    

ser.close();

print("good job, son")
