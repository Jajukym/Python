#!/usr/bin/evn python3

#this program just goes through the various inclines and makes a table for you

import serial
import time
import binascii
import sb_lib
import readline
import os
import sys
import subprocess

#open lxterminal and type "sudo systemctl enable pigpiod" to support import pigpio
import pigpio
import RPi.GPIO as IO


def common():
    print("see wiki for commands")
    print("")

#===============main=====================
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

print("Welcome to the ShortBus Terminal")
"""print(" type a ShortBus command and hit enter and it will be sent")
print(" use format \"address command data\" for quicker entry")
print(" omit the 3rd argument (data) for a get, otherwise it")
print(" assumes its a set command")
print(" type 'q' to quit")"""

"""GPIO=3 #for pedal encoder hardware verification
square = []
#                          ON       OFF    MICROS
square.append(pigpio.pulse(1<<GPIO, 0,       113))
square.append(pigpio.pulse(0,       1<<GPIO, 10))
pi = pigpio.pi() # connect to local Pi
pi.set_mode(GPIO, pigpio.OUTPUT)
pi.wave_add_generic(square)
wid = pi.wave_create()
if wid >= 0:
   pi.wave_send_repeat(wid)
   time.sleep(.1)
   #pi.wave_tx_stop()
   #pi.wave_delete(wid)
   #m = bytearray(b"")
   print("\n\n----------------------------------------------------")
   print("                  Encoder verify")
   print("----------------------------------------------------")
   sb_lib.sendMsg(ser,"51 5")
   time.sleep(3)"""
   
   
IO.setwarnings(False)           #do not show any warnings
IO.setmode (IO.BCM)         #we are programming the GPIO by BCM pin numbers. (PIN5 as ‘GPIO3’)
IO.setup(3,IO.OUT)           # initialize GPIO3 as an output.
p = IO.PWM(3,10)          #GPIO3 as PWM output, with 10Hz frequency
p.start(10)                              #generate PWM signal with 50% duty cycle

while 1:
   print("\n\n----------------------------------------------------")
   print("               Tach verify")
   print("----------------------------------------------------")
   sb_lib.sendMsg(ser,"51 2")
   time.sleep(3)
   
   
   
#input("Press Enter to run again.")
#subprocess.Popen("%Run sb_terminal_mod.py", shell=True)