
import cv2
from serial_thread import SerialThread

class AIGarden:
    def __init__(self):
        self.cam_0 = cv2.VideoCapture(0)

        self.serialThread = SerialThread()
        self.serialThread.run()

    # Watering
    def watering(self, pump_id, duration, force):
        pass

    def readSensors(self):
        print(self.serialThread.sensors)

    def scanPlants(self):
        # Capture frame
        ret, frame = self.cam_0.read()
        if ret:
            cv2.imwrite('image.jpg', frame)

            print("Image captured !")

    def close(self):
        self.serialThread.close()
        self.cam_0.release()
