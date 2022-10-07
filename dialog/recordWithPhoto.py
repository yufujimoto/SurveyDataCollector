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
import objects.features as features
import modules.error as error

# Import camera and image processing library.
import modules.imageProcessing as imageProcessing
import modules.setupRwpSkin as skin

import dialog.recordWithPhotoDialog as recordWithPhotoDialog

# Import libraries for sound recording.
import queue
import sounddevice as sd
import soundfile as sf
import numpy as np

import viewer.imageViewer as viewer

class RecordThreading(QThread):
    def __init__(self, parent, path):
        QThread.__init__(self)

        self.parent = parent
        self.path_snd = path

    def __del__(self):
        self.wait()

    def stop(self):
        self.terminate()

    def run(self):
        print("Start -> recordWithPhoto::run(self)")
        try:
            # Set the unique identifier for the sound data.
            snd_uuid = str(uuid.uuid4())

            # Set the sound file parameters.
            subtype = "PCM_24"
            channels = 2
            device_info = sd.query_devices(None, 'input')
            samplerate = 48000  #samplerate = int(device_info['default_samplerate'])

            # Give the original file name by using uuid of the sound file.
            filename = tempfile.mktemp(prefix=snd_uuid, suffix='.wav', dir=self.path_snd)

            # Set the Queue for the threading.
            q = queue.Queue()

            def callback(indata, frames, time, status):
                """This is called (from a separate thread) for each audio block."""
                if status:
                    print(status, sys.stderr)
                q.put(indata.copy())

            # Make sure the file is opened before recording anything:
            with sf.SoundFile(filename, mode='x', samplerate=samplerate, channels=channels, subtype=subtype) as file:
                with sd.InputStream(samplerate=samplerate, device=None, channels=channels, callback=callback):
                    while True:
                        # Get input signals and put to file.
                        value = q.get()
                        file.write(value)

                        # Visualize input signals.
                        try:
                            l, r = np.nan_to_num(value.mean(axis=0))

                            l = int(np.absolute(l)*10000)
                            r = int(np.absolute(r)*10000)

                            if int(math.fabs(l)) >= 1: self.parent.pbr_l.setValue(int(l))
                            if int(math.fabs(r)) >= 1: self.parent.pbr_r.setValue(int(r))
                        except:
                            pass
        except Exception as e:
            print(type(e).__name__ + ': ' + str(e))
        finally:
            print("End -> recordWithPhoto::run")


class RecordWithImage(QDialog, recordWithPhotoDialog.Ui_testDialog):
    # Default paths.
    @property
    def source_directory(self): return self._source_directory
    @property
    def icon_directory(self): return self._icon_directory
    @property
    def root_directory(self): return self._root_directory
    @property
    def language(self): return self._language
    @property
    def skin(self): return self._skin
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
    @language.setter
    def language(self, value): self._language = value
    @skin.setter
    def skin(self, value): self._skin = value
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
        super(RecordWithImage, self).__init__(parent)
        self.setupUi(self)

        # Set the source directory which this program located.
        self._source_directory = parent.source_directory
        self._icon_directory = parent.icon_directory
        self._language = parent.language
        self._skin = parent.skin
        self._qt_image = parent.qt_image
        self._image_extensions = parent.image_extensions
        self._sound_extensions = parent.sound_extensions

        # Get the path of the tethered image.
        self.path_img = img_path
        self.path_snd = snd_path

        # Initialize the window.
        self.setWindowTitle(self.tr("Record Sound with Photo"))
        self.setWindowState(Qt.WindowMaximized)



        # Create the graphic view item.
        self.graphicsView = viewer.ImageViewer()
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)

        # Initialyze the thumbnail selector.
        # Initialyze the list view of the thumbnails.
        self.lst_img_icon.setIconSize(QSize(200,200))
        self.lst_img_icon.setMovement(QListView.Static)
        self.lst_img_icon.setModel(QStandardItemModel())

        # Create recording thread.
        self.recThread = RecordThreading(parent=self, path=self.path_snd)

        #===============================
        # Connect to the slot.
        #===============================
        self.btn_rec_start.clicked.connect(self.startRecording)
        self.btn_rec_stop.clicked.connect(self.stopRecording)

        self.lst_img_icon.selectionModel().selectionChanged.connect(self.showImage)

        # Define the return values.
        self.bbx_rec_pht.accepted.connect(self.accept)
        self.bbx_rec_pht.rejected.connect(self.reject)

        # Get tethered image files.
        self.getImageFiles()
        self.getSoundFiles()

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

    def startRecording(self):
        print("recordWithPhoto::startRecording(self)")

        try:
            # Change the icon color black to red.
            self.btn_rec_start.setIcon(QIcon(QPixmap(os.path.join(self._icon_directory, 'recording.png'))))

            # Start the recording thread.
            self.recThread.start()

            # Stop the threading.
            self.btn_rec_stop.clicked.connect(self.stopRecording)
        except Exception as e:
            self.btn_rec_start.setIcon(QIcon(QPixmap(os.path.join(self._icon_directory, 'record.png'))))
            print("Error in RecordWithImage::recording(self)")
            print(str(e))

    def stopRecording(self):
        print("RecordWithImage::stopRecording(self)")

        try:
            # Change the icon color red to black.
            self.btn_rec_start.setIcon(QIcon(QPixmap(os.path.join(self._icon_directory, 'record.png'))))

            # Stop recording threading.
            self.recThread.stop()

            self.pbr_r.setValue(0)
            self.pbr_l.setValue(0)

            # Refresh temporal sound data.
            self.getSoundFiles()
        except Exception as e:
            print("Error in RecordWithImage::stopRecording(self)")
            print(str(e))

    def getSoundFiles(self):
        print("recordWithPhoto::getSoundFiles")

        try:
            # Clear itmes if exists.
            self.lst_snd_fls.clear()

            # Get the file list with given path.
            snd_lst = general.getFilesWithExtensionList(self.path_snd, self._sound_extensions)

            # Add each image file name to the list box.
            if len(snd_lst) > 0:
                for snd_fl in snd_lst:
                    snd_item = QListWidgetItem(snd_fl)
                    self.lst_snd_fls.addItem(snd_item)
        except Exception as e:
            print("Error in RecordWithImage::getSoundFiles")
            print(str(e))

    def getImageFiles(self):
        print("recordWithPhoto::getImageFiles(self)")

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
