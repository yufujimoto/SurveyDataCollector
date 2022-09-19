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


        elif parent.language == "en":

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

        elif skin == "white":
            icon_path = os.path.join(icon_path, "black")
            setIcons(parent, icon_path)

    except Exception as e:
        print("Error occured in setupTwpSkin::setSkin(parent, icon_directory, skin='grey')")
        print(str(e))
        error.ErrorMessageCameraDetection(details=str(e), show=True, language=parent.language)
        return(None)
