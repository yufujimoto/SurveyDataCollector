# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/yufujimoto/git/SurveyDataCollector/ui/textEditWithPhotoDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_textEditDialog(object):
    def setupUi(self, textEditDialog):
        textEditDialog.setObjectName("textEditDialog")
        textEditDialog.resize(863, 601)
        textEditDialog.setMinimumSize(QtCore.QSize(800, 600))
        self.gridLayout_3 = QtWidgets.QGridLayout(textEditDialog)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.frm_txt_edt = QtWidgets.QFrame(textEditDialog)
        self.frm_txt_edt.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_txt_edt.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_txt_edt.setObjectName("frm_txt_edt")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frm_txt_edt)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.lay_v_edt = QtWidgets.QVBoxLayout()
        self.lay_v_edt.setContentsMargins(-1, 0, -1, -1)
        self.lay_v_edt.setObjectName("lay_v_edt")
        self.lay_h_men = QtWidgets.QHBoxLayout()
        self.lay_h_men.setContentsMargins(-1, 0, -1, -1)
        self.lay_h_men.setObjectName("lay_h_men")
        self.btn_sav = QtWidgets.QPushButton(self.frm_txt_edt)
        self.btn_sav.setEnabled(False)
        self.btn_sav.setMaximumSize(QtCore.QSize(120, 16777215))
        self.btn_sav.setFlat(True)
        self.btn_sav.setObjectName("btn_sav")
        self.lay_h_men.addWidget(self.btn_sav)
        self.btn_opn_app = QtWidgets.QPushButton(self.frm_txt_edt)
        self.btn_opn_app.setMaximumSize(QtCore.QSize(120, 16777215))
        self.btn_opn_app.setFlat(True)
        self.btn_opn_app.setObjectName("btn_opn_app")
        self.lay_h_men.addWidget(self.btn_opn_app)
        self.chk_edit = QtWidgets.QCheckBox(self.frm_txt_edt)
        self.chk_edit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.chk_edit.setObjectName("chk_edit")
        self.lay_h_men.addWidget(self.chk_edit)
        self.dummy_0000 = QtWidgets.QPushButton(self.frm_txt_edt)
        self.dummy_0000.setText("")
        self.dummy_0000.setFlat(True)
        self.dummy_0000.setObjectName("dummy_0000")
        self.lay_h_men.addWidget(self.dummy_0000)
        self.lay_v_edt.addLayout(self.lay_h_men)
        self.cbx_type = QtWidgets.QComboBox(self.frm_txt_edt)
        self.cbx_type.setMinimumSize(QtCore.QSize(0, 0))
        self.cbx_type.setObjectName("cbx_type")
        self.cbx_type.addItem("")
        self.cbx_type.addItem("")
        self.cbx_type.addItem("")
        self.lay_v_edt.addWidget(self.cbx_type)
        self.textEdit = QtWidgets.QTextEdit(self.frm_txt_edt)
        self.textEdit.setEnabled(True)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.lay_v_edt.addWidget(self.textEdit)
        self.verticalLayout_6.addLayout(self.lay_v_edt)
        self.gridLayout_3.addWidget(self.frm_txt_edt, 1, 1, 2, 2)
        self.frm_img_sel = QtWidgets.QFrame(textEditDialog)
        self.frm_img_sel.setMinimumSize(QtCore.QSize(0, 100))
        self.frm_img_sel.setMaximumSize(QtCore.QSize(370, 16777215))
        self.frm_img_sel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_img_sel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_img_sel.setObjectName("frm_img_sel")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frm_img_sel)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.lbl_img = QtWidgets.QLabel(self.frm_img_sel)
        self.lbl_img.setObjectName("lbl_img")
        self.verticalLayout_7.addWidget(self.lbl_img)
        self.lst_img_icon = QtWidgets.QListView(self.frm_img_sel)
        self.lst_img_icon.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lst_img_icon.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.lst_img_icon.setMovement(QtWidgets.QListView.Static)
        self.lst_img_icon.setResizeMode(QtWidgets.QListView.Adjust)
        self.lst_img_icon.setViewMode(QtWidgets.QListView.IconMode)
        self.lst_img_icon.setObjectName("lst_img_icon")
        self.verticalLayout_7.addWidget(self.lst_img_icon)
        self.gridLayout_3.addWidget(self.frm_img_sel, 0, 0, 1, 1)
        self.frm_photo_view = QtWidgets.QFrame(textEditDialog)
        self.frm_photo_view.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frm_photo_view.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_photo_view.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_photo_view.setObjectName("frm_photo_view")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frm_photo_view)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.gridLayout_3.addWidget(self.frm_photo_view, 0, 1, 1, 2)
        self.lay_h_sbmt = QtWidgets.QHBoxLayout()
        self.lay_h_sbmt.setContentsMargins(-1, 0, -1, -1)
        self.lay_h_sbmt.setObjectName("lay_h_sbmt")
        self.bbx_rec_pht = QtWidgets.QDialogButtonBox(textEditDialog)
        self.bbx_rec_pht.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.bbx_rec_pht.setObjectName("bbx_rec_pht")
        self.lay_h_sbmt.addWidget(self.bbx_rec_pht)
        self.gridLayout_3.addLayout(self.lay_h_sbmt, 4, 0, 1, 3)
        self.frm_txt_sel = QtWidgets.QFrame(textEditDialog)
        self.frm_txt_sel.setEnabled(True)
        self.frm_txt_sel.setMaximumSize(QtCore.QSize(370, 16777215))
        self.frm_txt_sel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_txt_sel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_txt_sel.setObjectName("frm_txt_sel")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frm_txt_sel)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.lbl_fl_txt = QtWidgets.QLabel(self.frm_txt_sel)
        self.lbl_fl_txt.setObjectName("lbl_fl_txt")
        self.verticalLayout_8.addWidget(self.lbl_fl_txt)
        self.lst_txt_fls = QtWidgets.QListWidget(self.frm_txt_sel)
        self.lst_txt_fls.setMinimumSize(QtCore.QSize(0, 0))
        self.lst_txt_fls.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lst_txt_fls.setObjectName("lst_txt_fls")
        self.verticalLayout_8.addWidget(self.lst_txt_fls)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 10, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_new_txt = QtWidgets.QPushButton(self.frm_txt_sel)
        self.btn_new_txt.setMaximumSize(QtCore.QSize(120, 16777215))
        self.btn_new_txt.setFlat(True)
        self.btn_new_txt.setObjectName("btn_new_txt")
        self.horizontalLayout.addWidget(self.btn_new_txt)
        self.btn_ocr = QtWidgets.QPushButton(self.frm_txt_sel)
        self.btn_ocr.setMaximumSize(QtCore.QSize(120, 16777215))
        self.btn_ocr.setFlat(True)
        self.btn_ocr.setObjectName("btn_ocr")
        self.horizontalLayout.addWidget(self.btn_ocr)
        self.btn_bar = QtWidgets.QPushButton(self.frm_txt_sel)
        self.btn_bar.setMaximumSize(QtCore.QSize(120, 16777215))
        self.btn_bar.setFlat(True)
        self.btn_bar.setObjectName("btn_bar")
        self.horizontalLayout.addWidget(self.btn_bar)
        self.dummy_0001 = QtWidgets.QPushButton(self.frm_txt_sel)
        self.dummy_0001.setText("")
        self.dummy_0001.setFlat(True)
        self.dummy_0001.setObjectName("dummy_0001")
        self.horizontalLayout.addWidget(self.dummy_0001)
        self.verticalLayout_8.addLayout(self.horizontalLayout)
        self.gridLayout_3.addWidget(self.frm_txt_sel, 1, 0, 1, 1)

        self.retranslateUi(textEditDialog)
        QtCore.QMetaObject.connectSlotsByName(textEditDialog)

    def retranslateUi(self, textEditDialog):
        _translate = QtCore.QCoreApplication.translate
        textEditDialog.setWindowTitle(_translate("textEditDialog", "Dialog"))
        self.btn_sav.setText(_translate("textEditDialog", "Save"))
        self.btn_opn_app.setText(_translate("textEditDialog", "Open By"))
        self.chk_edit.setText(_translate("textEditDialog", "Edit Mode"))
        self.cbx_type.setItemText(0, _translate("textEditDialog", "Plane Text(*.txt)"))
        self.cbx_type.setItemText(1, _translate("textEditDialog", "Comma Separated Values(*.csv)"))
        self.cbx_type.setItemText(2, _translate("textEditDialog", "Markdown(*.md)"))
        self.lbl_img.setText(_translate("textEditDialog", "Image Selector"))
        self.lbl_fl_txt.setText(_translate("textEditDialog", "Text Files"))
        self.btn_new_txt.setText(_translate("textEditDialog", "New"))
        self.btn_ocr.setText(_translate("textEditDialog", "OCR"))
        self.btn_bar.setText(_translate("textEditDialog", "Barcode"))
