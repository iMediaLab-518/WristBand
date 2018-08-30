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
 
    # ble_mac = "cc:50:98:e9:2a:b9"
   
    # # scan 
    # scanner = btle.Scanner().withDelegate(MyDelegate(None))
    # timeout = 10.0
    # devices = scanner.scan(timeout)
    # for dev in devices:
    #     if dev.addr == ble_mac:
    #         print("\\nDiscovery:", "MAC:", dev.addr, " Rssi ", str(dev.rssi))
    #         for (adtype, desc, value) in dev.getScanData():
    #             print ("  %s(0x%x) = %s" % (desc, int(adtype), value))
    #         break



   
    # # connect  
    # ble_connect(ble_mac)
    # # write , set listen

    # ch = ""

    # for item in ble_conn.getServices():
    #     # print("services:",item.uuid)
    #     if item.uuid == "be940000-7333-be46-b7ae-689e71722bd5":
    #         # print(item.uuid)
    #         for iitem in item.getCharacteristics("be940001-7333-be46-b7ae-689e71722bd5"):

    #             ch = iitem

    #             break

    #             # ch.write(val = b"0x05060700010007",withResponse=True)

    #             # ch.peripheral.waitForNotifications(10.0)

    # print(ch.valHandle)

    # ble_conn.writeCharacteristic(39, b"0x05060700010007",withResponse=True)
    # ble_conn.waitForNotifications(2.0)


    # # wait notification  
    # # ble_conn.waitForNotifications(10.0)
    
    # # disconnect 
    # # ble_disconnect()


    p = btle.Peripheral("cc:50:98:e9:2a:b9", "random")
    services=p.getServices()
    for service in services:
       print(service)
    s = p.getServiceByUUID("be940000-7333-be46-b7ae-689e71722bd5")
    c = s.getCharacteristics()[0]
    print(c)
    c.write("e", "utf-8")
    print(c)
    p.disconnect()


