import os
from datetime import datetime
from time import sleep

import adafruit_dht
import board
from gpiozero import PWMOutputDevice, Servo


class AIGarden:
    def __init__(self, pump0_pin="12", pump1_pin="13", dht_pin=board.D5):
        # Watering
        self.pumps = [PWMOutputDevice(pump0_pin), PWMOutputDevice(pump1_pin)]

        # solar panels
        self.servos = [Servo(17), Servo(27), Servo(22)]
        for s in self.servos:
            s.value = 0

        # Humidity sensor
        self.dhtDevice = adafruit_dht.DHT22(dht_pin, use_pulseio=False)
        self.temp0 = 0.0
        self.humidity = 0.0

        # CSV log
        if os.path.exists("log.csv") is None:
            self.log_file.write(
                "time;temp0;humidity;pumps0;pumps1;servos0;servos1;servos2\r\n"
            )

        self.log_file = open("log.csv", "a")

    # Watering
    def watering(self, pump_id, duration, force):
        # start pump
        self.pumps[pump_id].value = force

        # write to log (befor)
        # self.readHumidity()
        now = datetime.now()
        self.log_file.write(
            f"{now.strftime('%H:%M:%S')};{self.temp0};{self.humidity};{self.pumps[0].value};{self.pumps[1].value};{self.servos[0].value};{self.servos[1].value};{self.servos[2].value}\r\n"
        )

        # waiting ...
        for t in range(1, 101, 1):
            sleep(duration / 100.0)
            print(f"Task Completed ... {t}%", end="\r")

        # stop pump
        self.pumps[pump_id].value = 0.0

        # write to log (befor)
        # self.readHumidity()
        now = datetime.now()
        self.log_file.write(
            f"{now.strftime('%H:%M:%S')};{self.temp0};{self.humidity};{self.pumps[0].value};{self.pumps[1].value};{self.servos[0].value};{self.servos[1].value};{self.servos[2].value}\r\n"
        )

    def readHumidity(self):
        try:
            self.temp0 = self.dhtDevice.temperature
            self.humidity = self.dhtDevice.humidity

            # debug
            print(f"Temp 0: {self.temp0}°C\tHumidity: {self.humidity}%")
        except RuntimeError as error:
            print(error.args[0])

    def readSoilMoisture(self):
        pass

    def close(self):
        self.log_file.close()

        self.dhtDevice.exit()
