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

# here is the lrc stuff
def calcLRC(msg):
    lrc = 0
    for i in range(0,len(msg),2):
        lrc += int(msg[i:i+2],16)#int(chr(b),16)
        lrc &= 0xff
    lrc = (~(lrc -1))&0xff
    return lrc
    
def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False

# and the shortbus stuff 


def deltafy(reg, arg):
    reg = bytearray(reg,"utf-8")
    #:aaddrrrrxxxx CRC \r\n
    #TODO: add support for a full command, just add checksum
    msg = b':01'
    if len(arg):
        msg += b'06' + reg.rjust(4,b'0') # since we have data we assume its a write
    else:
        msg += b'03' + reg.rjust(4,b'0') 
    if ("0x" in arg):
        msg += bytearray(hex(int(arg,16))[2:].rjust(4,"0"),"utf-8")
    elif len(arg):
        msg += bytearray(hex(int(arg))[2:].rjust(4,"0"),"utf-8")
    else:
        msg += b'0001'
    #print(calcLRC(addr[1:]))
    msg += bytearray(hex(calcLRC(msg[1:]))[2:].rjust(2,"0"),"utf-8")
    msg += bytearray("\r\n","utf-8")
    msg = msg.upper()
    return msg
   
def deltafyst(st):
    if(len(st.split())>1):
        return deltafy(st.split()[0],st.split()[1])
    else:
        return deltafy(st,"")


# returns data value from complete message
def getDeltadata(msg):
    #msg = bytearray(msg)
    #l = len(msg)
    #x = findmsgXsum(msg,l-1)
    if(isreply(msg)):
        i = msg.find(b':')+11
    else:
        i = msg.find(b':')+9
    j = msg.find(b'\r')-2
    return int(msg[i:j],16)

#this will break up multibyte data into the values
def printDeltadata(msg):
    if(isreply(msg)):
        i = msg.find(b':')+11
    else:
        i = msg.find(b':')+9
    j = msg.find(b'\r')-2
    if(i<9 or j == -1):
        return
    v = int(msg[i:i+4],16)
    print("\n returned: ",v," (", hex(v),")")
    for k in range(4,j-i,4):
        v = int(msg[i+k:i+k+4],16)
        print("           ",v," (", hex(v),")")

#this makes a tuple from a multiple byte data packet
def breakupDeltadata(msg):
    if(isreply(msg)):
        i = msg.find(b':')+11
    else:
        i = msg.find(b':')+9
    j = msg.find(b'\r')-2
    if(i<9 or j == -1):
        return
    v = (int(msg[i:i+4],16),)
    for k in range(4,j-i,4):
        v += ( int(msg[i+k:i+k+4],16),)
    return v
        

# here we know that it's a complete message this pretty prints it
def show(msg):
    print()
    print("%.3f" % time.time(), end=" ")
    i = msg.find(b'\r')
    if(i == -1):
        #it wasn't a complete message
        print(msg)
        return
    print(msg[0:3].decode('utf-8'), end="")
    if(msg[4] == 51): #
        #get
        print(bcolors.OKGREEN + msg[3:5].decode('utf-8') + bcolors.ENDC, end="")
    else:
        #set
        print(bcolors.OKBLUE + msg[3:5].decode('utf-8') + bcolors.ENDC, end="")

    j = i-2
    if(isreply(msg)):
        i = msg.find(b':')+7
    else:
        i = msg.find(b':')+9

    print(msg[5:i].decode('utf-8'), end=" ")
    print(msg[i:j].decode('utf-8'), end=" ")
    print(msg[j:j+2].decode('utf-8'), end="")
    #print("0x%2s 0x%2s" %(binascii.hexlify(msg[4:6]).decode('utf-8'), binascii.hexlify(msg[6:8]).decode('utf-8') ), end=" ")


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

# this assumes the first byte is the start char ':'
#TODO: this is broken, delta replies don't state the register
def isreply(msg):
    if(findmsgEnd(msg) < 15):
        return True
    return False



# finds the length to end of the message or the byte before the next begins (if cutoff), this assumes the first byte is the start of a message
def findmsgEnd(msg):
    i = msg.find(b'\r')
    if i==-1:
        i = msg.find(b':')#TODO: won't this find the first byte in a message?
    if i<1:
        return 0
    return i

# finds start of next message in a buffer of messages
def findmsg(msg,ignore):
    n = 0;
    r = iter(range(len(msg)))
    for i in r:
        b = msg[i];
        if b == 58: #':' == 58?
            j = findmsgEnd(msg[i:])
            if(j == 0 or j-i < 4 ):
                # don't have complete message yet, wait
                return i;
            if(n):
                # newline for start characters if they are in the middle of the message
                print("") 
                print("%.3f" % time.time(), end=" ")
            show(msg[i:]) 
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
        findmsg(out, 1) #2nd arg is ignore
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

#this function allows you to use it like you would the delta_terminal
def sendMsg(ser,st):
    print()
    m = deltafyst(st)
    send(ser,m)
    show(m)
    return getReply(ser) 

