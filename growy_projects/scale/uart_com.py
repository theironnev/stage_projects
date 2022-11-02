
import serial
import time

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.5)
ser.reset_input_buffer()


def return_weight():
    ser.write("w\n".encode('utf-8'))
    line =ser.readline().rstrip()
    print(line)
 
    return line

def send_tare():
    ser.write("t\n".encode('utf-8'))
#    line =ser.readline().rstrip()
#    print(line)
 
#    return line



def main():
    print("put nothing on the scale")
    time.sleep(4)
    send_tare()
    print("now you can put weight")
    while True:
        print(return_weight())


if __name__ == '__main__':
    
    main()
