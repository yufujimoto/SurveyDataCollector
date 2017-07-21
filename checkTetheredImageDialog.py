# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/yufujimoto/Desktop/tetheredShooting/Source/checkTetheredImageDialog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_testDialog(object):
    def setupUi(self, testDialog):
        testDialog.setObjectName("testDialog")
        testDialog.resize(400, 300)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(testDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.image_panel = QtWidgets.QLabel(testDialog)
        self.image_panel.setAlignment(QtCore.Qt.AlignCenter)
        self.image_panel.setObjectName("image_panel")
        self.verticalLayout.addWidget(self.image_panel)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_rec = QtWidgets.QPushButton(testDialog)
        self.btn_rec.setObjectName("btn_rec")
        self.horizontalLayout_2.addWidget(self.btn_rec)
        self.btn_rec_stop = QtWidgets.QPushButton(testDialog)
        self.btn_rec_stop.setObjectName("btn_rec_stop")
        self.horizontalLayout_2.addWidget(self.btn_rec_stop)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.lst_fls = QtWidgets.QListWidget(testDialog)
        self.lst_fls.setObjectName("lst_fls")
        self.verticalLayout.addWidget(self.lst_fls)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.tre_img_info = QtWidgets.QTreeWidget(testDialog)
        self.tre_img_info.setObjectName("tre_img_info")
        self.tre_img_info.headerItem().setText(0, "プロパティ")
        self.tre_img_info.header().setDefaultSectionSize(100)
        self.horizontalLayout.addWidget(self.tre_img_info)
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
        self.image_panel.setText(_translate("testDialog", "TextLabel"))
        self.btn_rec.setText(_translate("testDialog", "録音"))
        self.btn_rec_stop.setText(_translate("testDialog", "停止"))
        self.tre_img_info.headerItem().setText(1, _translate("testDialog", "値"))

