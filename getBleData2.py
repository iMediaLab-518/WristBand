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



class Crc16Util:
    
    def getBytesByString(data):
        byte[] bytes = null;
        if (data != null):
            data = data.toUpperCase();
            int length = data.length() / 2;
            char[] dataChars = data.toCharArray();
            bytes = new byte[length];
            for i in range(length):
                int pos = i * 2;
                bytes[i] = (byte) (charToByte(dataChars[pos]) << 4 | charToByte(dataChars[pos + 1]));
        return bytes;

    def crcTable(bytes):
        int[] table = {
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
                0x8201, 0x42C0, 0x4380, 0x8341, 0x4100, 0x81C1, 0x8081, 0x4040,
        };
        int crc = 0xffff;

        for b in bytes:
            crc = (crc >>> 8) ^ table[(crc ^ b) & 0xff];
        String crcStr = hex(crc);
        String substring = crcStr[2:];
        # System.out.println("substring:"+substring);
        byte[] bytes1 = getBytesByString(substring);
        String substring2 = crcStr[0:2];
        # System.out.println("substring2:"+substring2);
        byte[] bytes2 = getBytesByString(substring2);
        byte[] bytes3 = new byte[2];
        # System.arraycopy(bytes1,0,bytes3,0,bytes1.length);
        # System.arraycopy(bytes2,0,bytes3,1,bytes2.length);
        return bytes3;

    def getCrc(data):
        int high;
        int flag;

        # 16位寄存器，所有数位均为1
        int wcrc = 0xffff;
        for i in range(data.length):
            # 16 位寄存器的高位字节
            high = wcrc >> 8;
            # 取被校验串的一个字节与 16 位寄存器的高位字节进行“异或”运算
            wcrc = high ^ data[i];

            for j in range(8):
                flag = wcrc & 0x0001;
                # 把这个 16 寄存器向右移一位
                wcrc = wcrc >> 1;
                # 若向右(标记位)移出的数位是 1,则生成多项式 1010 0000 0000 0001 和这个寄存器进行“异或”运算
                if (flag == 1)
                    wcrc ^= 0xa001;

        return hex(wcrc)


def makeSend(test):
    testc = [0 for i in range(len(test) + 2)];

    count = 0;

    for i in range(len(test)):

        testc[i+count] = test[i];
        if (i == 1):
            length = len(test) + 4;
            testc[2] = str(length % 0x100).encode('utf-8')
            testc[3] = str(length / 0x100).encode('utf-8')
            count = 2;

    return makeCRC16(testc);

def makeCRC(msg):

        # print("MyApp","msg : "+ DataUtil.byteToHexString(msg));
        print("msg : "+ binascii.b2a_hex(msg));
        # xx = crc16JNI(msg);
        xx = msg;

        byte[] testaa = new byte[2];
        testaa[0] = (byte) xx;
        testaa[1] = (byte) (xx >> 8);

        return testaa;

def makeCRC16(test):
    crc = makeCRC(test);
    # bytess = Crc16Util.crcTable(test);
    # Log.e("Crc16Util",DataUtil.byteToHexString(bytes));
    # Log.e("Crc16",Crc16Util.getCrc(test));
    testc = [len(test) + 2];
    for i in range(len(test)):
        testc[i] = test[i];
    # System.out.println(test.length);

    testc[len(test)] = crc[0];
    testc[len(test) + 1] = crc[1];
    # Log.e("crc16",DataUtil.byteToHexString(testc));
    print("crc16 "+ binascii.b2a_hex(testc))
    return testc;


def onDoSynchronizedHistoryHeartRate(ble_conn):
    byte[] smsg = {0x05, 0x06, 0x01};
    smsg = makeSend(smsg);
    ble_conn.writeCharacteristic(ch.getHandle(), snd_content_str)

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

    # while(True):
        




    for item in ble_conn.getCharacteristics(uuid='BE940001-7333-BE46-B7AE-689E71722BD5'):
        print("characteristics:",item)


        ch = item

        # snd_content_str = "0x050601"
        # tmp = ble_conn.writeCharacteristic(ch.getHandle(), snd_content_str)

        # print("tmp: ",tmp)
        
        # print("ch: ",ch)
        # print(ch.read())
        # print(ch.getHandle())
        # print(binascii.b2a_hex(ch))

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



    # wait notification  
    # ble_conn.waitForNotifications(10.0)
    
    # disconnect 
    ble_disconnect()





