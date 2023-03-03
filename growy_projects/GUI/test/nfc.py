from py532lib.mifare_gutter import *

card = MifareGutter()
card.SAMconfigure()
card.set_max_retries(MIFARE_WAIT_FOR_ENTRY)

uid = card.scan_field()

weight = bytearray(b'8874.21') 
gutter_type =  b'plass'
char = b'hoide' 
#card.set_baseweight_gutter(weight)

#uid = "%02x%02x%02x%02x%02x%02x%02x"%(data


def test_write(adres, data):
    card.mifare_write_ultralight(adres,data)
    print(card.mifare_read(adres))

def test_read(adres):
    data = card.mifare_read(adres)
    print(data)
    new_int = int.from_bytes(data[0:4],"big")
    print(new_int)

def test_increment():
    card.reset_gutter_used()
    while True:
        card.increment_gutter_usage()
    

#test_increment()
test_write(0x15,b'\xFF\x30\x60\x01')
test_read(0x15)

a = '\xik\xzeg\xma\xar'
print(bytearray(a))
print(card.gutter_info())