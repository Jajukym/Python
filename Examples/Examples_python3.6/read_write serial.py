import serial

ser = serial.Serial("COM18",9600)
command = b'x30\x35\x30\x31'
ser.write(command)
s = ser.read(7)
print(s)
