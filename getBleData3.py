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

    for item in ble_conn.getServices():
        # print("services:",item.uuid)
        if item.uuid == "be940000-7333-be46-b7ae-689e71722bd5":
            # print(item.uuid)
            for iitem in item.getCharacteristics("be940001-7333-be46-b7ae-689e71722bd5"):

                ch = iitem

                ch.write(val = b"0x05060700010007",withResponse=True)

                ans = ch.read()

                print(ans)
                # print(ch.read())

                # print(ch.propertiesToString())

                # try:
                #     val = binascii.b2a_hex(ch.read())
                #     print ("step one:",str(val))
                # except:
                #     pass

                # try:
                #     val = binascii.unhexlify(val)
                #     print ("step two:",str(val))
                # except:
                #     pass


    # for item in ble_conn.getDescriptors():
    #     print("descriptors:",item)

    # for item in ble_conn.getCharacteristics():
    #     print("characteristics:",item)

    # while(True):
        




    # for item in ble_conn.getCharacteristics(uuid='BE940001-7333-BE46-B7AE-689E71722BD5'):
    #     print("characteristics:",item)


    #     ch = item

    #     snd_content_str = b"0x05060700010007"
    #     tmp = ble_conn.writeCharacteristic(ch.getHandle(), snd_content_str)


    #     print(tmp)

    #     print("--------------")
    #     # print("tmp: ",tmp)
        
    #     # print("ch: ",ch)
    #     # print(ch.read())
    #     print(ch.getHandle())
    #     # print(binascii.b2a_hex(ch))

    #     try:
    #         val = binascii.b2a_hex(ch.read())
    #         print ("step one:",str(val))
    #     except:
    #         pass

    #     try:
    #         val = binascii.unhexlify(val)
    #         print ("step two:",str(val))
    #     except:
    #         pass



    # wait notification  
    # ble_conn.waitForNotifications(10.0)
    
    # disconnect 
    ble_disconnect()





