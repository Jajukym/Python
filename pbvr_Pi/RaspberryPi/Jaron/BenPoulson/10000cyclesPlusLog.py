#!/usr/bin/env python3

#this program just alternates between various incline positions

import serial
import time
import binascii
import sb_lib
import math


#===============Switch===================

def switchRoutine():
    global currentTimer
    global highRoutine
    global lowRoutine
    global highTime
    global lowTime
    global routine
    global highRest
    global lowRest
    global restLen

    if (currentTimer == highTime):
        currentTimer = lowTime
        routine = lowRoutine
        restLen = lowRest
        print("Changing to Low Duty Cycle")
    elif(currentTimer == lowTime):
        currentTimer = highTime
        routine = highRoutine
        restLen = highRest
        print("Changing to High Duty Cycle")
    else:
        currentTimer = highTime
        routine = highRoutine
        print("ERROR: Unable to determine current duty cycle. Changing to High Duty Cycle")



#=================Time==================

def createTime(timeEl):
    hour = math.floor(timeEl/3600)
    timeEl = timeEl - (hour * 3600)
    min = math.floor(timeEl/60)
    timeEl = timeEl - (min * 60)
    sec = math.floor(timeEl)

    strTime = str(hour) + " hours " + str(min) + " minutes " + str(sec) + " seconds"

    return strTime

#=================Check Pos==================

def checkPosition():
    global sbser
    
    for i in range(0,100):
        m = sb_lib.sendMsg(sbser, "41 2")
        time.sleep(.1)
        if (len(m)):#(m.find(b"\n") > 0 and (m.find(b":") > 0)):
            curpos = sb_lib.breakupSBdata(m)[0]
            break
        else:
            print("There was a problem")
            curpos = -1
            

    return curpos


#=================Go to Position==================
def goPos(pos):
    global sbser
    
    while 1:
        m = sb_lib.sendMsg(sbser, "41 1 %i" % pos)
        time.sleep(.1)
        if(not len(m)):
            pass
        else:
            break
    

#=================Create Routine==================

def createRoutine():
    global HighTimestep
    global LowTimestep
    global maxPos
    global minPos
    global maxPosHalf
    global minPosHalf
    global initialWait
    global highRoutine
    global lowRoutine
    global sbser

    initialWait = 1
    maxPos = 50
    minPos = 20
    maxPosHalf = 40
    minPosHalf = 30

    #make sure incline is known
    goPos(maxPos)
    print("Going to max...")
    while 1:
        pos = checkPosition()
        if (pos == maxPos):
            break
        time.sleep(1)

    #Max to min time (Full Stroke)
    goPos(minPos)
    print("Going to min...")
    start = time.time()
    while 1:
        pos = checkPosition()
        if (pos == minPos):
            LowTimestep = time.time()-start + 1  # seconds half cycle
            print("LowTimestep = ", LowTimestep)
            break
        time.sleep(1)

    #make sure incline is known
    goPos(maxPosHalf)
    print("Going to max...")
    while 1:
        pos = checkPosition()
        if (pos == maxPosHalf):
            break
        time.sleep(1)


    # Max to min time (Full Stroke)
    goPos(minPosHalf)
    print("Going to min...")
    start = time.time()
    while 1:
        pos = checkPosition()
        if (pos == minPosHalf):
            HighTimestep = time.time() - start + 1  # seconds half cycle
            print("HighTimestep = ", HighTimestep)
            break
        time.sleep(1)




    highRoutine = ((initialWait, minPosHalf), (initialWait + HighTimestep, maxPosHalf), (initialWait + 2 * HighTimestep, minPosHalf),)
    lowRoutine = ((initialWait, minPos), (initialWait + LowTimestep, maxPos), (initialWait + 2 * LowTimestep, minPos),)

#===============Printtofile=====================

def printToFile(info):
    filename = "PBLogDC1.txt"
    file = open(filename, "a")
    file.write(str(time.time()))
    file.write("\n")
    file.write(str(info))
    file.write("\n")
    file.close


#===============main=====================


# this defines the movement, each line is (seconds, position)
# seconds is the time since the start of the routine, position is olympus reckoning


highRest = 0
lowRest = 3*60
restLen = highRest
subSet = 18

highTime = 10*60
lowTime = 50*60

#!open port
sbser = serial.Serial(      
    port='/dev/ttyUSB0',
    baudrate=38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

sbser.isOpen();#just a safety check

#createRoutine()
initialWait = 3
HighTimestep = 9
LowTimestep = 17
maxPos = 50
minPos = 20
maxPosHalf = 40
minPosHalf = 30
highRoutine = ((initialWait, minPosHalf), (initialWait + HighTimestep, maxPosHalf), (initialWait + (2 * HighTimestep), minPosHalf),)
lowRoutine = ((initialWait, minPos), (initialWait + LowTimestep, maxPos), (initialWait + (2 * LowTimestep), minPos),)




routine = highRoutine
currentTimer = highTime

needCycles = 45000
currentCycles = 1

driftCycles = 1000
driftCount = 0

cycling = 1

numRetry = 0
maxRetry = 10000

#routine = ((5,2),)
#for i in range(5,26,5):
#	routine += ((i*timestep+5,i),)
#for i in range(0,24,5):
#	routine += ((i*timestep+24*timestep,25-i),)

print(routine)



sbser.isOpen();#just a safety check


#!oly_lib.sendMsg(olyser,"Iwdi 0")

time.sleep(5)
start = time.time()
startTime = time.time()
highLowTimer = time.time()
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
    if(time.time()-highLowTimer >= currentTimer):
        switchRoutine()
        highLowTimer = time.time()
    #send the next command (if its time)
    time.sleep(1)
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
                driftCount += 1
                timeEl = time.time()-startTime
                strTimeEl = createTime(timeEl)
                print("Current Cycles: " , currentCycles)
                printToFile(currentCycles)
                #print("Current Time: %5d" %timeEl)
                print("Current Time: ", strTimeEl)
                printToFile(strTimeEl)
                if(currentCycles%subSet == 0):
                    if(driftCount >= driftCycles):
                        driftCount = 0
                        recal = sb_lib.sendMsg(sbser,"41 3 0" )
                        print("Recalibrating...")
                        printToFile("Recalibrating")
                        time.sleep(LowTimestep * 3)
                        #while cycling:
                            #if(checkPosition()!=40):
                                #time.sleep(5)
                            #else:
                                #createRoutine()
                                #break
                    print("Time to rest!")
                    printToFile("Time to rest!")
                    time.sleep(restLen)
                    start = time.time()
            else:
                cycling = 0
    #or resend if there was no response
    elif(retry):
        #numRetry += 1
        #if(numRetry>=maxRetry):
            #cycling = 0
        retry = 0;
        m = sb_lib.sendMsg(sbser,"41 1 %i" %targ )
        if(not len(m)):
            retry = 1;
        #else:
            #numRetry = 0
ser.close();

print("good job, son")

