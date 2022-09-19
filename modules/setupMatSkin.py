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
    print("## setupMatSkin::setText(parent)")

    try:
        if parent.language == "ja":
            parent.lbl_mat_uuid.setText("UUID :")
            parent.lbl_mat_number.setText("資料番号 :")
            parent.lbl_mat_name.setText("資料の名称 :")
            parent.lbl_mat_geo_lat.setText("緯度 :")
            parent.lbl_mat_geo_lon.setText("経度 :")
            parent.lbl_mat_geo_alt.setText("標高 :")
            parent.lbl_mat_tmp_bgn.setText("開始時期 :")
            parent.lbl_mat_tmp_mid.setText("中間時期 :")
            parent.lbl_mat_tmp_end.setText("終了時期 :")
            parent.lbl_mat_description.setText("資料の備考 :")
            parent.bbx_mat_res.buttons()[0].setText("OK")
            parent.bbx_mat_res.buttons()[1].setText("キャンセル")
        elif parent.language == "en":
            parent.lbl_mat_uuid.setText("UUID :")
            parent.lbl_mat_number.setText("Number :")
            parent.lbl_mat_name.setText("Name :")
            parent.lbl_mat_geo_lat.setText("Latitude :")
            parent.lbl_mat_geo_lon.setText("Longitude :")
            parent.lbl_mat_geo_alt.setText("Altitude :")
            parent.lbl_mat_tmp_bgn.setText("Begin :")
            parent.lbl_mat_tmp_mid.setText("Peak :")
            parent.lbl_mat_tmp_end.setText("End :")
            parent.lbl_mat_description.setText("Description :")
            parent.bbx_mat_res.buttons()[0].setText("OK")
            parent.bbx_mat_res.buttons()[1].setText("Cancel")

    except Exception as e:
        print("Error occured in setupMatSkin::setText(parent)")
        print(str(e))
        error.ErrorMessageCameraDetection(details=str(e), show=True, language=parent.language)
        return(None)

def setIcons(parent, icon_path):
    print("## setupMatSkin::setIcons(parent, icon_path)")

    try:
        # Set the dialog button size.
        dlg_btn_size = QSize(125, 30)
        parent.bbx_mat_res.buttons()[0].setMinimumSize(dlg_btn_size)
        parent.bbx_mat_res.buttons()[1].setMinimumSize(dlg_btn_size)

        parent.bbx_mat_res.buttons()[0].setFlat(True)
        parent.bbx_mat_res.buttons()[1].setFlat(True)

        # Set the skin and icon.
        icon_size = general.getIconSize()
        qicon_size = QSize(icon_size, icon_size)

        # Set the skin and icon.
        parent.bbx_mat_res.buttons()[0].setIcon(general.getIconFromPath(os.path.join(icon_path, 'check.png')))
        parent.bbx_mat_res.buttons()[1].setIcon(general.getIconFromPath(os.path.join(icon_path, 'close.png')))
        
        # Set Check box style
        check_on = "QCheckBox::indicator:unchecked {image: url(" + os.path.join(icon_path,"check_off_s.png") + ");}\n"
        check_off = "QCheckBox::indicator:checked {image: url(" + os.path.join(icon_path,"check_on_s.png") + ");}"
        #parent.rbtn_no_proxy.setStyleSheet(check_off + check_on)
        #parent.rbtn_proxy.setStyleSheet(check_off + check_on)

    except Exception as e:
        print("Error occured in setupMatSkin::setIcons(parent, icon_path)")
        print(str(e))
        error.ErrorMessageCameraDetection(details=str(e), show=True, language=parent.language)
        return(None)

def setSkin(parent, icon_directory, skin="grey"):
    print("## setupMatSkin::setSkin(parent, icon_directory, skin='grey')")

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
            text_border = 'border-style: outset; border-width: 0.5px; border-color: #4C4C4C;'
            text_background = "background-color: #6C6C6C;"
            parent.tbx_mat_uuid.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_mat_number.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_mat_name.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_mat_geo_lat.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_mat_geo_lon.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_mat_geo_alt.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_mat_tmp_bgn.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_mat_tmp_mid.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_mat_tmp_end.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_mat_description.setStyleSheet(font_style_color + font_style_size + text_border + text_background)

        elif skin == "white":
            icon_path = os.path.join(icon_path, "black")
            setIcons(parent, icon_path)

    except Exception as e:
        print("Error occured in setupMatSkin::setSkin(parent, icon_directory, skin='grey')")
        print(str(e))
        error.ErrorMessageCameraDetection(details=str(e), show=True, language=parent.language)
        return(None)
