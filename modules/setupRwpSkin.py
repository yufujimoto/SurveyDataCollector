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
            parent.lbl_fl_snd.setText("音声ファイル")
            parent.btn_rec_start.setText("録音開始")
            parent.btn_rec_stop.setText("録音停止")
            parent.lbl_img.setText("画像一覧")

        elif parent.language == "en":
            parent.lbl_fl_snd.setText("Sound Files")
            parent.btn_rec_start.setText("Rec")
            parent.btn_rec_stop.setText("Stop")
            parent.lbl_img.setText("Image File List")

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

        # Initialyze the record button.
        parent.btn_rec_start.setIcon(general.getIconFromPath(os.path.join(icon_path, 'record.png')))
        parent.btn_rec_start.setIconSize(qicon_size)

        # Initialyze the stop button.
        parent.btn_rec_stop.setIcon(general.getIconFromPath(os.path.join(icon_path, 'pause.png')))
        parent.btn_rec_stop.setIconSize(qicon_size)

        # Set the dialog button size.
        dlg_btn_size = QSize(125, 30)
        parent.bbx_rec_pht.buttons()[0].setMinimumSize(dlg_btn_size)
        parent.bbx_rec_pht.buttons()[1].setMinimumSize(dlg_btn_size)

        # Set the skin and icon.
        parent.bbx_rec_pht.buttons()[0].setIcon(general.getIconFromPath(os.path.join(icon_path, 'check.png')))
        parent.bbx_rec_pht.buttons()[1].setIcon(general.getIconFromPath(os.path.join(icon_path,  'close.png')))

        #parent.tab_conf_main.setTabIcon(0, general.getIconFromPath(os.path.join(icon_path, 'apps.png')))

        # Set Check box style
        check_on = "QCheckBox::indicator:unchecked {image: url(" + os.path.join(icon_path,"check_off_s.png") + ");}\n"
        check_off = "QCheckBox::indicator:checked {image: url(" + os.path.join(icon_path,"check_on_s.png") + ");}"
        #parent.rbtn_no_proxy.setStyleSheet(check_off + check_on)
        #parent.rbtn_proxy.setStyleSheet(check_off + check_on)

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

        # Setup the skin for the dialog.
        if parent.skin == "grey":
            # Set the icon path.
            icon_path = os.path.join(icon_directory, "white")
            setIcons(parent, icon_path)

            # Set the icon path.
            parent._icon_directory = os.path.join(parent._icon_directory, "white")

            # Set the default background and front color.
            back_color = 'background-color: #2C2C2C;'
            font_style_color = 'color: #FFFFFF;'
            font_style = font_style_color + font_style_size

            # Set the default skin for all components.
            parent.setStyleSheet(back_color + font_style + 'border-style: none; border-color: #4C4C4C;')
            #parent.frm_photo_view.setStyleSheet('border-style: solid; border-width: 0.5px; border-color: #FFFFFF;')
            parent.graphicsView.setStyleSheet('border-style: outset; border-width: 0.5px; border-color: #FFFFFF;')

            parent.lst_snd_fls.setStyleSheet('border-style: outset; border-width: 0.5px; border-color: #FFFFFF;')
            parent.lst_img_icon.setStyleSheet('border-style: outset; border-width: 0.5px; border-color: #FFFFFF;')

        elif skin == "white":
            icon_path = os.path.join(icon_path, "black")
            setIcons(parent, icon_path)

    except Exception as e:
        print("Error occured in setupTwpSkin::setSkin(parent, icon_directory, skin='grey')")
        print(str(e))
        error.ErrorMessageCameraDetection(details=str(e), show=True, language=parent.language)
        return(None)
