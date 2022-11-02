from py532lib.mifare_gutter import *

scanner = MifareGutter()
scanner.SAMconfigure()
scnner.set_max_retries(100)



def wait_on_gutter():
    while True:
        if scanner.scan_field()!= False:
            return True

        
#print(wait_on_gutter())