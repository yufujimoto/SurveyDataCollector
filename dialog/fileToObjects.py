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
import modules.setupF2oSkin as skin

# Import camera and image processing library.
import dialog.fileToObjectsDialog as fileToObjectsDialog

class fileToObjectsDialog(QDialog, fileToObjectsDialog.Ui_fileToObjectsDialog):
    # Default paths.
    @property
    def language(self): return self._language
    @property
    def skin(self): return self._skin
    @property
    def database(self): return self._database
    @property
    def icon_directory(self): return self._icon_directory
    @property
    def image_extensions(self): return self._image_extensions
    @property
    def importedFiles(self): return self._importedFiles
    @property
    def sample(self): return self._sample

    @language.setter
    def language(self, value): self._language = value
    @skin.setter
    def skin(self, value): self._skin = value
    @database.setter
    def database(self, value): self._database = value
    @icon_directory.setter
    def icon_directory(self, value): self._icon_directory = value
    @image_extensions.setter
    def image_extensions(self, value): self._image_extensions = value
    @importedFiles.setter
    def importedFiles(self, value): self._importedFiles = value
    @sample.setter
    def sample(self, value): self._sample = value


    def __init__(self, parent=None):
        # Set the source directory which this program located.
        super(fileToObjectsDialog, self).__init__(parent)
        self.setupUi(self)

        # Initialize the window.
        self.setWindowTitle(self.tr("File To Objects Dialog"))

        self._language = parent.language
        self._skin = parent.skin
        self._icon_directory = parent.icon_directory
        self._database = parent.database
        self._image_extensions = parent.image_extensions

        #===============================
        # Connect to the slot.
        #===============================
        self.btn_opn.clicked.connect(self.openDirectory)
        self.btn_chk_lbl.clicked.connect(self.getSample)
        self.chk_add_new.clicked.connect(self.setImportingType)

        # Define the return values.
        self.bbx_fto_res.accepted.connect(self.accept)
        self.bbx_fto_res.rejected.connect(self.reject)

        # Set skin for this UI.
        self.setSkin()

        # Set default setting
        self.chk_add_new.setChecked(True)
        self.tre_con.setEnabled(False)
        self.tre_con.setStyleSheet('background-color: #2C2C2C; border-color: #4C4C4C;')

    def setSkin(self):
        print("Start -> imagefileToObjectsDialog::setSkin(self, icon_path)")
        try:
            # Apply the new skin.
            skin.setSkin(self, self._icon_directory, skin=self._skin)
            skin.setText(self)

        except Exception as e:
            print("Error occured in imagefileToObjectsDialog::setSkin(self, icon_path)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

        finally:
            print("End -> imagefileToObjectsDialog::setSkin")

    def setImportingType(self):
        print("fileToObjectsDialog::setImportingType(self)")

        try:
            if self.chk_add_new.isChecked() == True:
                self.tre_con.setEnabled(False)
                self.tre_con.setStyleSheet('background-color: #2C2C2C; border-color: #4C4C4C;')

            else:
                self.tre_con.setEnabled(True)
                self.tre_con.setStyleSheet('background-color: #6C6C6C; border-color: #4C4C4C;')

        except Exception as e:
            print("Error occured in fileToObjectsDialog::setImportingType(self)")

            # Show the error message.
            error.ErrorMessageUnknown(details=str(e))

            # Return nothing.
            return(None)

    def getSample(self):
        print("fileToObjectsDialog::showSampleLine(self)")

        if self._sample == None: return(0)

        try:
            bgn = self.spn_pos_bgn.value()
            end = self.spn_pos_end.value()

            fl_nam = os.path.splitext(self._sample)[0]

            self.lbl_smpl_exmpl.setText(fl_nam[bgn:end])

        except Exception as e:
            print("Error occured in fileToObjectsDialog::showSampleLine(self)")

            # Show the error message.
            error.ErrorMessageUnknown(details=str(e))

            # Return nothing.
            return(None)
    def openDirectory(self):
        print("fileToObjectsDialog::openDirectory(self)")

        try:
            dir_fls = QFileDialog.getExistingDirectory(self, 'Select Folder')
            self.tbx_fnam.setText(dir_fls)

            if not dir_fls == None or not dir_fls == False:
                exts = None

                if self.cbx_ftyp.currentText() == "Image": exts = self._image_extensions

                # Get the file list with given path.
                fl_list = general.getFilesWithExtensionList(dir_fls, exts)

                # Get the first file as sample.
                if len(fl_list) > 0:
                    self._sample = fl_list[0]
                    self._importedFiles = fl_list

                    fl_nam = os.path.splitext(self._sample)[0]
                    self.spn_pos_end.setValue(len(fl_nam))

                    self.getSample()

        except Exception as e:
            print("Error occured in fileToObjectsDialog::openDirectory(self)")

            # Show the error message.
            error.ErrorMessageUnknown(details=str(e))

            # Return nothing.
            return(None)
