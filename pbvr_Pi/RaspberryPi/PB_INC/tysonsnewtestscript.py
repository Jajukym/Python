import RPi.GPIO as GPIO
import numpy as np
import time

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

#Input Pins
tachin = np.array([21, 20, 16, 12, 7])
incsense = 10
incsensecounter = 0


#Output Pins
tachout = np.array([26, 19, 13, 6, 5])
incup = 11
incdown = 9
#Output Pin Declarations
GPIO.setup(int(tachout[0]), GPIO.OUT)
GPIO.setup(int(tachout[1]), GPIO.OUT)
GPIO.setup(int(tachout[2]), GPIO.OUT)
GPIO.setup(int(tachout[3]), GPIO.OUT)
GPIO.setup(int(tachout[4]), GPIO.OUT)
GPIO.setup(incup, GPIO.OUT) #Incline up
GPIO.setup(incdown, GPIO.OUT) #Incline down

#Input pin Declarations
GPIO.setup(int(tachin[0]), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(int(tachin[1]), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(int(tachin[2]), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(int(tachin[3]), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(int(tachin[4]), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(incsense, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Incline Sense set to pull down.


#Tach Verification
print("-------------------------")
print("   Tach Test Starting    ")
print("-------------------------")

correctcounter = 0
incorrectpins = np.array([0,0,0,0,0])
for i in range(5):
    inpin = tachin[i]
    outpin = tachout[i]
    GPIO.output(int(outpin), 1)
    time.sleep(1)
    if GPIO.input(inpin) == 1:
        correctcounter += 1
    else:
        incorrectpins[i] = inpin
if correctcounter == 5:
    print("-------------------------")
    print("      Test Passed!       ")
    print("-------------------------")
else:
    print("-------------------------")
    print("    Test Failed on Pins: ")
    print(incorrectpins)
    print("-------------------------")


#Incline Verification
inclinecorrectcounter = 0
GPIO.add_event_detect(incsense, GPIO.RISING)
print("-------------------------")
print("  Incline Test Starting  ")
print("-------------------------")

GPIO.output(incup, 1) #set the incline to turn up
GPIO.output(incdown, 0)
time.sleep(1)

pulsecounter = 0
endtime = time.time() + 5
while time.time() < endtime:
    if GPIO.event_detected(int(incsense)):
        print("found pulse", pulsecounter)
        pulsecounter += 1

    

if pulsecounter >= 4:
    print("-------------------------")
    print("      Test Passed!       ")
    print("-------------------------")
    inclinecorrectcounter += 1
else:
    print("--------------------------")
    print("Test Failed. No Wave Found")
    print("--------------------------")
    GPIO.output(incup, 0)
    GPIO.output(incdown, 0)
    
time.sleep(2)   
GPIO.output(incup, 0) #Turn off the incline
GPIO.output(incdown, 0)
incsensecounter = 0

time.sleep(2)
GPIO.output(incdown, 1)
GPIO.output(incup, 0) #set the incline to turn down
time.sleep(2)

#set timing
pulsecounter = 0
endtime = time.time() + 5
while time.time() < endtime:
    if GPIO.event_detected(int(incsense)):
        print("found pulse", pulsecounter)
        pulsecounter += 1

if pulsecounter >= 4:
    print("-------------------------")
    print("      Test Passed!       ")
    print("-------------------------")
    inclinecorrectcounter += 1
else:
    print("--------------------------")
    print("Test Failed. No Wave Found")
    print("--------------------------")
    GPIO.output(incup, 0)
    GPIO.output(incdown, 0)

GPIO.output(incup, 0) #Turn off the incline
GPIO.output(incdown, 0)

if inclinecorrectcounter == 2 and correctcounter == 5:
    print("---------------------------------")
    print("        Sample Passed!           ")
    print("---------------------------------")
else:
    print("---------------------------------")
    print("        Sample Failed.           ")
    print("---------------------------------")
    
GPIO.cleanup()
