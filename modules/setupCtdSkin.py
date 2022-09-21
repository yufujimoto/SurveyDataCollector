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
            print("dummy")
        elif parent.language == "en":
            print("dummy")

    except Exception as e:
        print("Error occured in setupMatSkin::setText(parent)")
        print(str(e))
        error.ErrorMessageUnknown(details=str(e), show=True, language=parent.language)
        return(None)

def setIcons(parent, icon_path):
    print("## setupMatSkin::setIcons(parent, icon_path)")

    try:
        # Set the dialog button size.
        print("dummy")


    except Exception as e:
        print("Error occured in setupMatSkin::setIcons(parent, icon_path)")
        print(str(e))
        error.ErrorMessageUnknown(details=str(e), show=True, language=parent.language)
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
            #setIcons(parent, icon_path)

            # Set the default background and front color.
            back_color = 'background-color: #2C2C2C;'
            font_style_color = 'color: #FFFFFF;'
            font_style = font_style_color + font_style_size

            # Set the default skin for all components.
            parent.setStyleSheet(back_color + font_style + 'border-color: #4C4C4C;')

        elif skin == "white":
            icon_path = os.path.join(icon_path, "black")
            #setIcons(parent, icon_path)

    except Exception as e:
        print("Error occured in setupMatSkin::setSkin(parent, icon_directory, skin='grey')")
        print(str(e))
        error.ErrorMessageUnknown(details=str(e), show=True, language=parent.language)
        return(None)
