# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/yufujimoto/GitHub/SurveyDataCollector/ui/cameraSelectDialog.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CameraSelectDialog(object):
    def setupUi(self, CameraSelectDialog):
        CameraSelectDialog.setObjectName("CameraSelectDialog")
        CameraSelectDialog.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(CameraSelectDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.lst_camera = QtWidgets.QListWidget(CameraSelectDialog)
        self.lst_camera.setObjectName("lst_camera")
        self.gridLayout.addWidget(self.lst_camera, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(CameraSelectDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(CameraSelectDialog)
        self.buttonBox.accepted.connect(CameraSelectDialog.accept)
        self.buttonBox.rejected.connect(CameraSelectDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CameraSelectDialog)

    def retranslateUi(self, CameraSelectDialog):
        _translate = QtCore.QCoreApplication.translate
        CameraSelectDialog.setWindowTitle(_translate("CameraSelectDialog", "Dialog"))

