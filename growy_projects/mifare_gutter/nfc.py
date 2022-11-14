from py532lib.mifare_gutter import *
import datetime


card = MifareGutter()
card.SAMconfigure()
card.set_max_retries(MIFARE_WAIT_FOR_ENTRY)

uid = card.scan_field()

weight = bytearray(b'2390,21') 
gutter_type =  b'plastic'
char = b'hoide'
r = b'\x00\x00\x00\x04'



def test_write(adres, data):
    card.mifare_write_ultralight(adres,data)
    print(card.mifare_read(adres))

def test_read(adres):
    data = card.mifare_read(adres)
    print(data)
    #new_int = int.from_bytes(data[0:4],"big")
    

def test_increment():
    #card.reset_gutter_used()
    while True:
        card.increment_gutter_usage()

#test_read(0x14)a


print(uid)
#card.reset_gutter_used()
#card.increment()
#card.set_gutter_type(gutter_type)
#card.set_datetime()
#card.set_netweight_gutter(weight)


#test_write(0x15,b'nogu')



print(card.gutter_info())