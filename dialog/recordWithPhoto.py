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
    def __init__(self, parent=None, img_path=None, snd_path=None):
        # Set the source directory which this program located.
        self._source_directory = parent.source_directory
        self._icon_directory = parent.icon_directory
        self._qt_image = parent.qt_image
        self._image_extensions = parent.image_extensions
        self._raw_image_extensions = parent.raw_image_extensions
        self._sound_extensions = parent.sound_extensions
        
        super(RecordWithImage, self).__init__(parent)
        self.setupUi(self)
        
        # Initialize the window.
        self.setWindowTitle(self.tr("Check Tethered Image"))
        self.setWindowState(Qt.WindowMaximized)
        
        # Get the path of the tethered image.
        self.path_img = img_path
        self.path_snd = snd_path
        
        # Initialyze the play button.
        self.btn_play.setIcon(QIcon(QPixmap(os.path.join(self._icon_directory, 'ic_play_circle_filled_black_24dp_1x.png'))))
        self.btn_play.setIconSize(QSize(24,24))
        self.btn_play.clicked.connect(self.startPlaying)
        
        # Initialyze the record button.
        self.btn_rec_start.setIcon(QIcon(QPixmap(os.path.join(self._icon_directory, 'ic_fiber_manual_record_black_24dp_1x.png'))))
        self.btn_rec_start.setIconSize(QSize(24,24))
        self.btn_rec_start.clicked.connect(self.startRecording)
        
        # Initialyze the stop button.
        self.btn_rec_stop.setIcon(QIcon(QPixmap(os.path.join(self._icon_directory, 'ic_pause_circle_filled_black_24dp_1x.png'))))
        self.btn_rec_stop.setIconSize(QSize(24,24))
        
        # Define the return values.
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        # Initialyze the image panel.
        self.image_panel.resize(800, 600)
        self.image_panel.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        
        # Initialyze the file information view.
        self.lst_snd_fls.setMaximumSize(QSize(16777215, 100))
        self.lst_img_fls.setMaximumSize(QSize(16777215, 100))
        self.lst_img_fls.itemSelectionChanged.connect(self.showImage)
        
        # Get tethered image files.
        self.getImageFiles()
        self.getSoundFiles()
        
        #========================================
        # Initialyze objects for Sound recorder
        #========================================
        self.recThread = RecordThreading(self.path_snd)
    
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
    
    # Default labels.
    @property
    def label_consolidation(self): return self._label_consolidation
    @property
    def label_material(self): return self._label_material
    
    # Default extensions.
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
    
    def startRecording(self):
        try:
            # Change the icon color black to red.
            self.btn_rec_start.setIcon(QIcon(QPixmap(os.path.join(self._icon_directory, 'ic_fiber_manual_record_red_24dp_1x.png'))))
            
            # Start the recording thread.
            self.recThread.start()
            
            # Stop the threading.
            self.btn_rec_stop.clicked.connect(self.stopRecording)
        except Exception as e:
            self.btn_rec_start.setIcon(QIcon(QPixmap(os.path.join(self._icon_directory, 'ic_fiber_manual_record_black_24dp_1x.png'))))
            print("Error in RecordWithImage::recording(self)")
    
    def startPlaying(self):
        try:
            # Get the path to the sound path.
            if not self.lst_snd_fls.currentItem() == None:
                snd_file_name = self.lst_snd_fls.currentItem().text()
                snd_path = os.path.join(self.path_snd, snd_file_name)
            
            # Change the icon color black to green.
            self.btn_play.setIcon(QIcon(QPixmap(os.path.join(self._icon_directory, 'ic_play_circle_filled_green_24dp_1x.png'))))
            
            # Start the playing thread.
            data, fs = sf.read(snd_path, dtype='float32')
            sd.play(data, fs)
            
            self.btn_rec_stop.clicked.connect(self.stopPlaying)
        except Exception as e:
            self.btn_play.setIcon(QIcon(QPixmap(os.path.join(self._icon_directory, 'ic_play_circle_filled_black_24dp_1x.png'))))
            print("Error in RecordWithImage::playing(self)")
    
    def stopRecording(self):
        print("RecordWithImage::stopRecording(self)")
        
        try:
            # Change the icon color red to black.
            self.btn_rec_start.setIcon(QIcon(QPixmap(os.path.join(self._icon_directory, 'ic_fiber_manual_record_black_24dp_1x.png'))))
            
            # Stop recording threading.
            self.recThread.stop()
            
            # Refresh temporal sound data.
            self.getSoundFiles()
        except Exception as e:
            print("Error in RecordWithImage::stopRecording(self)")
    
    def stopPlaying(self):
        try:
            # Change the icon color green to black.
            self.btn_play.setIcon(QIcon(QPixmap(os.path.join(self._icon_directory, 'ic_play_circle_filled_black_24dp_1x.png'))))
            
            # Stop audio.
            sd.stop()        
        except Error as e:
            print("Error in RecordWithImage::stopping(self)")
        
    def getSoundFiles(self):
        self.lst_snd_fls.clear()
        
        # Get the file list with given path.
        snd_lst = general.getFilesWithExtensionList(self.path_snd, self._sound_extensions)
        
        # Add each image file name to the list box.
        if snd_lst > 0:
            for snd_fl in snd_lst:
                snd_item = QListWidgetItem(snd_fl)
                self.lst_snd_fls.addItem(snd_item)
    
    def getImageFiles(self):
        try:
            # Get the file list with given path.
            img_lst_main = general.getFilesWithExtensionList(self.path_img, self._image_extensions)
            img_lst_raw = general.getFilesWithExtensionList(self.path_img, self._raw_image_extensions)
            
            # Add each image file name to the list box.
            if img_lst_main > 0:
                for img_main in img_lst_main:
                    img_item = QListWidgetItem(img_main)
                    self.lst_img_fls.addItem(img_item)
            
            # Add each RAW file name to the list box.
            if img_lst_raw > 0:
                for img_raw in img_lst_raw:
                    img_item = QListWidgetItem(img_raw)
                    self.lst_img_fls.addItem(img_raw)
        except Exception as e:
            print("Error in RecordWithImage::getImageFiles(self)")
    
    def showImage(self):
        panel_w = self.image_panel.width()
        panel_h = self.image_panel.height()
        
        if not self.lst_img_fls.currentItem() == None:
            # Get the file name and its path.
            img_file_name = self.lst_img_fls.currentItem().text()
            img_path = os.path.join(self.path_img, img_file_name)
            
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
                # Extract the thumbnail image from the RAW image by using "dcraw".
                imageProcessing.getThumbnail(img_path)
                
                # Get the extracted thumbnail image.
                img_file_name = img_base + ".thumb.jpg"
                
                # Get the full path of the thumbnail image.
                img_path = os.path.join(self.tethered, img_file_name)
            
            if os.path.exists(img_path):
                # Create the container for displaying the image
                org_pixmap = QPixmap(img_path)
                scl_pixmap = org_pixmap.scaled(panel_w, panel_h, Qt.KeepAspectRatio)
                
                # Set the image file to the image view container.
                self.image_panel.setPixmap(scl_pixmap)
                
                # Show the selected image.
                self.image_panel.show()
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
