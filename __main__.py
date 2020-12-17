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
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from skimage import io

from .Camera import Camera


        
class SavingThread(QtCore.QThread):
    def __init__(self, parent):
        QtCore.QThread.__init__(self)
        self.running = False
        self.parent = parent
    def run(self):
        self.running = True
        while self.running:
            frame, s, i = self.parent.capture_q.get()
            filename = f"./data/{s}/{s}_{str(i).zfill(3)}.jpg"
            sys.stdout.write(f"Writing {filename}\n")
            frame = cv2.resize(frame, (80,60))
            cv2.imwrite(filename, frame)


class ClassifyingThread(QtCore.QThread):
    prediction_made = QtCore.pyqtSignal(str)
    def __init__(self, parent):
        QtCore.QThread.__init__(self)
        self.parent = parent
        self.running = False
        self.model = keras.models.load_model("model_home")
        self.classes = np.load("classes.npy")
        
    def run(self):
        sys.stdout.write("Predictions started")
        self.running = True
        while self.running:
            frame, s, i = self.parent.capture_q.get()
            frame = cv2.resize(frame, (80,60))
            frame = frame.reshape(1,60,80,1)
            prediction = self.model.predict_classes(frame)
            c = self.classes[prediction][0]
            # sys.stdout.write(c)
            self.prediction_made.emit(c)
        sys.stdout.write("Predictions stopped")
        
class ModelTrainer:
    def __init__(self):
        X_train, X_test, y_train, y_test, le = self.create_dataset()
        model = self.create_model(len(le.classes_))
        model.fit(X_train, y_train, validation_data = (X_test, y_test), epochs = 10)
        model.save("model_home")
        classes = le.classes_
        np.save("classes.npy", classes)
            
    def create_dataset(self, path_to_data = "./data"):
        images = glob.glob(f"{path_to_data}/**/*.jpg")
        X = []
        y = []
        for image in tqdm.tqdm(images):
            im = io.imread(image)
            label = image.split("/")[-2]
            X.append(im)
            y.append(label)
            
        labels = y
        le = LabelEncoder()
        y = keras.utils.to_categorical(le.fit_transform(labels))
        X, y = shuffle(X,y)
        X = np.array(X).reshape(len(X), 60, 80, 1)
        X_train, X_test, y_train, y_test = train_test_split(X, y)
        return X_train, X_test, y_train, y_test, le
    
    def create_model(self, output_size):
        model = keras.models.Sequential()
        model.add(keras.layers.Conv2D(64, kernel_size = 3, activation = "relu", input_shape = (60,80,1)))
        model.add(keras.layers.Dropout(.2))
        model.add(keras.layers.Conv2D(32, kernel_size = 3, activation = "relu"))
        # model.add(keras.layers.Dropout(.2))
        # model.add(keras.layers.Conv2D(16, kernel_size = 3, activation =  "relu"))
        model.add(keras.layers.Flatten())
        model.add(keras.layers.Dropout(.2))
        model.add(keras.layers.Dense(output_size, activation = "softmax"))
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model
            
        
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
        if not os.path.exists(f"./data/{s}"):
            os.mkdir(f"./data/{s}")
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
        im = self.convert_cv_qt(np.random.randint(0,255,size = (800,600)))
        self.ui.label.setPixmap(im)
        ModelTrainer()
        self.thread.change_pixmap_signal.connect(self.update_image)
        
        # m.start()
        
    def closeEvent(self, event):
        print("closing")
        self.thread.running = False
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())