# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/yufujimoto/GitHub/SurveyDataCollector/ui/flickr.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FlickrAPIDialog(object):
    def setupUi(self, FlickrAPIDialog):
        FlickrAPIDialog.setObjectName("FlickrAPIDialog")
        FlickrAPIDialog.resize(400, 160)
        self.gridLayout = QtWidgets.QGridLayout(FlickrAPIDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(FlickrAPIDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lbl_flickr_key = QtWidgets.QLabel(FlickrAPIDialog)
        self.lbl_flickr_key.setMinimumSize(QtCore.QSize(60, 0))
        self.lbl_flickr_key.setObjectName("lbl_flickr_key")
        self.horizontalLayout_3.addWidget(self.lbl_flickr_key)
        self.tbx_flickr_key = QtWidgets.QLineEdit(FlickrAPIDialog)
        self.tbx_flickr_key.setObjectName("tbx_flickr_key")
        self.horizontalLayout_3.addWidget(self.tbx_flickr_key)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lbl_flickr_sec = QtWidgets.QLabel(FlickrAPIDialog)
        self.lbl_flickr_sec.setMinimumSize(QtCore.QSize(60, 0))
        self.lbl_flickr_sec.setObjectName("lbl_flickr_sec")
        self.horizontalLayout.addWidget(self.lbl_flickr_sec)
        self.tbx_flickr_sec = QtWidgets.QLineEdit(FlickrAPIDialog)
        self.tbx_flickr_sec.setObjectName("tbx_flickr_sec")
        self.horizontalLayout.addWidget(self.tbx_flickr_sec)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(FlickrAPIDialog)
        self.buttonBox.accepted.connect(FlickrAPIDialog.accept)
        self.buttonBox.rejected.connect(FlickrAPIDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(FlickrAPIDialog)
        FlickrAPIDialog.setTabOrder(self.tbx_flickr_key, self.tbx_flickr_sec)

    def retranslateUi(self, FlickrAPIDialog):
        _translate = QtCore.QCoreApplication.translate
        FlickrAPIDialog.setWindowTitle(_translate("FlickrAPIDialog", "Dialog"))
        self.lbl_flickr_key.setText(_translate("FlickrAPIDialog", "API Key: "))
        self.lbl_flickr_sec.setText(_translate("FlickrAPIDialog", "Secret:"))

