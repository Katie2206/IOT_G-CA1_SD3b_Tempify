# #!/usr/bin/python3
# import RPi.GPIO as GPIO
# import time

# # GPIO setup
# channel = 21  # GPIO pin connected to the DO (Digital Output) of the sensor
# GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
# GPIO.setup(channel, GPIO.IN)  # Set GPIO pin as input

# try:
#     while True:
#         # Check if the sensor is connected properly
#         if GPIO.input(channel) not in [0, 1]:
#             print("Sensor not connected or malfunctioning")
#         else:
#             # Read the sensor state and print the corresponding message
#             sensor_state = GPIO.input(channel)
#             if sensor_state == 1:
#                 print("Dry Soil: GPIO State = HIGH (1)")
#             else:
#                 print("Water or Moist Soil: GPIO State = LOW (0)")

#         # Wait for 3 seconds before reading again
#         time.sleep(3)

# except KeyboardInterrupt:
#     # Graceful exit on Ctrl+C
#     print("Exiting gracefully")

# finally:
#     # Clean up GPIO configurations
#     GPIO.cleanup()
#!/usr/bin/python
import RPi.GPIO as GPIO
import time
 
#GPIO SETUP
channel = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)
 
def callback(channel):
        if GPIO.input(channel):
                print ("No Water Detected!")
        else:
                print ("Water Detected!")
 
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change
 
# infinite loop
try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    # Graceful exit on Ctrl+C
    print("Exiting gracefully")

finally:
    # Clean up GPIO configurations
    GPIO.cleanup()
