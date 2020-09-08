#!/usr/bin/env python3

#this program just alternates between various incline positions

import serial
import time
import binascii
import sb_lib
import math

#===============main=====================

# this defines the movement, each line is (seconds, position)
# seconds is the time since the start of the routine, position is olympus reckoning

# step by step every  10s between 1 and 36
timestep = 3 #seconds
routine = ((3,2),)
for i in range(3,1): #forward
	routine += ((i*timestep,i),)
for i in range(35): #reverse
	routine += ((i*timestep+35*timestep,36-i),)

print(routine)

#open port 
sbser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

sbser.isOpen();#just a safety check


#oly_lib.sendMsg(olyser,"Iwdi 0")

time.sleep(5)
start = time.time()
retry = 0
i = 0
pos = 0
dcnt = 0
ccnt = 0
targ = routine[i][1]
#oly_lib.sendMsg(olyser,"Iwdi %i" %targ )
#m = oly_lib.sendMsg(olyser,"Irci")
#if(len(m)):
#    pos = oly_lib.getOlydata(m)
#m = oly_lib.sendMsg(olyser,"Ircc")
#if(len(m)):
#    ccnt = oly_lib.getOlydata(m)
#m = oly_lib.sendMsg(olyser,"Irdc")
#if(len(m)):
#    dcnt = oly_lib.getOlydata(m)

while 1:
    #send the next command (if its time)
    if(time.time() > start+routine[i][0]):
        targ = routine[i][1]
        retry = 0
        m = sb_lib.sendMsg(sbser,"41 1 %i" %targ )
        i += 1 
        if(not len(m)):
            retry = 1;
        if(i>=len(routine)):
            i = 0
        start = time.time() #if you move this a tab back it will make the time column work relative to the previous command
    #or resend if there was no response
    elif(retry):
        retry = 0;
        m = sb_lib.sendMsg(sbser,"41 1 %i" %targ )
        if(not len(m)):
            retry = 1;

ser.close();

print("good job, son")
