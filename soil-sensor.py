#!/usr/bin/python
import RPi.GPIO as GPIO
import time

# GPIO Setup
channel = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

try:
    while True:
        if GPIO.input(channel):
            print("Sensor State: No Water Detected")
        else:
            print("Sensor State: Water Detected")
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting Program")
finally:
    GPIO.cleanup()
