import serial
from serial import SerialException
import time

port = '/dev/ttyACM0'
baudrate = 115200

class SerialToScale:
    
    def __init__(self):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=0.5)
            self.ser.reset_input_buffer()
            self.connect = True
        except SerialException:
            print("port not found")
            self.connect = False

    def return_weight(self):
        if self.connect == True:
            self.ser.write("w\n".encode('utf-8'))
            line = self.ser.readline().rstrip()
            print(line)
            return line
        else:
            print("no serial port found")
            return b'none'
            

    def send_tare(self):
        if sel.connect == True:
            self.ser.write("t\n".encode('utf-8'))
        else:
            print("no scale to tare")
    #    line =ser.readline().rstrip()
    #    print(line)

    #    return line



def main():
    s = SerialToScale()
    print("put nothing on the scale")
    time.sleep(4)
    s.send_tare()
    print("now you can put weight")
    while True:
        print(s.return_weight())


if __name__ == '__main__':
    
    main()
