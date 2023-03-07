# PN532 Gutter Reader

### Information
This modified PN532 module is for the use of reading & writing gutter-info from/to a ntag chip thats is stuck on the gutters.</br>
The card stores only the values `[BASE_WEIGHT, LAST_MESSURED_WEIGHT, GUTTER_TYPE, GUTTER_UASAGE_COUNT]`

these values can be written to by the `MiFareGutter()` class.

***To learn more about how the Mifare cards work [click Here](https://www.nxp.com/docs/en/data-sheet/MF1S50YYX_V1.pdf)***
<br/></br>
### Mifare_gutter() Callables
De functions that are needed to write and store values to the ntag chip are listed here, </br>with a description of what parameters to use.
</br></br>
`MifareGutter().scan_field()`</br>
This function should always be called when trying to communicate from the PN532 to a Mifare chip. It establishes a authentic connection and returns the Unique Identifier
</br></br>
`MifareGutter().set_baseweight_gutter(str_of_bytes)`<br/>
This function writes the base weight of the gutter to the defined address block and puts a 'B' for Base in front of the string.<br/>
***Notice: str_of_bytes can not be longer then 7 bytes,  str_of_bytes =  b'2883.23'*** 
</br></br>
`MifareGutter().write_last_messured(str_of_bytes)`<br/>
This function writes the lastmessured weight of the gutter to the defined address block and puts a 'W' for Weight in front of the string.<br/>
***Notice: str_of_bytes can not be longer then 7 bytes,  str_of_bytes =  b'9523.01'*** 
</br></br>
`MifareGutter().set_gutter_type(str_of_bytes)`<br/>
This function writes the gutter type to defined address block <br/>
***Notice: str_of_bytes can not be longer then 4 bytes,  str_of_bytes =  b'STLE' /  str_of_bytes =  b'PL'*** 
</br></br>
`MifareGutter().increment_gutter_usage()`<br/>
This function increments te gutter usage count <br/>
</br></br>
`MifareGutter().increment_gutter_usage()`<br/>
This function increments te gutter usage count <br/>
</br></br>
`MifareGutter().gutter_info()`<br/>
`gutter_info = [base_weight,last_messured, gutter_type, used_count]`<br/>
This function returns ***gutter_info*** <br/>
</br></br>

### Example
To use these functions all you have to do is add the module to yout ptoject and import the new Class **MifareGutter()**
```
from py532lib.mifare_gutter import *

scanner = MifareGutter()
scanner.SAMconfigure()

uid = scanner.scan_field()
```

# link to end product video
![scanningstation](./product.mp4)
