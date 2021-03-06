import blescan
import sys
import time

import bluetooth._bluetooth as bluez

dev_id = 0
sock = bluez.hci_open_dev(dev_id)
blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

measured_anterior = 0

try:
    while True:
        returnedList = blescan.parse_events(sock, 1)
        # print("------------------")
        # print(returnedList)
        # print("------------------")
        for returnedItem in returnedList:
        	(mac, uuid, major, minor, txpower, rssi) = returnedItem.split(',', 6)
        	if mac == 'cc:50:98:e9:2a:b9':
	        	print("------------------")
	        	print(returnedItem)
	        	print("------------------")
        if len(returnedList) > 0:
            (mac, uuid, major, minor, txpower, rssi) = returnedList[0].split(',', 6)
            # CAMBIAR LA DIRECCION MAC
            if mac == 'cc:50:98:e9:2a:b9':
                # print("get this device")
                # print(uuid)
                measunit = uuid[22:24]
                measured = int((uuid[26:28] + uuid[24:26]), 16) * 0.01

                unit = ''

                if measunit.startswith(('03', 'b3')): unit = 'lbs'
                if measunit.startswith(('12', 'b2')): unit = 'jin'
                if measunit.startswith(('22', 'a2')): unit = 'Kg' ; measured = measured / 2

                if unit:
                    if measured != measured_anterior:
                        print("measured : %s %s" % (measured, unit))
                        measured_anterior = measured


except KeyboardInterrupt:
    sys.exit(1)
