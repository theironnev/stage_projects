from py532lib.mifare_gutter import *

card = MifareGutter()
card.SAMconfigure()
card.set_max_retries(MIFARE_WAIT_FOR_ENTRY)

uid = card.scan_field()


def test_write(adres, data):
    card.mifare_write_ultralight(adres,data)
    print(card.mifare_read(adres))

def test_read(adres):
    data = card.mifare_read(adres)
    print(data)
    new_int = int.from_bytes(data[0:4],"big")
    print(new_int)

def test_increment():
    counter = b'\x00\x00\x00\x00'
    while True:
        new_int = int.from_bytes(counter,"big")+1
        print(counter)
        print(new_int)
        
            
        new_byte = new_int.to_bytes(4,"big")
        
        counter = new_byte
    

#card.mifare_write_ultralight(0x18, b'\x00\x00\x00\x35')
#print(card.mifare_read(0x18))

#test_increment()
#card.set_netweight_gutter(b'\x00\x00\x00\x00')
#card.set_gutter_type(b'\x00\x00\x00\x00')
#card.set_datetime()
card.reset_gutter_used()
#card.increment()
#print(card.gutter_info())

while True:
    card.increment_gutter_usage()
    print(card.gutter_info())
    
    