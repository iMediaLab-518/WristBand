import binascii
import struct
import time
from bluepy.btle import UUID, Peripheral
 
temp_uuid = UUID(0x2221)
 
p = Peripheral("cc:50:98:e9:2a:b9", "random")
 
try:
    ch = p.getCharacteristics(uuid=temp_uuid)[0]
    if (ch.supportsRead()):
        while 1:
            val = binascii.b2a_hex(ch.read())
            val = binascii.unhexlify(val)
            val = struct.unpack('f', val)[0]
            print (str(val) + " deg C")
            time.sleep(1)
 
finally:
    p.disconnect()