import threading

import cv2
from tflite_runtime.interpreter import Interpreter
from utils import load_labels


class CameraThread:
    """
    CameraThread
    ===============
    """

    def __init__(self):
        self.done = False

        # Init camera
        self.cam_0 = cv2.VideoCapture(0)

        # TFLite
        self._interpreter = Interpreter("models/detect.tflite")
        self._interpreter.allocate_tensors()
        self._input_details = self._interpreter.get_input_details()
        self._output_details = self._interpreter.get_output_details()

        # Load labels
        self._labels = load_labels("models/coco_labels.txt")

        # creating thread
        self.thread = threading.Thread(target=self.fn)  # , args=(10,))

    def fn(self):
        while not self.done:
            # Capture image
            ret, self.image = self.cam_0.read()

            if ret:
                # Preprocess the input image
                img = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img, (300, 300), interpolation=cv2.INTER_AREA)
                img = img.reshape(1, img.shape[0], img.shape[1], img.shape[2])

                # set input tensor
                self._interpreter.set_tensor(self._input_details[0]["index"], img)

                # predict
                self._interpreter.invoke()

                # get output tensor
                boxes = self._interpreter.get_tensor(self._output_details[0]["index"])
                classes = self._interpreter.get_tensor(self._output_details[1]["index"])
                scores = self._interpreter.get_tensor(self._output_details[2]["index"])
                count = self._interpreter.get_tensor(self._output_details[3]["index"])

                for i in range(int(count[0])):
                    if scores[0, i] > 0.5:
                        # get unnormalized coordinates
                        x0 = int(boxes[0, i, 1] * self.image.shape[1])
                        y0 = int(boxes[0, i, 0] * self.image.shape[0])
                        x1 = int(boxes[0, i, 3] * self.image.shape[1])
                        y1 = int(boxes[0, i, 2] * self.image.shape[0])

                        cv2.rectangle(self.image, (x0, y0), (x1, y1), (0, 255, 0), 2)
                        cv2.putText(
                            self.image,
                            f"{self._labels[classes[0, i]]}, {scores[0, i]}",
                            (x0, y0 + 25),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 255, 0),
                            2,
                        )

    def run(self):
        # starting thread
        self.thread.start()

    def close(self):
        self.done = True
        self.cam_0.release()

        self.thread.join()
