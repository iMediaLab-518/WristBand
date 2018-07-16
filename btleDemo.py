from bluepy import btle
from bluepy.btle import DefaultDelegate
import time

class NotifyDelegate(DefaultDelegate):
    def __init__(self):
            DefaultDelegate.__init__(self)
    def handleNotification(self,cHandle,data):
        print("notify from "+str(cHandle)+str(data)+"\n")

dev=btle.Peripheral("50:65:83:94:28:02").withDelegate(NotifyDelegate())

time.sleep(0.5)

for ser in dev.getServices():
    print(str(ser))
    for chara in ser.getCharacteristics():
        print(str(chara))
        print("Handle is "+str(chara.getHandle()))
        print("properties is "+chara.propertiesToString())
        if(chara.supportsRead()):
            print(type(chara.read()))
            print(chara.read())
    print("\n")



dev.writeCharacteristic(37,b'A',withResponse=True)
dev.waitForNotifications(1)
dev.writeCharacteristic(37,b'b',withResponse=True)
dev.waitForNotifications(1)
dev.writeCharacteristic(37,b'A',withResponse=True)
dev.waitForNotifications(1)
dev.writeCharacteristic(37,b'b',withResponse=True)

i=0
dev.writeCharacteristic(37,b'B',withResponse=False)
while(True):
    if(dev.waitForNotifications(1)):
        i=i+1
        if(i>1000):
            break
        continue
    print("Waiting...")
time.sleep(0.5)

dev.disconnect()