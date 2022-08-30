#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Import general libraries.
import sys, os, uuid, shutil, time, math, tempfile, logging, pyexiv2, datetime

# Import PyQt5 libraries for generating the GUI application.
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QThread, pyqtSignal

# Import general operations.
import modules.general as general
import modules.features as features

# Import camera and image processing library.
import modules.imageProcessing as imageProcessing
import dialog.textEditDialog as textEditDialog

# Import libraries for sound recording. 
import queue
import sounddevice as sd
import soundfile as sf
import numpy as np

import viewer.imageViewer as viewer

class textEdit(QDialog, textEditDialog.Ui_textWriteDialog):
    # Default paths.
    @property
    def source_directory(self): return self._source_directory
    @property
    def icon_directory(self): return self._icon_directory
    @property
    def root_directory(self): return self._root_directory
    @property
    def label_consolidation(self): return self._label_consolidation
    @property
    def label_material(self): return self._label_material
    @property
    def qt_image(self): return self._qt_image
    @property
    def image_extensions(self): return self._image_extensions
    @property
    def sound_extensions(self): return self._sound_extensions
    
    @source_directory.setter
    def source_directory(self, value): self._source_directory = value
    @icon_directory.setter
    def icon_directory(self, value): self._icon_directory = value
    @root_directory.setter
    def root_directory(self, value): self._root_directory = value
    @label_consolidation.setter
    def label_consolidation(self, value): self._label_consolidation = value
    @label_material.setter
    def label_material(self, value): self._label_material = value
    @qt_image.setter
    def qt_image(self, value): self._qt_image = value
    @image_extensions.setter
    def image_extensions(self, value): self._image_extensions = value
    @sound_extensions.setter
    def sound_extensions(self, value): self._sound_extensions = value
    
    def __init__(self, parent=None, img_path=None, snd_path=None):
        # Initialyze super class and set up this.
        super(textEdit, self).__init__(parent)
        self.setupUi(self)
        
        # Set the source directory which this program located.
        self._source_directory = parent.source_directory
        self._icon_directory = parent.icon_directory
        self._qt_image = parent.qt_image
        self._image_extensions = parent.image_extensions
        self._sound_extensions = parent.sound_extensions
        
        # Initialize the window.
        self.setWindowTitle(self.tr("Check Tethered Image"))
        self.setWindowState(Qt.WindowMaximized)
        
        if parent.skin == "grey":
            # Set the icon path.
            self._icon_directory = os.path.join(self._icon_directory, "white")
            
        elif skin == "white":
            # Set the icon path.
            self._icon_directory = os.path.join(self._icon_directory, "black")
        
        # Initialyze the list view of the thumbnails.
        self.lst_img_icon.setIconSize(QSize(200,200))
        self.lst_img_icon.setMovement(QListView.Static)
        self.lst_img_icon.setModel(QStandardItemModel())
        
        # Define the return values.
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        # Create the graphic view item.        
        self.graphicsView = viewer.ImageViewer()
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)
        
        # Get the path of the tethered image.
        self.path_img = img_path
        
        # Initialyze the thumbnail selector.
        self.lst_img_icon.selectionModel().selectionChanged.connect(self.showImage)
        
        # Get tethered image files.
        self.getImageFiles()
    
    def getImageFiles(self):
        print("recordWithPhoto::getImageFiles(self)")
        
        try:
            # Get the file list with given path.
            img_lst_main = general.getFilesWithExtensionList(self.path_img, self._image_extensions)
            
            # Add each image file name to the list box.
            if img_lst_main > 0:
                for img_main in img_lst_main:
                    # Check the image file can be displayed directry.
                    img_base, img_ext = os.path.splitext(img_main)
                    
                    # Get th ful path of the image.
                    img_path = os.path.join(self.path_img, img_main)
                    
                    # Get images that can be shown as QPixmap object.
                    for qt_ext in self._qt_image:
                        # Exit loop if extension is matched with Qt supported image.
                        if img_ext.lower() == qt_ext.lower(): break
                    
                    # Create the QPixmap object
                    pixmap = QPixmap(img_path)
                    
                    # Create the list view item.
                    item = QStandardItem(QIcon(pixmap), img_main)
                    
                    # Append the list view item to the list view.
                    self.lst_img_icon.model().appendRow(item)
        except Exception as e:
            print("Error in RecordWithImage::getImageFiles(self)")
            print(str(e))
    
    def showImage(self):
        print("recordWithPhoto::showImage(self)")
        
        try:
            # Do nothing if theh selected image is None.
            if not self.lst_img_icon.selectedIndexes() == None:
                # Retrive the selected object.
                selected_index = self.lst_img_icon.selectedIndexes()[0]
                
                # Decode the object data.
                img_main = selected_index.data()
                
                # Get the path to the image file.
                img_path = os.path.join(self.path_img, img_main)
                
                # Show the image on graphic view.
                self.graphicsView.setFile(img_path)
        except Exception as e:
            print("Error in RecordWithImage::showImage(self)")
            print(str(e))
