# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/yufujimoto/GitHub/tetheredShooting/ui/checkTetheredImageDialog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_tetheredDialog(object):
    def setupUi(self, tetheredDialog):
        tetheredDialog.setObjectName("tetheredDialog")
        tetheredDialog.resize(570, 402)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(tetheredDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.image_panel = QtWidgets.QLabel(tetheredDialog)
        self.image_panel.setAlignment(QtCore.Qt.AlignCenter)
        self.image_panel.setObjectName("image_panel")
        self.verticalLayout.addWidget(self.image_panel)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.lst_fls = QtWidgets.QListWidget(tetheredDialog)
        self.lst_fls.setObjectName("lst_fls")
        self.verticalLayout.addWidget(self.lst_fls)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.tre_img_info = QtWidgets.QTreeWidget(tetheredDialog)
        self.tre_img_info.setObjectName("tre_img_info")
        self.tre_img_info.headerItem().setText(0, "プロパティ")
        self.tre_img_info.header().setDefaultSectionSize(100)
        self.horizontalLayout.addWidget(self.tre_img_info)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(tetheredDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(tetheredDialog)
        self.buttonBox.accepted.connect(tetheredDialog.accept)
        self.buttonBox.rejected.connect(tetheredDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(tetheredDialog)

    def retranslateUi(self, tetheredDialog):
        _translate = QtCore.QCoreApplication.translate
        tetheredDialog.setWindowTitle(_translate("tetheredDialog", "Dialog"))
        self.image_panel.setText(_translate("tetheredDialog", "TextLabel"))
        self.tre_img_info.headerItem().setText(1, _translate("tetheredDialog", "値"))

