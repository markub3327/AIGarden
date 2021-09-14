import os
from datetime import datetime

import cv2
import serial


class AIGarden:
    def __init__(self):
        self.serial_fd = serial.Serial("/dev/ttyUSB0", 9600, timeout=0)
        self.serial_fd.flush()

        self.sensors = {
            "temp_0": 0.0,
            "temp_1": 0.0,
            "heat_index": 0.0,
            "humidity_0": 0.0,
            "pressure_0": 0.0,
            "soil_0": 0.0,
            "soil_1": 0.0,
        }

        self.cam_0 = cv2.VideoCapture(0)

        # CSV log
        if not os.path.exists("log.csv"):
            self.log_file.write(
                "time;temp_0;temp_1;heat_index;humidity_0;pressure_0;soil_0;soil_1\r\n"
            )

        self.log_file = open("log.csv", "a")

    # Watering
    def watering(self, pump_id, duration, force):
        pass

    def readSensors(self):
        # get time of measurement
        now = datetime.now()

        if self.serial_fd.in_waiting > 0:
            line = self.serial_fd.readline().decode("utf-8").rstrip()

            values = line.split(";")
            self.sensors["temp_0"] = values[0]
            self.sensors["temp_1"] = values[1]
            self.sensors["heat_index"] = values[2]
            self.sensors["humidity_0"] = values[3]
            self.sensors["pressure_0"] = values[4]
            self.sensors["soil_0"] = values[5]
            self.sensors["soil_1"] = values[6]

            print(self.sensors)

            self.log_file.write(
                f"{now.strftime('%d.%m.%Y, %H:%M:%S')};{self.sensors['temp_0']};{self.sensors['temp_1']};{self.sensors['heat_index']};{self.sensors['humidity_0']};{self.sensors['pressure_0']};{self.sensors['soil_0']};{self.sensors['soil_1']}\r\n"
            )

    def scanPlants(self):
        # Capture frame
        ret, frame = self.cam_0.read()
        if ret:
        	cv2.imwrite('image.jpg', frame)

    def close(self):
        self.log_file.close()

        self.cam_0.release()
