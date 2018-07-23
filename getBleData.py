# from bluepy.btle import Scanner, DefaultDelegate
# class ScanDelegate(DefaultDelegate): 
#     def __init__(self): 
#         DefaultDelegate.__init__(self)

#     def handleDiscovery(self, dev, isNewDev, isNewData): 
#         if isNewDev: 
#             print( "Discovered device", dev.addr )
#         elif isNewData: 
#             print( "Received new data from", dev.addr)

#     def handleNotification(self,cHandle,data):
#         print("notify from "+str(cHandle)+str(data)+"\n")

# scanner = Scanner().withDelegate(ScanDelegate()) 
# devices = scanner.scan(10.0)

# for dev in devices: 
#     print ("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi) )
#     for (adtype, desc, value) in dev.getScanData(): 
#         print ("  %s = %s" % (desc, value))



#!/usr/bin/python
#--*--coding=utf-8--*--

from __future__ import print_function
import sys
import binascii
from bluepy import btle
import os
import struct

ble_conn = None

class MyDelegate(btle.DefaultDelegate):

    def __init__(self, conn):
        btle.DefaultDelegate.__init__(self)
        self.conn = conn

    def handleNotification(self, cHandle, data):
        data = binascii.b2a_hex(data)
        print("Notification:", str(cHandle), " data ", data)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            pass
        elif isNewData:
            print("\\nDiscovery:", "MAC:", dev.addr, " Rssi ", str(dev.rssi))
            
            
def ble_connect(devAddr):
    global ble_conn
    if not devAddr is None and ble_conn is None:
        # ble_conn = btle.Peripheral(devAddr, btle.ADDR_TYPE_PUBLIC)
        ble_conn = btle.Peripheral(devAddr, btle.ADDR_TYPE_RANDOM)

        ble_conn.setDelegate(MyDelegate(ble_conn))
        print("connected")

def ble_disconnect():
    global ble_conn
    ble_conn = None
    print("disconnected")


if __name__ == '__main__':
# 
    ble_mac = "cc:50:98:e9:2a:b9"
   
    # scan 
    scanner = btle.Scanner().withDelegate(MyDelegate(None))
    timeout = 10.0
    devices = scanner.scan(timeout)
    for dev in devices:
        if dev.addr == ble_mac:
            print("\\nDiscovery:", "MAC:", dev.addr, " Rssi ", str(dev.rssi))
            for (adtype, desc, value) in dev.getScanData():
                print ("  %s(0x%x) = %s" % (desc, int(adtype), value))
            break
   
    # connect  
    ble_connect(ble_mac)
    # write , set listen
    snd_content_str = """\\x01\\x00"""
    for item in ble_conn.getServices():
        print("services:",item)

        try:
            ch = item
        except:
            pass

        try:
            val = binascii.b2a_hex(ch.read())
            print ("step one:",str(val))
        except:
            pass

        try:
            val = binascii.unhexlify(val)
            print ("step two:",str(val))
        except:
            pass

        try:
            val = struct.unpack('f', val)[0]
            print ("step three:",str(val))
        except:
            pass

    for item in ble_conn.getCharacteristics():
        print("characteristics:",item)
        # val = binascii.b2a_hex(ch.read())
        # val = binascii.unhexlify(val)
        # val = struct.unpack('f', val)[0]
        # print (str(val) + "************")

        try:
            ch = item
        except:
            pass

        try:
            val = binascii.b2a_hex(ch.read())
            print ("step one:",str(val))
        except:
            pass

        try:
            val = binascii.unhexlify(val)
            print ("step two:",str(val))
        except:
            pass

        try:
            val = struct.unpack('f', val)[0]
            print ("step three:",str(val))
        except:
            pass

    for item in ble_conn.getDescriptors():
        print("descriptors:",item)

        try:
            ch = item
        except:
            pass

        try:
            val = binascii.b2a_hex(ch.read())
            print ("step one:",str(val))
        except:
            pass

        try:
            val = binascii.unhexlify(val)
            print ("step two:",str(val))
        except:
            pass

        try:
            val = struct.unpack('f', val)[0]
            print ("step three:",str(val))
        except:
            pass
    # ble_conn.writeCharacteristic(handle, snd_content_str)
    # wait notification  
    ble_conn.waitForNotifications(20.0)
    
    # disconnect 
    ble_disconnect()

