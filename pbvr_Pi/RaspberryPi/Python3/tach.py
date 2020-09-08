
import pigpio
import time



GPIO=3 #for pedal encoder hardware verification
square = []

#                          ON       OFF    MICROS
square.append(pigpio.pulse(1<<GPIO, 0,       1000))#113 encoder, 1000 lowrestach
square.append(pigpio.pulse(0,       1<<GPIO, 332333))#10 encoder, 333333 lowrestach




pi = pigpio.pi() # connect to local Pi

pi.set_mode(GPIO, pigpio.OUTPUT)

pi.wave_add_generic(square)

wid = pi.wave_create()

if wid >= 0:
   pi.wave_send_repeat(wid)
   time.sleep(10)
   pi.wave_tx_stop()
   pi.wave_delete(wid)
