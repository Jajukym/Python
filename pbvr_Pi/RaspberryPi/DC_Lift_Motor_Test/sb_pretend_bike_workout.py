#!/usr/bin/env python3

#this program just alternates between various incline positions

import serial
import time
import binascii
import sb_lib
import math
import random

#===============main=====================

# this sends incline and resistance on a random walk with random period
# seconds is the time since the start of the routine, position is sb reckoning

minres = 20
maxres = 200
mincline = 0
maxcline = 60

timestep = 1 #seconds
steps = 50

incrange = maxcline-mincline
resrange = maxres-minres

#open port 
sbser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

sbser.isOpen();#just a safety check


inc = mincline
res = minres
start = time.time()
mi = ""
m = ""
while 1:
    #send the next incline
    inc = min(max(inc+random.randrange(-5,5),mincline),maxcline)
    mi = sb_lib.sendMsg(sbser,"41 1 %i" % inc)
    #send the next resistance
    res = min(max(res+random.randrange(-20,20),minres),maxres)
    m = sb_lib.sendMsg(sbser,"61 5 %i" % res)
    if(len(m) == 0 and len(mi) == 0):
        print("I think we are frozen?",time.time()-start)
        sbser.close()
        exit()
    #wait a random amount of time
    time.sleep(max(.1,random.gauss(2,1)))

ser.close();

