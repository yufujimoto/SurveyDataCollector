#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Import general libraries.
import sys, os, uuid, shutil, time, math, tempfile, logging, pyexiv2, datetime, subprocess

# import pytesseract
import cv2, pytesseract

# Import barcode tools.
from pyzbar.pyzbar import decode 
from PIL import Image

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
import modules.setupConfigSkin as skin

import dialog.textEditWithPhotoDialog as textEditWithPhotoDialog

# Import libraries for sound recording. 
import queue
import numpy as np

import viewer.imageViewer as viewer

class jottingWithImage(QDialog, textEditWithPhotoDialog.Ui_textEditDialog):
    # Default paths.
    @property
    def database(self): return self._database
    @property
    def source_directory(self): return self._source_directory
    @property
    def icon_directory(self): return self._icon_directory
    @property
    def root_directory(self): return self._root_directory
    @property
    def currentObject(self): return self._currentObject
    @property
    def con_uuid(self): return self._con_uuid
    @property
    def mat_uuid(self): return self._mat_uuid
    @property
    def text_path(self): return self._text_path
    @property
    def image_path(self): return self._image_path
    @property
    def qt_image(self): return self._qt_image
    @property
    def image_extensions(self): return self._image_extensions
    @property
    def ocr_lang(self): return self._ocr_lang
    @property
    def ocr_psm(self): return self._ocr_psm
    @property
    def app_textEdit(self): return self._app_textEdit
    
    @database.setter
    def database(self, value): self._database = value
    @source_directory.setter
    def source_directory(self, value): self._source_directory = value
    @icon_directory.setter
    def icon_directory(self, value): self._icon_directory = value
    @root_directory.setter
    def root_directory(self, value): self._root_directory = value
    @currentObject.setter
    def currentObject(self, value): self._currentObject = value
    @con_uuid.setter
    def con_uuid(self, value): self._con_uuid = vlaue
    @mat_uuid.setter
    def mat_uuid(self, value): self._mat_uuid = value
    @text_path.setter
    def text_path(self, value): self._text_path = value
    @image_path.setter
    def image_path(self, value): self._image_path = value
    @qt_image.setter
    def qt_image(self, value): self._qt_image = value
    @image_extensions.setter
    def image_extensions(self, value): self._image_extensions = value
    @ocr_lang.setter
    def ocr_lang(self, value): self._ocr_lang = value
    @ocr_psm.setter
    def ocr_psm(self, value): self._ocr_psm = value
    @app_textEdit.setter
    def app_textEdit(self, value): self._app_textEdit = value
    
    #mat_uuid, con_uuid, dbfile
    def __init__(self, parent=None, img_path=None, txt_path=None, sop=None, con_uuid=None, mat_uuid=None):
        # Initialyze super class and set up this.
        super(jottingWithImage, self).__init__(parent)
        self.setupUi(self)
        
        # Set the source directory which this program located.
        self._database = parent.database
        self._source_directory = parent.source_directory
        self._root_directory = parent.root_directory
        self._icon_directory = parent.icon_directory
        self._qt_image = parent.qt_image
        self._image_extensions = parent.image_extensions
        self._currentObject = sop
        self._con_uuid = con_uuid
        self._mat_uuid = mat_uuid
        self._text_path = txt_path
        self._image_path = img_path
        self._ocr_lang = parent.ocr_lang
        self._ocr_psm = parent.ocr_psm
        self._app_textEdit = parent.app_textEdit
        
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
                
        # Create the graphic view item.        
        self.graphicsView = viewer.ImageViewer()
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)
        
        # Initialyze the thumbnail selector.
        self.lst_img_icon.selectionModel().selectionChanged.connect(self.showImage)
        
        # Initialyze the text file selector.
        self.lst_txt_fls.selectionModel().selectionChanged.connect(self.showText)
        
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
        
        # Initialyze the save button.
        self.btn_sav.setIcon(QIcon(QPixmap(os.path.join(self._icon_directory, 'save.png'))))
        self.btn_sav.setIconSize(QSize(24,24))
        
        # Initialyze the OCR button.
        self.btn_ocr.setIcon(QIcon(QPixmap(os.path.join(self._icon_directory, 'ocr.png'))))
        self.btn_ocr.setIconSize(QSize(24,24))
        
        # Initialyze the barcode button.
        self.btn_bar.setIcon(QIcon(QPixmap(os.path.join(self._icon_directory, 'barcode.png'))))
        self.btn_bar.setIconSize(QSize(24,24))
        
        # Set the dialog button size.
        dlg_btn_size = QSize(125, 30)
        self.bbx_rec_pht.buttons()[0].setMinimumSize(dlg_btn_size)
        self.bbx_rec_pht.buttons()[1].setMinimumSize(dlg_btn_size)
        
        # Set the skin and icon.
        self.bbx_rec_pht.buttons()[0].setIcon(skin.getIconFromPath(os.path.join(self._icon_directory, 'check.png')))
        self.bbx_rec_pht.buttons()[1].setIcon(skin.getIconFromPath(os.path.join(self._icon_directory, 'close.png')))
        
        #===============================
        # Connect to the slot.
        #===============================
        self.chk_edit.stateChanged.connect(self.enableEditMode)     # Handle the edit mode.
        self.btn_new_txt.clicked.connect(self.createNewTextFile)    # Create a new empty file.
        self.btn_ocr.clicked.connect(self.getTextByOcr)             # Create a new text file by OCR.
        self.btn_bar.clicked.connect(self.getTextByBarcode)         # Create a new text file by barcodes.
        self.btn_sav.clicked.connect(self.saveText)                 # Save modification.
        self.btn_opn_app.clicked.connect(self.openByApp)            # Open and edit by the other app.
        
        # Define the return values.
        self.bbx_rec_pht.accepted.connect(self.accept)
        self.bbx_rec_pht.rejected.connect(self.reject)
        
    def createTextFileInstance(self, body, status, src, app, ope, lock, capt, uuid=None, cdate=None, mdate=None):
        print("Start -> textEditWithPhotoDialog::createTextFileInstance")
        
        try: 
            # Generate the GUID for the consolidation
            if not uuid == None:
                txt_uuid = str(uuid)
            else:
                txt_uuid = str(uuid.uuid4())
            
            # Get date of creation and modification.
            now = datetime.datetime.utcnow().isoformat()
            
            if cdate == None: cdate = now
            if mdate == None: mdate = now
            
            # Define the path of new file.
            txt_path = os.path.join(self._text_path, txt_uuid + ".txt")
            
            # Instantiate the File class.
            sop_txt_file = features.File(is_new=True, uuid=txt_uuid, dbfile=None)
            sop_txt_file.material = self._mat_uuid
            sop_txt_file.consolidation = self._con_uuid
            sop_txt_file.filename = general.getRelativePath(txt_path, "Consolidation")
            sop_txt_file.created_date = cdate
            sop_txt_file.modified_date = mdate
            sop_txt_file.file_type = "text"
            sop_txt_file.alias = ope
            sop_txt_file.status = status
            sop_txt_file.lock = lock
            sop_txt_file.public = False
            sop_txt_file.source = src
            sop_txt_file.operation = ope
            sop_txt_file.operating_application = app
            sop_txt_file.caption = capt
            sop_txt_file.description = ""
            
            # Insert the new entry into the self._database.
            sop_txt_file.dbInsert(self._database)
            
            # Create a new file at the path.
            if body == None or body == False:
                open(txt_path, 'w').close()
            else:
                with open(txt_path, 'w') as f: f.write(body)
            
        except Exception as e:
            print("Error in RecordWithImage::createNewTextFile")
            print(str(e))
            
        finally:
            # Update the text file list.
            self.getTextFiles()
        
    def createNewTextFile(self):
        print("Start -> textEditWithPhotoDialog::createNewTextFile")
        
        # properties for instance of SOP File object.
        body = None
        status = "Original"
        src = "Nothing"
        app = "Survey Data Collector"
        ope = "Created Manually"
        lock = False
        capt = "Original text"
        
        self.createTextFileInstance(body, status, src, app, ope, lock, capt)
    
    def getTextFiles(self):
        print("textEditWithPhotoDialog::getTextFiles")
        
        try:
            # Reload the current SOP object.
            if self._currentObject.__class__.__name__ == "Consolidation":
                # Get the Consolidation if the node have no parent.
                uuid = self._currentObject.uuid
                
                # Set current objects.
                self._currentObject = features.Consolidation(is_new=False, uuid=uuid, dbfile=self._database)
            elif self._currentObject.__class__.__name__ == "Material":
                # Get the Materil if the node have a parent.
                uuid = self._currentObject.uuid
                
                # Set current material.
                self._currentObject = features.Material(is_new=False, uuid=uuid, dbfile=self._database)
                
            # Clear itmes if exists.
            self.lst_txt_fls.clear()
            
            # Get the file list with given path.
            for txt in self._currentObject.texts:
                txt_name =os.path.basename(txt.filename)
                txt_item = QListWidgetItem(txt_name)
                self.lst_txt_fls.addItem(txt_item)
            
        except Exception as e:
            print("Error in RecordWithImage::getTextFiles")
            print(str(e))
    
    def getTextByOcr(self):
        print("textEditWithPhotoDialog::getTextByOcr(self)")
        
        # Get the image from the image list.
        selected = self.lst_img_icon.selectedIndexes()[0]
        
        img_fl_nam = self.lst_img_icon.model().itemFromIndex(selected).text()
        img_fl_path = os.path.join(self._image_path, img_fl_nam)
        
        # Get the uuid of the image from the file name.
        img_fl_uuid = os.path.splitext(img_fl_path)[0]
        
        # Get the image as cv2 object.
        org_img = cv2.imread(img_fl_path)
        
        # Convert to the grayscale image.
        ocr_img = cv2.cvtColor(org_img, cv2.COLOR_BGR2GRAY)
        
        # Get texts by tesseract-ocr. 
        ocr_conf = r" -l " + self._ocr_lang + " --psm " + str(int(self._ocr_psm)+1)
        ocr_txt = pytesseract.image_to_string(ocr_img, config=ocr_conf)
        
        # Properties for instance of SOP File object.
        body = ocr_txt
        status = "Original"
        src = img_fl_uuid
        app = "Tesseract OCR"
        ope = "Optically Recoginzed"
        lock = True
        capt = "Optically Recoginzed"
        
        # Create a text file by OCR.
        self.createTextFileInstance(body, status, src, app, ope, lock, capt)
    
    def getTextByBarcode(self):
        print("textEditWithPhotoDialog::getTextByOcr(self)")
        
        # Get the image from the image list.
        selected = self.lst_img_icon.selectedIndexes()[0]
        
        img_fl_nam = self.lst_img_icon.model().itemFromIndex(selected).text()
        img_fl_path = os.path.join(self._image_path, img_fl_nam)
        
        # Get the uuid of the image from the file name.
        img_fl_uuid = os.path.splitext(img_fl_path)[0]
        
        # Get texts by zbar lib.
        bar_objects = decode(Image.open(img_fl_path))
        bar_txt = ""
        
        if not bar_objects == None:
            for bar_obj in bar_objects:
                # Get the detected objects.
                bar_val = bar_obj.data.decode("utf-8")
                bar_typ = bar_obj.type
                
                # Make a line of detected bacode object.
                bar_line = "['value':'" + bar_val + "'," + "'type':'" + bar_typ + "']\n"
                
                # Add the new line to the body.
                bar_txt = bar_txt + bar_line
            
            # Properties for instance of SOP File object.
            body = bar_txt
            status = "Original"
            src = img_fl_uuid
            app = "ZBar"
            ope = "Optically Recoginzed"
            lock = True
            capt = "Optically Recoginzed"
            
            # Create a text file by OCR.
            self.createTextFileInstance(body, status, src, app, ope, lock, capt)
        else:
            print("None of barcodes are detected.")
    
    def saveText(self):
        print("textEditWithPhotoDialog::saveText(self)")
        
        selected_index = self.lst_txt_fls.selectedIndexes()[0]
        uuid = os.path.basename(selected_index.data())
                
        edt_txt = self.textEdit.toPlainText()
        
        self.createNewTextFile(body=edt_txt, status="Edited", src=uuid, app="Survey Data Collecto", ope="Manually Edited")
    
    def openByApp(self):
        print("textEditWithPhotoDialog::openByApp(self)")
        
        try:
            if not self.lst_txt_fls.selectedIndexes() == None:
                self.chk_edit.setChecked(False)
                self.textEdit.setReadOnly(True)
                
                selected_index = self.lst_txt_fls.selectedIndexes()[0]
                
                txt_file_name = selected_index.data()
                txt_file_path = os.path.join(self._text_path, txt_file_name)
                txt_file_ext = os.path.splitext(txt_file_path)[1].lower()
                old_uuid = os.path.basename(txt_file_name)
                
                if os.path.exists(txt_file_path):
                    # Define the new uuid for the image.
                    new_uuid = str(uuid.uuid4())
                    
                    # Get the time for opening GIMP.
                    time_open = datetime.datetime.utcnow().isoformat()
                    
                    # Get the parent directory of the original image.
                    out_dir = os.path.dirname(self._text_path)
                    new_file = os.path.join(self._text_path, new_uuid + txt_file_ext)
                    
                    # Copy the original file.
                    cdate = datetime.datetime.utcnow().isoformat()
                    shutil.copy(txt_file_path, new_file)
                    
                    # Open the image with GIMP.
                    # Define the subprocess for tethered shooting by using gphoto2
                    cmd_editor = [self._app_textEdit]
                    cmd_editor.append(new_file)
                    
                    # Execute the subprocess.
                    subprocess.check_output(cmd_editor)
                    mdate = datetime.datetime.utcnow().isoformat()
                    
                    # Properties for instance of SOP File object.
                    with open(new_file) as f: body = f.read()
                    status = "Original"
                    src = old_uuid
                    app = self._app_textEdit
                    ope = "Edit with " + self._app_textEdit
                    lock = False
                    capt = "Manually Edited"
                    
                    # Create a text file by OCR.
                    self.createTextFileInstance(body, status, src, app, ope, lock, capt, new_uuid, cdate, mdate)
                    
            else:
                error.ErrorMessageFileNotExist()
                
                # Returns nothing.
                return(None)
        except Exception as e:
            print("Error occured in textEditWithPhotoDialog::openByApp(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)
    
    def getImageFiles(self):
        print("textEditWithPhotoDialog::getImageFiles(self)")
        
        try:
            # Get the file list with given path.
            img_lst_main = general.getFilesWithExtensionList(self._image_path, self._image_extensions)
            
            # Add each image file name to the list box.
            if len(img_lst_main) > 0:
                for img_main in img_lst_main:
                    # Check the image file can be displayed directry.
                    img_base, img_ext = os.path.splitext(img_main)
                    
                    # Get th ful path of the image.
                    img_path = os.path.join(self._image_path, img_main)
                    
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
    
    def enableEditMode(self):
        print("textEditWithPhotoDialog::enableEditMode(self)")
        
        if self.chk_edit.isChecked():
            # Set the default background and front color.
            text_border = 'border-style: outset; border-width: 1.0px; border-color: #FFFFFF'
            back_color = "background-color: #6C6C6C;"
            font_style_color = 'color: #FF0000;'
            
            self.textEdit.setReadOnly(False)
            self.textEdit.setStyleSheet(text_border + font_style_color + back_color)
            
            # Set the save button.
            btn_style_color = 'color: #FF0000;'
            
            self.btn_sav.setDisabled(False)
            self.btn_sav.setIcon(QIcon(QPixmap(os.path.join(self._icon_directory, 'save_active.png'))))
            self.btn_sav.setStyleSheet(btn_style_color)
            
        else:
            # Set the default background and front color.
            text_border = 'border-style: outset; border-width: 1.0px; border-color: #FFFFFF'
            back_color = 'background-color: #2C2C2C;'
            font_style_color = 'color: #FFFFFF;'
            
            self.textEdit.setReadOnly(True)
            self.textEdit.setStyleSheet(text_border + font_style_color + back_color)
            
            # Set the save button.
            btn_style_color = 'color: #FFFFFF;'
            
            self.btn_sav.setDisabled(True)
            self.btn_sav.setIcon(QIcon(QPixmap(os.path.join(self._icon_directory, 'save.png'))))
            self.btn_sav.setStyleSheet(btn_style_color)
        
    def showText(self):
        print("Start -> textEditWithPhotoDialog::showText(self)")
        
        try:
            if not self.lst_txt_fls.selectedIndexes() == None:
                self.chk_edit.setChecked(False)
                self.textEdit.setReadOnly(True)
                
                selected_index = self.lst_txt_fls.selectedIndexes()[0]
                
                txt_file_name = selected_index.data()
                txt_file_path = os.path.join(self._text_path, txt_file_name)
                
                # Open the text file.
                txt_file_stream = open(txt_file_path, "r")
                
                self.textEdit.setText(txt_file_stream.read())
                
                txt_file_stream.close()
            else:
                self.textEdit.setText("")
        except Exception as e:
            print("Error in RecordWithImage::showImage(self)")
            print(str(e))
        
        finally:
            print("End -> textEditWithPhotoDialog::showText")
            
    def showImage(self):
        print("Start -> textEditWithPhotoDialog::showImage(self)")
        
        try:
            # Do nothing if theh seleoted image is None.
            if not self.lst_img_icon.selectedIndexes() == None:
                # Retrive the selected object.
                selected_index = self.lst_img_icon.selectedIndexes()[0]
                
                # Decode the object data.
                img_main = selected_index.data()
                
                # Get the path to the image file.
                img_path = os.path.join(self._image_path, img_main)
                
                # Show the image on graphic view.
                self.graphicsView.setFile(img_path)
                
        except Exception as e:
            print("Error in RecordWithImage::showImage(self)")
            print(str(e))
        
        finally:
            print("End -> textEditWithPhotoDialog::showImage")