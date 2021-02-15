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


timestep = 11  #seconds half cycle
initialWait = 3
maxPos = 60
minPos = 20
restLen = 1.5*60
subSet = 15
routine = ((initialWait,minPos),(timestep,maxPos),(2*timestep,minPos),)

needCycles = 10000
currentCycles = 0

cycling = 1

numRetry = 0
maxRetry = 10

#routine = ((5,2),)
#for i in range(5,26,5):
#	routine += ((i*timestep+5,i),)
#for i in range(0,24,5):
#	routine += ((i*timestep+24*timestep,25-i),)

print(routine)

#!open port
sbser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

sbser.isOpen();#just a safety check


#!oly_lib.sendMsg(olyser,"Iwdi 0")

time.sleep(5)
start = time.time()
retry = 0
i = 0
pos = 0
dcnt = 0
ccnt = 0
targ = routine[i][1]
#!oly_lib.sendMsg(olyser,"Iwdi %i" %targ )
#!m = oly_lib.sendMsg(olyser,"Irci")
#!if(len(m)):
#!    pos = oly_lib.getOlydata(m)
#!m = oly_lib.sendMsg(olyser,"Ircc")
#!if(len(m)):
#!    ccnt = oly_lib.getOlydata(m)
#!m = oly_lib.sendMsg(olyser,"Irdc")
#!if(len(m)):
#!    dcnt = oly_lib.getOlydata(m)

while cycling:
    #send the next command (if its time)
    if(time.time() > start+routine[i][0]):
        targ = routine[i][1]
        retry = 0
        m = sb_lib.sendMsg(sbser,"41 1 %i" %targ )
        print(targ)
        i += 1 
        if(not len(m)):
            retry = 1;
        else:
            numRetry = 0
        if(i>=len(routine)):
            i = 0
            start = time.time() #if you move this a tab back it will make the time column work relative to the previous command
            if(currentCycles<needCycles):
                currentCycles += 1
                print("Current Cycles: " , currentCycles)
                if(currentCycles%subSet == 0):
                    print("Time to rest!")
                    time.sleep(restLen)
                    start = time.time()
            else:
                cycling = 0
    #or resend if there was no response
    elif(retry):
        numRetry += 1
        if(numRetry>=maxRetry):
            cycling = 0
        retry = 0;
        m = sb_lib.sendMsg(sbser,"41 1 %i" %targ )
        if(not len(m)):
            retry = 1;
        else:
            numRetry = 0
ser.close();

print("good job, son")
