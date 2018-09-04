#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Import PyQt5 libraries for generating the GUI application.
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Import camera and image processing library.
import dialog.flickrDialog as flickrDialog

class FlickrAPIDialog(QDialog, flickrDialog.Ui_FlickrAPIDialog):
    @property
    def apikey(self): return self._apikey
    @property
    def secret(self): return self._secret
    
    @apikey.setter
    def apikey(self, value): self._secret = value
    @secret.setter
    def secret(self, value): self._secret = value
    
    def __init__(self, parent=None, apikey="Empty", secret="Empty"):
        super(FlickrAPIDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.tbx_flickr_key.setText(apikey)
        self.tbx_flickr_sec.setText(secret)