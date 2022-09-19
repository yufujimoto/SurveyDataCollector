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
    print("## setupConSkin::setText(parent)")

    try:
        if parent.language == "ja":
            parent.lbl_con_uuid.setText("UUID :")
            parent.lbl_con_name.setText("統合体の名称 :")
            parent.lbl_con_tempral.setText("時間識別子 :")
            parent.lbl_con_description.setText("統合体の備考 :")
            parent.lbl_con_geoname.setText("地理識別子 :")
            parent.bbx_con_res.buttons()[0].setText("OK")
            parent.bbx_con_res.buttons()[1].setText("キャンセル")

        elif parent.language == "en":
            parent.lbl_con_uuid.setText("UUID :")
            parent.lbl_con_description.setText("Description :")
            parent.lbl_con_name.setText("Name :")
            parent.lbl_con_geoname.setText("Location:")
            parent.lbl_con_tempral.setText("Era/Age:")
            parent.bbx_con_res.buttons()[0].setText("OK")
            parent.bbx_con_res.buttons()[1].setText("Cancel")

    except Exception as e:
        print("Error occured in setupConSkin::setText(parent)")
        print(str(e))
        error.ErrorMessageCameraDetection(details=str(e), show=True, language=parent.language)
        return(None)

def setIcons(parent, icon_path):
    print("## setupConSkin::setIcons(parent, icon_path)")

    dlg_btn_size = QSize(125, 30)
    parent.bbx_con_res.buttons()[0].setMinimumSize(dlg_btn_size)
    parent.bbx_con_res.buttons()[1].setMinimumSize(dlg_btn_size)

    try:
        # Set the skin and icon.
        icon_size = general.getIconSize()
        qicon_size = QSize(icon_size, icon_size)

        # Set the skin and icon.
        parent.bbx_con_res.buttons()[0].setIcon(general.getIconFromPath(os.path.join(icon_path, 'check.png')))
        parent.bbx_con_res.buttons()[1].setIcon(general.getIconFromPath(os.path.join(icon_path, 'close.png')))

        # Set Check box style
        check_on = "QCheckBox::indicator:unchecked {image: url(" + os.path.join(icon_path,"check_off_s.png") + ");}\n"
        check_off = "QCheckBox::indicator:checked {image: url(" + os.path.join(icon_path,"check_on_s.png") + ");}"
        #parent.rbtn_no_proxy.setStyleSheet(check_off + check_on)
        #parent.rbtn_proxy.setStyleSheet(check_off + check_on)

    except Exception as e:
        print("Error occured in setupConSkin::setIcons(parent, icon_path)")
        print(str(e))
        error.ErrorMessageCameraDetection(details=str(e), show=True, language=parent.language)
        return(None)

def setSkin(parent, icon_directory, skin="grey"):
    print("## setupConSkin::setSkin(parent, icon_directory, skin='grey')")

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

            # Set the default background and front color.
            back_color = 'background-color: #2C2C2C;'
            font_style_color = 'color: #FFFFFF;'
            font_style = font_style_color + font_style_size

            # Set the default skin for all components.
            parent.setStyleSheet(back_color + font_style + 'border-style: none; border-color: #4C4C4C;')
            parent.frame.setStyleSheet(back_color + font_style + 'border-style: none; border-color: #4C4C4C;')

            # Set the default skin for text boxes.
            text_border = 'border-style: none; border-width: 0.5px; border-color: #4C4C4C;'
            text_background = "background-color: #6C6C6C;"
            parent.tbx_con_uuid.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_con_name.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_con_geoname.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_con_temporal.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_con_description.setStyleSheet(font_style_color + font_style_size + text_border + text_background)

        elif skin == "white":
            icon_path = os.path.join(icon_path, "black")
            setIcons(parent, icon_path)

    except Exception as e:
        print("Error occured in setupConSkin::setSkin(parent, icon_directory, skin='grey')")
        print(str(e))
        error.ErrorMessageCameraDetection(details=str(e), show=True, language=parent.language)
        return(None)
