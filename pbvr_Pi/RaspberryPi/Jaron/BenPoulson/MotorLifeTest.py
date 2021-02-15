#!/usr/bin/env python3

#this program just alternates between various motor speeds

import serial
import time
import binascii
import delta_lib
import math
import os
import sys

#===============main=====================
# this defines the movement, each line is (seconds, frequency*100)
# seconds is the time since the start of the routine, freq is rhymebus reckoning
hztomph = 1295.646
tenthhztomph = 129.564
routine = ((0,6*hztomph),)

#Stepping speed going 1 mph for 60 seconds than 2 mph then back to 1 mph. Pattern 1,2,1,3,1,4,1,5 etc  to 15 than it will stop 60 sec go to next workout 2,3,2,4,2,5 etc repeats until 11 mph to 12 mph than moves to next routine
#First workout should be 30 min stop and 28 next whole workout here will be 3 hours 28 minutes
for i in range(1,12):
	routine +=((60,0),)
	for j in range(i+1,13):
		routine += ((60,i*hztomph),)
		routine += ((60,j*hztomph),)
#Go and stop .5 - 12 mph stepping at a tenth of a mile per step stopping on whole numbers
#115 minutes run time with 12 minutes wait
for i in range(5,121):
	routine +=((60,i*tenthhztomph),)
	if(i%10 == 0):
                routine +=((60,0),)
#quick stop 12mph than stop 30 seconds later
#time 15 minutes 7.5 minutes
for i in range(1,16):
	routine +=((60,0),)
	routine +=((30,12*hztomph),)




print(routine)

f = open("MotorLifeTest_%s.csv"%time.asctime(time.localtime(time.time()-21600)).replace(" ","_"),"a")
#get port index from argument
if os.name == 'nt':
    p = 'COM'
    i = '1'
else:
    p = '/dev/ttyUSB'
    i = '0' 
if(len(sys.argv) > 1):
    i = str(sys.argv[1])
p += i

#open port 
ser = serial.Serial(
    port=p,
    baudrate=38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)


ser.isOpen();#just a safety check


#intial complete
complete = 1

#send the run command
delta_lib.sendMsg(ser,"2000 0x12");

#finally the first step in the routine
start = time.time()
i =0
targ = int(routine[i][1])
delta_lib.sendMsg(ser,"2001 %i" %targ);
#retry = 0

while 1:
    #send the next command (if its time)
    if(time.time() > start+routine[i][0]):
        targ = int(routine[i][1])
        #retry = 0
        i += 1 
        #if(len(m)==0):
        #    retry = 1;
        if(i>=len(routine)):
            i = 0
            delta_lib.sendMsg(ser,"2000 0x12")
            f.write("%f, %i\n"%(time.time(),complete))
            complete += 1
            delta_lib.sendMsg(ser,"2000 0x12")
        start = time.time() #if you move this a tab back it will make the time column work relative to the previous command. Done
    #send every time to keepalive
    delta_lib.sendMsg(ser,"2001 %i" %targ);
    #delta_lib.sendMsg(ser,"2000 0x12")
   
    #or resend if there was no response
    #elif(retry):
    #    retry = 0;
    #    delta_lib.sendMsg(ser,rb_lib.rbMsgify(m))
    #    if(len(m)==0):
    #        retry = 1; 
    #m = bytearray(b"\x1a")
    #delta_lib.send(ser,rb_lib.rbMsgify(m))

ser.close();

