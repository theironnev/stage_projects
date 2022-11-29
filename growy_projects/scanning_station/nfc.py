from py532lib.mifare_gutter import *

card = MifareGutter()
card.SAMconfigure()
card.set_max_retries(MIFARE_WAIT_FOR_ENTRY)

uid = card.scan_field()


#card.mifare_write_ultralight(0x18, b'\x00\x00\x00\x35')
#print(card.mifare_read(0x18))

#card.set_netweight_gutter(b'\x00\x00\x00\x00')
#card.set_gutter_type(b'\x00\x00\x00\x00')
#card.set_datetime()
#card.reset_gutter_used()
#test_increment_gutter()
print(card.gutter_info())

    
    