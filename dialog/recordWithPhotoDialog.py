# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/yufujimoto/GitHub/SurveyDataCollector/ui/recordWithPhotoDialog.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_testDialog(object):
    def setupUi(self, testDialog):
        testDialog.setObjectName("testDialog")
        testDialog.resize(800, 601)
        testDialog.setMinimumSize(QtCore.QSize(800, 600))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(testDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(0, 0, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lbl_snd = QtWidgets.QLabel(testDialog)
        self.lbl_snd.setObjectName("lbl_snd")
        self.verticalLayout_3.addWidget(self.lbl_snd)
        self.lst_snd_fls = QtWidgets.QListWidget(testDialog)
        self.lst_snd_fls.setMinimumSize(QtCore.QSize(0, 0))
        self.lst_snd_fls.setMaximumSize(QtCore.QSize(370, 100))
        self.lst_snd_fls.setObjectName("lst_snd_fls")
        self.verticalLayout_3.addWidget(self.lst_snd_fls)
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
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.lbl_img = QtWidgets.QLabel(testDialog)
        self.lbl_img.setObjectName("lbl_img")
        self.verticalLayout_3.addWidget(self.lbl_img)
        self.lst_img_icon = QtWidgets.QListView(testDialog)
        self.lst_img_icon.setMaximumSize(QtCore.QSize(370, 16777215))
        self.lst_img_icon.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.lst_img_icon.setMovement(QtWidgets.QListView.Static)
        self.lst_img_icon.setResizeMode(QtWidgets.QListView.Adjust)
        self.lst_img_icon.setViewMode(QtWidgets.QListView.IconMode)
        self.lst_img_icon.setObjectName("lst_img_icon")
        self.verticalLayout_3.addWidget(self.lst_img_icon)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
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
        self.lbl_snd.setText(_translate("testDialog", "録音メニュー"))
        self.btn_rec_start.setText(_translate("testDialog", "録音する"))
        self.btn_rec_stop.setText(_translate("testDialog", "停止する"))
        self.btn_play.setText(_translate("testDialog", "再生する"))
        self.lbl_img.setText(_translate("testDialog", "画像一覧"))

