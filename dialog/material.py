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
#import modules.skin as skin
import modules.setupConfigSkin as skin


# Import camera and image processing library.
import dialog.materialDialog as materialDialog

class materialDialog(QDialog, materialDialog.Ui_materialDialog):    
    def __init__(self, parent=None):        
        super(materialDialog, self).__init__(parent)
        self.setupUi(self)
        
        # Initialize the window.
        self.setWindowTitle(self.tr("Material View"))
        
        self.bbx_mat_res.buttons()[0].setFlat(True)
        self.bbx_mat_res.buttons()[1].setFlat(True)
        
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
            text_border = 'border-style: outset; border-width: 0.5px; border-color: #4C4C4C;'
            text_background = "background-color: #6C6C6C;"
            self.tbx_mat_uuid.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            self.tbx_mat_number.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            self.tbx_mat_name.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            self.tbx_mat_geo_lat.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            self.tbx_mat_geo_lon.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            self.tbx_mat_geo_alt.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            self.tbx_mat_tmp_bgn.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            self.tbx_mat_tmp_mid.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            self.tbx_mat_tmp_end.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            self.tbx_mat_description.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            
        elif parent.skin == "white":
            # Set the icon path.
            icon_path = os.path.join(parent.icon_directory, "black")
        
        # Set the dialog button size.
        dlg_btn_size = QSize(125, 30)
        self.bbx_mat_res.buttons()[0].setMinimumSize(dlg_btn_size)
        self.bbx_mat_res.buttons()[1].setMinimumSize(dlg_btn_size)
        
        # Set the skin and icon.
        self.bbx_mat_res.buttons()[0].setIcon(skin.getIconFromPath(os.path.join(icon_path, 'check.png')))
        self.bbx_mat_res.buttons()[1].setIcon(skin.getIconFromPath(os.path.join(icon_path, 'close.png')))
        
        # Setup labels with designated language.
        if parent.language == "ja":
            self.lbl_mat_uuid.setText("UUID :")
            self.lbl_mat_number.setText("資料番号 :")
            self.lbl_mat_name.setText("資料の名称 :")
            self.lbl_mat_geo_lat.setText("緯度 :")
            self.lbl_mat_geo_lon.setText("経度 :")
            self.lbl_mat_geo_alt.setText("標高 :")
            self.lbl_mat_tmp_bgn.setText("開始時期 :")
            self.lbl_mat_tmp_mid.setText("中間時期 :")
            self.lbl_mat_tmp_end.setText("終了時期 :")
            self.lbl_mat_description.setText("資料の備考 :")
            self.bbx_mat_res.buttons()[0].setText("OK")
            self.bbx_mat_res.buttons()[1].setText("キャンセル")
        elif parent.language == "en":
            self.lbl_mat_uuid.setText("UUID :")
            self.lbl_mat_number.setText("Number :")
            self.lbl_mat_name.setText("Name :")
            self.lbl_mat_geo_lat.setText("Latitude :")
            self.lbl_mat_geo_lon.setText("Longitude :")
            self.lbl_mat_geo_alt.setText("Altitude :")
            self.lbl_mat_tmp_bgn.setText("Begin :")
            self.lbl_mat_tmp_mid.setText("Peak :")
            self.lbl_mat_tmp_end.setText("End :")
            self.lbl_mat_description.setText("Description :")
            self.bbx_mat_res.buttons()[0].setText("OK")
            self.bbx_mat_res.buttons()[1].setText("Cancel")
        
        # Set attributes to text boxes.
        self.tbx_mat_uuid.setText(parent._current_material.uuid)
        self.tbx_mat_number.setText(parent._current_material.material_number)
        self.tbx_mat_name.setText(parent._current_material.name)
        self.tbx_mat_tmp_bgn.setText(parent._current_material.estimated_period_beginning)
        self.tbx_mat_tmp_mid.setText(parent._current_material.estimated_period_peak)
        self.tbx_mat_tmp_end.setText(parent._current_material.estimated_period_ending)
        self.tbx_mat_geo_lat.setText(str(parent._current_material.latitude))
        self.tbx_mat_geo_lon.setText(str(parent._current_material.longitude))
        self.tbx_mat_geo_alt.setText(str(parent._current_material.altitude))
        self.tbx_mat_description.setText(parent._current_material.description)
        
        
        
        
