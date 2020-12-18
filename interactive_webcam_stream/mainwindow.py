# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton_get_data = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_get_data.setObjectName("pushButton_get_data")
        self.horizontalLayout.addWidget(self.pushButton_get_data)
        self.pushButton_predict = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_predict.setObjectName("pushButton_predict")
        self.horizontalLayout.addWidget(self.pushButton_predict)
        self.pushButton_train_model = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_train_model.setObjectName("pushButton_train_model")
        self.horizontalLayout.addWidget(self.pushButton_train_model)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 30))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionsetWorkingDir = QtWidgets.QAction(MainWindow)
        self.actionsetWorkingDir.setObjectName("actionsetWorkingDir")
        self.menuFile.addAction(self.actionsetWorkingDir)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Label:"))
        self.pushButton_get_data.setText(_translate("MainWindow", "get training data"))
        self.pushButton_predict.setText(_translate("MainWindow", "start predictions"))
        self.pushButton_train_model.setText(_translate("MainWindow", "train model"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.menuFile.setTitle(_translate("MainWindow", "Fi&le"))
        self.actionsetWorkingDir.setText(_translate("MainWindow", "setWorkingDir"))
