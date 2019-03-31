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
import modules.camera as camera

# Import camera and image processing library.
import dialog.configurationDialog as configurationDialog

class configurationDialog(QDialog, configurationDialog.Ui_configurationDialog):    
    def __init__(self, parent=None):
        try:
            super(configurationDialog, self).__init__(parent)
            self.setupUi(self)
            
            # Initialize the window.
            self.setWindowTitle(self.tr("Configuration"))
            
            #self.lst_camera.itemClicked.connect(self._getSelectedNumber)
            
            # Refresh camera parameters.
            self.refreshCameraParameters()
            
            # Initialyze the user interface.
            # Get the proper font size from the display size and set the font size.
            font_size = skin.getFontSize()
            
            # Make the style sheet.
            font_style_size = 'font: regular ' + str(skin.getFontSize()) + 'px;'
            
            # Define the font object for Qt.
            font = QFont()
            font.setPointSize(font_size)
            
            self.setFont(font)
            
            # Detect the connected camera.
            cams = camera.detectCamera()
            
            if not cams ==  None:
                for cam in cams:
                    item = QListWidgetItem(cam["name"])
                    self.lst_cam.addItem(item)
                self.lst_cam.show()
                
                if len(cams) > 0 :
                    self.lst_cam.setCurrentRow(0)
                    self._selected = 0
            
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
                self.frm_conf_btns.setStyleSheet(back_color + font_style + 'border-style: none; border-color: #4C4C4C;')
                self.frm_conf_main.setStyleSheet(back_color + font_style + 'border-style: none; border-color: #4C4C4C;')
                
                # Set the default skin for tabs.
                back_color_tab = 'QTabBar::tab {background-color: #2C2C2C; }'
                back_color_tab_act = 'QTabBar::tab::selected {background-color: #4C4C4C;}'
                self.tab_general.setStyleSheet(back_color_tab + back_color_tab_act)
                self.tab_camera.setStyleSheet(back_color_tab + back_color_tab_act)
                
                # Set the default skin for text boxes.
                text_border = 'border-style: none; border-width: 0.5px; border-color: #4C4C4C;'
                text_background = "background-color: #6C6C6C;"
                
                self.cbx_lang.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
                self.cbx_skin.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
                self.cbx_tool_awb.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
                self.cbx_tool_psp.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
                self.txt_flc_api.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
                self.txt_flc_sec.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
                
                self.cbx_cam_size.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
                self.cbx_cam_iso.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
                self.cbx_cam_wht.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
                self.cbx_cam_exp.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
                self.cbx_cam_fval.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
                self.cbx_cam_qoi.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
                self.cbx_cam_fmod.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
                self.cbx_cam_epg.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
                self.cbx_cam_cpt.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
                self.cbx_cam_met.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
                self.lst_cam.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            elif parent.skin == "white":
                # Set the icon path.
                icon_path = os.path.join(parent.icon_directory, "black")
            
            # Set the dialog button size.
            dlg_btn_size = QSize(125, 30)
            self.bbx_conf_res.buttons()[0].setMinimumSize(dlg_btn_size)
            self.bbx_conf_res.buttons()[1].setMinimumSize(dlg_btn_size)
            self.bbx_conf_res.buttons()[2].setMinimumSize(dlg_btn_size)
            
            # Set the skin and icon.
            self.bbx_conf_res.buttons()[0].setIcon(skin.getIconFromPath(os.path.join(icon_path, 'check.png')))
            self.bbx_conf_res.buttons()[1].setIcon(skin.getIconFromPath(os.path.join(icon_path, 'check.png')))
            self.bbx_conf_res.buttons()[2].setIcon(skin.getIconFromPath(os.path.join(icon_path, 'close.png')))
            
            '''            
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
            '''
            
            if parent.language == "ja":
                self.cbx_lang.setCurrentIndex(0)
            elif parent.language == "en":
                self.cbx_lang.setCurrentIndex(1)
            
            if parent.skin == "grey":
                self.cbx_skin.setCurrentIndex(0)
            elif parent.skin == "white":
                parent.cbx_skin.setCurrentIndex(1)
            
            # Set default auto white balance algorithms.
            if parent._awb_algo == "retinex_adjusted": self.cbx_tool_awb.setCurrentIndex(0)
            elif parent._awb_algo == "stretch": self.cbx_tool_awb.setCurrentIndex(1)
            elif parent._awb_algo == "gray_world": self.cbx_tool_awb.setCurrentIndex(2)
            elif parent._awb_algo == "max_white": self.cbx_tool_awb.setCurrentIndex(3)
            elif parent._awb_algo == "retinex": self.cbx_tool_awb.setCurrentIndex(4)
            elif parent._awb_algo == "stdev_luminance": self.cbx_tool_awb.setCurrentIndex(5)
            elif parent._awb_algo == "stdev_grey_world": self.cbx_tool_awb.setCurrentIndex(6)
            elif parent._awb_algo == "luminance_weighted": self.cbx_tool_awb.setCurrentIndex(7)
            elif parent._awb_algo == "automatic": self.cbx_tool_awb.setCurrentIndex(8)
            
            # Set default pan-sharpening algorithms.
            if parent.psp_algo == "ihsConvert": self.cbx_tool_psp.setCurrentIndex(0)
            elif parent.psp_algo == "simpleMeanConvert": self.cbx_tool_psp.setCurrentIndex(1)
            elif parent.psp_algo == "broveyConvert": self.cbx_tool_psp.setCurrentIndex(2)
            
            # Set Flickr API and Secret Key.
            self.txt_flc_api.setText(parent.flickr_apikey)
            self.txt_flc_sec.setText(parent.flickr_secret)
        except Exception as e:
            print(str(e))
    
    def refreshCameraParameters(self):
        print("main::refreshCameraParameters(self)")
        
        try:            
            # Clear comboboxes for camera parameters.
            self.cbx_cam_size.clear()
            self.cbx_cam_iso.clear()
            self.cbx_cam_wht.clear()
            self.cbx_cam_exp.clear()
            self.cbx_cam_fval.clear()
            self.cbx_cam_qoi.clear()
            self.cbx_cam_fmod.clear()
            self.cbx_cam_epg.clear()
            self.cbx_cam_cpt.clear()
            self.cbx_cam_met.clear()
        except Exception as e:
            print("Error occured in main::refreshCameraParameters(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)
        
        
        
