import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)

PIN_DATA  = 3
PIN_LATCH = 27
PIN_CLOCK = 17
GPIO.setup(PIN_DATA, GPIO.OUT)
GPIO.setup(PIN_LATCH, GPIO.OUT)
GPIO.setup(PIN_CLOCK, GPIO.OUT)


def shiftout(byte):
  GPIO.output(PIN_LATCH, 0)
  GPIO.output(PIN_DATA, 1)
  byte = 0xf0
  #y= 0
  for x in range(16):
    #print (byte, " ", y)
    GPIO.output(PIN_DATA,x%2)
    byte = byte >> 1
    #time.sleep(.015)
    GPIO.output(PIN_CLOCK, 1)
    #time.sleep(1.0955)
    GPIO.output(PIN_CLOCK, 0)
    GPIO.output(PIN_LATCH, 1)
    #byte = y
    print(byte)
    #print (y)
    
    
byte = 0xf0
shiftout(byte)
GPIO.cleanup()
