
import serial
import time

if __name__ == '__main__':
    #ttyS0 is rpi uart port
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    while True:
       # data = input()
        ser.write("w\n".encode('utf-8'))
        print("w\n".encode('utf-8'))
        line =ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(1)
