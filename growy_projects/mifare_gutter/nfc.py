#from py532lib.i2c import *
#from py532lib.frame import *
#from py532lib.constants import *
#from py532lib.mifare import *
from py532lib.mifare_gutter import *


card = MifareGutter()
card.SAMconfigure()

uid =card.scan_field()
weight = bytearray(b'8874.21') 
gutter_type =  b'STLE'
card.set_baseweight_gutter(weight)
card.set_gutter_type(gutter_type)
#card.reset_gutter_used()
card.increment_gutter_usage()



a= card.gutter_info()
print(uid)
print(a)



#print(sectorB)



    

    
