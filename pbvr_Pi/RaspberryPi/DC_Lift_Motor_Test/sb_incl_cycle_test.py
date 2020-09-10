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

timestep = .3 #seconds
lo = 1 #sb incl val
hi = 39 #sb incl val

# step by step every pos between lo and hi
routine = ((timestep,lo),)
for i in range(lo+1,hi+1):
	routine += ((i*timestep,i),)
for i in range(hi-lo):
	routine += (((i+hi-lo)*timestep,hi-i),)

# 2 up 1 down, then reverse
routine = ((0,lo),)
for i in range(0,hi-lo-1):
	routine += (((2*i+1)*timestep,lo+i+2),((2*i+2)*timestep,lo+i+1))
for i in range(0,hi-lo):
	routine += (((2*i+2*(hi-lo))*timestep,hi-i-1),((2*i+2*(hi-lo)+1)*timestep,hi-i))
routine += ((4*(hi-lo)*timestep,lo),)
routine = ((0,50),(1,50))

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
