"""This module provides convenient tools for the communication with
Mifare cards via the PN532.

Some knowledge of a Mifare card's layout and general access procedure
is needed to use this class effectively. Special care needs to be
taken when modifying trailer blocks because you may shut yourself
out of your card! Google "MF1S703x" for a good introduction to
Mifare cards.

A typical scenario would be:

card = Mifare()
card.SAMconfigure()
card.set_max_retries(MIFARE_SAFE_RETRIES)
uid = card.scan_field()
if uid:
    address = card.mifare_address(0,1)
    card.mifare_auth_a(address,MIFARE_FACTORY_KEY)
    data = card.mifare_read(address)
    card.in_deselect() # In case you want to authorize a different sector.
    
"""

import py532lib.i2c as i2c
from py532lib.frame import Pn532Frame as Pn532Frame
from py532lib.constants import *
import logging
import math
import warnings
import datetime


MIFARE_COMMAND_READ = 0x30
MIFARE_COMMAND_WRITE_16 = 0xA0
MIFARE_COMMAND_WRITE_4 = 0xA2
MIFARE_WAIT_FOR_ENTRY = 0xFF # MxRtyPassiveActivation value: wait until card enters field.
MIFARE_SAFE_RETRIES = 5 # This number of retries seems to detect most cards properlies.

"address of hese parameters have to stay next to ech other in the same order fot de read functions to work"
GUTTER_TYPE_ADRS = 0x10
NET_WEIGHT_ADRS = 0x12  #  BASE WEIGHT stored on 2 blocks address{0x12 & 0x13}
USE_COUNT_ADRS= 0x14    #address 0x14 & 0x15
DATE_TIME_ADRS =0x16





class MifareGutter(i2c.Pn532_i2c):

    """This class allows for the communication with Mifare cards via
    the PN532.

    Compared to its superclass, this class provides a bit more
    sophisticated tools such as reading the contents of a Mifare
    card or writing to them, access restrictions, and key management.
    """
    
    def __init__(self):
        """Set up and configure PN532."""
        i2c.Pn532_i2c.__init__(self)
        self._uid = False
    
    def set_max_retries(self,mx_rty_passive_activation):
        """Configure the PN532 for the number of retries attempted
        during the InListPassiveTarget operation (set to
        MIFARE_SAFE_RETRIES for a safe one-time check, set to
        MIFARE_WAIT_FOR_ENTRY so it waits until entry of a card).
        """
        # We set MxRtyPassiveActivation to 5 because it turns out that one
        # try sometimes does not detect the card properly.
        frame = Pn532Frame(frame_type=PN532_FRAME_TYPE_DATA,
                           data=bytearray([PN532_COMMAND_RFCONFIGURATION,
                                           PN532_RFCONFIGURATION_CFGITEM_MAXRETRIES,
                                           0xFF,0x01,mx_rty_passive_activation]))
        self.send_command_check_ack(frame)
        self.read_response()

    def scan_field(self):
        """Scans the PN532's field for a Mifare card using the
        InListPassiveTarget operation.

        Returns the card's UID (a bytearray) if a card was in the field
        or False if no card was in the field. Only one card is
        detected at a time (the PN532 can handle two but this is not
        implemented here). False is never returned if the number of
        retries (see set_max_retries()) is set to MIFARE_WAIT_FOR_ENTRY.
        """
        frame = Pn532Frame(frame_type=PN532_FRAME_TYPE_DATA,
                           data=bytearray([PN532_COMMAND_INLISTPASSIVETARGET, 0x01, 0x00]))
        self.send_command_check_ack(frame)
        response = self.read_response().get_data()
        target_count = response[1]
        if not target_count:
            self._uid = False
            return False
        uid_length = response[6]
        self._uid = response[7:7 + uid_length]
        self._uid="%02X %02X %02X %02X %02X %02X %02X" %(self._uid[0], self._uid[1], self._uid[2],
                                                         self._uid[3], self._uid[4],self._uid[5], self._uid[6])
        self._uid = self._uid.replace(" ", ":")
        return self._uid

    def in_data_exchange(self,data):
        """Sends a (Mifare) command to the currently active target.

        The "data" parameter contains the command data as a bytearray.
        Returns the data returned by the command (as a bytearray).
        Raises an IOError if the command failed.
        """
        logging.debug("InDataExchange sending: " + " ".join("{0:02X}".format(k) for k in data))
        logging.debug(data)
        frame = Pn532Frame(frame_type=PN532_FRAME_TYPE_DATA, data=bytearray([PN532_COMMAND_INDATAEXCHANGE, 0x01]) + data)
        self.send_command_check_ack(frame)
        response_frame = self.read_response()
        if response_frame.get_frame_type() == PN532_FRAME_TYPE_ERROR:
            raise IOError("InDataExchange failed (error frame returned)")
        response = response_frame.get_data()
        logging.debug("InDataExchange response: " + " ".join("{0:02X}".format(k) for k in response))
        if response[1] != 0x00:
            # Only the status byte was returned. There was an error.
            if response[1] == 0x14:
                raise IOError("Mifare authentication failed")
            else:
                raise IOError("InDataExchange returned error status: {0:#x}".format(response[1]))
        return response[2:]

    def in_deselect(self):
        """Deselects the current target."""
        logging.debug("InDeselect sending...")
        frame = Pn532Frame(frame_type=PN532_FRAME_TYPE_DATA, data=bytearray([PN532_COMMAND_INDESELECT, 0x01]))
        self.send_command_check_ack(frame)
        response_frame = self.read_response()
        if response_frame.get_frame_type() == PN532_FRAME_TYPE_ERROR:
            raise IOError("InDeselect failed (error frame returned)")
        response = response_frame.get_data()
        logging.debug("InDeselect response: " + " ".join("{0:02X}".format(k) for k in response))
        if response[1] != 0x00:
            # Only the status byte was returned. There was an error.
            raise IOError("InDataExchange returned error status: {0:#x}".format(response[1]))

    def mifare_address(self,sector,block):
        """Returns a one byte address for the given Mifare sector and block."""
        if sector < 32:
            if sector < 0 or block > 3 or block < 0:
                raise IndexError("Invalid sector / block: {0} / {1}".format(sector,block))
            return sector * 4 + block
        else:
            if sector > 39 or block < 0 or block > 15:
                raise IndexError("Invalid sector / block: {0} / {1}".format(sector,block))
            return 32 * 4 + (sector - 32) * 16 + block

    def mifare_sector_block(self,address):
        """Returns a tuple (sector,block) for the given address."""
        if address > 255 or address < 0:
            raise IndexError("Invalid Mifare block address: {0}".format(address))
        if address < 128:
            return (address >> 2,address & 3)
        else:
            return (32 + ((address - 128) >> 4),(address - 128) & 15)



    def mifare_read(self,address):
        """Read and return 16 bytes from the data block at the given address."""
        return self.in_data_exchange(bytearray([MIFARE_COMMAND_READ,address]))

    def mifare_write_standard(self,address,data):
        """Write 16 bytes to the data block on a Mifare Standard card
        at the given address."""
        if len(data) > 16:
            raise IndexError("Data cannot exceed 16 bytes (is {0} bytes)".format(len(data)))
        self.in_data_exchange(bytearray([MIFARE_COMMAND_WRITE_16,address]) + data + (b'\x00' * (16 - len(data))))

    def mifare_write_ultralight(self,address,data):
        """Write 4 bytes to the data block on a Mifare Ultralight card
        at the given address."""
        if len(data) > 4:
            raise IndexError("Data cannot exceed 4 bytes (is {0} bytes)".format(len(data)))
        self.in_data_exchange(bytearray([MIFARE_COMMAND_WRITE_4,address]) + data + (b'\x00' * (4 - len(data))))
    
    def set_netweight_gutter(self,str_of_bytes):
        """ This is just to give the value informtion code when storing it on the ntag, 'B'stnds for BaseWeight """
        byte_array = bytearray(str_of_bytes)
        
        
        """ deviding the string of bytes because on block can only take up 4 bytes"""
        first_four_bytes = byte_array[0:4]
        last_four_bytes = byte_array[4:8]
        self.mifare_write_ultralight(NET_WEIGHT_ADRS, first_four_bytes)
        self.mifare_write_ultralight((NET_WEIGHT_ADRS + 1), last_four_bytes)
        

    def set_datetime(self):
        date = datetime.datetime.now()
        date = date.strftime("%y%m%d%H%M")
        
        int_datetime = int(date)
     
        byte_array = int_datetime.to_bytes(4,"big")
        self.mifare_write_ultralight(DATE_TIME_ADRS, byte_array)

        
        
    def set_gutter_type(self, str_of_bytes):
        """the first for bytes wil be written if the str_of_byte is longer then  bytes"""
        self.mifare_write_ultralight(GUTTER_TYPE_ADRS, str_of_bytes[0:4])
        self.mifare_write_ultralight(GUTTER_TYPE_ADRS+1, str_of_bytes[4:8])
        
    def s32(self,value):
        return -(value &0x80000000)| (value & 0x7fffffff)
        
    
    def increment_gutter_usage(self):
        mx_count = 4294967294
        counter = self.in_data_exchange(bytearray([MIFARE_COMMAND_READ,USE_COUNT_ADRS]))
        de = self.s32(counter[0:4])
        new_int = int.from_bytes(de,"big")+1
        print(counter[0:4])
        print(new_int)
        
        #if new_int > mx_count:
         #   warnings.warn('max count of 4294967295 reched; count wil be reset to zero!' )
            #self.reset_gutter_used()
            
        new_byte = new_int.to_bytes(4,"big")
        
        scomplement = self.s32(new_byte) 
       
        self.mifare_write_ultralight(USE_COUNT_ADRS,scomplement)
    
    def reset_gutter_used(self):
        count = b'\x00\x00\x00\x00'
        self.mifare_write_standard(USE_COUNT_ADRS,count)
    
        
    def gutter_info(self):
        "these variables store the bytearrays from the address blocks that are used "
        type_gutter = self.mifare_read(GUTTER_TYPE_ADRS)
        weight =  self.mifare_read(NET_WEIGHT_ADRS)
        counts = self.mifare_read(USE_COUNT_ADRS)
        timedate = self.mifare_read(DATE_TIME_ADRS)
        
        "these variables take the value out of the bytearray and makes  srting of them"
        gutter_type = type_gutter[0:7].decode()
        net_weight = weight[0:7].decode()
        used_count = str(int.from_bytes(counts[0:4],"big"))
        datetime = str(int.from_bytes(timedate[0:4],"big"))
        
        "string array"
        gutter_info = [gutter_type,net_weight, used_count, datetime]
        
        return gutter_info
        