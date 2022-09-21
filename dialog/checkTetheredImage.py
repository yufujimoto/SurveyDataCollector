#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Import general libraries.
import sys, os, uuid, shutil

# Import PyQt5 libraries for generating the GUI application.
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Import general operations.
import modules.general as general
import modules.imageProcessing as imageProcessing

#import modules.skin as skin
import modules.setupCtdSkin as skin
import modules.error as error

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../viewer')
import viewer.imageViewer as viewer

import dialog.checkTetheredImageDialog as checkTetheredImageDialog

class CheckImageDialog(QDialog, checkTetheredImageDialog.Ui_tetheredDialog):
    # Properties for default paths.
    @property
    def language(self): return self._language
    @property
    def skin(self): return self._skin
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
    @property
    def label_consolidation(self): return self._label_consolidation
    @property
    def label_material(self): return self._label_material
    @property
    def qt_image(self): return self._qt_image
    @property
    def image_extensions(self): return self._image_extensions
    @property
    def raw_image_extensions(self): return self._raw_image_extensions
    @property
    def sound_extensions(self): return self._sound_extensions

    # Setter for default paths.
    @language.setter
    def language(self, value): self._language = value
    @skin.setter
    def skin(self, value): self._skin = value
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
    @label_consolidation.setter
    def label_consolidation(self, value): self._label_consolidation = value
    @label_material.setter
    def label_material(self, value): self._label_material = value
    @qt_image.setter
    def qt_image(self, value): self._qt_image = value
    @image_extensions.setter
    def image_extensions(self, value): self._image_extensions = value
    @raw_image_extensions.setter
    def raw_image_extensions(self, value): self._raw_image_extensions = value
    @sound_extensions.setter
    def sound_extensions(self, value): self._sound_extensions = value

    def __init__(self, parent=None, path=None):
        # Set the source directory which this program located.
        self._skin = parent.skin
        self._language = parent.language
        self._source_directory = parent.source_directory
        self._icon_directory = parent.icon_directory
        self._qt_image = parent.qt_image
        self._image_extensions = parent.image_extensions
        self._raw_image_extensions = parent.raw_image_extensions
        self._sound_extensions = parent.sound_extensions

        super(CheckImageDialog, self).__init__(parent)
        self.setupUi(self)

        # Create the graphic view item.
        self.graphicsView = viewer.ImageViewer()
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout_2.addWidget(self.graphicsView)

        # Initialize the window.
        self.setWindowTitle(self.tr("Check Tethered Image"))
        self.setWindowState(Qt.WindowMaximized)

        # Get the path of the tethered image.
        self.tethered = path

        # Define the return values.
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Initialyze the image info view.
        self.tre_img_info.setMaximumSize(QSize(600, 16777215))

        # Initialyze the file information view.
        self.lst_fls.setMaximumSize(QSize(16777215, 100))
        self.lst_fls.itemSelectionChanged.connect(self.getImageFileInfo)

        # Get tethered image files.
        self.getImageFiles()

        # Set the Skin for this dialog.
        self.setSkin(self._icon_directory)

    def setSkin(self, icon_path):
        print("Start -> textEditWithPhotoDialog::setSkin(self, icon_path)")
        try:
            # Apply the new skin.
            skin.setSkin(self, icon_path, skin=self._skin)
            #skin.setText(self)

        except Exception as e:
            print("Error occured in textEditWithPhotoDialog::setSkin(self, icon_path)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=parent.language)
            return(None)

        finally:
            print("End -> textEditWithPhotoDialog::setSkin")

    def getImageFiles(self):
        print("CheckImageDialog::getImageFiles(self)")

        try:
            # Get the file list with given path.
            img_lst_main = general.getFilesWithExtensionList(self.tethered, self._image_extensions)
            img_lst_raw = general.getFilesWithExtensionList(self.tethered, self._raw_image_extensions)

            # Count image files.
            img_cnt = 0

            # Add each image file name to the list box.
            if len(img_lst_main) > 0:
                for img_main in img_lst_main:
                    img_item = QListWidgetItem(img_main)
                    self.lst_fls.addItem(img_item)

                    # Increment the count of the image file.
                    img_cnt += 1

            # Add each RAW file name to the list box.
            if len(img_lst_raw) > 0:
                for img_raw in img_lst_raw:
                    img_item = QListWidgetItem(img_raw)
                    self.lst_fls.addItem(img_raw)

                    # Increment the count of the image file.
                    img_cnt += 1

            # Set the top item as the default.
            if img_cnt > 0: self.lst_fls.setCurrentRow(0)

            # Select the first file.
        except Exception as e:
            print("Error occured in CheckImageDialog::getImageFiles(self)")
            print(str(e))

    def getImageFileInfo(self):
        print("CheckImageDialog::getImageFileInfo(self)")

        try:
            # Get the path to the image directory of the tethered imagesw
            img_path = self.tethered

            # Get the selected image file.
            lst_fls = self.lst_fls.currentItem().text()

            # Get the file name which is currently selected.
            img_file_name = lst_fls

            # Make the full path of the selected image file.
            img_file_path = os.path.join(img_path,img_file_name)

            if os.path.exists(img_file_path):
                # Clear the image file information.
                self.tre_img_info.clear()

                # Get file information by using "dcraw" library.
                tags = imageProcessing.getMetaInfo(img_file_path)

                for tag in sorted(tags.keys()):
                        self.tre_img_info.addTopLevelItem(QTreeWidgetItem([str(tag), str(tags[tag])]))

                # Refresh the tree view.
                self.tre_img_info.show()

                # Show the preview
                self.showImage()

                # Adjust columns width.
                self.tre_img_info.resizeColumnToContents(0)
                self.tre_img_info.resizeColumnToContents(1)

            else:
                # Deselect the item.
                self.tre_img_info.clearSelection()
                self.tre_img_info.clear()
        except Exception as e:
            print("Error occured in CheckImageDialog::getImageFileInfo(self)")
            print(str(e))

    def showImage(self):
        print("CheckImageDialog::showImage(self)")

        try:
            if not self.lst_fls.currentItem() == None:
                # Get the file name and its path.
                img_file_name = self.lst_fls.currentItem().text()
                img_path = os.path.join(self.tethered, img_file_name)

                # Check the image file can be displayed directry.
                img_base, img_ext = os.path.splitext(img_file_name)
                img_valid = False

                for qt_ext in self._qt_image:
                    # Exit loop if extension is matched with Qt supported image.
                    if img_ext.lower() == qt_ext.lower():
                        img_valid = True
                        break

                # Check whether the image is Raw image or not.
                if not img_valid == True:
                    # Create error messages.
                    error_title = "プレビューに対応していません。"
                    error_msg = "このファイルはプレビューに対応していません。"
                    error_info = "プレビュー機能はJPEGにのみ対応しています。"
                    error_icon = QMessageBox.Critical
                    error_detailed = str(e)

                    # Handle error.
                    general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)

                    # Returns nothing.
                    return(None)

                if os.path.exists(img_path):
                    # Show the image on graphic view.
                    self.graphicsView.setFile(img_path)
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
            else:
                return(None)
        except Exception as e:
                print("Error occured in CheckImageDialog::showImage(self)")
                print(str(e))
