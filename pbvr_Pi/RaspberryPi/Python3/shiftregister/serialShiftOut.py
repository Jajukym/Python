import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)

encDATA  = 22
encSH_LD = 27
encCLOCK = 17
GPIO.setup(encDATA, GPIO.OUT)
GPIO.setup(encSH_LD, GPIO.OUT)
GPIO.setup(encCLOCK, GPIO.OUT)


def shiftout(byte):
  GPIO.output(encSH_LD, 0)
  for x in range(8):
    #print (byte, " ", y)   
    GPIO.output(encDATA,x%2)
    byte = byte >> 1
    GPIO.output(encCLOCK, 1)
    #time.sleep(1.0955)
    GPIO.output(encCLOCK, 0)
    GPIO.output(encSH_LD, 1)
    #byte = y
    print(byte)
    #print (y)
    
    
byte = 0xf0
shiftout(byte)
GPIO.cleanup()


#right shifting counting byte
print ("shifting bits right")
x = 128.0
for i in range (18):
   print (int(x))
   if x == 1:
       x = 129
       print (int(x))
       x = 128
       print (int(x))
   x = (x + x - (x/2))
   print (int(x))
   x = (x /3)
   
#left shifting counting byte
print ("Shifting bits left")
y = 1.0
for i in range(18):
   print (int(y))
   y = y * 3
   print (int(y))
   y = (y / 3 * 2)
   if y == 384:
       y = 129.0
       print (int(y))
       y = 1.0

    
