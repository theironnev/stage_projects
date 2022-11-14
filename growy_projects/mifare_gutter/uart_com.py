import serial
import time


class SerialToScale:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.5)
        self.ser.reset_input_buffer()

    def return_weight(self):
        self.ser.write("w\n".encode('utf-8'))
        line = self.ser.readline().rstrip()
        print(line)

        return line

    def send_tare(self):
        self.ser.write("t\n".encode('utf-8'))
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
