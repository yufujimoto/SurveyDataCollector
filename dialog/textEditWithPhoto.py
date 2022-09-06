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
#import modules.skin as skin
import modules.setupConfigSkin as skin

import dialog.textEditWithPhotoDialog as textEditWithPhotoDialog

# Import libraries for sound recording. 
import queue
import numpy as np

import viewer.imageViewer as viewer

class jottingWithImage(QDialog, textEditWithPhotoDialog.Ui_textEditDialog):
    # Default paths.
    @property
    def source_directory(self): return self._source_directory
    @property
    def icon_directory(self): return self._icon_directory
    @property
    def root_directory(self): return self._root_directory
    @property
    def currentObject(self): return self._currentObject
    @property
    def qt_image(self): return self._qt_image
    @property
    def image_extensions(self): return self._image_extensions
    
    @source_directory.setter
    def source_directory(self, value): self._source_directory = value
    @icon_directory.setter
    def icon_directory(self, value): self._icon_directory = value
    @root_directory.setter
    def root_directory(self, value): self._root_directory = value
    @currentObject.setter
    def currentObject(self, value): self._currentObject = value
    @qt_image.setter
    def qt_image(self, value): self._qt_image = value
    @image_extensions.setter
    def image_extensions(self, value): self._image_extensions = value
    
    def __init__(self, parent=None, img_path=None, txt_path=None, sop=None):
        # Initialyze super class and set up this.
        super(jottingWithImage, self).__init__(parent)
        self.setupUi(self)
        
        # Set the source directory which this program located.
        self._source_directory = parent.source_directory
        self._icon_directory = parent.icon_directory
        self._qt_image = parent.qt_image
        self._image_extensions = parent.image_extensions
        self._currentObject = sop
        
        # Initialize the window.
        self.setWindowTitle(self.tr("Jotting memo with obser"))
        self.setWindowState(Qt.WindowMaximized)        
        
        # Setup labels with designated language.
        if parent.language == "ja":
            self.lbl_img.setText("画像一覧")
            self.lbl_fl_txt.setText("テキストファイル一覧")
            self.btn_new_txt.setText("新規作成")
            self.btn_sav.setText("保存")
            self.btn_bar.setText("バーコード")
        elif parent.language == "en":
            self.lbl_img.setText("Image Slector")
            self.lbl_fl_txt.setText("Text Files")
            self.btn_new_txt.setText("New")
            self.btn_sav.setText("Save")
            self.btn_bar.setText("Barcode")
        
        # Initialyze the list view of the thumbnails.
        self.lst_img_icon.setIconSize(QSize(200,200))
        self.lst_img_icon.setMovement(QListView.Static)
        self.lst_img_icon.setModel(QStandardItemModel())
         
        # # Initialyze the stop button.
        # self.btn_rec_stop.setIcon(QIcon(QPixmap(os.path.join(self._icon_directory, 'pause.png'))))
        # self.btn_rec_stop.setIconSize(QSize(24,24))
        
        # # Define the return values.
        # self.bbx_rec_pht.accepted.connect(self.accept)
        # self.bbx_rec_pht.rejected.connect(self.reject)
        
        # Create the graphic view item.        
        self.graphicsView = viewer.ImageViewer()
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)
        
        # Get the path of the tethered image.
        self.path_img = img_path
        self.path_txt = txt_path
        
        # Initialyze the thumbnail selector.
        self.lst_img_icon.selectionModel().selectionChanged.connect(self.showImage)
        
        # Get tethered image files.
        self.getImageFiles()
        self.getTextFiles()
        
        # Initialyze the user interface.
        # Get the proper font size from the display size and set the font size.
        font_size = skin.getFontSize()
        
        # Make the style sheet.
        font_style_size = 'font: regular ' + str(skin.getFontSize()) + 'px;'
        
        # Define the font object for Qt.
        font = QFont()
        font.setPointSize(font_size)
        
        self.setFont(font)
        
        if parent.skin == "grey":
            # Set the icon path.
            self._icon_directory = os.path.join(self._icon_directory, "white")
            
            # Set the default background and front color.
            back_color = 'background-color: #2C2C2C;'
            font_style_color = 'color: #FFFFFF;'
            font_style = font_style_color + font_style_size
            
            # Set the default skin for all components.
            self.setStyleSheet(back_color + font_style + 'border-style: none; border-color: #4C4C4C;')
            #self.frm_photo_view.setStyleSheet('border-style: solid; border-width: 0.5px; border-color: #FFFFFF;')
            self.graphicsView.setStyleSheet('border-style: outset; border-width: 0.5px; border-color: #FFFFFF;')
            
            self.lst_txt_fls.setStyleSheet('border-style: outset; border-width: 0.5px; border-color: #FFFFFF;')
            self.lst_img_icon.setStyleSheet('border-style: outset; border-width: 0.5px; border-color: #FFFFFF;')
            
            self.textEdit.setStyleSheet('border-style: outset; border-width: 0.5px; border-color: #FFFFFF;')
        elif skin == "white":
            # Set the icon path.
            self._icon_directory = os.path.join(self._icon_directory, "black")
        
        # Initialyze the new document button.
        self.btn_new_txt.setIcon(QIcon(QPixmap(os.path.join(self._icon_directory, 'new_document.png'))))
        self.btn_new_txt.setIconSize(QSize(24,24))
        self.btn_new_txt.clicked.connect(self.createNewTextFile)
        
        # Initialyze the save button.
        self.btn_sav.setIcon(QIcon(QPixmap(os.path.join(self._icon_directory, 'save.png'))))
        self.btn_sav.setIconSize(QSize(24,24))
        #self.btn_sav.clicked.connect(self.startRecording)
        
        # Initialyze the OCR button.
        self.btn_ocr.setIcon(QIcon(QPixmap(os.path.join(self._icon_directory, 'ocr.png'))))
        self.btn_ocr.setIconSize(QSize(24,24))
        #self.btn_ocr.clicked.connect(self.startRecording)s
        
        # Initialyze the barcode button.
        self.btn_bar.setIcon(QIcon(QPixmap(os.path.join(self._icon_directory, 'barcode.png'))))
        self.btn_bar.setIconSize(QSize(24,24))
        #self.btn_bar.clicked.connect(self.startRecording)
        
        
        # Set the dialog button size.
        dlg_btn_size = QSize(125, 30)
        self.bbx_rec_pht.buttons()[0].setMinimumSize(dlg_btn_size)
        self.bbx_rec_pht.buttons()[1].setMinimumSize(dlg_btn_size)
        
        # Set the skin and icon.
        self.bbx_rec_pht.buttons()[0].setIcon(skin.getIconFromPath(os.path.join(self._icon_directory, 'check.png')))
        self.bbx_rec_pht.buttons()[1].setIcon(skin.getIconFromPath(os.path.join(self._icon_directory, 'close.png')))
        
    def createNewTextFile(self):
        print("textEditWithPhotoDialog::createNewTextFile")
        
        try:
            # Generate the GUID for the consolidation
            txt_uuid = str(uuid.uuid4())
            
            # Define the path of new file.
            txt_path = os.path.join(self.path_txt, txt_uuid + ".txt")
            
            # Instantiate the File class.
            txt_file = features.File(is_new=True, uuid=None, dbfile=None)
            txt_file.material = mat_uuid
            txt_file.consolidation = con_uuid
            txt_file.filename = general.getRelativePath(txt_path, "Consolidation")
            txt_file.created_date = now
            txt_file.modified_date = now
            txt_file.file_type = "text"
            txt_file.alias = "Description"
            txt_file.status = "Original"
            txt_file.lock = True
            txt_file.public = False
            txt_file.source = "Nothing"
            txt_file.operation = "Make an empty text file"
            txt_file.operating_application = "Survey Data Collector"
            txt_file.caption = "Original text"
            txt_file.description = ""
            
            # Insert the new entry into the self._database.
            txt_file.dbInsert(parent._database)
            
            # Create a new file at the path.
            open(txt_path, 'w').close()
            
            # Add new file to the text file list.
            txt_item = QListWidgetItem(txt_path)
            self.lst_txt_fls.addItem(txt_item)
            
        except Exception as e:
            print("Error in RecordWithImage::createNewTextFile")
            print(str(e))
    
    def getTextFiles(self):
        print("textEditWithPhotoDialog::getTextFiles")
        
        try:
            # Clear itmes if exists.
            self.lst_txt_fls.clear()
            
            # Get the file list with given path.
            txt_lst = os.listdir(self.path_txt)
                        
            # Add each image file name to the list box.
            if len(txt_lst) > 0:
                for txt_fl in txt_lst:
                    if os.path.isfile(txt_fl):
                        txt_item = QListWidgetItem(txt_fl)
                        self.lst_txt_fls.addItem(txt_item)
        except Exception as e:
            print("Error in RecordWithImage::getTextFiles")
            print(str(e))
    
    def getImageFiles(self):
        print("textEditWithPhotoDialog::getImageFiles(self)")
        
        try:
            # Get the file list with given path.
            img_lst_main = general.getFilesWithExtensionList(self.path_img, self._image_extensions)
            
            # Add each image file name to the list box.
            if len(img_lst_main) > 0:
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
        print("textEditWithPhotoDialog::showImage(self)")
        
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
