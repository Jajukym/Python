#***************************************************************************************
#     version 7
#
#     AFTER DEVICE UNDER TEST IS CONNECTED PRESS F5 TO BEGIN TEST
#
#     Shell window displays test results
#
#***************************************************************************************

# If you see the following error message - Can't connect to pigpio at localhost(8888)
# You need to perform the following steps
# 1. open terminal and enter this command - sudo systemctl enable pigpiod
# 2. open terminal and enter this command - sudo systemctl start pigpiod

#These numbers should be changed to match the data for the device being tested
#ICON MODEL DCIHB148-EXT - desiredHardwareNumber = 418177 desiredSoftwareNumber = 418205 desiredCodeVersion = 4142
desiredHardwareNumber = 418177
desiredSoftwareNumber = 418205
desiredCodeVersion = 4142
beginPauseTime = 15

#These numbers should be changed to match the lift motor being used in the test fixture
#ICON PART NUMBER 415173 - desiredTransMax = 3700 desiredMaxIncline = 37 desiredMinIncline = 0
desiredTransMax = 3700
desiredMaxIncline = 60
desiredMinIncline = 0
#NO CHANGES SHOULD BE MADE BELOW THIS LINE

minResistance = 50
maxResistance = 200
desiredTach = 90

inclineChange = 4
inclinePauseTime = 3

resistanceChange = 25
resistancePauseTime = 2
resistanceTolerance = 3

desiredTransMaxString = str(desiredTransMax)
desiredMinInclineString = str(desiredMinIncline)
desiredMaxInclineString = str(desiredMaxIncline)
desiredActualInclineString = desiredMaxInclineString
desiredNegIncOffsetString = "20"

minResistanceString = str(minResistance)
maxResistanceString = str(maxResistance)
   
import serial
import time
import sb_lib
import os
import sys


import pigpio


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

PIN_TACH_OUTPUT=3


#open port 
ser = serial.Serial(
    port=p,
    baudrate=38400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

ser.isOpen();#just a safety check


#print("Welcome to the ShortBus Terminal")
print("----------------------------------------------------")
print("                BEGIN TEST")
print("----------------------------------------------------")
square = []

#                          ON       OFF    MICROS
square.append(pigpio.pulse(1<<PIN_TACH_OUTPUT, 0,       1000))#113 encoder, 1000 lowrestach
square.append(pigpio.pulse(0,       1<<PIN_TACH_OUTPUT, 332333))#10 encoder, 333333 lowrestach


pin_IO = pigpio.pi() # connect to local Pi

pin_IO.set_mode(PIN_TACH_OUTPUT, pigpio.OUTPUT)


successfulTests = 0


pin_IO.wave_add_generic(square)

wid = pin_IO.wave_create()

if wid >= 0:
   pin_IO.wave_send_repeat(wid)
   

#   sb_lib.sendMsg(ser,"41 3 1")#calibrate incline 
#   time.sleep(45)
#   transMax = sb_lib.sendMsg(ser,"41 5")#read transmax
#   transMaxDEC = sb_lib.convertResponseMessage(transMax)
#   print(transmaxDEC)
   
   sb_lib.sendMsg(ser,"41 9 " + desiredNegIncOffsetString)
   sb_lib.sendMsg(ser,"41 8 " + desiredActualInclineString)
   sb_lib.sendMsg(ser,"41 7 " + desiredMaxInclineString)
   sb_lib.sendMsg(ser,"41 6 " + desiredMinInclineString)
   sb_lib.sendMsg(ser,"41 5 " + desiredTransMaxString)

   #VERIFY THAT THE TRANSMAX WAS WRITTEN CORRECTLY
   dataPacket = sb_lib.sendMsg(ser,"41 5")#read back the transmax
   transMax = sb_lib.convertResponseMessage(dataPacket)
   if transMax == desiredTransMax:
       print("TRANSMAX WRITE PASS")
       successfulTests = successfulTests + 1
   else:
       print("TRANSMAX WRITE FAIL")
       
   sb_lib.sendMsg(ser,"41 1 0") #bottom seek
   beginMove = time.time()
   inclineMoveTime = 0
   
   startInclinePosition = 255

   while startInclinePosition !=0 and inclineMoveTime < beginPauseTime:
       dataPacket = sb_lib.sendMsg(ser,"41 2")#Read Current incline location
       startInclinePosition = sb_lib.convertResponseMessage(dataPacket)
       inclineMoveTime = time.time() - beginMove
   
   if startInclinePosition == 0:
       desiredPosition = inclineChange
   elif startInclinePosition == desiredMaxIncline:
       desiredPosition = (desiredMaxIncline-inclineChange)
   elif startInclinePosition < (desiredMaxIncline-inclineChange):
       desiredPosition = startInclinePosition + inclineChange
   else:
       desiredPosition = startInclinePosition - inclineChange
       
   dpString = str(desiredPosition)
   writePositionCommand = "41 1 " + dpString
   
   sb_lib.sendMsg(ser,writePositionCommand)#move to new incline position
   beginMove = time.time()
   inclineMoveTime = 0
   
   firstInclinePosition = 255
   
   while firstInclinePosition != desiredPosition and inclineMoveTime < inclinePauseTime:
       dataPacket = sb_lib.sendMsg(ser,"41 2")#Read Current incline location
       firstInclinePosition = sb_lib.convertResponseMessage(dataPacket)
       inclineMoveTime = time.time() - beginMove
   

#VERIFY THAT INCLINE REACHED THE CORRECT POSITION
   if firstInclinePosition == desiredPosition:
       print("INC MOVE DIR_A PASS")
       successfulTests = successfulTests + 1
   else:
       print("INCLINE MOVE DIR_A FAIL")
   
   if startInclinePosition == 0:
       desiredPosition = 1
   elif startInclinePosition == desiredMaxIncline:
       desiredPosition = desiredMaxIncline -1
   else:
       desiredPosition = startInclinePosition

   dpString = str(desiredPosition)
   writePositionCommand = "41 1 " + dpString
   
   sb_lib.sendMsg(ser,writePositionCommand)#move to new incline position
   beginMove = time.time()
   inclineMoveTime = 0
   
   endInclinePosition = 255
   
   while endInclinePosition != desiredPosition and inclineMoveTime < inclinePauseTime:
       dataPacket = sb_lib.sendMsg(ser,"41 2")#Read Current incline location
       endInclinePosition = sb_lib.convertResponseMessage(dataPacket)
       inclineMoveTime = time.time() - beginMove
   

   #VERIFY THAT INCLINE REACHED THE CORRECT POSITION
   if endInclinePosition == desiredPosition:
       print("INC MOVE DIR_B PASS")
       successfulTests = successfulTests + 1
   else:
       print("INCLINE MOVE DIR_B FAIL")

   #print("----------------------------------------------------")
   #print("                  Revision_Read verify")
   #print("----------------------------------------------------")

   codeVersion = sb_lib.sendMsg(ser, "41 F1")#code version
   hardwareNumber = sb_lib.sendMsg(ser, "41 F2")#hardware number
   softwareNumber = sb_lib.sendMsg(ser, "41 F3")#software number
   
   codeVersionDEC = sb_lib.convertLongResponseMessage(codeVersion)
   hardwareNumberDEC = sb_lib.convertLongResponseMessage(hardwareNumber)
   softwareNumberDEC = sb_lib.convertLongResponseMessage(softwareNumber)
      
   #VERIFY THAT HARDWARE AND SOFTWARE AND CODE REVISION MATCH
   if codeVersionDEC == desiredCodeVersion:
       print("CODE VERSION PASS")
       successfulTests = successfulTests + 1
   else:
       print("CODE VERSION FAIL")
   if hardwareNumberDEC == desiredHardwareNumber:
       print("HARDWARE NUMBER PASS")
       successfulTests = successfulTests + 1
   else:
       print("HARDWARE NUMBER FAIL")
   if softwareNumberDEC == desiredSoftwareNumber:
       print("SOFTWARE NUMBER PASS")
       successfulTests = successfulTests + 1
   else:
       print("SOFTWARE NUMBER FAIL")
          

   #print("----------------------------------------------------")
   #print("                  Tach verify")
   #print("----------------------------------------------------")
   tachInput = sb_lib.sendMsg(ser,"51 2")#lowrestach
   tachInputDEC = sb_lib.convertResponseMessage(tachInput)
   
   #VERIFY THAT TACH IS READING CORRECTLY
   if tachInputDEC == desiredTach:
       print("TACH READ PASS")
       successfulTests = successfulTests + 1
   else:
       print("TACH READ FAIL")
       
   #print("----------------------------------------------------")
   #print("               Resistance Clockwise")
   #print("----------------------------------------------------")

   startResistancePosition = sb_lib.sendMsg(ser,"61 6")#Read Current resistance location
   startResistancePositionDEC = sb_lib.convertResponseMessage(startResistancePosition)
   
   if startResistancePositionDEC<(maxResistance - resistanceChange):
       desiredResPosition = startResistancePositionDEC + resistanceChange
   else:
       desiredResPosition = maxResistance
       
   resistanceString = str(desiredResPosition)
      
   sb_lib.sendMsg(ser,"61 5 " + resistanceString)
   time.sleep(resistancePauseTime)
   
   firstResistancePosition = sb_lib.sendMsg(ser,"61 6")
   firstResistancePositionDEC = sb_lib.convertResponseMessage(firstResistancePosition)
   
   #VERIFY THAT RESISTANCE REACHED THE CORRECT POSITION
   if (firstResistancePositionDEC - desiredResPosition) >-resistanceTolerance and (firstResistancePositionDEC - desiredResPosition) <resistanceTolerance:
       print("CLOCKWISE RESISTANCE PASS")
       successfulTests = successfulTests + 1
   else:
       print("CLOCKWISE RESISTANCE FAIL")
       
       
   #print("----------------------------------------------------")
   #print("          Resistance Counter Clockwise")
   #print("----------------------------------------------------")
   
   if firstResistancePositionDEC>(minResistance + resistanceChange):
       desiredResPosition = firstResistancePositionDEC - resistanceChange
   else:
       desiredResPosition = minResistance
   
   resistanceString = str(desiredResPosition)
   
   sb_lib.sendMsg(ser,"61 5 " + resistanceString)
   time.sleep(resistancePauseTime)
   
   endResistancePosition = sb_lib.sendMsg(ser,"61 6")
   endResistancePositionDEC = sb_lib.convertResponseMessage(endResistancePosition)
   #VERIFY THAT RESISTANCE REACHED THE CORRECT POSITION
   if (endResistancePositionDEC - desiredResPosition) >-resistanceTolerance and (endResistancePositionDEC - desiredResPosition) <resistanceTolerance:
       print("COUNTER CLOCKWISE RESISTANCE PASS")
       successfulTests = successfulTests + 1
   else:
       print("COUNTER CLOCKWISE RESISTANCE FAIL")

   sb_lib.sendMsg(ser, "41 5 0")
   
   dataPacket = sb_lib.sendMsg(ser,"41 5")#read back the transmax
   transMax = sb_lib.convertResponseMessage(dataPacket)

   if transMax == 0:
       print("CLEAR TRANSMAX WRITE PASS")
       successfulTests = successfulTests + 1
   else:
       print("CLEAR TRANSMAX WRITE FAIL")

   print()
   print("----------------------------------------------------")
   print()

   if successfulTests == 10:
       print("************  SUCCESS - ALL TESTS PASS  ************")
   else:
       print("XXXXXXXXXXXX    FAIL - SAMPLE FAILED    XXXXXXXXXXXX")

   print()
   print("----------------------------------------------------")
  
   pin_IO.wave_tx_stop()
   pin_IO.wave_delete(wid)
   
 