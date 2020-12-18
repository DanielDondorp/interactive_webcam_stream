#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 10:54:23 2020

@author: daniel
"""
import sys, os
import cv2
from mainwindow import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
from queue import Queue
from tensorflow import keras
import glob
import tqdm

from skimage import io

from Camera import Camera
from QtThreads import SavingThread, ClassifyingThread
from models import ModelTrainer

            
        
class Main(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.label.resize(1200,800)

        self.thread = Camera()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()
        
        self.capturing = False
        self.capture_q = Queue()
        self.counter = 0
        self.predicting = False
        self.ui.pushButton_get_data.clicked.connect(self.start_capture)
        self.ui.pushButton_predict.clicked.connect(self.start_prediction)
        self.ui.pushButton_train_model.clicked.connect(self.train_model)
        self.ui.actionsetWorkingDir.triggered.connect(self.set_working_dir)

        self.wd = os.getenv("HOME")
        sys.stdout.write(f"\n workingdir = {self.wd}")
        if not os.path.exists(os.path.join(self.wd, "iws_data")):
            os.mkdir(os.path.join(self.wd, "iws_data"))


    def set_working_dir(self):
        # print("YAAY")
        wd = QtWidgets.QFileDialog.getExistingDirectory(self, caption = "Choose a work directory to save training data and models",
                                                             directory= self.wd,
                                                             options=QtWidgets.QFileDialog.DontUseNativeDialog)
        if wd:
            self.wd = wd
        else:
            QtWidgets.QMessageBox.warning(self, "No directory chosen.", f"workdir remains {self.wd}")
        
    @QtCore.pyqtSlot(np.ndarray)
    def update_image(self, frame):
        qt_img = self.convert_cv_qt(frame)
        self.ui.label.setPixmap(qt_img)
        
        if self.capturing:
            self.capture_q.put((frame, self.ui.lineEdit.text(), self.counter))
            self.counter+=1
            self.ui.label_2.setText(f"Capturing image {self.counter}/300")
        
            if self.counter >= 300:
                self.capturing = False
                self.counter = 0
                self.ui.label_2.setText("Label:")
                self.saving_thread.running = False
        
        if self.predicting:
            self.capture_q.put((frame, self.ui.lineEdit.text(), self.counter))
            
            
    
    def convert_cv_qt(self, cv_img):
        # rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
       # h, w, ch = rgb_image.shape
       rgb_image = cv_img
       h, w = cv_img.shape
       ch = 1
       bytes_per_line = ch * w
       convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_Grayscale8)
       p = convert_to_Qt_format.scaled(800, 600, QtCore.Qt.KeepAspectRatio)
       return QtGui.QPixmap.fromImage(p)
   
    def start_capture(self):
        s = self.ui.lineEdit.text()
        if not os.path.exists(f"{self.wd}/iws_data"):
            os.mkdir(f"{self.wd}/iws_data")
        if not os.path.exists(f"{self.wd}/iws_data/{s}"):
            os.mkdir(f"{self.wd}/iws_data/{s}")
        self.capturing = True
        self.saving_thread = SavingThread(self)
        self.saving_thread.start()
        
    def start_prediction(self):
        if self.predicting == False:
            self.classifyer = ClassifyingThread(self)
            self.classifyer.prediction_made.connect(self.prediction_made)
            self.predicting = True
            self.classifyer.start()
            self.ui.pushButton_predict.setText("stop predictions")
        else:
            self.predicting = False
            self.classifyer.running = False
            self.classifyer.prediction_made.disconnect()
            self.ui.pushButton_predict.setText("start predictions")
   
    def prediction_made(self, prediction):
        self.ui.lineEdit.setText(prediction)
        
    def train_model(self):
        self.thread.change_pixmap_signal.disconnect()
        # im = self.convert_cv_qt(np.random.randint(0,255,size = (800,600)))
        # self.ui.label.setPixmap(im)
        self.update_image(np.random.random(size = (800,600)))
        self.ui.label.setText("TRAINING!")
        ModelTrainer(parent = self)
        self.thread.change_pixmap_signal.connect(self.update_image)
        
        # m.start()
        
    def closeEvent(self, event):
        print("\\n closing")
        self.thread.running = False
        try:
            self.saving_thread.running = False
        except:
            pass
        try:
            self.classifyer.running = False
        except:
            pass
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())