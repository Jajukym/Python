#import RPi.GPIO
import time
import pigpio

"""RPi.GPIO.setmode(RPi.GPIO.BCM) #Board vs BCM
RPi.GPIO.setup(3, RPi.GPIO.OUT) #set as output

while True:
    RPi.GPIO.output(3, True) #on
    time.sleep(.001) #1 second
    RPi.GPIO.output(3, False) #off
    time.sleep(.001)"""

GPIO=3
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
   time.sleep(3)
   pi.wave_tx_stop()
   #pi.wave_delete(wid)
