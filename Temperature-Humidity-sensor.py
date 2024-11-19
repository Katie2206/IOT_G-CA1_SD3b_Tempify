import time
import board
import adafruit_dht

# Initialize the DHT device, with the data pin connected to GPIO4 (D4)
dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

try:
    while True:
        try:
            # Read the temperature and humidity values
            temperature_c = dhtDevice.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = dhtDevice.humidity

            print(
                "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                    temperature_f, temperature_c, humidity
                )
            )

        except RuntimeError as error:
            # Handle common reading errors without exiting
            print(f"Reading error: {error.args[0]}")
            time.sleep(2.0)
            continue

        time.sleep(2.0)

except KeyboardInterrupt:
    print("Exiting script")

finally:
    dhtDevice.exit()  # Ensures the device is released properly on exit
