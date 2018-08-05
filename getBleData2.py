#!/usr/bin/python
#--*--coding=utf-8--*--

from __future__ import print_function
import sys
import binascii
from bluepy import btle
import os
import struct
import cv2

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

    # for item in ble_conn.getServices():
    #     print("services:",item)

    # for item in ble_conn.getDescriptors():
    #     print("descriptors:",item)

    # for item in ble_conn.getCharacteristics():
    #     print("characteristics:",item)

    while(True):

        ch = ble_conn.getCharacteristics(uuid='BE940001-7333-BE46-B7AE-689E71722BD5')
        
        print(ch)

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

        print("---------------------------------------")
        
        for item in ble_conn.getCharacteristics(uuid='BE940001-7333-BE46-B7AE-689E71722BD5'):
            print("characteristics:",item)

            ch = item
            print(ch)
            print(ch.read())
            # print(ch.getHandle())
            # print(binascii.b2a_hex(ch))

            # snd_content_str = """\\x01\\x00"""
            # ble_conn.writeCharacteristic(39, snd_content_str)

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


        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break

    # wait notification  
    # ble_conn.waitForNotifications(10.0)
    
    # disconnect 
    ble_disconnect()





