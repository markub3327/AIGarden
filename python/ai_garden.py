import cv2
from core import CameraThread, SerialThread


class AIGarden:
    def __init__(self):
        # Init camera
        self.camThread = CameraThread()
        self.camThread.run()

        # Init serial port
        self.serialThread = SerialThread()
        self.serialThread.run()

    # Watering
    def watering(self, pump_id, duration, force):
        pass

    def readSensors(self):
        return self.serialThread.sensors

    def scanPlants(self):
        while True:
            ret, jpeg = cv2.imencode(".jpg", self.camThread.image)
            if ret:
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + jpeg.tobytes() + b"\r\n\r\n"
                )

    def close(self):
        self.serialThread.close()
        self.camThread.close()
