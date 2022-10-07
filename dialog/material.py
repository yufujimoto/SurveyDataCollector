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
import objects.features as features
import modules.error as error

#import modules.skin as skin
import modules.setupMatSkin as skin

# Import camera and image processing library.
import dialog.materialDialog as materialDialog

class materialDialog(QDialog, materialDialog.Ui_materialDialog):
    # Default paths.
    @property
    def language(self): return self._language
    @property
    def skin(self): return self._skin
    @property
    def icon_directory(self): return self._icon_directory

    @language.setter
    def language(self, value): self._language = value
    @skin.setter
    def skin(self, value): self._skin = value
    @icon_directory.setter
    def icon_directory(self, value): self._icon_directory = value

    def __init__(self, parent=None):
        super(materialDialog, self).__init__(parent)
        self.setupUi(self)

        self._language = parent.language
        self._skin = parent.skin
        self._icon_directory = parent.icon_directory

        # Initialize the window.
        self.setWindowTitle(self.tr("Material View"))

        # Set skin for this UI.
        self.setSkin()

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

    def setSkin(self):
        print("Start -> material::setSkin(self, icon_path)")
        try:
            # Apply the new skin.
            skin.setSkin(self, self._icon_directory, skin=self._skin)
            skin.setText(self)

        except Exception as e:
            print("Error occured in material::setSkin(self, icon_path)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

        finally:
            print("End -> material::setSkin")
