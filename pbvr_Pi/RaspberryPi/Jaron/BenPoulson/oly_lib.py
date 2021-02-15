#!/usr/bin/env python3

#this is just a bunch of helper functions

import serial
import time
import binascii
import readline
from itertools import islice
import os

if os.name == 'nt':
    class bcolors:
        HEADER = ''
        OKBLUE = ''
        OKGREEN = ''
        WARNING = ''
        FAIL = ''
        ENDC = ''
        BOLD = ''
        UNDERLINE = ''
else:
    class bcolors:
        HEADER = '\033[35m'
        OKBLUE = '\033[34m'
        OKGREEN = '\033[32m'
        WARNING = '\033[33m'
        FAIL = '\033[31m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'


# here is the crc stuff
INITIAL_MODBUS = 0xFFFF
INITIAL_DF1 = 0x0000
 
table = (
0x0000, 0xC0C1, 0xC181, 0x0140, 0xC301, 0x03C0, 0x0280, 0xC241,
0xC601, 0x06C0, 0x0780, 0xC741, 0x0500, 0xC5C1, 0xC481, 0x0440,
0xCC01, 0x0CC0, 0x0D80, 0xCD41, 0x0F00, 0xCFC1, 0xCE81, 0x0E40,
0x0A00, 0xCAC1, 0xCB81, 0x0B40, 0xC901, 0x09C0, 0x0880, 0xC841,
0xD801, 0x18C0, 0x1980, 0xD941, 0x1B00, 0xDBC1, 0xDA81, 0x1A40,
0x1E00, 0xDEC1, 0xDF81, 0x1F40, 0xDD01, 0x1DC0, 0x1C80, 0xDC41,
0x1400, 0xD4C1, 0xD581, 0x1540, 0xD701, 0x17C0, 0x1680, 0xD641,
0xD201, 0x12C0, 0x1380, 0xD341, 0x1100, 0xD1C1, 0xD081, 0x1040,
0xF001, 0x30C0, 0x3180, 0xF141, 0x3300, 0xF3C1, 0xF281, 0x3240,
0x3600, 0xF6C1, 0xF781, 0x3740, 0xF501, 0x35C0, 0x3480, 0xF441,
0x3C00, 0xFCC1, 0xFD81, 0x3D40, 0xFF01, 0x3FC0, 0x3E80, 0xFE41,
0xFA01, 0x3AC0, 0x3B80, 0xFB41, 0x3900, 0xF9C1, 0xF881, 0x3840,
0x2800, 0xE8C1, 0xE981, 0x2940, 0xEB01, 0x2BC0, 0x2A80, 0xEA41,
0xEE01, 0x2EC0, 0x2F80, 0xEF41, 0x2D00, 0xEDC1, 0xEC81, 0x2C40,
0xE401, 0x24C0, 0x2580, 0xE541, 0x2700, 0xE7C1, 0xE681, 0x2640,
0x2200, 0xE2C1, 0xE381, 0x2340, 0xE101, 0x21C0, 0x2080, 0xE041,
0xA001, 0x60C0, 0x6180, 0xA141, 0x6300, 0xA3C1, 0xA281, 0x6240,
0x6600, 0xA6C1, 0xA781, 0x6740, 0xA501, 0x65C0, 0x6480, 0xA441,
0x6C00, 0xACC1, 0xAD81, 0x6D40, 0xAF01, 0x6FC0, 0x6E80, 0xAE41,
0xAA01, 0x6AC0, 0x6B80, 0xAB41, 0x6900, 0xA9C1, 0xA881, 0x6840,
0x7800, 0xB8C1, 0xB981, 0x7940, 0xBB01, 0x7BC0, 0x7A80, 0xBA41,
0xBE01, 0x7EC0, 0x7F80, 0xBF41, 0x7D00, 0xBDC1, 0xBC81, 0x7C40,
0xB401, 0x74C0, 0x7580, 0xB541, 0x7700, 0xB7C1, 0xB681, 0x7640,
0x7200, 0xB2C1, 0xB381, 0x7340, 0xB101, 0x71C0, 0x7080, 0xB041,
0x5000, 0x90C1, 0x9181, 0x5140, 0x9301, 0x53C0, 0x5280, 0x9241,
0x9601, 0x56C0, 0x5780, 0x9741, 0x5500, 0x95C1, 0x9481, 0x5440,
0x9C01, 0x5CC0, 0x5D80, 0x9D41, 0x5F00, 0x9FC1, 0x9E81, 0x5E40,
0x5A00, 0x9AC1, 0x9B81, 0x5B40, 0x9901, 0x59C0, 0x5880, 0x9841,
0x8801, 0x48C0, 0x4980, 0x8941, 0x4B00, 0x8BC1, 0x8A81, 0x4A40,
0x4E00, 0x8EC1, 0x8F81, 0x4F40, 0x8D01, 0x4DC0, 0x4C80, 0x8C41,
0x4400, 0x84C1, 0x8581, 0x4540, 0x8701, 0x47C0, 0x4680, 0x8641,
0x8201, 0x42C0, 0x4380, 0x8341, 0x4100, 0x81C1, 0x8081, 0x4040 )
  
# this function is untested
def calcByte( ch, crc):
    """Given a new Byte and previous CRC, Calc a new CRC-16"""
    if type(ch) == type("c"):
        by = ord( ch)
    else:
        by = ch
    crc = (crc >> 8) ^ table[(crc ^ by) & 0xFF]
    return (crc & 0x7F7F)
                                       
# use this one
def calcStringCRC( st, crc):
    """Given a binary string and starting CRC, Calc a final CRC-16 """
    crc = 0xFFFF
    for ch in st:
        #crc = (crc >> 8) ^ table[(crc ^ ord(ch)) & 0xFF] #for strings
        crc = (crc >> 8) ^ table[(crc ^ ch) & 0xFF]
    return (crc & 0x7f7f)

def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False

# and the olympus stuff 


def olympify(cmd):
    cmd = bytearray(cmd,"utf8")
    if len(cmd)<6:
        cmd += int(0).to_bytes(2,'big')
    cmd += calcStringCRC(cmd,0).to_bytes(2,"big")
    return cmd

def olympifarg(cmd,arg):
    cmd = bytearray(cmd,"utf8")
    if ("0x" in arg):
        cmd += int(arg,16).to_bytes(2,'big')
    else:
        cmd += int(arg).to_bytes(2,'big')
    cmd += calcStringCRC(cmd,0).to_bytes(2,"big")
    return cmd
   
def olympifyst(st):
    if(len(st.split())>1):
        return olympifarg(st.split()[0],st.split()[1])
    else:
        return olympify(st)


# returns data value from complete message
def getOlydata(msg):
    msg = bytearray(msg)
    #l = len(msg)
    #x = findmsgXsum(msg,l-1)
    #TODO: these numbers are wrong
    hi = int.from_bytes(msg[4:5],'big')*128
    lo = int.from_bytes(msg[5:6],'big')
    return hi+lo

# here we know that it's a complete message this pretty prints it
# note l is index of last byte
def showmsg(msg,l):
    print()
    print("%.3f" % time.time(), end=" ")
    print(msg[0:4].decode('utf-8'), end=" ")
    print("0x%2s 0x%2s" %(binascii.hexlify(msg[4:6]).decode('utf-8'), binascii.hexlify(msg[6:8]).decode('utf-8') ), end=" ")


def show(msg):
    showmsg(msg,len(msg)-1)

def consume(iterator, n):
    "Advance the iterator n-steps ahead. If n is none, consume entirely."
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        collections.deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(islice(iterator, n, n), None)

# find index of first byte in xsum, assumes complete message
#def findmsgXsum(msg):
#    x = len(msg)-2;
#    if(msg[x] == 0xf7):
#        x -= 1 
#    if(msg[x-1] == 0xf7):
#        x -= 1
#    return x


# finds the length to end of the message or the byte before the next begins (if cutoff), this assumes the first byte is the start of a message
def findmsgEnd(msg):
    r = range(1,len(msg));
    for i in r:
        if msg[i] == 73: #'I'==73
            return i
        elif i == 7: 
            return 8
    return 0

# finds start of next message in a buffer of messages
def findmsg(msg,ignore):
    n = 0;
    r = iter(range(len(msg)))
    for i in r:
        b = msg[i];
        if b == 73:
            j = findmsgEnd(msg[i:])
            if(j == 0):
                # don't have complete message yet, wait
                return i;
            if(n):
                # newline for start characters if they are in the middle of the message
                print("") 
                print("%.3f" % time.time(), end=" ")
            showmsg(msg[i:],j) 
#disable comm timeout
            i += j
            consume(r,j)
        elif not ignore:
            if not n:
                print()
                print("%.3f" % time.time(), end=" ")
            print(chr(b), end="")
            n = 1
    return i+1

# this simplified function adds delay to give time for the message to come through
# for more control use recieve and showmsg separately
def getReply(ser):
    time.sleep(.1)
    out = recieve(ser)
    if(out):
        findmsg(out, 0)
    return out

# this grabs the data from the serial RX and returns it
def recieve(ser):
    time.sleep(.01)
    out = bytearray(b"")
    while ser.inWaiting() > 0:
        n = ser.inWaiting()
        out += ser.read(n)
    return out

# this sends and shows the sent message
def send(ser,m):
    ser.write(m)
    show(m)

#this function allows you to use it like you would the oly_terminal
def sendMsg(ser,st):
    print()
    send(ser,olympifyst(st))
    return getReply(ser) 

