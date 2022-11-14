from py532lib.mifare_gutter import *
import binascii

#scanner = MifareGutter()
#scanner.SAMconfigure()
#scnner.set_max_retries(100)



#def wait_on_gutter():
#    while True:
#        if scanner.scan_field()!= False:
#            return True

        
#print(wait_on_gutter())
        
value = b'\x00\x00\x00\x00'
r = b'\x00\x00\x003' 
oo = 'ff090101' 
split = [value[i] for i in range(0,len(value))]
# x = 0
# while split[3] <255:
#     print(split[3])
#     split[3] += 1
#     joined = bytes(split)
#     print(joined)
    
#print(joined)
#print(value)
d = binascii.b2a_hex(r)
e = binascii.unhexlify(d)
length = len(value)
new_int = int.from_bytes(e,'big')+1

make = new_int.to_bytes(4,'big')
n = binascii.hexlify(make)
print(new_int)
print(make)

def inc(v):
    d = binascii.b2a_hex(v)
    e = binascii.unhexlify(d)
    length = len(value)
    new_int = int.from_bytes(e,'big')+1

    make = new_int.to_bytes(4,'big')
    n = binascii.hexlify(make)
    print(new_int)
    print(make)
    inc(make)

inc(value)

#for i in range(0,len(value)):
#    print(joined[i])