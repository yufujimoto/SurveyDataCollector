#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Import general libraries.
import sys, os, uuid, shutil, time, math, tempfile, logging, pyexiv2, datetime

# Import the library for acquiring file information.
from stat import *
from dateutil.parser import parse

# Import PyQt5 libraries for generating the GUI application.
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QThread, pyqtSignal

import modules.features as features

# Import general operations.
import modules.general as general

# Import camera and image processing library.
import modules.imageProcessing as imageProcessing
import dialog.fileInformationDialog as fileInformationDialog

class fileInformationDialog(QDialog, fileInformationDialog.Ui_fileInformationDialog):
    def __init__(self, parent=None, sop_file=None):
        # Get the path of the tethered image.
        self._sop_file = sop_file
        
        # Set the source directory which this program located.
        self._root_directory = parent.root_directory
        self._source_directory = parent.source_directory
        self._icon_directory = parent.icon_directory
        self._qt_image = parent.qt_image
        self._image_extensions = parent.image_extensions
        self._raw_image_extensions = parent.raw_image_extensions
        self._sound_extensions = parent.sound_extensions
        
        super(fileInformationDialog, self).__init__(parent)
        self.setupUi(self)
        
        # Initialize the window.
        self.setWindowTitle(self.tr("File Information Dialog"))
        
        # Define the return values.
        self.box_fil_ope.accepted.connect(self.accept)
        self.box_fil_ope.rejected.connect(self.reject)
        
        # Initialyze the image panel.
        self.image_panel.resize(800, 600)
        self.image_panel.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        
        # Get the image properties from the instance.
        if sop_file.public == "1":
            self.cbx_fil_pub.setChecked(True)
        else:
            self.cbx_fil_pub.setChecked(False)
        
        if sop_file.lock == "1":
            self.cbx_fil_edit.setChecked(False)
            self.cbx_fil_edit.setDisabled(True)
        else:
            self.cbx_fil_edit.setChecked(True)
            self.cbx_fil_edit.setDisabled(False)
        
        # Set the alias name of the file object.
        self.tbx_fil_ali.setText(sop_file.alias)
        
        # Set the date of creation and modification.
        
        #set an arbitrary date and time
        fil_dt_create = general.pyDateTimeToQDateTime(parse(sop_file.created_date))
        fil_dt_modify = general.pyDateTimeToQDateTime(parse(sop_file.modified_date))
        
        self.dte_fil_dt_cre.setDateTime(fil_dt_create)
        self.dte_fil_dt_mod.setDateTime(fil_dt_modify)

        # Set the operating application software.
        self.tbx_fil_ope_app.setText(sop_file.operating_application)
        
        # Set the caption of the file object.
        self.tbx_fil_capt.setText(sop_file.caption)
        
        # Set the status of the file object and optional values.
        self.cmb_fil_stts.addItem(sop_file.status)
        self.cmb_fil_stts.addItem("Original")
        self.cmb_fil_stts.addItem("Removed")
        self.cmb_fil_stts.addItem("Imported")
        self.cmb_fil_stts.addItem("Edited")
        
        # Set the operation of the file object and option values.
        self.cmb_fil_eope.addItem(sop_file.operation)
        self.cmb_fil_eope.addItem("Editing on GIMP")
        self.cmb_fil_eope.addItem("Rotating")
        self.cmb_fil_eope.addItem("Grayscaling")
        self.cmb_fil_eope.addItem("White balance adjusting")
        self.cmb_fil_eope.addItem("Normalizing")
        self.cmb_fil_eope.addItem("Cropping")
        self.cmb_fil_eope.addItem("Color inverting")
        self.cmb_fil_eope.addItem("Removing")
        self.cmb_fil_eope.addItem("Colorlizing")
        self.cmb_fil_eope.addItem("Unknown")
        self.cmb_fil_eope.addItem("Other")
        
        if sop_file.file_type == "image":
            # Set active control tab for material.
            self.tab_src.setCurrentIndex(0)
            self.getImageFileInfo(sop_file)
        if sop_file.file_type == "audio":
            # Set active control tab for material.
            self.tab_src.setCurrentIndex(1)
            #self.getSoundFileInfo(sop_file)
        
        # Get tethered image files.
        #self.getImageFiles()
        
    # Properties for default paths.
    @property
    def source_directory(self): return self._source_directory
    @property
    def siggraph_directory(self): return self._siggraph_directory
    @property
    def icon_directory(self): return self._icon_directory
    @property
    def temporal_directory(self): return self._temporal_directory
    @property
    def root_directory(self): return self._root_directory
    @property
    def table_directory(self): return self._table_directory
    @property
    def consolidation_directory(self): return self._consolidation_directory
    @property
    def database(self): return self._database
    
    # Properties for default labels.
    @property
    def label_consolidation(self): return self._label_consolidation
    @property
    def label_material(self): return self._label_material
    
    # Properties for default extensions.
    @property
    def qt_image(self): return self._qt_image
    @property
    def image_extensions(self): return self._image_extensions
    @property
    def raw_image_extensions(self): return self._raw_image_extensions
    @property
    def sound_extensions(self): return self._sound_extensions
    
    # Property for selected SOP object
    @property
    def sop_file(self): return self._sop_file
    
    # Setter for default paths.
    @source_directory.setter
    def source_directory(self, value): self._source_directory = value
    @siggraph_directory.setter
    def siggraph_directory(self, value): self._siggraph_directory = value
    @icon_directory.setter
    def icon_directory(self, value): self._icon_directory = value
    @temporal_directory.setter
    def temporal_directory(self, value): self._temporal_directory = value
    @root_directory.setter
    def root_directory(self, value): self._root_directory = value
    @table_directory.setter
    def table_directory(self, value): self._table_directory = value
    @consolidation_directory.setter
    def consolidation_directory(self, value): self._consolidation_directory = value
    @database.setter
    def database(self, value): self._database = value
    
    # Setter for default labels.
    @label_consolidation.setter
    def label_consolidation(self, value): self._label_consolidation = value
    @label_material.setter
    def label_material(self, value): self._label_material = value
    
    # Setter for default extensions.
    @qt_image.setter
    def qt_image(self, value): self._qt_image = value
    @image_extensions.setter
    def image_extensions(self, value): self._image_extensions = value
    @raw_image_extensions.setter
    def raw_image_extensions(self, value): self._raw_image_extensions = value
    @sound_extensions.setter
    def sound_extensions(self, value): self._sound_extensions = value
    
    # Setter for selected object.
    @sop_file.setter
    def sop_file(self, value): self._sop_file = value
    
    def showImage(self, img_file_path):
        print("fileInformationDialog::showImage(self)")
        
        try:
            # Check the image file can be displayed directry.
            img_base, img_ext = os.path.splitext(img_file_path)
            img_valid = False
            
            # Get container size.
            panel_w = self.lbl_img_preview.width()
            panel_h = self.lbl_img_preview.height()
            
            for qt_ext in self._qt_image:
                # Exit loop if extension is matched with Qt supported image.
                if img_ext.lower() == qt_ext.lower():
                    img_valid = True
                    break
            
            # Check whether the image is Raw image or not.
            if not img_valid == True:
                # Extract the thumbnail image from the RAW image by using "dcraw".
                imageProcessing.getThumbnail(img_file_path)
                
                # Get the extracted thumbnail image.
                img_file_path = img_base + ".thumb.jpg"
            
            if os.path.exists(img_file_path):
                # Create the container for displaying the image
                org_pixmap = QPixmap(img_file_path)
                scl_pixmap = org_pixmap.scaled(panel_w, panel_h, Qt.KeepAspectRatio)
                
                # Set the image file to the image view container.
                self.lbl_img_preview.setPixmap(scl_pixmap)
                            
                # Show the selected image.
                self.lbl_img_preview.show()
            else:
                # Create error messages.
                error_title = "エラーが発生しました"
                error_msg = "このファイルはプレビューに対応していません。"
                error_info = "諦めてください。RAW + JPEG で撮影することをお勧めします。"
                error_icon = QMessageBox.Critical
                error_detailed = str(e)
                
                # Handle error.
                general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
                
                # Returns nothing.
                return(None)
        except Exception as e:
            print("Error occurs in fileInformationDialog::showImage(self)")
            
            # Show the error message.
            self.errorUnknown("fileInformationDialog::showImage(self)", str(e))
            
            # Return nothing.
            return(None)
    
    def getImageFileInfo(self, sop_image):
        print("fileInformationDialog::getImageFileInfo(self)")
        
        try:
            # Get the full path of the image.
            if sop_image.filename == "":
                img_file_path = os.path.join(os.path.join(self._source_directory, "images"),"noimage.jpg")
            else:
                if not os.path.exists(os.path.join(self._root_directory, sop_image.filename)):
                    img_file_path = os.path.join(os.path.join(self._source_directory, "images"),"noimage.jpg")
                else:
                    img_file_path = os.path.join(self._root_directory, sop_image.filename)
            
            # Show preview.
            self.showImage(img_file_path)
            
        except Exception as e:
            print("Error occurs in fileInformationDialog::getImageFileInfo(self)")
            print(str(e))
            
            return(None)