from time import sleep

import adafruit_dht
import board
from gpiozero import PWMOutputDevice


class AIGarden:
    def __init__(self, pump0_pin="GPIO12", pump1_pin="GPIO13", dht_pin=board.D18):
        # Watering
        self.pumps = [PWMOutputDevice(pump0_pin), PWMOutputDevice(pump1_pin)]

        # Humidity sensor
        self.dhtDevice = adafruit_dht.DHT11(dht_pin, use_pulseio=False)

    # Watering
    def watering(self, pump_id, duration):
        # start pump
        self.pumps[pump_id].value = 0.75

        # waiting ...
        for t in range(1, 101, 1):
            sleep(duration / 100.0)
            print(f"Task Completed ... {t}%", end="\r")

        # stop pump
        self.pumps[pump_id].value = 0.0

    def readHumidity(self):
        self.temperature_c = self.dhtDevice.temperature
        self.humidity = self.dhtDevice.humidity

        # debug
        print(
            "Temp 0: {:.1f}°C\tHumidity: {}%".format(self.temperature_c, self.humidity)
        )

    def readSoilMoisture(self):
        pass
