#!/usr/bin/env python3

#this program just alternates between various incline positions

import serial
import time
import binascii
import sb_lib
import math
import readline
import os
import sys
#===============main=====================

if os.name == 'nt':
    pr = 'COM'
    i = '1'
else:
    pr = '/dev/ttyUSB'
    i = '0' 
if(len(sys.argv) > 1):
    i = str(sys.argv[1])
pt = pr
pr += i
i = str(int(i)+1)
if(len(sys.argv) > 2):
    i = str(sys.argv[2])
pt += i

#open port 
serRx = serial.Serial(
    port=pr,
    baudrate=38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)
serTx = serial.Serial(
    port=pt,
    baudrate=38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

serRx.isOpen();#just a safety check
serTx.isOpen();#just a safety check

print("Calibrating...")
st = ""
st2 = ""
done = ""
cycles = ""
calibrate = "41 3 1"
m = bytearray(b"")
m = sb_lib.sbifyst(calibrate)
sb_lib.send(serTx,m)

time.sleep(20)


st = input("Message 1: ")
st2 = input("Message 2: ")
cycles = input("Number of Cycles: ")

currenttime = time.time()

while done != 'n':
	i = 0
	success = 0
	while i < int(cycles):
		#Send the first message
		if(time.time() > currenttime+3 and i%2 == 0):
			m = bytearray(b"")
			m = sb_lib.sbifyst(st)
			sb_lib.send(serTx,m)
			sb_lib.show(m)
			i += 1
			r = sb_lib.getReply(serRx)
			if(not len(r)):
				sb_lib.send(serTx,m)
				sb_lib.show(m)
			success += 1
			print("\n success %d" % (success))
			currenttime = time.time()
		elif(time.time() > currenttime+3 and i%2 == 1):
			m = bytearray(b"")
			m = sb_lib.sbifyst(st2)
			sb_lib.send(serTx,m)
			sb_lib.show(m)
			i += 1
			r = sb_lib.getReply(serRx)
			if(not len(r)):
				sb_lib.send(serTx,m)
				sb_lib.show(m)
			success += 1
			print("\n success %d" % (success))
			currenttime = time.time()
	print("\n success %d \n" % (success))
	done = input("Enter y to repeat or n to exit: ")
	
serRx.close();
serTx.close();
print("good job, son")
