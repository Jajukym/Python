import sb_lib
import RPi.GPIO as GPIO
import time
import numpy
import serial
import os
import sys

numpassed = 0
responseposition = 11

#************************Pin Definitions****************
incsense = 20
dmk = 21
desiredtransmax = 3700
#*******************************************************

#***********************GPIO setups*********************
GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

GPIO.setup(incsense, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dmk, GPIO.OUT)
#*******************************************************

#**********************Setup Serial Port****************
if os.name == 'nt':
    p = 'COM'
    i = '1'
else:
    p = '/dev/ttyUSB'
    i = '0' 
if(len(sys.argv) > 1):
    i = str(sys.argv[1])
p += i

ser = serial.Serial(
    port=p,
    baudrate=38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)
#*******************************************************
print()
print("Getting Code Version......") 
response = sb_lib.sendMsg(ser,"41 F1")
version = sb_lib.getSBdata(response)
print("Code Version: ", version)
if version != 4153:
    print()
    print("-------------------------")
    print("Wrong Code Version. Update Hex File")
    print("--------------------------")
else:
    numpassed = numpassed + 1

print()
print("Getting Software Part Number......")
response = sb_lib.sendMsg(ser,"41 F2")
softnum = sb_lib.getSBdata(response)
print()
print("-------------------------------")
print("Software Part Number: ", softnum)

print()
print("Getting Hardware Part Number.....")
response = sb_lib.sendMsg(ser,"41 F3")
hardnum = sb_lib.getSBdata(response)
print()
print("---------------------------------------")
print("Hardware Part Number: ", sb_lib.getSBdata(response))

print()
print("----------------------------------")
print("Checking Transmax Write")
print()
sb_lib.sendMsg(ser, "41 5 3700")
response = sb_lib.sendMsg(ser, "41 5")
actualtransmax = sb_lib.getSBdata(response)
print()
print("Transmax read: ",actualtransmax)
if actualtransmax == desiredtransmax:
    print()
    print("-------------------------------")
    print("Transmax Write Pass")
    numpassed = numpassed + 1
    print("-------------------------------")
    print()
else:
    print()
    print("-------------------------------")
    print("Transmax Write Fail")
    print("-------------------------------")
    print()

GPIO.output(dmk, GPIO.LOW)

print()
print("-------------------------")
print("Starting Incline test....")
print("-------------------------")
sb_lib.sendMsg(ser, "41 1 0")
i = 0
while sb_lib.getSBdata(sb_lib.sendMsg(ser, "41 2")) != 0 and i<100:
    time.sleep(0.2)
    print("Bottom Seeking.....")
    i+=1

currentpos=sb_lib.sendMsg(ser, "41 2")
value = sb_lib.getSBdata(currentpos)
print(value)


sb_lib.sendMsg(ser, "41 1 15")
j = 0
while sb_lib.getSBdata(sb_lib.sendMsg(ser, "41 2")) != 15 and j < 100:
    time.sleep(.2)
    j+=1
    
sb_lib.sendMsg(ser,"41 4 1")


newpos = sb_lib.getSBdata(sb_lib.sendMsg(ser, "41 2"))
if newpos == 15:
    print()
    print("--------------------------------")
    print("First Incline Test Passed!")
    print("--------------------------------")
    numpassed = numpassed + 1
else:
    print()
    print("-------------------------------")
    print("First Incline Test Failed.")
    print("-------------------------------")



currentpos = sb_lib.sendMsg(ser, "41 2")
firstpos = sb_lib.getSBdata(currentpos)
endpos = firstpos + 400

j = 0
sb_lib.sendMsg(ser, "41 1 2")
while sb_lib.getSBdata(sb_lib.sendMsg(ser, "41 2")) != 2 and j<100:
    time.sleep(.2)
    j += 1
    
newpos = sb_lib.getSBdata(sb_lib.sendMsg(ser, "41 2"))
if newpos == 2:
    print()
    print("--------------------------------")
    print("Second Incline Test Passed!")
    print("--------------------------------")
    numpassed = numpassed + 1
else:
    print()
    print("-------------------------------")
    print("Second Incline Test Failed.")
    print("-------------------------------")



print("Starting PWM Test...")
GPIO.add_event_detect(incsense, GPIO.RISING)
sb_lib.sendMsg(ser, "28 1 20")
pulsecounter = 0
endtime = time.time() + 5
while time.time() < endtime:
    if GPIO.event_detected(int(incsense)):
       print("found pulse",pulsecounter)
       pulsecounter += 1
if pulsecounter >= 18:
       print("PWM test Passed")
       numpassed = numpassed+1
else:
        print("PWM test Failed")
        
        
        


GPIO.output(dmk, 1) #set the dmk High
sb_lib.sendMsg(ser, "28 1 20")
pulsecounter = 0
endtime = time.time() + 5
while time.time() < endtime:
    if GPIO.event_detected(int(incsense)):
        print("found pulse",pulsecounter)
        pulsecounter += 1   
        print("found pulse",pulsecounter)
if pulsecounter > 1:
    print()
    print("-----------------------------")
    print("DMK PWM test failed")
    print("-----------------------------")
    print()
else:
    print()
    print("---------------------------")
    print("DMK PWM test Passed!")
    numpassed = numpassed + 1
    print("---------------------------")

print()
print("--------------------------------")
print("DMK incline testing...")
print("--------------------------------")

initpos = sb_lib.getSBdata(sb_lib.sendMsg(ser,"41 2"))

GPIO.output(dmk, 1)
sb_lib.sendMsg(ser, "41 1 7")
time.sleep(5)
if sb_lib.getSBdata(sb_lib.sendMsg(ser, "41 2")) != initpos:
    print()
    print("----------------------------------")
    print("DMK incline test failed.")
    print("----------------------------------")
else:
    numpassed = numpassed + 1
    print()
    print("------------------------")
    print("DMK incline test passed!")
    print("-------------------------")
    

sb_lib.sendMsg(ser, "41 5 0")
print()
finaltran = sb_lib.sendMsg(ser,"41 5")
zeromax = sb_lib.getSBdata(finaltran)
if zeromax != 0:
    print()
    print("---------------------------")
    print("Could not clear transmax.")
    print("----------------------------")
else:
    numpassed += 1

if numpassed >= 8:
    print()
    print("--------------------------")
    print("Sample Passed!")
    print("--------------------------")
else:
    print()
    print("----------------------------")
    print("Sample Failed")
    print("----------------------------")
    
    

    
