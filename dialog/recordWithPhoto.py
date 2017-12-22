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
import dialog.recordWithPhotoDialog as recordWithPhotoDialog

# Import libraries for sound recording. 
import Queue as queue
import sounddevice as sd
import soundfile as sf

import viewer.imageViewer as viewer

class RecordThreading(QThread):
    def __init__(self, path):
        QThread.__init__(self)
        self.path_snd = path

    def __del__(self):
        self.wait()
    
    def stop(self):
        self.terminate()

    def run(self):
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
                        file.write(q.get())
        except Exception as e:
            print(type(e).__name__ + ': ' + str(e))

class RecordWithImage(QDialog, recordWithPhotoDialog.Ui_testDialog):
    # Default paths.
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
    
    def __init__(self, parent=None, img_path=None, snd_path=None):
        # Initialyze super class and set up this.
        super(RecordWithImage, self).__init__(parent)
        self.setupUi(self)
        
        # Set the source directory which this program located.
        self._source_directory = parent.source_directory
        self._icon_directory = parent.icon_directory
        self._qt_image = parent.qt_image
        self._image_extensions = parent.image_extensions
        self._raw_image_extensions = parent.raw_image_extensions
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
        
        # Initialyze the play button.
        self.btn_play.setIcon(QIcon(QPixmap(os.path.join(self._icon_directory, 'play.png'))))
        self.btn_play.setIconSize(QSize(24,24))
        self.btn_play.clicked.connect(self.startPlaying)
        
        # Initialyze the record button.
        self.btn_rec_start.setIcon(QIcon(QPixmap(os.path.join(self._icon_directory, 'record.png'))))
        self.btn_rec_start.setIconSize(QSize(24,24))
        self.btn_rec_start.clicked.connect(self.startRecording)
        
        # Initialyze the stop button.
        self.btn_rec_stop.setIcon(QIcon(QPixmap(os.path.join(self._icon_directory, 'pause.png'))))
        self.btn_rec_stop.setIconSize(QSize(24,24))
        
        # Define the return values.
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        # Create the graphic view item.        
        self.graphicsView = viewer.ImageViewer()
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)
        
        # Get the path of the tethered image.
        self.path_img = img_path
        self.path_snd = snd_path
        
        # Initialyze the thumbnail selector.
        self.lst_img_icon.selectionModel().selectionChanged.connect(self.showImage)
        
        # Create recording thread.
        self.recThread = RecordThreading(self.path_snd)
        
        # Get tethered image files.
        self.getImageFiles()
        self.getSoundFiles()   
        
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
    
    def startPlaying(self):
        print("recordWithPhoto::startPlaying(self)")
        
        try:
            # Get the path to the sound path.
            if not self.lst_snd_fls.currentItem() == None:
                snd_file_name = self.lst_snd_fls.currentItem().text()
                snd_path = os.path.join(self.path_snd, snd_file_name)
            
            # Change the icon color black to green.
            self.btn_play.setIcon(QIcon(QPixmap(os.path.join(self._icon_directory, 'playing.png'))))
            
            # Start the playing thread.
            data, fs = sf.read(snd_path, dtype='float32')
            sd.play(data, fs)
            
            self.btn_rec_stop.clicked.connect(self.stopPlaying)
        except Exception as e:
            self.btn_play.setIcon(QIcon(QPixmap(os.path.join(self._icon_directory, 'play.png'))))
            print("Error in RecordWithImage::playing(self)")
            print(str(e))
            
    def stopRecording(self):
        print("RecordWithImage::stopRecording(self)")
        
        try:
            # Change the icon color red to black.
            self.btn_rec_start.setIcon(QIcon(QPixmap(os.path.join(self._icon_directory, 'record.png'))))
            
            # Stop recording threading.
            self.recThread.stop()
            
            # Refresh temporal sound data.
            self.getSoundFiles()
        except Exception as e:
            print("Error in RecordWithImage::stopRecording(self)")
            print(str(e))
    
    def stopPlaying(self):
        print("RecordWithImage::stopPlaying(self)")
        
        try:
            # Change the icon color green to black.
            self.btn_play.setIcon(QIcon(QPixmap(os.path.join(self._icon_directory, 'play.png'))))
            
            # Stop audio.
            sd.stop()        
        except Exception as e:
            print("Error in RecordWithImage::stopping(self)")
            print(str(e))
    
    def getSoundFiles(self):
        print("recordWithPhoto::getSoundFiles")
        
        try:
            # Clear itmes if exists.
            self.lst_snd_fls.clear()
            
            # Get the file list with given path.
            snd_lst = general.getFilesWithExtensionList(self.path_snd, self._sound_extensions)
            
            # Add each image file name to the list box.
            if snd_lst > 0:
                for snd_fl in snd_lst:
                    snd_item = QListWidgetItem(snd_fl)
                    self.lst_snd_fls.addItem(snd_item)
        except Exception as e:
            print("Error in RecordWithImage::stopping(self)")
            print(str(e))
    
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