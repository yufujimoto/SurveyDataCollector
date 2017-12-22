#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Import PyQt5 libraries for generating the GUI application.
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Import camera and image processing library.
import dialog.cameraSelectDialog as cameraSelectDialog

class SelectCameraDialog(QDialog, cameraSelectDialog.Ui_CameraSelectDialog):
    @property
    def selected(self): return self._selected
    @selected.setter
    def selected(self, value): self._selected = value
    
    def __init__(self, parent=None, cameras=None):
        super(SelectCameraDialog, self).__init__(parent)
        self.setupUi(self)
        
        self._selected = None
        self.lst_camera.itemClicked.connect(self._getSelectedNumber)
        
        for camera in cameras:
            item = QListWidgetItem(camera["name"])
            self.lst_camera.addItem(item)
        self.lst_camera.show()
        
        if len(cameras) > 0 :
            self.lst_camera.setCurrentRow(0)
            self._selected = 0
    
    def _getSelectedNumber(self):
        self._selected = self.lst_camera.currentRow()