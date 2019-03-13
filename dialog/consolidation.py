#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Import general libraries.
import sys, os, uuid, shutil, time, math, tempfile, logging, pyexiv2, datetime, exifread

# Import the library for acquiring file information.
from stat import *
from dateutil.parser import parse

# Import PyQt5 libraries for generating the GUI application.
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QThread, pyqtSignal

# Import general operations.
import modules.general as general
import modules.features as features
import modules.error as error
import modules.skin as skin

# Import camera and image processing library.
import dialog.consolidationDialog as consolidationDialog

class consolidationDialog(QDialog, consolidationDialog.Ui_ConsolidationDialog):    
    def __init__(self, parent=None):        
        super(consolidationDialog, self).__init__(parent)
        self.setupUi(self)
        
        # Initialize the window.
        self.setWindowTitle(self.tr("Consolidation View"))
        
        # Initialyze the user interface.
        # Get the proper font size from the display size and set the font size.
        font_size = skin.getFontSize()
        
        # Make the style sheet.
        font_style_size = 'font: regular ' + str(skin.getFontSize()) + 'px;'
        
        # Define the font object for Qt.
        font = QFont()
        font.setPointSize(font_size)
        
        self.setFont(font)
        
        # Setup the skin for the dialog.
        if parent.skin == "grey":
            # Set the icon path.
            icon_path = os.path.join(parent.icon_directory, "white")
            
            # Set the default background and front color.
            back_color = 'background-color: #2C2C2C;'
            font_style_color = 'color: #FFFFFF;'
            font_style = font_style_color + font_style_size
            
            # Set the default skin for all components.
            self.setStyleSheet(back_color + font_style + 'border-style: none; border-color: #4C4C4C;')
            self.frame.setStyleSheet(back_color + font_style + 'border-style: none; border-color: #4C4C4C;')
            
            # Set the default skin for text boxes.
            text_border = 'border-style: none; border-width: 0.5px; border-color: #4C4C4C;'
            text_background = "background-color: #6C6C6C;"
            self.tbx_con_uuid.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            self.tbx_con_name.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            self.tbx_con_geoname.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            self.tbx_con_temporal.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            self.tbx_con_description.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        
        elif parent.skin == "white":
            # Set the icon path.
            icon_path = os.path.join(parent.icon_directory, "black")
        
        # Set the dialog button size.
        dlg_btn_size = QSize(125, 30)
        self.bbx_con_res.buttons()[0].setMinimumSize(dlg_btn_size)
        self.bbx_con_res.buttons()[1].setMinimumSize(dlg_btn_size)
        
        # Set the skin and icon.
        self.bbx_con_res.buttons()[0].setIcon(skin.getIconFromPath(os.path.join(icon_path, 'check.png')))
        self.bbx_con_res.buttons()[1].setIcon(skin.getIconFromPath(os.path.join(icon_path, 'close.png')))
        
        # Setup labels with designated language.
        if parent.language == "ja":
            self.lbl_con_uuid.setText("UUID :")
            self.lbl_con_name.setText("統合体の名称 :")
            self.lbl_con_tempral.setText("時間識別子 :")
            self.lbl_con_description.setText("統合体の備考 :")
            self.lbl_con_geoname.setText("地理識別子 :")
            self.bbx_con_res.buttons()[0].setText("OK")
            self.bbx_con_res.buttons()[1].setText("キャンセル")
        elif parent.language == "en":
            self.lbl_con_uuid.setText("UUID :")
            self.lbl_con_description.setText("Description :")
            self.lbl_con_name.setText("Name :")
            self.lbl_con_geoname.setText("Location:")
            self.lbl_con_tempral.setText("Era/Age:")
            self.bbx_con_res.buttons()[0].setText("OK")
            self.bbx_con_res.buttons()[1].setText("Cancel")
        
        # Set attributes to text boxes.
        self.tbx_con_uuid.setText(parent._current_consolidation.uuid)
        self.tbx_con_name.setText(parent._current_consolidation.name)
        self.tbx_con_geoname.setText(parent._current_consolidation.geographic_annotation)
        self.tbx_con_temporal.setText(parent._current_consolidation.temporal_annotation)
        self.tbx_con_description.setText(parent._current_consolidation.description)
        
        
        
        
