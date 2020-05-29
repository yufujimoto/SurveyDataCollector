# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/yufujimoto/GitHub/SurveyDataCollector/ui/textEditDialog.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_textWriteDialog(object):
    def setupUi(self, textWriteDialog):
        textWriteDialog.setObjectName("textWriteDialog")
        textWriteDialog.resize(800, 601)
        textWriteDialog.setMinimumSize(QtCore.QSize(800, 600))
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(textWriteDialog)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lay_h_img = QtWidgets.QHBoxLayout()
        self.lay_h_img.setContentsMargins(-1, 10, -1, -1)
        self.lay_h_img.setObjectName("lay_h_img")
        self.frm_thmb = QtWidgets.QFrame(textWriteDialog)
        self.frm_thmb.setMinimumSize(QtCore.QSize(0, 100))
        self.frm_thmb.setMaximumSize(QtCore.QSize(370, 16777215))
        self.frm_thmb.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_thmb.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_thmb.setObjectName("frm_thmb")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frm_thmb)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(0, 0, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lst_img_icon = QtWidgets.QListView(self.frm_thmb)
        self.lst_img_icon.setMaximumSize(QtCore.QSize(370, 16777215))
        self.lst_img_icon.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.lst_img_icon.setMovement(QtWidgets.QListView.Static)
        self.lst_img_icon.setResizeMode(QtWidgets.QListView.Adjust)
        self.lst_img_icon.setViewMode(QtWidgets.QListView.IconMode)
        self.lst_img_icon.setObjectName("lst_img_icon")
        self.verticalLayout_3.addWidget(self.lst_img_icon)
        self.gridLayout_2.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.lay_h_img.addWidget(self.frm_thmb)
        self.frm_viewer = QtWidgets.QFrame(textWriteDialog)
        self.frm_viewer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_viewer.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_viewer.setObjectName("frm_viewer")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frm_viewer)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.lay_h_img.addWidget(self.frm_viewer)
        self.verticalLayout_4.addLayout(self.lay_h_img)
        self.frm_txt_body = QtWidgets.QFrame(textWriteDialog)
        self.frm_txt_body.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_txt_body.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_txt_body.setObjectName("frm_txt_body")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frm_txt_body)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.txt_body = QtWidgets.QTextBrowser(self.frm_txt_body)
        self.txt_body.setObjectName("txt_body")
        self.horizontalLayout_3.addWidget(self.txt_body)
        self.verticalLayout_4.addWidget(self.frm_txt_body)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 10, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_commit = QtWidgets.QDialogButtonBox(textWriteDialog)
        self.btn_commit.setOrientation(QtCore.Qt.Horizontal)
        self.btn_commit.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.btn_commit.setObjectName("btn_commit")
        self.horizontalLayout.addWidget(self.btn_commit)
        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.retranslateUi(textWriteDialog)
        self.btn_commit.accepted.connect(textWriteDialog.accept)
        self.btn_commit.rejected.connect(textWriteDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(textWriteDialog)

    def retranslateUi(self, textWriteDialog):
        _translate = QtCore.QCoreApplication.translate
        textWriteDialog.setWindowTitle(_translate("textWriteDialog", "Dialog"))

