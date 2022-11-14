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
#card.set_netweight_gutter("2456".encode())
#card.set_gutter_type("STEEL".encode())
#card.set_datetime()
#card.increment_gutter_usage()
card.reset_gutter_used()

while True:
    card.increment_gutter_usage()
    b = card. mifare_read(USE_COUNT_ADRS)
    print(b)
    if b == '53':
        print("einde")

a = card.gutter_info()
print(a)
#print(card.gutter_info())