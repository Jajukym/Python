#!/usr/bin/env python3

#this program runs the drive motor at 5mph and runs the incline 4 cycles ending on 15% incline 

import serial
import time
import binascii
import delta_lib
import oly_lib
import sb_lib
import math
import os
import sys

#===============main=====================

# this defines the movement, each line is (seconds, position)
# seconds is the time since the start of the routine, position is olympus reckoning


#incline does 4 cycles in 8 minutes and rests for 52 minutes doing 4 cycles every hour
#rename routine to incroutine
routine = ((0,6),(30,36),(330,6),)
           #,(180,36),(240,6),(300,36),(360,6),(420,36),(3600,6),)

print(routine)

#run 5mph
hztomph = 1295.646
targmph = hztomph*5 

#open port 
olyser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)
#accser = serial.Serial(
#    port='/dev/ttyUSB0',
#    baudrate=38400,
#    parity=serial.PARITY_NONE,
#    stopbits=serial.STOPBITS_TWO,
#    bytesize=serial.SEVENBITS
#)

olyser.isOpen();#just a safety check
#accser.isOpen();#just a safety check


oly_lib.sendMsg(olyser,"Iwdi 0")
time.sleep(5)
start = time.time()
retry = 0
i = 0
pos = 0
dcnt = 0
ccnt = 0
targ = routine[i][1]
oly_lib.sendMsg(olyser,"Iwdi %i" %targ)
m = oly_lib.sendMsg(olyser,"Irci")
if(len(m)):
    pos = oly_lib.getOlydata(m)
m = oly_lib.sendMsg(olyser,"Ircc")
if(len(m)):
    ccnt = oly_lib.getOlydata(m)
m = oly_lib.sendMsg(olyser,"Irdc")
if(len(m)):
    dcnt = oly_lib.getOlydata(m)

#f = open("oly_test_w_accel_%s.csv"%time.asctime(time.localtime(time.time()-21600)).replace(" ","_"),"a")
#send delta 5mph
delta_lib.sendMsg(olyser,"2000 0x12");

delta_lib.sendMsg(olyser,"2001 %i" %targmph);
while 1:
    #send the next command (if its time)
    if(time.time() > start+routine[i][0]):
        targ = routine[i][1]
        retry = 0
        delta_lib.sendMsg(olyser,"2001 %i" %targmph)
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
    delta_lib.sendMsg(olyser,"2000 0x12");
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
    #m = sb_lib.sendMsg(accser,"27 2")
    #if(len(m)):
        #sb_lib.printSBdata(m)
    #    accel = sb_lib.breakupSBdata(m) 
    #    if(accel):
    #        if(len(accel)>2):
    #             f.write("%f, %i, %i, %i, %i, %i, %i, %i\n"%(time.time(),targ,pos,accel[0],accel[1],accel[2],dcnt,ccnt))

    

ser.close();

print("good job, son")
