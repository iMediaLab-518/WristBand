#!/usr/bin/env python
#--*--coding=utf-8--*--
import time
from bluetooth import *
def rfcommCon(addr,port):
    sock = BluetoothSocket(RFCOMM)
    try:
        sock.connect((addr,port))
        print ("[+] RFCOMM port : " +str(port)+' open')
        sock.close()
    except Exception,e:
        print ('[-] RFCOMM port :' +str(port)+' closed')
 
for port in range(1,30):
    rfcommCon('CC:50:98:E9:2A:B9',port)