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


def common():
    print("see wiki for commands")
    print("")

#===============main=====================
if os.name == 'nt':
    p = 'COM'
    i = '0'
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

GPIO=3 #for pedal encoder hardware verification
square = []

#                          ON       OFF    MICROS
square.append(pigpio.pulse(1<<GPIO, 0,       10000))#113 encoder, 1000 lowrestach
square.append(pigpio.pulse(0,       1<<GPIO, 10000))#10 encoder, 333333 lowrestach




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
   #sb_lib.sendMsg(ser, "41 5 xx")
   print("\n\n----------------------------------------------------")
   print("                Incline Verify")
   print("----------------------------------------------------")
#   sb_lib.sendMsg(ser,"41 3 01")#calibration
   sb_lib.sendMsg(ser,"41 5 99")#transmax set
   sb_lib.sendMsg(ser,"41 5")#transmax read
   sb_lib.sendMsg(ser,"41 2")#Currentlocation
   sb_lib.sendMsg(ser,"41 1 20")#inclineRet
   time.sleep(3)
   sb_lib.sendMsg(ser,"41 1 2")#InclineExt
   print("\n\n----------------------------------------------------")
   print("                  Revision_Read verify")
   print("----------------------------------------------------")
   #m = bytearray(b"")
   sb_lib.sendMsg(ser, "41 F1")#code version
   sb_lib.sendMsg(ser, "41 F2")#hardware number
   sb_lib.sendMsg(ser, "41 F3")#software number
   time.sleep(3)
   print("\n\n----------------------------------------------------")
   print("                  Tach verify")
   print("----------------------------------------------------")
   sb_lib.sendMsg(ser,"51 2")#lowrestach
   
   print("\n\n----------------------------------------------------")
   print("               Resistance Clockwise")
   print("----------------------------------------------------")
   sb_lib.sendMsg(ser,"61 5 69")
   time.sleep(3)
   
   print("\n\n----------------------------------------------------")
   print("          Resistance Counter Clockwise")
   print("----------------------------------------------------")
   sb_lib.sendMsg(ser,"61 5 25")
   sb_lib.sendMsg(ser,"41 5 10")#transmax set
   sb_lib.sendMsg(ser,"41 5")#transmax set
   pi.wave_tx_stop()
   pi.wave_delete(wid)
   
   



"""#a = [int(s) for s in st.replace(',',' ').split() if s.isdigit()]
st = ""
while st != 'q':
    print("")
    st = input("Next message (h for help, q to quit): ")
    if(st and st != 'q'):
        if(st == 'h'):
            common();
            continue
        m = bytearray(b"")
        m = sb_lib.sendMsg(ser,st)
        #if(len(m)):
        #    sb_lib.printSBdata(m)


ser.close();

print("fwhew! Is that all?")"""
#input("Press Enter to run again.")
#subprocess.Popen("%Run sb_terminal_mod.py", shell=True)
"""with open("422_test.py") as f:
    code = compile(f.read(), "422_test.py", 'exec')
    exec(code, global_vars, local_vars)"""
 
 