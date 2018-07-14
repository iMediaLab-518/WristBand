#!/usr/bin/env python
#--*--coding=utf-8--*--
# import time
# from bluetooth import *
# def rfcommCon(addr,port):
#     sock = BluetoothSocket(RFCOMM)
#     try:
#         sock.connect((addr,port))
#         print "[+] RFCOMM port : " +str(port)+' open'
#         sock.close()
#     except Exception,e:
#         print '[-] RFCOMM port :' +str(port)+' closed'
 
# for port in range(1,30):
#     rfcommCon('98:E9:2A:B9:XX:57',port)




# import time
# from bluetooth import *
# alreadyFound = []
# def findDevs():
#     foundDevs = discover_devices(lookup_names=True)
#     for(addr,name) in foundDevs:
#         if addr not in alreadyFound:
#             print "[*] Found Bluetooth Device :  " +str(name)
#             print "[+] MAC address :  " +str(addr)
#             alreadyFound.append(addr)
 
# while True:
#     findDevs()
#     time.sleep(5)