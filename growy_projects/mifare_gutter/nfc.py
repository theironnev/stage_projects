#from py532lib.i2c import *
#from py532lib.frame import *
#from py532lib.constants import *
#from py532lib.mifare import *
from py532lib.mifare_gutter import *


card = MifareGutter()
card.SAMconfigure()

uid =card.scan_field()
weight = bytearray(b'8874.21')    

f = b'\x00\x00\x00\x00'
data = bytearray(b'\x00\x00\xFF\xFF' )
mx_count = bytearray(b'\xFF\xFF\xFF\xFF' )
#sectorB = card.mifare_sector_block(14)
#adr = card.mifare_address(6,0)
#card.mifare_write_standard(0x15,f)
card.reset_gutter_used()
card.increment_gutter_usage()






a= card.gutter_info()
b = card.mifare_read(0x15)
#g = data2.encode()
print(a)
print(b)



#print(sectorB)



    

    
