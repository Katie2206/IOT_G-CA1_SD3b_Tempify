#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

# GPIO setup
channel = 21  # GPIO pin connected to the DO (Digital Output) of the sensor
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
GPIO.setup(channel, GPIO.IN)  # Set GPIO pin as input

try:
    while True:
        # Check if the sensor is connected properly
        if GPIO.input(channel) not in [0, 1]:
            print("Sensor not connected or malfunctioning")
        else:
            # Read the sensor state and print the corresponding message
            sensor_state = GPIO.input(channel)
            if sensor_state == 1:
                print("Dry Soil: GPIO State = HIGH (1)")
            else:
                print("Water or Moist Soil: GPIO State = LOW (0)")

        # Wait for 3 seconds before reading again
        time.sleep(3)

except KeyboardInterrupt:
    # Graceful exit on Ctrl+C
    print("Exiting gracefully")

finally:
    # Clean up GPIO configurations
    GPIO.cleanup()
