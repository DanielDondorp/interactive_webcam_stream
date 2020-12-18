from PyQt5 import QtCore
import cv2
import numpy as np
import sys
from tensorflow import keras

class SavingThread(QtCore.QThread):
    def __init__(self, parent):
        QtCore.QThread.__init__(self)
        self.running = False
        self.parent = parent
    def run(self):
        self.running = True
        while self.running:
            frame, s, i = self.parent.capture_q.get()
            filename = f"{self.parent.wd}/iws_data/{s}/{s}_{str(i).zfill(3)}.jpg"
            sys.stdout.write(f"Writing {filename}\n")
            frame = cv2.resize(frame, (80 ,60))
            cv2.imwrite(filename, frame)


class ClassifyingThread(QtCore.QThread):
    prediction_made = QtCore.pyqtSignal(str)
    def __init__(self, parent):
        QtCore.QThread.__init__(self)
        self.parent = parent
        self.running = False
        self.model = keras.models.load_model(f"{self.parent.wd}/iws_data/model")
        self.classes = np.load(f"{self.parent.wd}/iws_data/classes.npy")

    def run(self):
        sys.stdout.write("Predictions started")
        self.running = True
        while self.running:
            frame, s, i = self.parent.capture_q.get()
            frame = cv2.resize(frame, (80 ,60))
            frame = frame.reshape(1 ,60 ,80 ,1)
            prediction = self.model.predict_classes(frame)
            c = self.classes[prediction][0]
            # sys.stdout.write(c)
            self.prediction_made.emit(c)
        sys.stdout.write("Predictions stopped")