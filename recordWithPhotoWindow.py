# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/yufujimoto/GitHub/tetheredShooting/recordWithPhotoWindow.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(798, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 776, 225))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.image_panel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.image_panel.setText("")
        self.image_panel.setObjectName("image_panel")
        self.gridLayout_3.addWidget(self.image_panel, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_rec_start = QtWidgets.QPushButton(self.centralwidget)
        self.btn_rec_start.setObjectName("btn_rec_start")
        self.horizontalLayout_2.addWidget(self.btn_rec_start)
        self.btn_rec_stop = QtWidgets.QPushButton(self.centralwidget)
        self.btn_rec_stop.setObjectName("btn_rec_stop")
        self.horizontalLayout_2.addWidget(self.btn_rec_stop)
        self.btn_play = QtWidgets.QPushButton(self.centralwidget)
        self.btn_play.setObjectName("btn_play")
        self.horizontalLayout_2.addWidget(self.btn_play)
        self.btn_refresh = QtWidgets.QPushButton(self.centralwidget)
        self.btn_refresh.setObjectName("btn_refresh")
        self.horizontalLayout_2.addWidget(self.btn_refresh)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lst_img_fls = QtWidgets.QListWidget(self.centralwidget)
        self.lst_img_fls.setObjectName("lst_img_fls")
        self.horizontalLayout.addWidget(self.lst_img_fls)
        self.lst_snd_fls = QtWidgets.QListWidget(self.centralwidget)
        self.lst_snd_fls.setObjectName("lst_snd_fls")
        self.horizontalLayout.addWidget(self.lst_snd_fls)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout_2.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 798, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_rec_start.setText(_translate("MainWindow", "録音する"))
        self.btn_rec_stop.setText(_translate("MainWindow", "停止する"))
        self.btn_play.setText(_translate("MainWindow", "再生する"))
        self.btn_refresh.setText(_translate("MainWindow", "リスト更新"))

