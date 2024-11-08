#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

# GPIO SETUP
channel = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

def callback(channel):
    if GPIO.input(channel):
        print("Soil level is optimal")
    else:
        print("Soil is dry, consider watering")

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # detect pin state changes
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, run function on change

try:
    # Infinite loop
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting gracefully")
finally:
    GPIO.cleanup()  # cleanup on exit
