#!/usr/bin/env python3

#this program just alternates between various incline positions

import serial
import time
import binascii
import sb_lib
import math

#=================Time==================

def createTime(timeEl):
    hour = math.floor(timeEl/3600)
    timeEl = timeEl - (hour * 3600)
    min = math.floor(timeEl/60)
    timeEl = timeEl - (min * 60)
    sec = math.floor(timeEl)

    strTime = str(hour) + " hours " + str(min) + " minutes " + str(sec) + " seconds"

    return strTime

#===============Printtofile=====================

def printToFile(info):
    filename = "LifeTestLog.txt"
    file = open(filename, "a")
    file.write(str(time.time()))
    file.write("\n")
    file.write(str(info))
    file.write("\n")
    file.close

#===============main=====================

# this defines the movement, each line is (seconds, position)
# seconds is the time since the start of the routine, position is olympus reckoning

#!open port
sbser = serial.Serial(      
    port='/dev/ttyUSB0',
    baudrate=38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

sbser.isOpen();#just a safety check


needCycles = 3000
currentCycles = 0

# 1 complete cycle every 96 seconds with intermittent stops
timestep = 1  #seconds
routine = ((3,2),(12,20),(24,40),(36,60),(48,78),(60,60),(72,40),(84,20),(96,2),)

cycling = 1
#currentCycle = 1

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
startTime = time.time()
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
        if(i>=len(routine)):
            i = 0

            start = time.time() #if you move this a tab back it will make the time column work relative to the previous command
            if(currentCycles<needCycles):
                currentCycles += 1
                #timeEl = time.time()-startTime
                #strTimeEl = createTime(timeEl)
                print("Current Cycles: " , currentCycles)
                printToFile(currentCycles)
                #print("Current Time: %5d" %timeEl)
                #print("Current Time: ", strTimeEl)
                #printToFile(strTimeEl)

            
#            currentCycle += 1
#            print("Cycle Number: ")
#            print(currentCycle)
#            start = time.time() #if you move this a tab back it will make the time column work relative to the previous command
    #or resend if there was no response
            
    elif(retry):
        retry = 0;
        m = sb_lib.sendMsg(sbser,"41 1 %i" %targ )
        if(not len(m)):
            retry = 1;

ser.close();

print("good job, son")
