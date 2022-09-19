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
import modules.imageProcessing as imageProcessing
import modules.features as features
import modules.error as error

#import modules.skin as skin
import modules.setupIidSkin as skin

# Import camera and image processing library.
import modules.imageProcessing as imageProcessing
import dialog.imageInformationDialog as imageInformationDialog

# Import image viewer object.
import viewer.imageViewer as viewer

class imageInformationDialog(QDialog, imageInformationDialog.Ui_imageInformationDialog):
    @property
    def sop_file(self): return self._sop_file
    @property
    def source_directory(self): return self._source_directory
    @property
    def root_directory(self): return self._root_directory
    @property
    def language(self): return self._language
    @property
    def skin(self): return self._skin
    @property
    def icon_directory(self): return self._icon_directory
    @property
    def qt_image(self): return self._qt_image

    @sop_file.setter
    def sop_file(self, value): self._sop_file = value
    @source_directory.setter
    def source_directory(self, value): self._source_directory = value
    @root_directory.setter
    def root_directory(self, value): self._root_directory = value
    @language.setter
    def language(self, value): self._language = value
    @skin.setter
    def skin(self, value): self._skin = value
    @icon_directory.setter
    def icon_directory(self, value): self._icon_directory = value
    @qt_image.setter
    def qt_image(self, value): self._qt_image = value

    def __init__(self, parent=None, sop_file=None):
        # Get the path of the tethered image.
        self._sop_file = sop_file
        self._source_directory = parent.source_directory
        self._root_directory = parent.root_directory
        self._language = parent.language
        self._skin = parent.skin
        self._icon_directory = parent.icon_directory
        self._qt_image = parent.qt_image

        # Set the source directory which this program located.
        super(imageInformationDialog, self).__init__(parent)
        self.setupUi(self)

        # Initialize the window.
        self.setWindowTitle(self.tr("File Information Dialog"))

        #===============================
        # Connect to the slot.
        #===============================
        self.btn_fil_dt_cre_exif.clicked.connect(self.getCreateDateByExif)
        self.btn_fil_dt_mod_exif.clicked.connect(self.getModifiedDateByExif)
        self.tab_src.currentChanged.connect(self.toggleTab)

        # Define the return values.
        self.box_fil_ope.accepted.connect(self.accept)
        self.box_fil_ope.rejected.connect(self.reject)

        # Get the image properties from the instance.
        if self._sop_file.public == "1":
            self.cbx_fil_pub.setChecked(True)
        else:
            self.cbx_fil_pub.setChecked(False)

        if self._sop_file.lock == "1":
            self.cbx_fil_edit.setChecked(False)
            self.cbx_fil_edit.setDisabled(True)
        else:
            self.cbx_fil_edit.setChecked(True)
            self.cbx_fil_edit.setDisabled(False)

        # Set the alias name of the file object.
        self.tbx_fil_ali.setText(self._sop_file.alias)

        # Get the date of creation and modification.
        cdate = self._sop_file.created_date
        mdate = self._sop_file.modified_date

        # Set the maximum date if the given date is invalid.
        if (cdate == None or cdate == ""): cdate = "7999-12-31T23:59:59"
        if (mdate == None or mdate == ""): mdate = "7999-12-31T23:59:59"

        # Convert string date format to the PyQt date type.
        fil_dt_create = general.pyDateTimeToQDateTime(parse(cdate))
        fil_dt_modify = general.pyDateTimeToQDateTime(parse(mdate))

        # Set dates of creation and modification.
        self.dte_fil_dt_cre.setDateTime(fil_dt_create)
        self.dte_fil_dt_mod.setDateTime(fil_dt_modify)

        # Set the operating application software.
        self.tbx_fil_ope_app.setText(self._sop_file.operating_application)

        # Set the caption of the file object.
        self.tbx_fil_capt.setText(self._sop_file.caption)
        self.tbx_fil_dsc.setText(self._sop_file.description)

        # Set the status of the file object and optional values.
        self.cmb_fil_stts.addItem(self._sop_file.status)
        self.cmb_fil_stts.addItem("Original")
        self.cmb_fil_stts.addItem("Original(RAW)")
        self.cmb_fil_stts.addItem("Removed")
        self.cmb_fil_stts.addItem("Imported")
        self.cmb_fil_stts.addItem("Edited")

        if self._sop_file.file_type == "image":
            # Set the operation of the file object and option values.
            img_ope_list = parent.image_file_operation

            if self._sop_file.operation in img_ope_list:
                img_ope_list.remove(self._sop_file.operation)

            self.cmb_fil_eope.addItem(self._sop_file.operation)
            for img_ope in img_ope_list:
                self.cmb_fil_eope.addItem(img_ope)

            # Get the path from selected image object.
            img_file_path = os.path.join(parent.root_directory, self._sop_file.filename)

            if self.imageIsValid(img_file_path) == True:
                skin.setImageDataView(self)

                # Get the image file.
                self.showImage(img_file_path)

        # Set skin for this UI.
        self.setSkin()

    def setSkin(self):
        print("Start -> imageInformation::setSkin(self, icon_path)")
        try:
            # Apply the new skin.
            skin.setSkin(self, self._icon_directory, skin=self._skin)
            skin.setText(self)

        except Exception as e:
            print("Error occured in imageInformation::setSkin(self, icon_path)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

        finally:
            print("End -> imageInformation::setSkin")


    def toggleTab(self):
        print("information::toggleTab(self)")
        try:
            # Get the full path of the image.
            img_file_path = os.path.join(os.path.join(self._source_directory, "images"),"noimage.jpg")

            if os.path.exists(os.path.join(self._root_directory, self._sop_file.filename)):
                img_file_path = os.path.join(self._root_directory, self._sop_file.filename)

            # Get the currently selected tab name.
            current_tab = self.tab_src.currentIndex()

            if current_tab == 0: self.setViewer()
            elif current_tab ==1: self.showExif(img_file_path)

        except Exception as e:
            print(str(e))

    def showExif(self, img_file_path):
        print("imageInformationDialog::showImage(self)")

        self.tre_img_exif.clear()

        # Get file information by using "dcraw" library.
        tags = imageProcessing.getMetaInfo(img_file_path)

        for tag in sorted(tags.keys()):
            self.tre_img_exif.addTopLevelItem(QTreeWidgetItem([str(tag), str(tags[tag])]))

        # Refresh the tree view.
        self.tre_img_exif.show()

        # Adjust columns width.
        self.tre_img_exif.resizeColumnToContents(0)
        self.tre_img_exif.resizeColumnToContents(1)


    def showImage(self, img_file_path):
        print("imageInformationDialog::showImage(self)")

        try:
            # Check whether the image is Raw image or not.
            if not self.imageIsValid(img_file_path) == True:
                # Extract the thumbnail image from the RAW image by using "dcraw".
                imageProcessing.getThumbnail(img_file_path)

                # Get the extracted thumbnail image.
                img_file_path = os.path.splitext(img_file_path)[0] + ".thumb.jpg"

            self.graphicsView.setFile(img_file_path)

            # else:
            #     # Create error messages.
            #     error_title = "エラーが発生しました"
            #     error_msg = "このファイルはプレビューに対応していません。"
            #     error_info = "諦めてください。RAW + JPEG で撮影することをお勧めします。"
            #     error_icon = QMessageBox.Critical
            #     error_detailed = str(e)
            #
            #     # Handle error.
            #     general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
            #
            #     # Returns nothing.
            #     return(None)
        except Exception as e:
            print("Error occured in imageInformationDialog::showImage(self)")

            # Show the error message.
            error.ErrorMessageUnknown(details=str(e))

            # Return nothing.
            return(None)

    def setViewer(self):
        print("imageInformationDialog::setViewer(self)")

        try:
            # Get the full path of the image.
            if self._sop_file.filename == "":
                img_file_path = os.path.join(os.path.join(self._source_directory, "images"),"noimage.jpg")
            else:
                if not os.path.exists(os.path.join(self._root_directory, self._sop_file.filename)):
                    img_file_path = os.path.join(os.path.join(self._source_directory, "images"),"noimage.jpg")
                else:
                    img_file_path = os.path.join(self._root_directory, self._sop_file.filename)

            # Show the image on graphic view.
            self.graphicsView.setFile(img_file_path)

        except Exception as e:
            print("Error occured in imageInformationDialog::setViewer(self)")
            print(str(e))

            return(None)

    def imageIsValid(self, img_file_path):
        print("information::imageIsValid(self)")

        # Initialyze the value.
        img_valid = False

        # Check the image file can be displayed directry.
        img_base, img_ext = os.path.splitext(img_file_path)

        for qt_ext in self._qt_image:
            # Exit loop if extension is matched with Qt supported image.
            if img_ext.lower() == qt_ext.lower(): return(True)

        return(img_valid)

    def getCreateDateByExif(self):
        print("imageInformationDialog::getCreateDateByExif(self)")

        try:
            # Set dates of creation and modification.
            self.dte_fil_dt_cre.setDateTime(self.getOriginalTime())
        except Exception as e:
            print(str(e))

    def getModifiedDateByExif(self):
        print("imageInformationDialog::getModifiedDateByExif(self)")

        try:
            # Set dates of creation and modification.
            self.dte_fil_dt_mod.setDateTime(self.getOriginalTime())
        except Exception as e:
            print(str(e))

    def getOriginalTime(self):
        print("imageInformationDialog::getMetaInfo(self)")

        try:
            # Get the full path of the image.
            if self._sop_file.filename == "":
                img_file_path = os.path.join(os.path.join(parent.source_directory, "images"),"noimage.jpg")
            else:
                if not os.path.exists(os.path.join(parent.root_directory, self._sop_file.filename)):
                    img_file_path = os.path.join(os.path.join(parent.source_directory, "images"),"noimage.jpg")
                else:
                    img_file_path = os.path.join(parent.root_directory, self._sop_file.filename)

            # Open the image.
            img_object = open(img_file_path, 'rb')
            print("OK")
            # Get the exif entries.
            org_tags = exifread.process_file(img_object)

            # Parse the exif entries.
            for org_tag in sorted(org_tags.iterkeys()):
                if org_tag in ('EXIF DateTimeDigitized'):
                    # Split the tag value with a space.
                    value = str(org_tags[org_tag]).split(" ")

                    # Convert the text format.
                    date = value[0].replace(":", "-")
                    time = value[1]

                    print(str(date) + "T" + str(time))

                    # Convert the python date time to QDateTime.
                    exif_date = general.pyDateTimeToQDateTime(parse(str(date) + "T" + str(time)))

                    # Return the result.
                    return(exif_date)

                    # Exit the roop.
                    break

        except Exception as e:
            print("Error occured in imageProcessing::getMetaInfo(img_input)")
            print(str(e))

            return(None)
