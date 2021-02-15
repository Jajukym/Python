#!/usr/bin/env python3

#this program just alternates between various incline positions

import serial
import time
import binascii
import oly_lib
import sb_lib
import math

#===============main=====================

# this defines the movement, each line is (seconds, position)
# seconds is the time since the start of the routine, position is olympus reckoning

# step by step every  10s between 1 and 36
routine = ((3,2),)
for i in range(3,37):
	routine += ((i*10,i),)
for i in range(35):
	routine += ((i*10+35*10,36-i),)

print(routine)

#open port 
olyser = serial.Serial(
    port='/dev/ttyUSB1',
    baudrate=38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)
accser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

olyser.isOpen();#just a safety check
accser.isOpen();#just a safety check


oly_lib.sendMsg(olyser,"Iwdi 0")
time.sleep(5)
start = time.time()
retry = 0
i = 0
pos = 0
dcnt = 0
ccnt = 0
targ = routine[i][1]
oly_lib.sendMsg(olyser,"Iwdi %i" %targ )
m = oly_lib.sendMsg(olyser,"Irci")
if(len(m)):
    pos = oly_lib.getOlydata(m)
m = oly_lib.sendMsg(olyser,"Ircc")
if(len(m)):
    ccnt = oly_lib.getOlydata(m)
m = oly_lib.sendMsg(olyser,"Irdc")
if(len(m)):
    dcnt = oly_lib.getOlydata(m)

f = open("oly_test_w_accel_%s.csv"%time.asctime(time.localtime(time.time()-21600)).replace(" ","_"),"a")
while 1:
    #send the next command (if its time)
    if(time.time() > start+routine[i][0]):
        targ = routine[i][1]
        retry = 0
        m = oly_lib.sendMsg(olyser,"Iwdi %i" %targ )
        i += 1 
        if(len(m)):
            pos = math.floor(oly_lib.getOlydata(m)/127)
        else:
            retry = 1;
        if(i>=len(routine)):
            i = 0
            start = time.time() #if you move this a tab back it will make the time column work relative to the previous command
    #or resend if there was no response
    elif(retry):
        retry = 0;
        m = oly_lib.sendMsg(olyser,"Iwdi %i" %targ )
        if(len(m)):
            pos = math.floor(oly_lib.getOlydata(m)/127)
        else:
            retry = 1;

    #now ask for the current incline
    m = oly_lib.sendMsg(olyser,"Irci")
    if(len(m)):
        pos = oly_lib.getOlydata(m)
        if(pos>36):
            pos = math.floor(oly_lib.getOlydata(m)/127)
    #then target count
    m = oly_lib.sendMsg(olyser,"Irdc")
    if(len(m)):
        dcnt = oly_lib.getOlydata(m)
    #then current count
    m = oly_lib.sendMsg(olyser,"Ircc")
    if(len(m)):
        ccnt = oly_lib.getOlydata(m)
	
    #finally the accelerometer
    m = sb_lib.sendMsg(accser,"27 2")
    if(len(m)):
        #sb_lib.printSBdata(m)
        accel = sb_lib.breakupSBdata(m) 
        if(accel):
            if(len(accel)>2):
                 f.write("%f, %i, %i, %i, %i, %i, %i, %i\n"%(time.time(),targ,pos,accel[0],accel[1],accel[2],dcnt,ccnt))

    

ser.close();

print("good job, son")
