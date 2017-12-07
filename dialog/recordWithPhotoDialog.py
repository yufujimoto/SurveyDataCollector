# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/yufujimoto/GitHub/tetheredShooting/ui/recordWithPhotoDialog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_testDialog(object):
    def setupUi(self, testDialog):
        testDialog.setObjectName("testDialog")
        testDialog.resize(570, 402)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(testDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.image_panel = QtWidgets.QLabel(testDialog)
        self.image_panel.setMinimumSize(QtCore.QSize(0, 500))
        self.image_panel.setText("")
        self.image_panel.setAlignment(QtCore.Qt.AlignCenter)
        self.image_panel.setObjectName("image_panel")
        self.verticalLayout.addWidget(self.image_panel)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_rec_start = QtWidgets.QPushButton(testDialog)
        self.btn_rec_start.setObjectName("btn_rec_start")
        self.horizontalLayout_3.addWidget(self.btn_rec_start)
        self.btn_rec_stop = QtWidgets.QPushButton(testDialog)
        self.btn_rec_stop.setObjectName("btn_rec_stop")
        self.horizontalLayout_3.addWidget(self.btn_rec_stop)
        self.btn_play = QtWidgets.QPushButton(testDialog)
        self.btn_play.setObjectName("btn_play")
        self.horizontalLayout_3.addWidget(self.btn_play)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(0, 0, -1, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lst_img_fls = QtWidgets.QListWidget(testDialog)
        self.lst_img_fls.setObjectName("lst_img_fls")
        self.horizontalLayout_4.addWidget(self.lst_img_fls)
        self.lst_snd_fls = QtWidgets.QListWidget(testDialog)
        self.lst_snd_fls.setObjectName("lst_snd_fls")
        self.horizontalLayout_4.addWidget(self.lst_snd_fls)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(testDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(testDialog)
        self.buttonBox.accepted.connect(testDialog.accept)
        self.buttonBox.rejected.connect(testDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(testDialog)

    def retranslateUi(self, testDialog):
        _translate = QtCore.QCoreApplication.translate
        testDialog.setWindowTitle(_translate("testDialog", "Dialog"))
        self.btn_rec_start.setText(_translate("testDialog", "録音する"))
        self.btn_rec_stop.setText(_translate("testDialog", "停止する"))
        self.btn_play.setText(_translate("testDialog", "再生する"))

