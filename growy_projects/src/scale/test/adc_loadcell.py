#!/usr/bin/env python3
import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711


try:
    GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
    # Create an object hx which represents your real hx711 chip
    # Required input parameters are only 'dout_pin' and 'pd_sck_pin'
    hx = HX711(6,5)
    # measure tare and save the value as offset for current channel
    # and gain selected. That means channel A and gain 128
    err = hx.zero()
    # check if successful
    if err:
        raise ValueError('Tare is unsuccessful.')

    while True:
        print(hx.get_weight_mean(), 'raw conversion')

except (KeyboardInterrupt, SystemExit):
    print('Bye :)')

finally:
    GPIO.cleanup()

if __name__ == "__main__":
        example()
