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

        # Init camera - set to 720p
        self.cam_0 = cv2.VideoCapture(0)
        self.cam_0.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cam_0.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        # TFLite
        self._interpreter = Interpreter("models/detect.tflite")
        self._interpreter.allocate_tensors()
        self._input_details = self._interpreter.get_input_details()
        self._output_details = self._interpreter.get_output_details()

        # Load labels
        self._labels = load_labels("models/coco.yaml")

        # creating thread
        self.thread = threading.Thread(target=self.fn)  # , args=(10,))

    def fn(self):
        while not self.done:
            # Capture image
            ret, img_org = self.cam_0.read()

            if ret:
                # Preprocess the input image
                img_org = cv2.copyMakeBorder(
                    img_org, 280, 280, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0]
                )  # zero-padding
                img = cv2.cvtColor(img_org, cv2.COLOR_BGR2RGB)
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
                        x0 = int(boxes[0, i, 1] * img_org.shape[1])
                        y0 = int(boxes[0, i, 0] * img_org.shape[0])
                        x1 = int(boxes[0, i, 3] * img_org.shape[1])
                        y1 = int(boxes[0, i, 2] * img_org.shape[0])

                        cv2.rectangle(img_org, (x0, y0), (x1, y1), (0, 0, 255), 2)
                        cv2.putText(
                            img_org,
                            f"{self._labels[int(classes[0, i])]}, {scores[0, i]}",
                            (x0, y0 + 25),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 0, 255),
                            2,
                        )

                # save img_org to RAM
                self.image = img_org

    def run(self):
        # starting thread
        self.thread.start()

    def close(self):
        self.done = True
        self.cam_0.release()

        self.thread.join()
