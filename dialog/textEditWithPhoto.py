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
import modules.imageProcessing as imageProcessing
import modules.error as error
import modules.setupTwpSkin as skin

import dialog.textEditWithPhotoDialog as textEditWithPhotoDialog

# Import libraries for sound recording.
import queue
import numpy as np

import viewer.imageViewer as viewer

class jottingWithImage(QDialog, textEditWithPhotoDialog.Ui_textEditDialog):
    # Default paths.
    @property
    def language(self): return self._language
    @property
    def skin(self): return self._skin
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

    @language.setter
    def language(self, value): self._language = value
    @skin.setter
    def skin(self, value): self._skin = value
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
        self._skin = parent.skin
        self._language = parent.language
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
        self.setWindowState(Qt.WindowMaximized)

        # Create the graphic view item.
        self.graphicsView = viewer.ImageViewer()
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)

        self.setSkin(self._icon_directory)

        # Get tethered image files.
        self.getImageFiles()
        self.getTextFiles()

        #===============================
        # Connect to the slot.
        #===============================
        self.lst_img_icon.selectionModel().selectionChanged.connect(self.showImage) # Initialyze the thumbnail selector.
        self.lst_txt_fls.selectionModel().selectionChanged.connect(self.showText)   # Initialyze the text file selector.
        self.chk_edit.stateChanged.connect(self.enableEditMode)                     # Handle the edit mode.
        self.btn_new_txt.clicked.connect(self.createNewTextFile)                    # Create a new empty file.
        self.btn_ocr.clicked.connect(self.createTextByOcr)                          # Create a new text file by OCR.
        self.btn_bar.clicked.connect(self.createTextByBarcode)                      # Create a new text file by barcodes.
        self.btn_sav.clicked.connect(self.saveText)                                 # Save modification.
        self.btn_opn_app.clicked.connect(self.openByApp)                            # Open and edit by the other app.

        # Define the return values.
        self.bbx_rec_pht.accepted.connect(self.accept)
        self.bbx_rec_pht.rejected.connect(self.reject)

    def setSkin(self, icon_path):
        print("Start -> textEditWithPhotoDialog::setSkin(self, icon_path)")
        try:
            # Apply the new skin.
            skin.setSkin(self, icon_path, skin=self._skin)
            skin.setText(self)

        except Exception as e:
            print("Error occured in textEditWithPhotoDialog::setSkin(self, icon_path)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=parent.language)
            return(None)

        finally:
            print("End -> textEditWithPhotoDialog::setSkin")

    def createTextFileInstance(self, obj_body, obj_status, obj_src, obj_app, obj_ope, obj_lock, obj_capt, obj_uuid=None, obj_cdate=None, obj_mdate=None):
        print("Start -> textEditWithPhotoDialog::createTextFileInstance")

        try:
            # Generate the GUID for the consolidation
            if not obj_uuid == None:
                txt_uuid = str(uuid)
            else:
                txt_uuid = str(uuid.uuid4())

            # Get date of creation and modification.
            now = datetime.datetime.utcnow().isoformat()

            if obj_cdate == None: cdate = now
            if obj_mdate == None: mdate = now

            # Define the path of new file.
            txt_path = os.path.join(self._text_path, txt_uuid + ".txt")

            # Instantiate the File class.
            sop_txt_file = features.File(is_new=True, uuid=txt_uuid, dbfile=None)
            sop_txt_file.material = self._mat_uuid
            sop_txt_file.consolidation = self._con_uuid
            sop_txt_file.filename = general.getRelativePath(txt_path, "Consolidation")
            sop_txt_file.created_date = obj_cdate
            sop_txt_file.modified_date = obj_mdate
            sop_txt_file.file_type = "text"
            sop_txt_file.alias = obj_ope
            sop_txt_file.status = obj_status
            sop_txt_file.lock = obj_lock
            sop_txt_file.public = False
            sop_txt_file.source = obj_src
            sop_txt_file.operation = obj_ope
            sop_txt_file.operating_application = obj_app
            sop_txt_file.caption = obj_capt
            sop_txt_file.description = ""

            # Insert the new entry into the self._database.
            sop_txt_file.dbInsert(self._database)

            # Create a new file at the path.
            if obj_body == None or obj_body == False:
                open(txt_path, 'w').close()
            else:
                with open(txt_path, 'w') as f: f.write(obj_body)

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

        self.createTextFileInstance(
            obj_body=body,
            obj_status=status,
            obj_src=src,
            obj_app=app,
            obj_ope=ope,
            obj_lock=lock,
            obj_capt=capt
        )

    def createTextByOcr(self):
        print("textEditWithPhotoDialog::createTextByOcr(self)")

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
        self.createTextFileInstance(
            obj_body=body,
            obj_status=status,
            obj_src=src,
            obj_app=app,
            obj_ope=ope,
            obj_lock=lock,
            obj_capt=capt
        )

    def createTextByBarcode(self):
        print("textEditWithPhotoDialog::createTextByBarcode(self)")

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
            self.createTextFileInstance(
                obj_body=body,
                obj_status=status,
                obj_src=src,
                obj_app=app,
                obj_ope=ope,
                obj_lock=lock,
                obj_capt=capt
            )
        else:
            print("None of barcodes are detected.")

    def saveText(self):
        print("textEditWithPhotoDialog::saveText(self)")

        selected_index = self.lst_txt_fls.selectedIndexes()[0]
        src_uuid = os.path.basename(selected_index.data())

        edt_txt = self.textEdit.toPlainText()

        # Properties for instance of SOP File object.
        body = edt_txt
        status = "Edited"
        src = src_uuid
        app = "Survey Data Collecto"
        ope = "Manually Edited"
        lock = True
        capt = "Manually Edited"

        # Create a new text file by editing.
        self.createTextFileInstance(
            obj_body=body,
            obj_status=status,
            obj_src=src,
            obj_app=app,
            obj_ope=ope,
            obj_lock=lock,
            obj_capt=capt
        )

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

                    # Instantiate the File class.
                    sop_txt_file = features.File(is_new=True, uuid=new_uuid, dbfile=None)
                    sop_txt_file.material = self._mat_uuid
                    sop_txt_file.consolidation = self._con_uuid
                    sop_txt_file.filename = general.getRelativePath(new_file, "Consolidation")
                    sop_txt_file.created_date = cdate
                    sop_txt_file.modified_date = mdate
                    sop_txt_file.file_type = "text"
                    sop_txt_file.alias = "Edit with " + self._app_textEdit
                    sop_txt_file.status = "Edited"
                    sop_txt_file.lock = lock = False
                    sop_txt_file.public = False
                    sop_txt_file.source = old_uuid
                    sop_txt_file.operation = "Edit with " + self._app_textEdit
                    sop_txt_file.operating_application = self._app_textEdit
                    sop_txt_file.caption = "Manually Edited"
                    sop_txt_file.description = ""

                    # Insert the new entry into the self._database.
                    sop_txt_file.dbInsert(self._database)
            else:
                error.ErrorMessageFileNotExist()

                # Returns nothing.
                return(None)
        except Exception as e:
            print("Error occured in textEditWithPhotoDialog::openByApp(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)
        finally:
            # Update the text file list.
            self.getTextFiles()

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
            if not self._currentObject.texts == None:
                if len(self._currentObject.texts) > 0:
                    for txt in self._currentObject.texts:
                        txt_name =os.path.basename(txt.filename)
                        txt_item = QListWidgetItem(txt_name)
                        self.lst_txt_fls.addItem(txt_item)

        except Exception as e:
            print("Error in RecordWithImage::getTextFiles")
            print(str(e))

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
            text_border = 'border-style: outset; border-width: 1.0px; border-color: #DDDDDD'
            back_color = "background-color: #6C6C6C;"
            font_style_color = 'color: #FF0000;'

            self.textEdit.setReadOnly(False)
            self.textEdit.setStyleSheet(text_border + font_style_color + back_color)

            # Set the save button.
            btn_style_color = 'color: #FF0000;'

            # Set the skin and icon.
            self.btn_sav.setDisabled(False)

            if self.skin == "grey":
                icon_path = os.path.join(self._icon_directory, "white")
                self.btn_sav.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'save_active.png'))))
            else:
                icon_path = os.path.join(self._icon_directory, "black")
                self.btn_sav.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'save_active.png'))))

            icon_size = general.getIconSize()
            qicon_size = QSize(icon_size, icon_size)
            self.btn_sav.setIconSize(qicon_size)

        else:
            # Set the default background and front color.
            text_border = 'border-style: outset; border-width: 1.0px; border-color: #DDDDDD'
            back_color = 'background-color: #2C2C2C;'
            font_style_color = 'color: #FFFFFF;'

            self.textEdit.setReadOnly(True)
            self.textEdit.setStyleSheet(text_border + font_style_color + back_color)

            # Set the save button.
            btn_style_color = 'color: #FFFFFF;'

            # Set the skin and icon.
            icon_size = general.getIconSize()
            qicon_size = QSize(icon_size, icon_size)

            self.btn_sav.setDisabled(True)

            if self.skin == "grey":
                icon_path = os.path.join(self._icon_directory, "white")
                self.btn_sav.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'save.png'))))
            else:
                icon_path = os.path.join(self._icon_directory, "black")
                self.btn_sav.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'save.png'))))

            icon_size = general.getIconSize()
            qicon_size = QSize(icon_size, icon_size)
            self.btn_sav.setIconSize(qicon_size)

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
