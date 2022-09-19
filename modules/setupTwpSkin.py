#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Import general libraries.
import sys, os, subprocess

# Import general operations.
import modules.general as general
import modules.error as error

# Import PyQt5 libraries for generating the GUI application.
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

def setText(parent):
    print("## setupTwpSkin::setText(parent)")

    try:
        if parent.language == "ja":
            parent.setWindowTitle(parent.tr("テキストメモツール"))
            parent.lbl_img.setText("画像一覧")
            parent.lbl_fl_txt.setText("テキストファイル一覧")
            parent.btn_new_txt.setText("新規作成")
            parent.btn_sav.setText("保存")
            parent.btn_bar.setText("バーコード")

        elif parent.language == "en":
            parent.setWindowTitle(parent.tr("Jotting memo with photo"))
            parent.lbl_img.setText("Image Slector")
            parent.lbl_fl_txt.setText("Text Files")
            parent.btn_new_txt.setText("New")
            parent.btn_sav.setText("Save")
            parent.btn_bar.setText("Barcode")

    except Exception as e:
        print("Error occured in setupTwpSkin::setText(parent)")
        print(str(e))
        error.ErrorMessageCameraDetection(details=str(e), show=True, language=parent.language)
        return(None)

def setIcons(parent, icon_path):
    print("## setupTwpSkin::setIcons(parent, icon_path)")

    try:
        # Set the skin and icon.
        icon_size = general.getIconSize()
        qicon_size = QSize(icon_size, icon_size)

        # Initialyze the new document button.
        parent.btn_new_txt.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'new_document.png'))))
        parent.btn_new_txt.setIconSize(qicon_size)

        # Initialyze the save button.
        parent.btn_sav.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'save.png'))))
        parent.btn_sav.setIconSize(qicon_size)

        # Initialyze the OCR button.
        parent.btn_ocr.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'ocr.png'))))
        parent.btn_ocr.setIconSize(qicon_size)

        # Initialyze the barcode button.
        parent.btn_bar.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'barcode.png'))))
        parent.btn_bar.setIconSize(qicon_size)

        # Set the skin and icon.
        parent.bbx_rec_pht.buttons()[0].setIcon(general.getIconFromPath(os.path.join(icon_path, 'check.png')))
        parent.bbx_rec_pht.buttons()[1].setIcon(general.getIconFromPath(os.path.join(icon_path, 'close.png')))

        # Set Check box style
        check_on = "QCheckBox::indicator:unchecked {image: url(" + os.path.join(icon_path,"check_off_s.png") + ");}\n"
        check_off = "QCheckBox::indicator:checked {image: url(" + os.path.join(icon_path,"check_on_s.png") + ");}"
        parent.chk_edit.setStyleSheet(check_off + check_on)
        parent.chk_edit.setStyleSheet(check_off + check_on)

    except Exception as e:
        print("Error occured in setupTwpSkin::setIcons(parent, icon_path)")
        print(str(e))
        error.ErrorMessageCameraDetection(details=str(e), show=True, language=parent.language)
        return(None)

def setSkin(parent, icon_directory, skin="grey"):
    print("## setupTwpSkin::setSkin(parent, icon_directory, skin='grey')")

    try:
        # Get the proper font size from the display size and set the font size.
        font_size = general.getFontSize()

        # Make the style sheet.
        font_style_size = 'font: regular ' + str(font_size) + 'px;'

        # Define the font object for Qt.
        font = QFont()
        font.setPointSize(font_size)

        # Apply the font style.
        parent.setFont(font)

        # Initialyze the list view of the thumbnails.
        parent.lst_img_icon.setIconSize(QSize(200,200))
        parent.lst_img_icon.setMovement(QListView.Static)
        parent.lst_img_icon.setModel(QStandardItemModel())

        # Setup the skin for the dialog.
        if parent.skin == "grey":
            # Set the icon path.
            icon_path = os.path.join(icon_directory, "white")
            setIcons(parent, icon_path)

            # Set the default background and front color.
            back_color = 'background-color: #2C2C2C;'
            font_style_color = 'color: #FFFFFF;'
            font_style = font_style_color + font_style_size

            # Set the default skin for all components.
            parent.setStyleSheet(back_color + font_style + 'border-style: none; border-color: #4C4C4C;')
            parent.graphicsView.setStyleSheet('border-style: outset; border-width: 0.5px; border-color: #FFFFFF;')
            parent.lst_txt_fls.setStyleSheet('border-style: outset; border-width: 0.5px; border-color: #FFFFFF;')
            parent.lst_img_icon.setStyleSheet('border-style: outset; border-width: 0.5px; border-color: #FFFFFF;')
            parent.textEdit.setStyleSheet('border-style: outset; border-width: 0.5px; border-color: #FFFFFF;')

        elif skin == "white":
            icon_path = os.path.join(icon_path, "black")
            setIcons(parent, icon_path)

    except Exception as e:
        print("Error occured in setupTwpSkin::setSkin(parent, icon_directory, skin='grey')")
        print(str(e))
        error.ErrorMessageCameraDetection(details=str(e), show=True, language=parent.language)
        return(None)
