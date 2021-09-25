import serial
import threading
from datetime import datetime
import os



class SerialThread():
    """
    SerialThread
    ===============
    
    Attributes:
        port_name (str): port name
    """
    
    def __init__(self, port_name="/dev/ttyUSB0"):
        self.done = False

        self.serial_fd = serial.Serial(port_name, 9600, timeout=None)
        self.serial_fd.flush()
    
        # CSV log
        self.log_file = open("log.csv", "a")
        if not os.path.exists("log.csv"):
            self.log_file.write(
                "time;temp_0;temp_1;heat_index;humidity_0;pressure_0;soil_0;soil_1\r\n"
            )

        # creating thread
        self.thread = threading.Thread(target=self.fn) #, args=(10,))
    
        self.sensors = {
            "temp_0": 0.0,
            "temp_1": 0.0,
            "heat_index": 0.0,
            "humidity_0": 0.0,
            "pressure_0": 0.0,
            "soil_0": 0.0,
            "soil_1": 0.0,
        }

    def fn(self):
        while not self.done:
            # get time of measurement
            now = datetime.now()

            # use CSV formatting
            if self.serial_fd.in_waiting > 0:
                line = self.serial_fd.readline().decode("utf-8").rstrip()
                values = line.split(";")

                if "$READ" in values[0]:
                    self.sensors["temp_0"] = values[1]
                    self.sensors["temp_1"] = values[2]
                    self.sensors["heat_index"] = values[3]
                    self.sensors["humidity_0"] = values[4]
                    self.sensors["pressure_0"] = values[5]
                    self.sensors["soil_0"] = values[6]
                    self.sensors["soil_1"] = values[7]

                    self.log_file.write(
                        f"{now.strftime('%d.%m.%Y, %H:%M:%S')};{self.sensors['temp_0']};{self.sensors['temp_1']};{self.sensors['heat_index']};{self.sensors['humidity_0']};{self.sensors['pressure_0']};{self.sensors['soil_0']};{self.sensors['soil_1']}\r\n"
                    )

            # Automatically sync clock
            self.write(f"$TIME;{now.day};{now.month};{now.year};{now.hour};{now.minute};{now.second}")

    def run(self):
        # starting thread
        self.thread.start()
    
    def write(self, data):
        return self.serial_fd.write(data)

    def close(self):
        self.done = True
        self.log_file.close()

        self.thread.join()
