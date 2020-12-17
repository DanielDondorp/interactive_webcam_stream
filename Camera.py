
import cv2
from PyQt5 import QtCore

class Camera(QtCore.QThread):
    change_pixmap_signal = QtCore.pyqtSignal(np.ndarray)
    def __init__(self, camera_index = 0):
        QtCore.QThread.__init__(self)
        self.running = False
        self.camera_index = camera_index
    def run(self):
        self.running = True
        cap = cv2.VideoCapture(self.camera_index)
        while self.running:
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.flip(frame, 1)
                self.change_pixmap_signal.emit(frame)
        cap.release()