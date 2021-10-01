import cv2
from serial_thread import SerialThread
from tflite_runtime.interpreter import Interpreter
from utils import load_labels


class AIGarden:
    def __init__(self):
        # Init camera
        self.cam_0 = cv2.VideoCapture(0)

        # TFLite
        self._interpreter = Interpreter("models/detect.tflite")
        self._interpreter.allocate_tensors()
        self._input_details = self._interpreter.get_input_details()
        self._output_details = self._interpreter.get_output_details()
        print(self._input_details)
        print(self._output_details)

        # Load labels
        self._labels = load_labels("models/coco_labels.txt")

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
            # Capture image
            ret, img = self.cam_0.read()

            if ret:
                # Preprocess the input image
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, (300, 300), interpolation=cv2.INTER_AREA)
                img = img.reshape(1, img.shape[0], img.shape[1], img.shape[2])
                print(img.dtype)

                # set input tensor
                self._interpreter.set_tensor(self._input_details[0]["index"], img)

                # predict
                self._interpreter.invoke()

                # get output tensor
                boxes = self._interpreter.get_tensor(self._output_details[0]["index"])
                classes = self._interpreter.get_tensor(self._output_details[1]["index"])
                scores = self._interpreter.get_tensor(self._output_details[2]["index"])
                count = self._interpreter.get_tensor(self._output_details[3]["index"])

                print(f"count: {count}")
                print(f"boxes.shape[1]: {boxes.shape[1]}")

                for i in range(count):
                    if scores[0, i] > 0.5:
                        # get unnormalized coordinates
                        x0 = int(boxes[0, i, 1] * img.shape[1])
                        y0 = int(boxes[0, i, 0] * img.shape[0])
                        x1 = int(boxes[0, i, 3] * img.shape[1])
                        y1 = int(boxes[0, i, 2] * img.shape[0])
                        print(f"{x0}, {y0}, {x1}, {y1}")

                        cv2.rectangle(img, (x0, y0), (x1, y1), (0, 255, 0), 2)
                        cv2.putText(
                            img,
                            f"{self._labels[classes[0, i]]}, {scores[0, i]}",
                            (x0, y0),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 255, 0),
                            2,
                        )

                ret, jpeg = cv2.imencode(".jpg", img)
                if ret:
                    yield (
                        b"--frame\r\n"
                        b"Content-Type: image/jpeg\r\n\r\n"
                        + jpeg.tobytes()
                        + b"\r\n\r\n"
                    )

    def close(self):
        self.serialThread.close()
        self.cam_0.release()
