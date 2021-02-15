#!/usr/bin/env python3

#this is just a bunch of helper functions 

import serial
import time
import binascii
#import readline
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


def sbify(addr, cmd, arg):
    addr = bytearray(addr,"utf-8")
    cmd = bytearray(cmd,"utf-8")
    #:aaddccccxxxx CRC \r\n
    if addr[0] != b':':
        addr = b':' + addr
    if len(arg):
        addr += b'06' # since we have data we assume its a write
    elif len(addr)<5:
        addr += b'03'
    if len(addr)<6: 
        addr += cmd.rjust(4,b'0')
    if ("0x" in arg):
        addr += bytearray(hex(int(arg,16))[2:].rjust(4,"0"),"utf-8")
    elif len(arg):
        addr += bytearray(hex(int(arg))[2:].rjust(4,"0"),"utf-8")
    else:
        addr += b'0000'
    #print(calcLRC(addr[1:]))
    addr += bytearray(hex(calcLRC(addr[1:]))[2:].rjust(2,"0"),"utf-8")
    addr += bytearray("\r\n","utf-8")
    addr = addr.upper()
    return addr
   
def sbifyst(st):
    if(len(st.split())>2):
        return sbify(st.split()[0],st.split()[1],st.split()[2])
    elif(len(st.split())>1): 
        return sbify(st.split()[0],st.split()[1],"")
    else:
        return sbify(st,"","")


# returns data value from complete message
def getSBdata(msg):
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
def printSBdata(msg):
    if(isreply(msg)):
        i = msg.find(b':')+11
        l = int(msg[i-6:i-4],16)
    else:
        i = msg.find(b':')+9
        l = 2
    j = msg.find(b'\r')-2
    if(i<9 or j == -1):
        return
    if l <= 2:
        v = int(msg[i:i+l*2],16)
    else:
        v = int(msg[i:i+4],16)
    print("\n returned: ",v," (", hex(v),")")
    for k in range(4,j-i,4):
        v = int(msg[i+k:i+k+4],16)
        print("           ",v," (", hex(v),")")

#this makes a tuple from a multiple byte data packet
def breakupSBdata(msg):
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
    print("%.3f" % time.time(), end =" ")
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
        i = 11#msg.find(b':')+11
    else:
        i = 9#msg.find(b':')+9

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
def isreply(msg):
    #if(findmsgEnd(msg) > 15):
    if msg[6] != 48: #check for reserved byte or length
        return True
    return False



# finds the length to end of the message or the byte before the next begins (if cutoff), this assumes the first byte is the start of a message
def findmsgEnd(msg):
    i = msg.find(b'\r')
    if i==-1:
        msg.find(b':')
    if i==-1:
        return 0
    return i

# finds start of next message in a buffer of messages
def findmsg(msg,ignore):
    n = 0;
    r = iter(range(len(msg)))
    for i in r:
        b = msg[i];
        if b == 58:
            j = findmsgEnd(msg[i:])
            if(j == 0):
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
            # print partial or bad message
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
        findmsg(out, True) #2nd arg is ignore
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

#this function allows you to use it like you would the sb_terminal
def sendMsg(ser,st):
    print()
    m = sbifyst(st)
    send(ser,m)
    show(m)
    return getReply(ser) 

