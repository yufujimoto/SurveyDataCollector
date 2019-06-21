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
import modules.setupConfigSkin as setupConfigSkin
import modules.camera as camera

# Import camera and image processing library.
import dialog.configurationDialog as configurationDialog

class configurationDialog(QDialog, configurationDialog.Ui_configurationDialog):
    @property
    def language(self): return self._language
    @property
    def skin(self): return self._skin
    
    @language.setter
    def language(self, value): self._language = value
    @skin.setter
    def skin(self, value): self._skin = value
    
    def __init__(self, parent=None):
        try:
            super(configurationDialog, self).__init__(parent)
            self.setupUi(self)
            
            # Initialize the window.
            self.setWindowTitle(self.tr("Configuration"))
            
            #self.lst_camera.itemClicked.connect(self._getSelectedNumber)
            
            # Refresh camera parameters.
            self.refreshCameraParameters()
            
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
            
            
            # Set the dialog button size.
            dlg_btn_size = QSize(125, 30)
            self.bbx_conf_res.buttons()[0].setMinimumSize(dlg_btn_size)
            self.bbx_conf_res.buttons()[1].setMinimumSize(dlg_btn_size)
            
            self._language = parent.language
            self._skin = parent.skin
            
            if self._language == "ja":
                self.cbx_lang.setCurrentIndex(0)
            elif self._language == "en":
                self.cbx_lang.setCurrentIndex(1)
            
            if self._skin == "grey":
                self.cbx_skin.setCurrentIndex(0)
            elif self._skin == "white":
                self.cbx_skin.setCurrentIndex(1)
            
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
            
            # Apply skin to the window.
            self.setSkin(parent.icon_directory)
            
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
        
    def setSkin(self, icon_path):
        print("configuration::setSkin(self, icon_path)")
        
        try:
            # Apply the new skin.
            setupConfigSkin.applyConfigWindowSkin(self, icon_path, skin=self._skin)
            setupConfigSkin.setConfigWindowButtonText(self)
            
            # Set the tool tips with the specific language.
            #setupConfigSkin.setMainWindowToolTips(self)
        except Exception as e:
            print("Error occured in configuration::setSkin(self, icon_path)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)
