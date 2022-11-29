import serial
from serial import SerialException
import time

port = '/dev/ttyACM0'
baudrate = 115200

class SerialToScale:
    
    def __init__(self):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=None)
            self.ser.reset_input_buffer()
            self.connect = True
        except SerialException:
            self.connect = False

    def return_weight(self):
        if self.connect == True:
            self.ser.write("w\n".encode('utf-8'))
            line = self.ser.readline().rstrip()
            print(line)
            return line
        else:
            return b'none'
            

    def send_tare(self):
        if self.connect == True:
            self.ser.write("t\n".encode('utf-8'))
        else:
            print("no scale to tare")
