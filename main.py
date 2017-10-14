#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Import general libraries.
import sys, os, uuid, shutil, time, math, tempfile, logging, pyexiv2, datetime

# Import the library for acquiring file information.
from stat import *

# Import PyQt5 libraries for generating the GUI application.
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QThread, pyqtSignal

# Import DB libraries
import sqlite3 as sqlite
from sqlite3 import Error

# Import general operations.
import modules.general as general
import modules.features as features

# Import GUI window.
import modules.mainWindow as mainWindow
import modules.checkTetheredImageDialog as checkTetheredImageDialog
import modules.recordWithPhotoDialog as recordWithPhotoDialog

# Import camera and image processing library.
import modules.imageProcessing as imageProcessing

# Import libraries for sound recording. 
import Queue as queue
import sounddevice as sd
import soundfile as sf

# Define the default path.
SRC_DIR = None
ICN_DIR = None
TMP_DIR = None
ROOT_DIR = None
TABLE_DIR = None
CON_DIR = None

DATABASE = None
TETHERED = None
IMGPROC = None

# Define the equipments.
CAMERA = None

# Labels for Consolidation and Material
LAB_CON = u"統合体"
LAB_MAT = u"資料"

# Define the default extensions.
QT_IMG = [".BMP", ".GIF", ".JPG", ".JPEG", ".PNG", ".PBM", ".PGM", ".PPM", ".XBM", ".XPM"]
IMG_EXT = [".JPG", ".TIF", ".JPEG", ".TIFF", ".PNG", ".JP2", ".J2K", ".JPF", ".JPX", ".JPM"]
RAW_EXT = [".RAW", ".ARW"]
SND_EXT = [".WAV"]

# Connected devices.
CUR_CAM = None

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
        # Get the root directory for this script.
        global SRC_DIR
        global TMP_DIR
        global ICN_DIR
        
        # Set the source directory which this program located.
        SRC_DIR = os.path.dirname(os.path.abspath(__file__))
        ICN_DIR = os.path.join(SRC_DIR, "icon")
        
        super(RecordWithImage, self).__init__(parent)
        self.setupUi(self)
        
        # Initialize the window.
        self.setWindowTitle(self.tr("Check Tethered Image"))
        self.setWindowState(Qt.WindowMaximized)
        
        # Get the path of the tethered image.
        self.path_img = img_path
        self.path_snd = snd_path
        
        # Initialyze the play button.
        self.btn_play.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_play_circle_filled_black_24dp_1x.png'))))
        self.btn_play.setIconSize(QSize(24,24))
        self.btn_play.clicked.connect(self.startPlaying)
        
        # Initialyze the record button.
        self.btn_rec_start.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_fiber_manual_record_black_24dp_1x.png'))))
        self.btn_rec_start.setIconSize(QSize(24,24))
        self.btn_rec_start.clicked.connect(self.startRecording)
        
        # Initialyze the stop button.
        self.btn_rec_stop.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_pause_circle_filled_black_24dp_1x.png'))))
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
    
    def startRecording(self):
        try:
            # Change the icon color black to red.
            self.btn_rec_start.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_fiber_manual_record_red_24dp_1x.png'))))
            
            # Start the recording thread.
            self.recThread.start()
            
            # Stop the threading.
            self.btn_rec_stop.clicked.connect(self.stopRecording)
        except:
            self.btn_rec_start.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_fiber_manual_record_black_24dp_1x.png'))))
            print("Error in RecordWithImage::recording(self)")
    
    def startPlaying(self):
        try:
            # Get the path to the sound path.
            if not self.lst_snd_fls.currentItem() == None:
                snd_file_name = self.lst_snd_fls.currentItem().text()
                snd_path = os.path.join(self.path_snd, snd_file_name)
            
            # Change the icon color black to green.
            self.btn_play.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_play_circle_filled_green_24dp_1x.png'))))
            
            # Start the playing thread.
            data, fs = sf.read(snd_path, dtype='float32')
            sd.play(data, fs)
            
            self.btn_rec_stop.clicked.connect(self.stopPlaying)
        except:
            self.btn_play.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_play_circle_filled_black_24dp_1x.png'))))
            print("Error in RecordWithImage::playing(self)")
    
    def stopRecording(self):
        print("RecordWithImage::stopRecording(self)")
        
        try:
            # Change the icon color red to black.
            self.btn_rec_start.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_fiber_manual_record_black_24dp_1x.png'))))
            
            # Stop recording threading.
            self.recThread.stop()
            
            # Refresh temporal sound data.
            self.getSoundFiles()
        except:
            print("Error in RecordWithImage::stopRecording(self)")
    
    def stopPlaying(self):
        try:
            # Change the icon color green to black.
            self.btn_play.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_play_circle_filled_black_24dp_1x.png'))))
            
            # Stop audio.
            sd.stop()        
        except:
            print("Error in RecordWithImage::stopping(self)")
        
    def getSoundFiles(self):
        global SND_EXT
        self.lst_snd_fls.clear()
        
        # Get the file list with given path.
        snd_lst = general.getFilesWithExtensionList(self.path_snd, SND_EXT)
        
        # Add each image file name to the list box.
        if snd_lst > 0:
            for snd_fl in snd_lst:
                snd_item = QListWidgetItem(snd_fl)
                self.lst_snd_fls.addItem(snd_item)
    
    def getImageFiles(self):
        global IMG_EXT
        global RAW_EXT
        
        # Get the file list with given path.
        img_lst_main = general.getFilesWithExtensionList(self.path_img, IMG_EXT)
        img_lst_raw = general.getFilesWithExtensionList(self.path_img, RAW_EXT)
        
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
            
            for qt_ext in QT_IMG:
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
                error_detailed = None
                
                # Handle error.
                general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
                
                # Returns nothing.
                return(None)
        else:
            return(None)

class CheckImageDialog(QDialog, checkTetheredImageDialog.Ui_tetheredDialog):
    def __init__(self, parent=None, path=None):
        super(CheckImageDialog, self).__init__(parent)
        self.setupUi(self)
        
        # Initialize the window.
        self.setWindowTitle(self.tr("Check Tethered Image"))
        self.setWindowState(Qt.WindowMaximized)
        
        # Get the path of the tethered image.
        self.tethered = path
        
        # Define the return values.
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        # Initialyze the image panel.
        self.image_panel.resize(800, 600)
        self.image_panel.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        
        # Initialyze the image info view.
        self.tre_img_info.setMaximumSize(QSize(300, 16777215))
        
        # Initialyze the file information view.
        self.lst_fls.setMaximumSize(QSize(16777215, 100))
        self.lst_fls.itemSelectionChanged.connect(self.getImageFileInfo)
        
        # Get tethered image files.
        self.getImageFiles()
        
    def getImageFiles(self):
        global IMG_EXT
        global RAW_EXT
        
        # Get the file list with given path.
        img_lst_main = general.getFilesWithExtensionList(self.tethered, IMG_EXT)
        img_lst_raw = general.getFilesWithExtensionList(self.tethered, RAW_EXT)
        
        # Add each image file name to the list box.
        if img_lst_main > 0:
            for img_main in img_lst_main:
                img_item = QListWidgetItem(img_main)
                self.lst_fls.addItem(img_item)
                
        # Add each RAW file name to the list box.
        if img_lst_raw > 0:
            for img_raw in img_lst_raw:
                img_item = QListWidgetItem(img_raw)
                self.lst_fls.addItem(img_raw)
    
    def getImageFileInfo(self):
        # Get the path to the image directory of the tethered imagesw
        img_path = self.tethered
        
        # Get the tree view for the metadata of consolidation.
        tre_fl = self.tre_img_info
        
        # Get the selected image file.
        lst_fls = self.lst_fls.currentItem().text()
        
        # Get the file name which is currently selected.
        img_file_name = lst_fls
        
        # Make the full path of the selected image file.
        img_file_path = os.path.join(img_path,img_file_name)
        
        if os.path.exists(img_file_path):
            # Clear the image file information.
            tre_fl.clear()
            
            # Get file information by using "dcraw" library.
            img_stat = imageProcessing.getMetaInfo(img_file_path).strip().split("\n")
            
            # Get each metadata entry.
            for entry in img_stat:
                # Split metadata entry by ":".
                entry_line = entry.split(":")
                
                # Get the metadata key.
                entry_key = entry_line[0]
                
                # Get the metadata value.
                entry_val = entry_line[1]
                
                # Add file information to the tree list.
                tre_fl.addTopLevelItem(QTreeWidgetItem([entry_key, entry_val]))
            
            # Get file information by using python "stat" library.
            fl_stat = os.stat(img_file_path)
            
            # Get file size.
            fl_size = str(round(float(fl_stat[ST_SIZE]/1000),3))+"KB"
            
            # Get time for last access, modified and creat.
            fl_time_last = time.asctime(time.localtime(fl_stat[ST_ATIME]))
            fl_time_mod = time.asctime(time.localtime(fl_stat[ST_MTIME]))
            fl_time_cre = time.asctime(time.localtime(fl_stat[ST_CTIME]))
            
            # Add file information to the tree list.
            tre_fl.addTopLevelItem(QTreeWidgetItem(["Created", fl_time_cre]))
            tre_fl.addTopLevelItem(QTreeWidgetItem(["Last Modified", fl_time_mod]))
            tre_fl.addTopLevelItem(QTreeWidgetItem(["Last Access", fl_time_last]))
            tre_fl.addTopLevelItem(QTreeWidgetItem(["File Size", fl_size]))
            
            # Refresh the tree view.
            tre_fl.show()
            self.showImage()
        else:
            # Deselect the item.
            tre_fl.clearSelection()
            tre_fl.clear()
    
    def showImage(self):
        panel_w = self.image_panel.width()
        panel_h = self.image_panel.height()
        
        if not self.lst_fls.currentItem() == None:
            # Get the file name and its path.
            img_file_name = self.lst_fls.currentItem().text()
            img_path = os.path.join(self.tethered, img_file_name)
            
            # Check the image file can be displayed directry.
            img_base, img_ext = os.path.splitext(img_file_name)
            img_valid = False
            
            for qt_ext in QT_IMG:
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
                error_detailed = None
                
                # Handle error.
                general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
                
                # Returns nothing.
                return(None)
        else:
            return(None)

class mainPanel(QMainWindow, mainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        # Get the root directory for this script.
        global SRC_DIR
        global TMP_DIR
        
        # Set the source directory which this program located.
        SRC_DIR = os.path.dirname(os.path.abspath(__file__))
        
        # Create temporal directory.
        TMP_DIR = os.path.join(SRC_DIR, "temp")
        
        # Initialyze the temporal directory.
        if not os.path.exists(TMP_DIR):
            # Create the temporal directory if not exists.
            os.mkdir(TMP_DIR)
        else:
            # Delete the existing temporal directory before create.
            shutil.rmtree(TMP_DIR)
            os.mkdir(TMP_DIR)
        
        # Define icon path.
        ICN_DIR = os.path.join(SRC_DIR, "icon")
        
        # Make this class as the super class and initialyze the class.
        super(mainPanel, self).__init__(parent)
        self.setupUi(self)
        
        # Initialyze the window.
        self.setWindowState(Qt.WindowMaximized)     # Show as maximized.
        
        #========================================
        # Initialyze objects for project
        #========================================
        self.bar_menu.setNativeMenuBar(False)
        self.act_prj_open.triggered.connect(self.getTheRootDirectory)
        self.act_prj_open.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_folder_open_black_24dp_1x.png'))))
        
        
        self.act_export_html.triggered.connect(self.exportAsHtml)
        
        
        # Handle current selection of consolidations and materials.
        self.tre_prj_item.itemSelectionChanged.connect(self.toggleSelectedItem)
        
        # Activate the tab for grouping manupilating consolidations and materials.
        self.tab_target.setTabIcon(0, QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_apps_black_24dp_1x.png'))))
        self.tab_target.setTabIcon(1, QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_insert_photo_black_24dp_1x.png'))))
        self.tab_target.currentChanged.connect(self.toggleCurrentObject)
        
        # Activate the tab for grouping manupilating consolidations and materials.
        self.tab_control.setTabIcon(0, QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_view_list_black_24dp_1x.png'))))
        self.tab_control.setTabIcon(1, QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_add_a_photo_black_24dp_1x.png'))))
        self.tab_control.setCurrentIndex(0)
        
        #========================================
        # Initialyze objects for consolidation
        #========================================
        # Activate the adding a consolidation button.
        self.btn_con_add.clicked.connect(self.addConsolidation)
        self.btn_con_add.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_add_box_black_24dp_1x.png'))))
        self.btn_con_add.setIconSize(QSize(24,24))
        
        # Activate the updating the selected consolidation button.
        self.btn_con_update.clicked.connect(self.updateConsolidation)
        self.btn_con_update.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_check_box_black_24dp_1x.png'))))
        self.btn_con_update.setIconSize(QSize(24,24))
        
        # Activate the deleting the selected consolidation button.
        self.btn_con_del.clicked.connect(self.deleteConsolidation)
        self.btn_con_del.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_indeterminate_check_box_black_24dp_1x.png'))))
        self.btn_con_del.setIconSize(QSize(24,24))
        
        # Activate the taking a image of the consolidation button.
        self.btn_con_take.clicked.connect(self.tetheredShooting)
        self.btn_con_take.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_local_see_black_24dp_1x.png'))))
        self.btn_con_take.setIconSize(QSize(24,24))
        
        # Activate the opening recording dialog button.
        self.btn_con_rec.clicked.connect(self.recordWithPhoto)
        self.btn_con_rec.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_keyboard_voice_black_24dp_1x.png'))))
        self.btn_con_rec.setIconSize(QSize(24,24))
        
        # Activate operation mode selecting button.
        self.grp_con_ope = QButtonGroup()
        self.grp_con_ope.addButton(self.rad_con_new, 0)
        self.grp_con_ope.addButton(self.rad_con_mod, 1)
        self.grp_con_ope.buttonClicked.connect(self.toggleEditModeForConsolidation)
        
        # Initialyze the edit consolidation mode as modifying.
        self.rad_con_mod.setChecked(True)
        self.toggleEditModeForConsolidation()
        
        #========================================
        # Initialyze objects for materials
        #========================================
        
        # Activate the adding a material button.
        self.btn_mat_add.clicked.connect(self.addMaterial)
        self.btn_mat_add.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_add_circle_black_24dp_1x.png'))))
        self.btn_mat_add.setIconSize(QSize(24,24))
        
        # Activate the updating the selected material button.
        self.btn_mat_update.clicked.connect(self.updateMaterial)
        self.btn_mat_update.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_check_circle_black_24dp_1x.png'))))
        self.btn_mat_update.setIconSize(QSize(24,24))
        
        # Activate the consolidation delete button.
        self.btn_mat_del.clicked.connect(self.deleteMaterial)
        self.btn_mat_del.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_remove_circle_black_24dp_1x.png'))))
        self.btn_mat_del.setIconSize(QSize(24,24))
        
        # Activate the taking a image of the material button.
        self.btn_mat_take.clicked.connect(self.tetheredShooting)
        self.btn_mat_take.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_local_see_black_24dp_1x.png'))))
        self.btn_mat_take.setIconSize(QSize(24,24))
        
        # Activate the opening recording dialog button.
        self.btn_mat_rec.clicked.connect(self.recordWithPhoto)
        self.btn_mat_rec.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_keyboard_voice_black_24dp_1x.png'))))
        self.btn_mat_rec.setIconSize(QSize(24,24))
        
        # Activate selecting operation mode button.
        self.grp_mat_ope = QButtonGroup()
        self.grp_mat_ope.addButton(self.rad_mat_new, 0)
        self.grp_mat_ope.addButton(self.rad_mat_mod, 1)
        self.grp_mat_ope.buttonClicked.connect(self.toggleEditModeForMaterial)
        
        # Initialyze the edit material mode as modifying.
        self.rad_mat_mod.setChecked(True)
        
        #========================================
        # Initialyze objects for file
        #========================================
        # Handle current selection of consolidations and materials.
        self.tre_fls.itemSelectionChanged.connect(self.toggleSelectedFile)
        
        self.tab_src.setTabIcon(0, QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_collections_black_24dp_1x.png'))))
        self.tab_src.setTabIcon(1, QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_library_music_black_24dp_1x.png'))))
        self.tab_src.setCurrentIndex(0)
        
        self.cbx_fil_pub.setChecked(False)
        self.cbx_fil_pub.clicked.connect(self.updateFile)
        
        self.cbx_fil_original.clicked.connect(self.toggleShowFileMode)
        self.cbx_fil_deleted.clicked.connect(self.toggleShowFileMode)
        
        self.btn_open_gimp.clicked.connect(self.openWithGimp)
        self.btn_open_gimp.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'gimp-icon.png'))))
        self.btn_open_gimp.setIconSize(QSize(24,24))
        self.btn_open_gimp.setToolTip("選択したファイルをGIMPで開きます。")  
        
        # Activate image proccessing tool buttons.
        self.btn_img_cnt.clicked.connect(self.extractContour)
        self.btn_img_cnt.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_crop_black_24dp_1x.png'))))
        self.btn_img_cnt.setIconSize(QSize(24,24))
        self.btn_img_cnt.setToolTip("選択したファイルの画像領域を自動で抽出します。")  
        
        self.btn_img_inv.clicked.connect(self.negativeToPositive)
        self.btn_img_inv.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_compare_black_24dp_1x.png'))))
        self.btn_img_inv.setIconSize(QSize(24,24))
        self.btn_img_inv.setToolTip("選択したファイルをネガティブ画像からポジティブ画像に変換します。")
        
        self.btn_img_del.clicked.connect(self.deleteSelectedImage)
        self.btn_img_del.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_delete_forever_black_24dp_1x.png'))))
        self.btn_img_del.setIconSize(QSize(24,24))
        self.btn_img_del.setToolTip("選択したファイルを削除します（データベースには残ります）。")
        
        self.btn_img_rot_r.clicked.connect(self.rotateImageRight)
        self.btn_img_rot_r.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_rotate_right_black_24dp_1x.png'))))
        self.btn_img_rot_r.setIconSize(QSize(24,24))
        self.btn_img_rot_r.setToolTip("選択したファイルを右に回転します。")
        
        self.btn_img_rot_l.clicked.connect(self.rotateImageLeft)
        self.btn_img_rot_l.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_rotate_left_black_24dp_1x.png'))))
        self.btn_img_rot_l.setIconSize(QSize(24,24))
        self.btn_img_rot_l.setToolTip("選択したファイルを左に回転します。")
        
        self.btn_img_rot_u.clicked.connect(self.rotateImageInvert)
        self.btn_img_rot_u.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_sync_black_24dp_1x.png'))))
        self.btn_img_rot_u.setIconSize(QSize(24,24))
        self.btn_img_rot_u.setToolTip("選択したファイルを180度回転します。")
        
        self.btn_img_mno.clicked.connect(self.makeMonoImage)
        self.btn_img_mno.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_monochrome_photos_black_24dp_1x.png'))))
        self.btn_img_mno.setIconSize(QSize(24,24))
        self.btn_img_mno.setToolTip("選択したファイルをモノクロ画像に変換します。")
        
        self.btn_img_enh.clicked.connect(self.enhanceImage)
        self.btn_img_enh.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_photo_filter_black_24dp_1x.png'))))
        self.btn_img_enh.setIconSize(QSize(24,24))
        self.btn_img_enh.setToolTip("選択したファイルにヒストグラム平滑化処理を加えます")
        
        self.btn_img_sav.clicked.connect(self.saveImageAs)
        self.btn_img_sav.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_move_to_inbox_black_24dp_1x.png'))))
        self.btn_img_sav.setIconSize(QSize(24,24))
        self.btn_img_sav.setToolTip("選択したファイルを指定のファイル名で出力します。")
        
        #========================================
        # Initialyze objects for camera & images
        #========================================
        
        # Activate detecting a connected camera button.
        self.btn_cam_detect.clicked.connect(self.detectCamera)
        self.btn_cam_detect.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_party_mode_black_24dp_1x.png'))))
        self.btn_cam_detect.setIconSize(QSize(24,24))
        
        #========================================
        # Initialyze objects for audio file
        #========================================
        
        # Initialyze the play button.
        self.btn_snd_play.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_play_circle_filled_black_24dp_1x.png'))))
        self.btn_snd_play.setIconSize(QSize(24,24))
        self.btn_snd_play.clicked.connect(self.soundPlay)
        
        self.btn_snd_stop.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_pause_circle_filled_black_24dp_1x.png'))))
        self.btn_snd_stop.setIconSize(QSize(24,24))
        
        # Detect the camera automatically.
        self.detectCamera()
        self.refreshItemInfo()
    
    # ==========================
    # General operation
    # ==========================
    def getTheRootDirectory(self):
        # Define constants.
        global ROOT_DIR
        global TABLE_DIR
        global CON_DIR
        global DATABASE
                
        # Initialyze the tree view.
        self.tre_prj_item.clear()
        
        # Reflesh the last selection.
        self.refreshItemInfo()
        
        # Define directories for storing files.
        ROOT_DIR = QFileDialog.getExistingDirectory(self, "プロジェクト・ディレクトリの選択")
        TABLE_DIR = os.path.join(ROOT_DIR, "Table")
        CON_DIR = os.path.join(ROOT_DIR, "Consolidation")
        
        # Define the DB file.
        DATABASE = os.path.join(TABLE_DIR, "project.db")
        
        if not os.path.exists(DATABASE):
            # Confirm whether create a directory for consolidations.
            reply = QMessageBox.question(
                    self, 
                    'データベース・ファイルが見つかりません。', 
                    '新規プロジェクトを作成しますか？', 
                    QMessageBox.Yes, 
                    QMessageBox.No
                )
            # Create the directory of consolidation
            if reply == QMessageBox.No:
                # Initialyze  global vaiables.
                ROOT_DIR = None
                TABLE_DIR = None
                CON_DIR = None
                DATABASE = None
                
                # Exit if canceled.
                return(None)
            elif reply == QMessageBox.Yes:
                try:
                    # Create the consolidation directory and the table directory.
                    os.mkdir(CON_DIR)
                    os.mkdir(TABLE_DIR)
                    
                    # Create the connection object to create empty database file.
                    conn = sqlite.connect(DATABASE)
                    
                    # Create new tables which defined by Simple Object Profile(SOP).
                    general.createTables(DATABASE)
                except Error as e:
                    # Create error messages.
                    error_title = "エラーが発生しました"
                    error_msg = "新規プロジェクトを作成できませんでした。"
                    error_info = "エラーの詳細を確認してください。"
                    error_icon = QMessageBox.Critical
                    error_detailed = e.args[0]
                    
                    # Handle error.
                    general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
                    
                    # Returns nothing.
                    return(None)
                finally:
                    # Finally close the connection.
                    conn.close()
            else:
                # Exit if canceled.
                return(None)
        
        if os.path.exists(DATABASE):
            # Create a sqLite file if not exists. 
            try:
                # Establish the connection to the DataBase file.
                conn = sqlite.connect(DATABASE)
                
                if conn is not None:
                    # Check whether table exists or not.
                    if not general.checkTableExist(DATABASE, "consolidation"): general.createTableConsolidation(DATABASE)
                    if not general.checkTableExist(DATABASE, "material"): general.createTableMaterial(DATABASE)
                    if not general.checkTableExist(DATABASE, "file"): general.createTableFile(DATABASE)
                    
                    # Check wether columns exists or not.
                    con_fields = [("uuid", "text"),
                                  ("name", "text"),
                                  ("geographic_annotation", "text"),
                                  ("temporal_annotation", "text"),
                                  ("description", "text")]
                    
                    mat_fields= [("con_id", "text"),
                                ("name", "text"),
                                ("material_number", "text"),
                                ("estimated_period_beginning", "character varying(255)"),
                                ("estimated_period_peak", "character varying(255)"),
                                ("estimated_period_ending", "character varying(255)"),
                                ("latitude", "real"),
                                ("longitude", "real"),
                                ("altitude", "real"),
                                ("material_number", "text"),
                                ("description", "text")]
                    
                    fil_fields = [("uuid", "text"),
                                  ("con_id", "text"),
                                  ("mat_id", "text"),
                                  ("created_date", "datetime"),
                                  ("modified_date", "datetime"),
                                  ("file_name", "character varying(255)"),
                                  ("file_type", "character varying(20)"),
                                  ("make_public", "bool"),
                                  ("alias_name", "character varying(255)"),
                                  ("status", "character varying(255)"),
                                  ("is_locked", "bool"),
                                  ("source", "character varying(255)"),
                                  ("file_operation", "character varying(255)"),
                                  ("operating_application", "character varying(255)"),
                                  ("caption", "character varying(255)"),
                                  ("description", "text")]
                    
                    general.checkFieldsExists(DATABASE, "consolidation", con_fields)
                    general.checkFieldsExists(DATABASE, "material", mat_fields)
                    general.checkFieldsExists(DATABASE, "file", fil_fields)
                    
                    # Create the SQL query for selecting consolidation.
                    sql_con_sel = """SELECT uuid, name, description FROM consolidation"""
                    
                    # Create the SQL query for selecting the consolidation.
                    sql_mat_sel = """SELECT uuid, name, description FROM material WHERE con_id=?"""
                    
                    # Instantiate the cursor for query.
                    cur_con = conn.cursor()
                    rows_con = cur_con.execute(sql_con_sel)
                    
                    # Execute the query and get consolidation recursively
                    for row_con in rows_con:
                        # Get attributes from the row.
                        con_uuid = row_con[0]
                        con_name = row_con[1]
                        con_description = row_con[2]
                        
                        if con_uuid == None or con_uuid == "NULL": con_uuid = ""
                        if con_name == None or con_name == "NULL": con_name = ""
                        if con_description == None or con_description == "NULL": con_description = ""
                        
                        # Update the tree view.
                        tre_prj_con_items = QTreeWidgetItem(self.tre_prj_item)
                        
                        tre_prj_con_items.setText(0, con_uuid)
                        tre_prj_con_items.setText(1, con_name)
                        
                        # Instantiate the cursor for query.
                        cur_mat = conn.cursor()
                        rows_mat = cur_mat.execute(sql_mat_sel, [con_uuid])
                            
                        for row_mat in rows_mat:
                            # Get attributes from the row.
                            mat_uuid = row_mat[0]
                            mat_name = row_mat[1]
                            mat_description = row_mat[2]
                            
                            if mat_uuid == None or mat_uuid == "NULL": mat_uuid = ""
                            if mat_name == None or mat_name == "NULL": mat_name = ""
                            if mat_description == None or mat_description == "NULL": mat_description = ""
                            
                            # Update the tree view.
                            tre_prj_mat_items = QTreeWidgetItem(tre_prj_con_items)
                            
                            tre_prj_mat_items.setText(0, mat_uuid)
                            tre_prj_mat_items.setText(1, mat_name)
                            
                        # Refresh the tree view.
                        self.tre_prj_item.show()
                        
                        self.tre_prj_item.resizeColumnToContents(0)
                        self.tre_prj_item.resizeColumnToContents(1)
                        
            except Error as e:
                # Connection error.
                error_title = "エラーが発生しました"
                error_msg = "データベースの情報を取得できません。"
                error_info = "エラーの詳細を確認してください。"
                error_icon = QMessageBox.Critical
                error_detailed = e.args[0]
                
                # Handle error.
                general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
                
                # Returns nothing.
                return(None)
            finally:
                conn.close()
        
        # Finally set the root path to the text box.
        self.lbl_prj_path.setText(ROOT_DIR)
    
    def getSoundFileInfo(self, sop_sound):
        print("main::getSoundFileInfo(self, sop_sound)")
    
    def showImage(self, img_file_path):
        print("main::showImage(self)")
        # Check the image file can be displayed directry.
        img_base, img_ext = os.path.splitext(img_file_path)
        img_valid = False
        
        # Get container size.
        panel_w = self.lbl_img_preview.width()
        panel_h = self.lbl_img_preview.height()
        
        for qt_ext in QT_IMG:
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
            error_detailed = None
            
            # Handle error.
            general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
            
            # Returns nothing.
            return(None)
    
    def toggleCurrentObject(self):
        print("main::toggleCurrentObject(self)")
        
        # Exit if the root directory is not loaded.
        if ROOT_DIR == None: return(None)
        
        # Initialyze the variable.
        select_type = None
        
        # Get the item of the material.
        selected = self.tre_prj_item.selectedItems()
        
        # Exit if selected item is 0.
        if len(selected) == 0: self.errorTreeItemNotSelected("self.tre_prj_item.selectedItems() == 0"); return(None)
        
        # Get the current object type from the tree view item.
        if selected[0].parent() == None:
            # The case of that a consolidation is selected in the tree view widget.
            select_type = "consolidation"
        elif not selected[0].parent() == None:
            # The case of that a material is selected in the tree view widget.
            select_type = "material"
        else:
            print("002: Cannot get current object type: main::toggleCurrentObject(self)")
            return(None)
                
        # Get the current object in target tab.
        if self.tab_target.currentIndex() == 0:
            # Get the current consolidation uuid.
            con_uuid = self.tbx_con_uuid.text()
            
            # Refresh the consolidation and the material infomation.
            self.refreshMaterialInfo()
            
            # Refresh the image information.
            self.refreshImageInfo()
            
            # Consolidation to Consolidation.
            if select_type == "consolidation":
                # Get the current consolidation.
                self.getConsolidation(con_uuid)
            # Material to Consolidation.
            elif select_type == "material":                
                # Select the parent consolidation.
                parent = self.tre_prj_item.selectedItems()[0].parent()
                self.tre_prj_item.setCurrentItem(parent)
                
                # Get the current consolidation.
                self.getConsolidation(con_uuid)
            else:
                self.errorUnknown()
        elif self.tab_target.currentIndex() == 1:
            # Get the current consolidation uuid.
            mat_uuid = self.tbx_mat_uuid.text()
            
            # Refresh the consolidation and the material infomation.
            self.refreshConsolidationInfo()
            
            # Refresh the image information.
            self.refreshImageInfo()
            
            # Consolidation to Material.
            if select_type == "consolidation":
                # Get the first child of the consolidation.
                child = selected[0].child(0)
                
                if not child == None:
                    # Select the first child of the consolidation.
                    self.tre_prj_item.setCurrentItem(selected[0].child(0))
                else:
                    self.refreshMaterialInfo()
            # Material to Material.
            elif select_type == "material":
                self.getMaterial(mat_uuid)
            else:
                self.errorUnknown()
        else:
            print("003: Invalid tab index: main::toggleCurrentObject(self)")
            return(None)
    
    def toggleSelectedItem(self):
        print("main::toggleSelectedItem(self)")
        
        global DATABASE
        global CON_DIR
        
        # Exit if the root directory is not loaded.
        if ROOT_DIR == None: self.errorProjectNotOpened(); return(None)
    
        # Get the item of the material.
        selected = self.tre_prj_item.selectedItems()
        
        # Exit if selected item is 0.
        if len(selected) == 0: return(None)
        
        if len(selected) > 0:
            # Clear all information beforehand.
            self.refreshItemInfo()
            
            if selected[0].parent() == None:
                # Get the Consolidation if the node have no parent.
                selected_uuid = selected[0].text(0)
                self.getConsolidation(selected_uuid)
                
                # Returns True.
                return(True)
            elif selected[0].parent() != None:
                # Get the Materil if the node have a parent.
                selected_uuid = selected[0].text(0)
                self.getMaterial(selected_uuid)
                
                # Returns True.
                return(True)
            else:  
                # Returns True.
                return(False)
        else:
            # Create error messages.
            error_title = "取得エラー"
            error_msg = LAB_CON + u"あるいは" + LAB_MAT + u"が選択されていません。"
            error_info = "ツリービューから再度選択してください。"
            error_icon = QMessageBox.Information
            error_detailed = None
            
            # Handle error.
            general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
            
            # Returns nothing.
            return(False)
    
    def toggleSelectedFile(self):
        print("main::toggleSelectedFile(self)")
        
        # Exit if the root directory is not loaded.
        if ROOT_DIR == None: self.errorProjectNotOpened(); return(None)
        
        # Get the current tree view item.
        selected = self.tre_fls.selectedItems()
        
        try:
            if not selected == None:
                if not len(selected) == 0:
                    # Get the uuid of the selected file.
                    fil_uuid = selected[0].text(0)
                    
                    # Instantiate the file object of SOP.
                    sop_file = features.File(is_new=False, uuid=fil_uuid, dbfile=DATABASE)
                    
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
                    
                    self.tbx_fil_capt.setText(sop_file.caption)
                    self.tbx_fil_stts.setText(sop_file.status)
                    self.tbx_fil_eope.setText(sop_file.operation)
                    
                    if sop_file.file_type == "image":
                        # Set active control tab for material.
                        self.tab_src.setCurrentIndex(0)
                        self.getImageFileInfo(sop_file)
                    if sop_file.file_type == "audio":
                        # Set active control tab for material.
                        self.tab_src.setCurrentIndex(1)
                        self.getSoundFileInfo(sop_file)
                else:
                    print("main::toggleSelectedFile(self) == 0")
        except Exception as e:
            self.errorUnknown("main::toggleSelectedFile(self)", e)
    
    def toggleShowFileMode(self):
        # Initialyze the uuid for the consolidation and the material.
        sop_object = None
        
        # Initialyze the variables.
        con_uuid = None
        mat_uuid = None
        item_path = None
        
        # Get the current object from the selected tab index.
        if self.tab_target.currentIndex() == 0:
            # Get the current consolidaiton uuid.
            con_uuid = self.tbx_con_uuid.text()
            
            # Instantiate the consolidation.
            sop_object = features.Consolidation(is_new=False, uuid=con_uuid, dbfile=DATABASE)
        elif self.tab_target.currentIndex() == 1:
            # Get the current material uuid.
            mat_uuid = self.tbx_mat_uuid.text()
            
            # Instantiate the material.
            sop_object = features.Material(is_new=False, uuid=mat_uuid, dbfile=DATABASE)
        else:
            return(None)
        
        # Refresh the file list.
        if not sop_object == None: self.refreshFileList(sop_object)
    
    def refreshItemInfo(self):
        print("main::refreshItemInfo(self)")
        try:
            self.refreshConsolidationInfo()
            self.refreshMaterialInfo()
            self.refreshImageInfo()
        except:
            print("Error occurs in mainPanel::refreshItemInfo(self)")
            return(None)
    
    def refreshFileList(self, sop_object):
        print("main::refreshFileList(self, sop_object)")
        
        try:
            # "Clear the file list view"
            self.tre_fls.clear()
            
            # Get images from the given class.
            images = sop_object.images
            sounds = sop_object.sounds
            
            if not images == None and len(images) > 0:
                for image in images: self.setFileInfo(image)
            if not sounds == None and len(sounds) > 0:
                for sound in sounds: self.setFileInfo(sound)
                
            # Refresh the tree view.
            self.tre_fls.resizeColumnToContents(0)
            self.tre_fls.resizeColumnToContents(1)
            self.tre_fls.resizeColumnToContents(2)
            
            # Selct the top item as the default.
            self.tre_fls.setCurrentItem(self.tre_fls.topLevelItem(0))
            self.tre_fls.show()
        except:
            print("Error occurs in mainPanel::refreshFileList")
            return(None)
    
    # ==========================
    # Consolidation
    # ==========================
    def addConsolidation(self):
        print("main::addConsolidation(self)")
        global CON_DIR
        
        # Exit if the root directory is not loaded.
        if ROOT_DIR == None: self.errorProjectNotOpened(); return(None)
        
        try:
            # Initialize the Consolidation Class.
            con = features.Consolidation(is_new=True, uuid=None, dbfile=None)
            
            # Instantiate the consolidation class
            con.name = self.tbx_con_name.text()
            con.geographic_annotation = self.tbx_con_geoname.text()
            con.temporal_annotation = self.tbx_con_temporal.text()
            con.description = self.tbx_con_description.text()
            
            # Insert the instance into DBMS.
            con.dbInsert(DATABASE)
            
            # Create a directory to store consolidation.
            general.createDirectories(os.path.join(CON_DIR,con.uuid), True)
            
            # Update the tree view.
            tre_prj_item_items = QTreeWidgetItem(self.tre_prj_item)
            tre_prj_item_items.setText(0, con.uuid)
            tre_prj_item_items.setText(1, con.name)
            
            # Refresh the tree view.
            self.tre_prj_item.show()
            
            self.tre_prj_item.resizeColumnToContents(0)
            self.tre_prj_item.resizeColumnToContents(1)
            
            # Change edit mode to modifying.
            self.rad_con_mod.setChecked(True)
            self.toggleEditModeForConsolidation()
        except:
            # Create error messages.
            error_title = LAB_CON + u"の作成エラー"
            error_msg = LAB_CON + u"の作成に失敗しました。"
            error_info = "不明なエラーです。"
            error_icon = QMessageBox.Information
            error_detailed = None
            
            # Handle error.
            general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
            
            # Returns nothing.
            return(None)
    
    def getConsolidation(self, uuid):
        print("main::getConsolidation(self)")
        
        global DATABASE
        
        try:
            # Instantiate by the DB record.
            consolidation = features.Consolidation(is_new=False, uuid=uuid, dbfile=DATABASE)
            
            # Input text box by the instance.
            self.setConsolidationInfo(consolidation)
            
            # Refresh the consolidation files.
            self.refreshFileList(consolidation)
        except Error as e:
            print("Catch except in mainPanel::getConsolidation(self)")
            
            # Create error messages.
            error_title = "エラーが発生しました"
            error_msg = "インスタンスを取得することができませんでした。"
            error_info = "SQLiteのデータベース・ファイルあるいはデータベースの設定を確認してください。"
            error_icon = QMessageBox.Critical
            error_detailed = e.args[0]
            
            # Handle error.
            general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
            
            # Returns nothing.
            return(None)
    
    def updateConsolidation(self):
        print("main::updateConsolidation(self)")
        
        # Exit if the root directory is not loaded.
        if ROOT_DIR == None: self.errorProjectNotOpened(); return(None)
        
        try:
            con_uuid = self.tbx_con_uuid.text()
            
            # Initialize the Consolidation Class.
            con = features.Consolidation(is_new=False, uuid=con_uuid, dbfile=DATABASE)
            
            # Instantiate the consolidation class
            con.name = self.tbx_con_name.text()
            con.geographic_annotation = self.tbx_con_geoname.text()
            con.temporal_annotation = self.tbx_con_temporal.text()
            con.description = self.tbx_con_description.text()
            
            # Update the instance into DBMS.
            con.dbUpdate(DATABASE)
            
            # Get the item of the material.
            selected = self.tre_prj_item.selectedItems()[0]
            
            # Update the tree view.
            if selected.text(0) == con.uuid:
                selected.setText(1, con.name)
            
            # Refresh the tree view.
            self.tre_prj_item.show()
            self.tre_prj_item.resizeColumnToContents(0)
            self.tre_prj_item.resizeColumnToContents(1)
        except:
            # Create error messages.
            error_title = LAB_CON + u"の更新エラー"
            error_msg = LAB_CON + u"の更新に失敗しました。"
            error_info = "不明なエラーです。"
            error_icon = QMessageBox.Information
            error_detailed = None
            
            # Handle error.
            general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
            
            # Returns nothing.
            return(None)
        else:
            # Returns nothing.
            return(None)
    
    def deleteConsolidation(self):
        print("main::deleteConsolidation(self)")
        
        global CON_DIR
        
        # Exit if the root directory is not loaded.
        if ROOT_DIR == None: self.errorProjectNotOpened(); return(None)
        
        # Confirm deletion.
        reply = QMessageBox.question(
                self, 
                LAB_CON + u"の削除", 
                LAB_CON + u"が内包する全ての" + LAB_MAT + u"およびデータが削除されます。本当に削除しますか？", 
                QMessageBox.Yes, 
                QMessageBox.No
            )
        
        # Confirm deleting the consolidation.
        if not reply == QMessageBox.Yes: return(None)
        
        try:
            con_uuid = self.tbx_con_uuid.text()
            
            # Initialize the Consolidation Class.
            con = features.Consolidation(is_new=False, uuid=con_uuid, dbfile=DATABASE)
            
            # Get the item of the material.
            selected = self.tre_prj_item.selectedItems()[0]
            
            # Update the tree view.
            if selected.text(0) == con.uuid:
                # Remove the consolidation from the tree view.
                root = self.tre_prj_item.invisibleRootItem()
                
                # Update the tree view.
                root.removeChild(selected)
                
                # Clear selection.
                self.tre_prj_item.clearSelection()
                
                # Refresh the tree view.
                self.tre_prj_item.show()
                self.tre_prj_item.resizeColumnToContents(0)
                self.tre_prj_item.resizeColumnToContents(1)
            
            # Delete all files from consolidation directory.
            shutil.rmtree(os.path.join(CON_DIR, con.uuid))
            
            # Drop the consolidation from the DB table.
            con.dbDrop(DATABASE)
            
            # Reflesh the last selection.
            self.refreshItemInfo()
        except:
            # Create error messages.
            error_title = LAB_CON + u"の削除エラー"
            error_msg = LAB_CON + u"の削除に失敗しました。"
            error_info = "不明なエラーです。"
            error_icon = QMessageBox.Information
            error_detailed = None
            
            # Handle error.
            general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
            
            # Returns nothing.
            return(None)
    
    def setConsolidationInfo(self, consolidation):
        print("main::setConsolidationInfo(self, consolidation)")
        
        try:
            # Initialyze the consolidation info.
            self.refreshConsolidationInfo()
            
            # Initialyze the edit material mode as modifying.
            self.rad_con_mod.setChecked(True)
            self.toggleEditModeForConsolidation()
            
            # Set attributes to text boxes.
            self.tbx_con_uuid.setText(consolidation.uuid)
            self.tbx_con_name.setText(consolidation.name)
            self.tbx_con_geoname.setText(consolidation.geographic_annotation)
            self.tbx_con_temporal.setText(consolidation.temporal_annotation)
            self.tbx_con_description.setText(consolidation.description)
            
            # Set active control tab for consolidation.
            self.tab_target.setCurrentIndex(0)
        except:
            print("Error occors in main::setConsolidationInfo(self, consolidation)")
            return(False)
    
    def refreshConsolidationInfo(self):
        print("main::refreshConsolidationInfo(self)")
        
        try:
            self.rad_con_new.setChecked(True)
            
            # Clear the file list for consolidation.
            self.tre_fls.clearSelection()
            self.tre_fls.clear()
            
            # Only the add new consolidation button enabled.
            self.btn_con_add.setDisabled(False)
            self.btn_con_del.setDisabled(True)
            self.btn_con_take.setDisabled(True)
            self.btn_con_update.setDisabled(True)
            
            # Text boxes for attributes are enabled.
            self.tbx_con_name.setDisabled(False)
            self.tbx_con_geoname.setDisabled(False)
            self.tbx_con_temporal.setDisabled(False)
            self.tbx_con_description.setDisabled(False)
            
            # Change text color for text boxes.
            self.tbx_con_name.setStyleSheet("color: rgb(255, 0, 0);")
            self.tbx_con_geoname.setStyleSheet("color: rgb(255, 0, 0);")
            self.tbx_con_temporal.setStyleSheet("color: rgb(255, 0, 0);")
            self.tbx_con_description.setStyleSheet("color: rgb(255, 0, 0);")
            
            # Clear text boxes for attributes.
            self.tbx_con_name.setText("")
            self.tbx_con_geoname.setText("")
            self.tbx_con_temporal.setText("")
            self.tbx_con_description.setText("")
        except:
            print("Error occurs in main::refreshConsolidationInfo(self)")
    
    def toggleEditModeForConsolidation(self):
        print("main::toggleEditModeForConsolidation(self)")
        global ROOT_DIR
        
        try: 
            if self.grp_con_ope.checkedId() == 1:
                # Only the add new consolidation button is disabled.
                self.btn_con_add.setDisabled(True)
                self.btn_con_update.setDisabled(False)
                self.btn_con_take.setDisabled(False)
                self.btn_con_del.setDisabled(False)
                
                # Change text color for text boxes.
                self.tbx_con_name.setStyleSheet("color: rgb(0, 0, 0);")
                self.tbx_con_geoname.setStyleSheet("color: rgb(0, 0, 0);")
                self.tbx_con_temporal.setStyleSheet("color: rgb(0, 0, 0);")
                self.tbx_con_description.setStyleSheet("color: rgb(0, 0, 0);")
                
                # All text boxes for attributes of consolidation is enabled.
                self.tbx_con_name.setDisabled(False)
                self.tbx_con_geoname.setDisabled(False)
                self.tbx_con_temporal.setDisabled(False)
                self.tbx_con_description.setDisabled(False)
            else:
                self.refreshConsolidationInfo()
        except:
                # Connection error.
                error_title = "エラーが発生しました"
                error_msg = LAB_CON + u"の編集モードを変更できません。"
                error_info = "不明のエラーです。"
                error_icon = QMessageBox.Critical
                error_detailed = None
                
                # Handle error.
                general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
                
                # Returns nothing.
                return(None)
    
    # ==========================
    # Material
    # ==========================
    def addMaterial(self):
        print("main::addMaterial(self)")
        
        global CON_DIR
        
        # Exit if the root directory is not loaded.
        if ROOT_DIR == None: self.errorProjectNotOpened(); return(None)
        
        # Get the item of the material.
        con_uuid = None
        tre_prj_item_items = None
        selected = self.tre_prj_item.selectedItems()
        
        # Exit if no tree items are selected.
        if not len(selected) > 0: return(None)
        
        # Check the selected object is consolidation or not.
        if not selected[0].parent() == None:
            # Get the parent consolidation uuid if the selected object is a material.
            con_uuid = selected[0].parent().text(0)
            
            # Set the tree view item.
            tre_prj_item_items = QTreeWidgetItem(selected[0].parent())
            
            # Confirm whether select the parent consolidations.
            reply = QMessageBox.question(
                    self, 
                    LAB_MAT + u"を内包する" + LAB_CON + u"が指定されていません。", 
                    u"現在の" + LAB_CON + u"（" + con_uuid.decode("utf-8") + u"）に新規の" + LAB_MAT + u"を追加しますか？", 
                    QMessageBox.Yes, 
                    QMessageBox.No
                )
            
            # Handle the return value.
            if not reply == QMessageBox.Yes: return(None)
        else:
            # Get the consolidation uuid from the selected object.
            con_uuid = selected[0].text(0)
            
            # Set the tree view item.
            tre_prj_item_items = QTreeWidgetItem(selected[0])
        
        # Exit if the conslidation uuid is None.
        if con_uuid == None: return(None)
        print()
        try:
            # Generate the GUID for the material
            mat = features.Material(is_new=True, uuid=None, dbfile=None)
            
            # Get attributes from text boxes.
            mat.consolidation = con_uuid
            mat.material_number = self.tbx_mat_number.text()
            mat.name = self.tbx_mat_name.text()
            mat.estimated_period_beginning = self.tbx_mat_tmp_bgn.text()
            mat.estimated_period_peak = self.tbx_mat_tmp_mid.text()
            mat.estimated_period_ending = self.tbx_mat_tmp_end.text()
            mat.latitude = self.tbx_mat_geo_lat.text()
            mat.longitude = self.tbx_mat_geo_lon.text()
            mat.altitude = self.tbx_mat_geo_alt.text()
            mat.description = self.tbx_mat_description.text()
            
            # Create the SQL query for inserting the new consolidation.
            mat.dbInsert(DATABASE)
            
            # Create a directory to store consolidation.
            con_dir = os.path.join(CON_DIR, mat.consolidation)
            mat_dir = os.path.join(con_dir, "Materials")
            
            general.createDirectories(os.path.join(mat_dir, mat.uuid), False)
            
            # Update the tree view.
            tre_prj_item_items.setText(0, mat.uuid)
            tre_prj_item_items.setText(1, mat.name)
            
            self.tre_prj_item.show()
            self.tre_prj_item.resizeColumnToContents(0)
            self.tre_prj_item.resizeColumnToContents(1)
        except:
            # Create error messages.
            error_title = LAB_MAT + u"の作成エラー"
            error_msg = LAB_MAT + u"の作成に失敗しました。"
            error_info = "不明なエラーです。"
            error_icon = QMessageBox.Information
            error_detailed = None
            
            # Handle error.
            general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
            
            # Returns nothing.
            return(None)
    
    def getMaterial(self, uuid):
        print("main::getMaterial(self)")
        
        try:
            # Instantiate by the DB record.
            material = features.Material(is_new=False, uuid=uuid, dbfile=DATABASE)
            print("ok:set material")
            # Set material information.
            self.setMaterialInfo(material)
            print("ok:set material info")
            # Refresh the image file list.
            self.refreshFileList(material)
        except Error as e:
            print("Catch except in mainPanel::getMaterial(self)")
            
            # Create error messages.
            error_title = "エラーが発生しました"
            error_msg = "インスタンスを取得することができませんでした。"
            error_info = "SQLiteのデータベース・ファイルあるいはデータベースの設定を確認してください。"
            error_icon = QMessageBox.Critical
            error_detailed = e.args[0]
            
            # Handle error.
            general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
            
            # Returns nothing.
            return(None)
    
    def updateMaterial(self):
        print("main::updateMaterial(self)")
        
        # Exit if the root directory is not loaded.
        if ROOT_DIR == None: self.errorProjectNotOpened(); return(None)
        
        try:
            # Generate the GUID for the material
            mat_uuid = self.tbx_mat_uuid.text()
            
            # Instantiate the material by using uuid.
            mat = features.Material(is_new=False, uuid=mat_uuid, dbfile=DATABASE)
            
            # Get attributes from text boxes.
            mat.name = self.tbx_mat_name.text()
            mat.material_number = self.tbx_mat_number.text()
            mat.estimated_period_beginning = self.tbx_mat_tmp_bgn.text()
            mat.estimated_period_peak = self.tbx_mat_tmp_mid.text()
            mat.estimated_period_ending = self.tbx_mat_tmp_end.text()
            mat.latitude = self.tbx_mat_geo_lat.text()
            mat.longitude = self.tbx_mat_geo_lon.text()
            mat.altitude = self.tbx_mat_geo_alt.text()
            mat.description = self.tbx_mat_description.text()
            
            # Create the SQL query for updating the new consolidation.
            mat.dbUpdate(DATABASE)
            
            # Get the item of the material.
            selected = self.tre_prj_item.selectedItems()[0]
            
            # Update the tree view.
            if selected.text(0) == mat.uuid:
                selected.setText(1, mat.name)
            
            # Refresh the tree view.
            self.tre_prj_item.show()
            
            self.tre_prj_item.resizeColumnToContents(0)
            self.tre_prj_item.resizeColumnToContents(1)
        except:
            # Create error messages.
            error_title = LAB_MAT + u"の更新エラー"
            error_msg = LAB_MAT + u"の更新に失敗しました。"
            error_info = "不明なエラーです。"
            error_icon = QMessageBox.Information
            error_detailed = None
            
            # Handle error.
            general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
            
            # Returns nothing.
            return(None)
    
    def deleteMaterial(self):
        print("main::deleteMaterial(self)")
        
        global CON_DIR
        
        # Exit if the root directory is not loaded.
        if ROOT_DIR == None: self.errorProjectNotOpened(); return(None)
        
        # Confirm deleting the consolidation.
        reply = QMessageBox.question(
                self, 
                LAB_MAT + u"の削除", 
                LAB_MAT + u"が内包する全てのデータが削除されます。本当に削除しますか？", 
                QMessageBox.Yes, 
                QMessageBox.No
            )
        if not reply == QMessageBox.Yes: return(None)
        
        try:
            # Generate the GUID for the material
            mat_uuid = self.tbx_mat_uuid.text()
            
            # Generate the GUID for the material
            mat = features.Material(is_new=False, uuid=mat_uuid, dbfile=DATABASE)
            con_uuid = mat.consolidation
            
            # Get the item of the material.
            selected = self.tre_prj_item.selectedItems()
            
            # Exit if no tree items are selected.
            if not len(selected) > 0: return(None)
            
            # Exit if the parent consolidation is selected.
            if selected[0].parent() == None: return(None)
            
            # Update the tree view.
            if selected[0].text(0) == mat.uuid:
                selected[0].parent().removeChild(selected[0])
            
            # Clear selection.
            self.tre_prj_item.clearSelection()
            
            # Refresh the tree view.
            self.tre_prj_item.show()
            self.tre_prj_item.resizeColumnToContents(0)
            self.tre_prj_item.resizeColumnToContents(1)
            
            # Delete all files from consolidation directory.
            con_mat_path = os.path.join(os.path.join(CON_DIR,con_uuid),"Materials")
            mat_path = os.path.join(con_mat_path, mat.uuid)
            
            # Delete files.
            shutil.rmtree(mat_path)
            
            # Drop the consolidation from the DB table.
            mat.dbDrop(DATABASE)
            
            # Reflesh the last selection.
            self.refreshItemInfo()
        except:
            # Create error messages.
            error_title = LAB_MAT + u"の削除エラー"
            error_msg = LAB_MAT + u"の削除に失敗しました。"
            error_info = "不明なエラーです。"
            error_icon = QMessageBox.Information
            error_detailed = None
            
            # Handle error.
            general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
            
            # Returns nothing.
            return(None)
    
    def setMaterialInfo(self, material):
        print("main::setMaterialInfo(self, material)")
        
        try:
            # Initialyze the material info.
            self.refreshMaterialInfo()
            
            # Initialyze the edit material mode as modifying.
            self.rad_mat_mod.setChecked(True)
            
            # Set attributes to text boxes.
            self.tbx_mat_uuid.setText(material.uuid)
            self.tbx_mat_number.setText(material.material_number)
            self.tbx_mat_name.setText(material.name)
            self.tbx_mat_tmp_bgn.setText(material.estimated_period_beginning)
            self.tbx_mat_tmp_mid.setText(material.estimated_period_peak)
            self.tbx_mat_tmp_end.setText(material.estimated_period_ending)
            self.tbx_mat_geo_lat.setText(material.latitude)
            self.tbx_mat_geo_lon.setText(material.longitude)
            self.tbx_mat_geo_alt.setText(material.altitude)
            self.tbx_mat_description.setText(material.description)
            
            self.toggleEditModeForMaterial()
            
            # Set active control tab for material.
            self.tab_target.setCurrentIndex(1)
            
            # Returns the value.
            return(True)
        except:
            print("Error occors in main::setMaterialInfo(self, material)")
            return(False)
    
    def refreshMaterialInfo(self):
        print("main::refreshMaterialInfo(self)")
        
        try:
            self.rad_mat_new.setChecked(True)
            
            # Clear the file list for consolidation.
            self.tre_fls.clearSelection()
            self.tre_fls.clear()
            
            # Only the add new material button enabled.
            self.btn_mat_add.setDisabled(False)
            self.btn_mat_del.setDisabled(True)
            self.btn_mat_take.setDisabled(True)
            self.btn_mat_update.setDisabled(True)
            
            # Text boxes for attributes are enabled.
            self.tbx_mat_number.setDisabled(False)
            self.tbx_mat_name.setDisabled(False)
            self.tbx_mat_geo_lat.setDisabled(False)
            self.tbx_mat_geo_lon.setDisabled(False)
            self.tbx_mat_geo_alt.setDisabled(False)
            self.tbx_mat_tmp_bgn.setDisabled(False)
            self.tbx_mat_tmp_mid.setDisabled(False)
            self.tbx_mat_tmp_end.setDisabled(False)
            self.tbx_mat_description.setDisabled(False)
            
            # Change text color for text boxes.
            self.tbx_mat_number.setStyleSheet("color: rgb(255, 0, 0);")
            self.tbx_mat_name.setStyleSheet("color: rgb(255, 0, 0);")
            self.tbx_mat_geo_lat.setStyleSheet("color: rgb(255, 0, 0);")
            self.tbx_mat_geo_lon.setStyleSheet("color: rgb(255, 0, 0);")
            self.tbx_mat_geo_alt.setStyleSheet("color: rgb(255, 0, 0);")
            self.tbx_mat_tmp_bgn.setStyleSheet("color: rgb(255, 0, 0);")
            self.tbx_mat_tmp_mid.setStyleSheet("color: rgb(255, 0, 0);")
            self.tbx_mat_tmp_end.setStyleSheet("color: rgb(255, 0, 0);")
            self.tbx_mat_description.setStyleSheet("color: rgb(255, 0, 0);")
            
            # Clear text boxes for attributes.
            self.tbx_mat_uuid.setText("")
            self.tbx_mat_number.setText("")
            self.tbx_mat_name.setText("")
            self.tbx_mat_geo_lat.setText("")
            self.tbx_mat_geo_lon.setText("")
            self.tbx_mat_geo_alt.setText("")
            self.tbx_mat_tmp_bgn.setText("")
            self.tbx_mat_tmp_mid.setText("")
            self.tbx_mat_tmp_end.setText("")
            self.tbx_mat_description.setText("")
        except:
            print("Error occcurs in main::refreshMaterialInfo(self)")
    
    def toggleEditModeForMaterial(self):
        print("main::toggleEditModeForMaterial(self)")
        
        try:
            if self.grp_mat_ope.checkedId() == 1:
                # Only the add new consolidation button is disabled.
                self.btn_mat_add.setDisabled(True)
                self.btn_mat_update.setDisabled(False)
                self.btn_mat_take.setDisabled(False)
                self.btn_mat_del.setDisabled(False)
                
                # All text boxes for attributes of material is enabled.
                self.tbx_mat_number.setDisabled(False)
                self.tbx_mat_name.setDisabled(False)
                self.tbx_mat_geo_lat.setDisabled(False)
                self.tbx_mat_geo_lon.setDisabled(False)
                self.tbx_mat_geo_alt.setDisabled(False)
                self.tbx_mat_tmp_bgn.setDisabled(False)
                self.tbx_mat_tmp_mid.setDisabled(False)
                self.tbx_mat_tmp_end.setDisabled(False)
                self.tbx_mat_description.setDisabled(False)
                
                # Change text color for text boxes.
                self.tbx_mat_number.setStyleSheet("color: rgb(0, 0, 0);")
                self.tbx_mat_name.setStyleSheet("color: rgb(0, 0, 0);")
                self.tbx_mat_geo_lat.setStyleSheet("color: rgb(0, 0, 0);")
                self.tbx_mat_geo_lon.setStyleSheet("color: rgb(0, 0, 0);")
                self.tbx_mat_geo_alt.setStyleSheet("color: rgb(0, 0, 0);")
                self.tbx_mat_tmp_bgn.setStyleSheet("color: rgb(0, 0, 0);")
                self.tbx_mat_tmp_mid.setStyleSheet("color: rgb(0, 0, 0);")
                self.tbx_mat_tmp_end.setStyleSheet("color: rgb(0, 0, 0);")
                self.tbx_mat_description.setStyleSheet("color: rgb(0, 0, 0);")
                
                if self.tbx_mat_uuid.text() == "":
                    # Get the item of the material.
                    error_title = "編集対象の" + LAB_MAT + u"が選択されていません。"
                    error_msg = LAB_MAT + u"の編集モードを変更できません。"
                    error_info = "編集対象の" + LAB_MAT + u"を再選択してください。"
                    error_icon = QMessageBox.Critical
                    error_detailed = None
                    
                    # Handle error.
                    general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
                    
                    self.refreshMaterialInfo()
                    
                    # Returns nothing.
                    return(None)
            else:
                self.refreshMaterialInfo()
        except:
                # Connection error.
                error_title = "エラーが発生しました"
                error_msg = LAB_MAT + u"の編集モードを変更できません。"
                error_info = "不明のエラーです。"
                error_icon = QMessageBox.Critical
                error_detailed = None
                
                # Handle error.
                general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
                
                # Returns nothing.
                return(None)
    
    # ==========================
    # Image
    # ==========================
    def getImageFileInfo(self, sop_image):
        print("main::getImageFileInfo(self)")
        
        # Get the full path of the image.
        if sop_image.filename == "":
            img_file_path = os.path.join(os.path.join(SRC_DIR, "images"),"noimage.jpg")
        else:
            if not os.path.exists(os.path.join(ROOT_DIR, sop_image.filename)):
                img_file_path = os.path.join(os.path.join(SRC_DIR, "images"),"noimage.jpg")
            else:
                img_file_path = os.path.join(ROOT_DIR, sop_image.filename)
        
        # Clear.
        self.tre_img_prop.clear()
        
        try:
            # Get file information by using "dcraw" library.
            img_stat = imageProcessing.getMetaInfo(img_file_path).strip().split("\n")
            
            # Get each metadata entry.
            for entry in img_stat:
                # Split metadata entry by ":".
                entry_line = entry.split(":")
                
                # Get the metadata key.
                entry_key = entry_line[0]
                
                # Get the metadata value.
                entry_val = entry_line[1]
                
                # Add file information to the tree list.
                self.tre_img_prop.addTopLevelItem(QTreeWidgetItem([entry_key, entry_val]))
        except:
            print("Cannot get the meta information.")
        # Get file information by using python "stat" library.
        fl_stat = os.stat(img_file_path)
        
        # Get file size.
        fl_size = str(round(float(fl_stat[ST_SIZE]/1000),3))+"KB"
        
        # Get time for last access, modified and creat.
        fl_time_last = time.asctime(time.localtime(fl_stat[ST_ATIME]))
        fl_time_mod = time.asctime(time.localtime(fl_stat[ST_MTIME]))
        fl_time_cre = time.asctime(time.localtime(fl_stat[ST_CTIME]))
        
        # Add file information to the tree list.
        self.tre_img_prop.addTopLevelItem(QTreeWidgetItem(["Created", fl_time_cre]))
        self.tre_img_prop.addTopLevelItem(QTreeWidgetItem(["Last Modified", fl_time_mod]))
        self.tre_img_prop.addTopLevelItem(QTreeWidgetItem(["Last Access", fl_time_last]))
        self.tre_img_prop.addTopLevelItem(QTreeWidgetItem(["File Size", fl_size]))
        
        # Refresh the tree view.
        self.tre_img_prop.show()
        
        # Show preview.
        self.showImage(img_file_path)
    
    def setFileInfo(self, sop_object):
        if sop_object.public == "1":
            self.cbx_fil_pub.setChecked(True)
        else:
            self.cbx_fil_pub.setChecked(False)
        
        if sop_object.lock == "1":
            self.cbx_fil_edit.setChecked(False)
            self.cbx_fil_edit.setDisabled(True)
        else:
            self.cbx_fil_edit.setChecked(True)
            self.cbx_fil_edit.setDisabled(False)
            self.cbx_fil_edit.setEnabled(True)
            
        self.tbx_fil_capt.setText(sop_object.caption)
        self.tbx_fil_stts.setText(sop_object.status)
        self.tbx_fil_eope.setText(sop_object.operation)
        
        fil_status = sop_object.status
        
        if fil_status == "Original":
            if self.cbx_fil_original.isChecked() == True:
                # Update the tree view.
                tre_fls_item = QTreeWidgetItem(self.tre_fls)
                
                tre_fls_item.setText(0, sop_object.uuid)
                tre_fls_item.setText(1, sop_object.alias)
                tre_fls_item.setText(2, sop_object.file_type)
                
                tre_fls_item.setForeground(0,QBrush(QColor("#0000FF")))
                tre_fls_item.setForeground(1,QBrush(QColor("#0000FF")))
                tre_fls_item.setForeground(2,QBrush(QColor("#0000FF")))
        elif fil_status == "Removed":
            if self.cbx_fil_deleted.isChecked() == True:
                # Update the tree view.
                tre_fls_item = QTreeWidgetItem(self.tre_fls)
                
                tre_fls_item.setText(0, sop_object.uuid)
                tre_fls_item.setText(1, sop_object.alias)
                tre_fls_item.setText(2, sop_object.file_type)
                
                tre_fls_item.setForeground(0,QBrush(QColor("#FF0000")))
                tre_fls_item.setForeground(1,QBrush(QColor("#FF0000")))
                tre_fls_item.setForeground(2,QBrush(QColor("#FF0000")))
        else:
            # Update the tree view.
            tre_fls_item = QTreeWidgetItem(self.tre_fls)
            
            tre_fls_item.setText(0, sop_object.uuid)
            tre_fls_item.setText(1, sop_object.alias)
            tre_fls_item.setText(2, sop_object.file_type)
            
            tre_fls_item.setForeground(0,QBrush(QColor("#000000")))
            tre_fls_item.setForeground(1,QBrush(QColor("#000000")))
            tre_fls_item.setForeground(2,QBrush(QColor("#000000")))
    
    def updateFile(self):
        global ROOT_DIR
        
        if not ROOT_DIR == None:
            selected = self.tre_fls.selectedItems()
            
            if not selected == None or not len(selected) == 0:
                fil_uuid = selected[0].text(0)
                print(fil_uuid)
        else:
            # Create error messages.
            error_title = "プロジェクトのエラー"
            error_msg = "プロジェクトが開かれていません。"
            error_info = "プロジェクトのディレクトリを参照し、指定ください。"
            error_icon = QMessageBox.Critical
            error_detailed = None
            
            # Handle error.
            general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
            
            self.refreshItemInfo()
            
            # Returns nothing.
            return(None)
    
    def refreshImageInfo(self):
        print("main::refreshImageInfo(self)")
        
        try:
            # Clear the file list tree view..
            self.tre_fls.clear()
            
            # Initialyze the checkboxes.
            self.cbx_fil_pub.setChecked(False)
            self.cbx_fil_edit.setChecked(False)
            
            # Define the no image avatar for preview panel.
            noimage_path = os.path.join(os.path.join(SRC_DIR, "images"),"noimage.jpg")
            self.showImage(noimage_path)
            
            # Clear entries on image properties view.
            self.tre_img_prop.clear()
            
            # Initialyze checkboxes.
            self.cbx_fil_pub.setChecked(False)
            self.cbx_fil_edit.setChecked(True)
            self.cbx_fil_edit.setDisabled(False)
            
            # Clear texts relating to the previous instance.
            self.tbx_fil_capt.setText("")
            self.tbx_fil_stts.setText("")
            self.tbx_fil_eope.setText("")
        except:
            print("Error occurs in main::refreshImageInfo(self)")
    
    # ==========================
    # Sound Play
    # ==========================
    def soundPlay(self):
        # Handle the selected SOP file object.
        selected = self.tre_fls.selectedItems()
        
        if len(selected) > 0:
            fil_uuid = selected[0].text(0)
            
            # Instantiate the SOP File object by selected uuid.
            fil_object = features.File(is_new=False, uuid=fil_uuid, dbfile=DATABASE)
            
            if fil_object.file_type == "audio":
                # Get the path to the sound path.
                snd_path = os.path.join(ROOT_DIR, fil_object.filename)
                
                # Set data and samplig rate.
                data, fs = sf.read(snd_path, dtype='float32')
                
                # Start playing.
                sd.play(data, fs)
                
                # Connect to the stop button.
                self.btn_snd_play.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_play_circle_filled_green_24dp_1x.png'))))
                self.btn_snd_stop.clicked.connect(self.soundStop)
            else:
                # Create error messages.
                error_title = "音声再生エラー"
                error_msg = "選択中のファイルは音声ファイルではありません。"
                error_info = "再生可能な音声ファイルを選択してください。"
                error_icon = QMessageBox.Critical
                error_detailed = None
    
    def soundStop(self):
        self.btn_snd_play.setIcon(QIcon(QPixmap(os.path.join(ICN_DIR, 'ic_play_circle_filled_black_24dp_1x.png'))))
        sd.stop()
    
    # ==========================
    # Image processing tools
    # ==========================
    def getCurrentImage(self):
        print("main::getCurrentImage(self)")
        
        # Exit if the root directory is not loaded.
        if ROOT_DIR == None: self.errorProjectNotOpened(); return(None)
        
        try:
            selected = self.tre_fls.selectedItems()
            
            if not selected == None:
                if not len(selected) == 0:
                    # Get the uuid of the selected file.
                    fil_uuid = selected[0].text(0)
                    
                    # Instantiate the file object of SOP.
                    sop_file = features.File(is_new=False, uuid=fil_uuid, dbfile=DATABASE)
                    
                    if sop_file.file_type == "image":
                        # Set active control tab for material.
                        self.tab_src.setCurrentIndex(0)
                        self.getImageFileInfo(sop_file)
                                                
                        # Get the image path.
                        return(sop_file)
                    else:
                        # Create error messages.
                        error_title = "画像編集エラー"
                        error_msg = "選択中のファイルは画像ファイルではありません。"
                        error_info = "編集可能な画像ファイルを選択してください。"
                        error_icon = QMessageBox.Critical
                        error_detailed = None
                        
                        # Handle error.
                        general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
                        
                        # Returns nothing.
                        return(None)
                else:
                    self.errorTreeItemNotSelected("self.tre_fls.selectedItems() == 0")
                    return(None)
        except:
            # Display the error message.
            self.errorUnknown("main::getCurrentImage(self)")
            return(None)
    
    def openWithGimp(self):
        print("main::openWithGimp(self)")
        
        # Instantiate the file object of SOP.
        sop_file = self.getCurrentImage()
        
        if sop_file == None:
            return(None)
        
        if sop_file.file_type == "image":
            # Set active control tab for material.
            self.tab_src.setCurrentIndex(0)
            self.getImageFileInfo(sop_file)
            
            print("Let's go")           
            # Get the image path.
            img_path = os.path.join(ROOT_DIR, sop_file.filename)
            
            if os.path.exists(img_path):
                # Chec the extension of the file.
                ext = os.path.splitext(img_path)[1].lower()
                print(ext)
                # Cancel if the file extension is not JPEG.
                if not ext == ".jpg" or ext == ".jpeg":
                    # Create error messages.
                    error_title = "画像編集エラー"
                    error_msg = "選択中のファイルはJPEGファイルではありません。"
                    error_info = "GIMPで編集可能な画像ファイルを選択してください。"
                    error_icon = QMessageBox.Critical
                    error_detailed = None
                    
                    # Handle error.
                    general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
                    
                    # Returns nothing.
                    return(None)
                
                # Define the new uuid for the image.
                new_uuid = str(uuid.uuid4())
                
                # Get the time for opening GIMP.
                time_open = datetime.datetime.utcnow().isoformat()
                
                # Get the parent directory of the original image.
                out_dir = os.path.dirname(img_path)
                new_file = os.path.join(out_dir, new_uuid+".jpg")
                
                # Copy the original file.
                shutil.copy(img_path, new_file)
                
                # Open the image with GIMP.
                imageProcessing.openWithGimp(new_file)
                
                # Get the time for closing GIMP.
                time_close = datetime.datetime.utcnow().isoformat()
                
                # Instantiate the File class.
                img_file = features.File(is_new=True, uuid=new_uuid, dbfile=None)
                img_file.material = sop_file.material
                img_file.consolidation = sop_file.consolidation
                img_file.filename = general.getRelativePath(new_file, "Consolidation")
                img_file.created_date = time_open
                img_file.modified_date = time_close
                img_file.file_type = "image"
                img_file.alias = "Edited by GIMP"
                img_file.status = "Edited"
                img_file.lock = False
                img_file.public = False
                img_file.source = sop_file.uuid
                img_file.operation = "Edit on GIMP"
                img_file.operating_application = "GIMP"
                img_file.caption = "Edited by GIMP"
                img_file.description = "This file is edited by GIMP."
                
                img_file.dbInsert(DATABASE)
                
                sop_object = None
                if img_file.material == "":
                    sop_object = features.Consolidation(is_new=False, uuid=img_file.consolidation, dbfile=DATABASE)
                else:
                    sop_object = features.Material(is_new=False, uuid=img_file.material, dbfile=DATABASE)
                
                # Refresh the image file list.
                self.refreshFileList(sop_object)
        else:
            # Create error messages.
            error_title = "画像編集エラー"
            error_msg = "選択中のファイルは画像ファイルではありません。"
            error_info = "GIMPで編集可能な画像ファイルを選択してください。"
            error_icon = QMessageBox.Critical
            error_detailed = None
            
            # Handle error.
            general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
            
            # Returns nothing.
            return(None)
        
    def rotateImageLeft(self):
        print("rotateImageLeft(self)")
        
        # Exit if the root directory is not loaded.
        if ROOT_DIR == None: self.errorProjectNotOpened(); return(None)
        
        # Rotate the image -90 degree.
        self.rotateImage(-90)
    
    def rotateImageRight(self):
        print("rotateImageRight(self)")
        
        # Exit if the root directory is not loaded.
        if ROOT_DIR == None: self.errorProjectNotOpened(); return(None)
        
        # Rotate the image 90 degree.
        self.rotateImage(90)
    
    def rotateImageInvert(self):
        print("rotateImageInvert(self)")
        
        # Exit if the root directory is not loaded.
        if ROOT_DIR == None: self.errorProjectNotOpened(); return(None)
        
        # Rotate the image 180 degree.
        self.rotateImage(180)
    
    def rotateImage(self, angle):
        print("main::rotateImage(self, angle)")
        
        # Instantiate the file object of SOP.
        sop_file = self.getCurrentImage()
        
        if sop_file == None: return(None)
        
        if sop_file.file_type == "image":
            # Set active control tab for material.
            self.tab_src.setCurrentIndex(0)
            self.getImageFileInfo(sop_file)
            
            # Get the image path.
            img_path = os.path.join(ROOT_DIR, sop_file.filename)
            
            if os.path.exists(img_path):
                # Chec the extension of the file.
                ext = os.path.splitext(img_path)[1].lower()
                
                # Cancel if the file extension is not JPEG.
                if not ext == ".jpg" or ext == ".jpeg":
                    # Create error messages.
                    error_title = "画像編集エラー"
                    error_msg = "このファイルはJPEGファイルではありません。"
                    error_info = "編集可能な画像ファイルを選択してください。"
                    error_icon = QMessageBox.Critical
                    error_detailed = None
                    
                    # Handle error.
                    general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
                    
                    # Returns nothing.
                    return(None)
                
                # Define the new uuid for the image.
                new_uuid = str(uuid.uuid4())
                
                # Get the time for opening GIMP.
                time_open = datetime.datetime.utcnow().isoformat()
                
                # Get the parent directory of the original image.
                out_dir = os.path.dirname(img_path)
                new_file = os.path.join(out_dir, new_uuid+".jpg")
                
                # Rotate the image 90 degree.
                imageProcessing.rotation(img_path, new_file, angle)
                
                # Copy the exif information.
                general.copyExif(img_path, new_file)
                
                # Get the time for closing GIMP.
                time_close = datetime.datetime.utcnow().isoformat()
                
                # Instantiate the File class.
                img_file = features.File(is_new=True, uuid=new_uuid, dbfile=None)
                img_file.material = sop_file.material
                img_file.consolidation = sop_file.consolidation
                img_file.filename = general.getRelativePath(new_file, "Consolidation")
                img_file.created_date = time_open
                img_file.modified_date = time_close
                img_file.file_type = "image"
                img_file.alias = "Rotated(" + str(angle) + " degree)"
                img_file.status = "Edited"
                img_file.lock = False
                img_file.public = False
                img_file.source = sop_file.uuid
                img_file.operation = "Rotating " + str(angle) + " degree"
                img_file.operating_application = "This System"
                img_file.caption = "Rotated(" + str(angle) + " degree)"
                img_file.description = "Rotated(" + str(angle) + " degree) by this system."
                
                img_file.dbInsert(DATABASE)
                
                sop_object = None
                if img_file.material == "":
                    sop_object = features.Consolidation(is_new=False, uuid=img_file.consolidation, dbfile=DATABASE)
                else:
                    sop_object = features.Material(is_new=False, uuid=img_file.material, dbfile=DATABASE)
                
                # Refresh the image file list.
                self.refreshFileList(sop_object)
    
    def makeMonoImage(self):
        print("main::makeMonoImage(self, angle)")
        
        # Instantiate the file object of SOP.
        sop_file = self.getCurrentImage()
        
        if sop_file == None:
            return(None)
        
        if sop_file.file_type == "image":
            # Set active control tab for material.
            self.tab_src.setCurrentIndex(0)
            self.getImageFileInfo(sop_file)
            
            # Get the image path.
            img_path = os.path.join(ROOT_DIR, sop_file.filename)
            
            if os.path.exists(img_path):
                # Chec the extension of the file.
                ext = os.path.splitext(img_path)[1].lower()
                
                # Cancel if the file extension is not JPEG.
                if not ext == ".jpg" or ext == ".jpeg":
                    # Create error messages.
                    error_title = "画像編集エラー"
                    error_msg = "このファイルはJPEGファイルではありません。"
                    error_info = "編集可能な画像ファイルを選択してください。"
                    error_icon = QMessageBox.Critical
                    error_detailed = None
                    
                    # Handle error.
                    general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
                    
                    # Returns nothing.
                    return(None)
                
                # Define the new uuid for the image.
                new_uuid = str(uuid.uuid4())
                
                # Get the time for opening GIMP.
                time_open = datetime.datetime.utcnow().isoformat()
                
                # Get the parent directory of the original image.
                out_dir = os.path.dirname(img_path)
                new_file = os.path.join(out_dir, new_uuid+".jpg")
                
                # Invert the negative image.
                imageProcessing.makeMono(img_path, new_file)
                
                # Copy exif information.
                general.copyExif(img_path, new_file)
                
                # Get the time for closing GIMP.
                time_close = datetime.datetime.utcnow().isoformat()
                
                # Instantiate the File class.
                img_file = features.File(is_new=True, uuid=new_uuid, dbfile=None)
                img_file.material = sop_file.material
                img_file.consolidation = sop_file.consolidation
                img_file.filename = general.getRelativePath(new_file, "Consolidation")
                img_file.created_date = time_open
                img_file.modified_date = time_close
                img_file.file_type = "image"
                img_file.alias = "Grayscale version"
                img_file.status = "Edited"
                img_file.lock = False
                img_file.public = False
                img_file.source = sop_file.uuid
                img_file.operation = "Grayscaling"
                img_file.operating_application = "This System"
                img_file.caption = "Grayscale version"
                img_file.description = "Make grayscale by this system."
                
                img_file.dbInsert(DATABASE)
                
                sop_object = None
                if img_file.material == "":
                    sop_object = features.Consolidation(is_new=False, uuid=img_file.consolidation, dbfile=DATABASE)
                else:
                    sop_object = features.Material(is_new=False, uuid=img_file.material, dbfile=DATABASE)
                
                # Refresh the image file list.
                self.refreshFileList(sop_object)
    
    def enhanceImage(self):
        print("main::enhanceImage(self)")
        
        # Instantiate the file object of SOP.
        sop_file = self.getCurrentImage()
        
        if sop_file == None:
            return(None)
        
        if sop_file.file_type == "image":
            # Set active control tab for material.
            self.tab_src.setCurrentIndex(0)
            self.getImageFileInfo(sop_file)
            
            # Get the image path.
            img_path = os.path.join(ROOT_DIR, sop_file.filename)
            
            if os.path.exists(img_path):
                # Chec the extension of the file.
                ext = os.path.splitext(img_path)[1].lower()
                
                # Cancel if the file extension is not JPEG.
                if not ext == ".jpg" or ext == ".jpeg":
                    # Create error messages.
                    error_title = "画像編集エラー"
                    error_msg = "このファイルはJPEGファイルではありません。"
                    error_info = "編集可能な画像ファイルを選択してください。"
                    error_icon = QMessageBox.Critical
                    error_detailed = None
                    
                    # Handle error.
                    general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
                    
                    # Returns nothing.
                    return(None)
                
                # Define the new uuid for the image.
                new_uuid = str(uuid.uuid4())
                
                # Get the time for opening GIMP.
                time_open = datetime.datetime.utcnow().isoformat()
                
                # Get the parent directory of the original image.
                out_dir = os.path.dirname(img_path)
                new_file = os.path.join(out_dir, new_uuid+".jpg")
                
                # Invert the negative image.
                imageProcessing.enhance(img_path, new_file)
                
                # Copy exif information.
                general.copyExif(img_path, new_file)
                
                # Get the time for closing GIMP.
                time_close = datetime.datetime.utcnow().isoformat()
                
                # Instantiate the File class.
                img_file = features.File(is_new=True, uuid=new_uuid, dbfile=None)
                img_file.material = sop_file.material
                img_file.consolidation = sop_file.consolidation
                img_file.filename = general.getRelativePath(new_file, "Consolidation")
                img_file.created_date = time_open
                img_file.modified_date = time_close
                img_file.file_type = "image"
                img_file.alias = "Normalized version"
                img_file.status = "Edited"
                img_file.lock = False
                img_file.public = False
                img_file.source = sop_file.uuid
                img_file.operation = "Normalizing"
                img_file.operating_application = "This System"
                img_file.caption = "Normalized version"
                img_file.description = "Make normalized by this system."
                
                img_file.dbInsert(DATABASE)
                
                sop_object = None
                if img_file.material == "":
                    sop_object = features.Consolidation(is_new=False, uuid=img_file.consolidation, dbfile=DATABASE)
                else:
                    sop_object = features.Material(is_new=False, uuid=img_file.material, dbfile=DATABASE)
                
                # Refresh the image file list.
                self.refreshFileList(sop_object)
    
    def extractContour(self):
        print("main::extractContour(self)")
        
        # Instantiate the file object of SOP.
        sop_file = self.getCurrentImage()
        
        if sop_file == None: return(None)
        
        if sop_file.file_type == "image":
            # Set active control tab for material.
            self.tab_src.setCurrentIndex(0)
            self.getImageFileInfo(sop_file)
            
            # Get the image path.
            img_path = os.path.join(ROOT_DIR, sop_file.filename)
            
            if os.path.exists(img_path):
                # Chec the extension of the file.
                ext = os.path.splitext(img_path)[1].lower()
                
                # Cancel if the file extension is not JPEG.
                if not ext == ".jpg" or ext == ".jpeg":
                    # Create error messages.
                    error_title = "画像編集エラー"
                    error_msg = "このファイルはJPEGファイルではありません。"
                    error_info = "編集可能な画像ファイルを選択してください。"
                    error_icon = QMessageBox.Critical
                    error_detailed = None
                    
                    # Handle error.
                    general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
                    
                    # Returns nothing.
                    return(None)
                
                # Define the new uuid for the image.
                new_uuid = str(uuid.uuid4())
                
                # Get the time for opening GIMP.
                time_open = datetime.datetime.utcnow().isoformat()
                
                # Get the parent directory of the original image.
                out_dir = os.path.dirname(img_path)
                new_file = os.path.join(out_dir, new_uuid+".jpg")
                
                # Extract contour and save the inner frame of the contour.
                imageProcessing.extractInnerFrame(img_path, new_file, ratio = 0.05)
                
                # Copy exif information.
                general.copyExif(img_path, new_file)
                
                # Get the time for closing GIMP.
                time_close = datetime.datetime.utcnow().isoformat()
                
                # Instantiate the File class.
                img_file = features.File(is_new=True, uuid=new_uuid, dbfile=None)
                img_file.material = sop_file.material
                img_file.consolidation = sop_file.consolidation
                img_file.filename = general.getRelativePath(new_file, "Consolidation")
                img_file.created_date = time_open
                img_file.modified_date = time_close
                img_file.file_type = "image"
                img_file.alias = "Automatically cropped"
                img_file.status = "Edited"
                img_file.lock = False
                img_file.public = False
                img_file.source = sop_file.uuid
                img_file.operation = "Cropping"
                img_file.operating_application = "This System"
                img_file.caption = "Cropped version"
                img_file.description = "Make cropped by this system."
                
                img_file.dbInsert(DATABASE)
                
                sop_object = None
                if img_file.material == "":
                    sop_object = features.Consolidation(is_new=False, uuid=img_file.consolidation, dbfile=DATABASE)
                else:
                    sop_object = features.Material(is_new=False, uuid=img_file.material, dbfile=DATABASE)
                
                # Refresh the image file list.
                self.refreshFileList(sop_object)
    
    def negativeToPositive(self):
        print("main::negativeToPositive(self)")
        
        # Instantiate the file object of SOP.
        sop_file = self.getCurrentImage()
        
        if sop_file == None: return(None)
        
        if sop_file.file_type == "image":
            # Set active control tab for material.
            self.tab_src.setCurrentIndex(0)
            self.getImageFileInfo(sop_file)
            
            # Get the image path.
            img_path = os.path.join(ROOT_DIR, sop_file.filename)
            
            if os.path.exists(img_path):
                # Chec the extension of the file.
                ext = os.path.splitext(img_path)[1].lower()
                
                # Cancel if the file extension is not JPEG.
                if not ext == ".jpg" or ext == ".jpeg":
                    # Create error messages.
                    error_title = "画像編集エラー"
                    error_msg = "このファイルはJPEGファイルではありません。"
                    error_info = "編集可能な画像ファイルを選択してください。"
                    error_icon = QMessageBox.Critical
                    error_detailed = None
                    
                    # Handle error.
                    general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
                    
                    # Returns nothing.
                    return(None)
                
                # Define the new uuid for the image.
                new_uuid = str(uuid.uuid4())
                
                # Get the time for opening GIMP.
                time_open = datetime.datetime.utcnow().isoformat()
                
                # Get the parent directory of the original image.
                out_dir = os.path.dirname(img_path)
                new_file = os.path.join(out_dir, new_uuid+".jpg")
                
                
                # Invert the negative image.
                imageProcessing.negaToPosi(img_path, new_file)
                
                # Copy exif information.
                general.copyExif(img_path, new_file)
                
                # Get the time for closing GIMP.
                time_close = datetime.datetime.utcnow().isoformat()
                
                # Instantiate the File class.
                img_file = features.File(is_new=True, uuid=new_uuid, dbfile=None)
                img_file.material = sop_file.material
                img_file.consolidation = sop_file.consolidation
                img_file.filename = general.getRelativePath(new_file, "Consolidation")
                img_file.created_date = time_open
                img_file.modified_date = time_close
                img_file.file_type = "image"
                img_file.alias = "Automatically cropped"
                img_file.status = "Edited"
                img_file.lock = False
                img_file.public = False
                img_file.source = sop_file.uuid
                img_file.operation = "Cropping"
                img_file.operating_application = "This System"
                img_file.caption = "Cropped version"
                img_file.description = "Make cropped by this system."
                
                img_file.dbInsert(DATABASE)
                
                sop_object = None
                if img_file.material == "":
                    sop_object = features.Consolidation(is_new=False, uuid=img_file.consolidation, dbfile=DATABASE)
                else:
                    sop_object = features.Material(is_new=False, uuid=img_file.material, dbfile=DATABASE)
                
                # Refresh the image file list.
                self.refreshFileList(sop_object)
    
    def saveImageAs(self):
        print("main::saveImageAs(self)")
        
        # Instantiate the file object of SOP.
        sop_file = self.getCurrentImage()
        
        if sop_file == None:
            return(None)
        
        if sop_file.file_type == "image":
            # Set active control tab for material.
            self.tab_src.setCurrentIndex(0)
            self.getImageFileInfo(sop_file)
            
            # Get the image path.
            img_path = os.path.join(ROOT_DIR, sop_file.filename)
            
            if os.path.exists(img_path):
                # Chec the extension of the file.
                ext = os.path.splitext(img_path)[1].lower()
                
                # Cancel if the file extension is not JPEG.
                if not ext == ".jpg" or ext == ".jpeg":
                    # Create error messages.
                    error_title = "画像編集エラー"
                    error_msg = "このファイルはJPEGファイルではありません。"
                    error_info = "編集可能な画像ファイルを選択してください。"
                    error_icon = QMessageBox.Critical
                    error_detailed = None
                    
                    # Handle error.
                    general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
                    
                    # Returns nothing.
                    return(None)
                
                # Get the output file name by using file save dialog.
                new_file, img_file_type = QFileDialog.getSaveFileName(self, "保存先の選択", "output.jpg","Images (*.jpg)")
                
                if new_file:
                    if not os.path.exists(new_file):
                        # Export the original file into given path.
                        shutil.copyfile(img_path, new_file)
                        
                        # Export file info by XML.
                        sop_xml = sop_file.writeAsXml()
                        if not sop_xml == None:
                            xml_image_info = open(new_file+'.xml', "w") 
                            xml_image_info.write(sop_xml) 
                            xml_image_info.close() 
                    else:
                        # Create error messages.
                        error_title = "エクスポート・エラー"
                        error_msg = "すでに、ファイルが存在しています。"
                        error_info = "別名で保存するか、保存場所を変更してください。"
                        error_icon = QMessageBox.Critical
                        error_detailed = None
                        
                        # Handle error.
                        general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
                        
                        # Returns nothing.
                        return(None)
    
    def deleteSelectedImage(self):
        print("main::deleteSelectedImage(self)")
        
        # Exit if the root directory is not loaded.
        if ROOT_DIR == None: self.errorProjectNotOpened(); return(None)
        
        if not self.cbx_fil_edit.isChecked():
            # Create error messages.
            error_title = "ファイルの更新エラー"
            error_msg = "ファイルの削除ができません。"
            error_info = "このファイルはロックされているため削除できません。"
            error_icon = QMessageBox.Information
            error_detailed = None
            
            # Handle error.
            general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
            
            # Returns nothing.
            return(None)
        
        # Confirm deletion.
        reply = QMessageBox.question(
                self, 
                '画像の削除', 
                '選択されたファイルを本当に削除しますか？', 
                QMessageBox.Yes, 
                QMessageBox.No
            )
        
        # Confirm deleting the consolidation.
        if not reply == QMessageBox.Yes: return(None)
        
        # Instantiate the file object of SOP.
        sop_file = self.getCurrentImage()
        
        if sop_file == None: return(None)
        
        # Get the time for closing GIMP.
        time_delete = datetime.datetime.utcnow().isoformat()
        
        sop_file.alias = "Already Removed."
        sop_file.modified_date = time_delete
        sop_file.status = "Removed"
        sop_file.lock = True
        sop_file.public = False
        sop_file.operation = "Removing"
        sop_file.operating_application = "This System"
        sop_file.caption = "Removed"
        
        # Get the image path.
        fil_path = os.path.join(ROOT_DIR, sop_file.filename)
        
        if os.path.exists(fil_path):
            # Delete the selected file.
            os.remove(fil_path)
            
            # Update DB table.
            sop_file.filename = ""
            
            # Initialyze the image file name.
            sop_file.dbUpdate(DATABASE)
        else:
            # Initialyze the image file name.
            sop_file.filename = ""
            
            # Update DB table.
            sop_file.dbUpdate(DATABASE)
        # Refresh the image file list.
        sop_object = None
        if sop_file.material == "":
            sop_object = features.Consolidation(is_new=False, uuid=sop_file.consolidation, dbfile=DATABASE)
        else:
            sop_object = features.Material(is_new=False, uuid=sop_file.material, dbfile=DATABASE)
        # Refresh the image file list.
        self.refreshFileList(sop_object)
    
    # ==========================
    # Cemera operation
    # ==========================
    def detectCamera(self):
        global CUR_CAM
        
        # Detect the connected camera.
        cams = imageProcessing.detectCamera()
        
        if cams != None and len(cams) == 1:
            cam = cams[0]
        
            # Display the camera information.
            if not imageProcessing.setCamera(cam["name"], cam["port"]) == None:
                # Set the connected camera to the header.
                self.lbl_cam_detected.setStyleSheet("color: rgb(0, 0, 0);")
                self.lbl_cam_detected.setText(cam["name"])
                
                # Get camera parameter for the image size. 
                cam_size = imageProcessing.getConfig("imagesize",cam["name"], cam["port"])
                cam_iso = imageProcessing.getConfig("iso",cam["name"], cam["port"])
                cam_wht = imageProcessing.getConfig("whitebalance",cam["name"], cam["port"])
                cam_exp = imageProcessing.getConfig("exposurecompensation",cam["name"], cam["port"])
                cam_fval = imageProcessing.getConfig("f-number",cam["name"], cam["port"])
                cam_qoi = imageProcessing.getConfig("imagequality",cam["name"], cam["port"])
                cam_fmod = imageProcessing.getConfig("focusmode",cam["name"], cam["port"])
                cam_epg = imageProcessing.getConfig("expprogram",cam["name"], cam["port"])
                cam_cpt = imageProcessing.getConfig("capturemode",cam["name"], cam["port"])
                cam_met = imageProcessing.getConfig("exposuremetermode",cam["name"], cam["port"])
                
                # Set parameters to comboboxes.
                if not cam_size == None: self.setCamParamCbx(self.cbx_cam_size, cam_size)
                if not cam_iso == None: self.setCamParamCbx(self.cbx_cam_iso, cam_iso)
                if not cam_wht == None: self.setCamParamCbx(self.cbx_cam_wht, cam_wht)
                if not cam_exp == None: self.setCamParamCbx(self.cbx_cam_exp, cam_exp)
                if not cam_fval == None: self.setCamParamCbx(self.cbx_cam_fval, cam_fval)
                if not cam_qoi == None: self.setCamParamCbx(self.cbx_cam_qoi, cam_qoi)
                if not cam_fmod == None: self.setCamParamCbx(self.cbx_cam_fmod, cam_fmod)
                if not cam_epg == None: self.setCamParamCbx(self.cbx_cam_epg, cam_epg)
                if not cam_cpt == None: self.setCamParamCbx(self.cbx_cam_cpt, cam_cpt)
                if not cam_met == None: self.setCamParamCbx(self.cbx_cam_met, cam_met)
                
                CUR_CAM = cam["name"]
                
                print("Camera success fully detected.")
        else:
            # Set the message to the header.
            self.lbl_cam_detected.setStyleSheet("color: rgb(255, 0, 0);")
            self.lbl_cam_detected.setText("No Camera detected")
            
            # Clear comboboxes for camera parameters.
            self.cbx_cam_size.clear()
            self.cbx_cam_iso.clear()
            self.cbx_cam_wht.clear()
            self.cbx_cam_exp.clear()
            self.cbx_cam_fval.clear()
            self.cbx_cam_qoi.clear()
            self.cbx_cam_fmod.clear()
            self.cbx_cam_epg.clear()
            self.cbx_cam_cpt.clear()
            self.cbx_cam_met.clear()
            
            # Create error messages.
            error_title = "カメラの接続エラー"
            error_msg = "カメラが接続されていないか、複数のイメージデバイス（スマートフォンも含む）が接続されています。"
            error_info = "カメラの接続状態を確認してください。"
            error_icon = QMessageBox.Information
            error_detailed = "カメラ以外の全ての機器を取り外して再度実行してください。"
            
            # Handle error.
            general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
            
            # Return nothing.
            return(None)
        
    def setCamParamCbx(self, cbx, param):
        # Clear the combobox.
        cbx.clear()
        
        try:
            # Add the first position for the combobox as the current value.
            cbx.addItem(param["current"])
            
            # Add the options into the combobox.
            for opt in param["choice"]:
                opt_txt = str(opt.keys()[0])
                opt_val = str(opt.values()[0])
                
                cbx.addItem(opt_txt)
        except:
            # Create error messages.
            error_title = "エラーが発生しました"
            error_msg = "カメラのプロパティをセットできませんでした。"
            error_info = "カメラが対応していない可能性があります。"
            error_icon = QMessageBox.Critical
            error_detailed = None
            
            # Handle error.
            general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
            
            # Returns nothing.
            return(None)
        
    def recordWithPhoto(self):
        print("recordWithPhoto(self)")
        
        global TMP_DIR
        global CON_DIR
        
        # Exit if the root directory is not loaded.
        if ROOT_DIR == None: self.errorProjectNotOpened(); return(None)
        
        # Get the item of the material.
        selected = self.tre_prj_item.selectedItems()
        
        # Exit if selected item is 0.
        if len(selected) == 0: self.errorTreeItemNotSelected("self.tre_prj_item.selectedItems() == 0"); return(None)
        
        # Initialyze the uuid for the consolidation and the material.
        sop_object = None
        
        # Initialyze the variables.
        con_uuid = None
        mat_uuid = None
        item_path = None
        
        # Get the current object from the selected tab index.
        if self.tab_target.currentIndex() == 0:
            # Get the current consolidaiton uuid.
            con_uuid = self.tbx_con_uuid.text()
            
            # Instantiate the consolidation.
            sop_object = features.Consolidation(is_new=False, uuid=con_uuid, dbfile=DATABASE)
            
            # Get the item path of the selected consolidaiton.
            item_path = os.path.join(CON_DIR, con_uuid)
        elif self.tab_target.currentIndex() == 1:
            # Get the current material uuid.
            mat_uuid = self.tbx_mat_uuid.text()
            
            # Instantiate the material.
            sop_object = features.Material(is_new=False, uuid=mat_uuid, dbfile=DATABASE)
            
            # Instantiate the consolidation.
            con_uuid = sop_object.consolidation
            con_path = os.path.join(CON_DIR, sop_object.consolidation)
            item_path = os.path.join(os.path.join(con_path, "Materials"), mat_uuid) 
        else:
            return(None)
        
        print(con_uuid)
        
        # Exit if none of objecs are instantiated.
        if sop_object == None: return(None)
        
        if sop_object.sounds == None: sop_object.sounds = list()
        
        # Initialyze the temporal directory.
        recording_path = os.path.join(TMP_DIR, "recording")
        
        if not os.path.exists(recording_path):
            # Create the temporal directory if not exists.
            os.mkdir(recording_path)
        else:
            # Delete the existing temporal directory before create.
            shutil.rmtree(recording_path)
            os.mkdir(recording_path)
        
        # Define the path for saving images.
        snd_path = os.path.join(item_path, "Sounds")
        img_path = os.path.join(os.path.join(item_path, "Images"),"Main")
        
        try:
            # Check the result of the tethered image.
            self.dialogRecording = RecordWithImage(parent=self, img_path=img_path, snd_path=recording_path)
            isAccepted = self.dialogRecording.exec_()
            
            if isAccepted == 1:
                # Get the current date and time from accepted timing.
                now = datetime.datetime.utcnow().isoformat()    
                
                # Define the output directory.
                snd_lst_main = general.getFilesWithExtensionList(recording_path, SND_EXT)
                
                # Move to proper directory.
                if len(snd_lst_main) > 0:
                    # Get the resultants recursively.
                    for i in range(0, len(snd_lst_main)):
                        # Get the temporal file path and the destination path for putting.
                        snd_orig = os.path.join(recording_path, snd_lst_main[i])
                        snd_dest = os.path.join(snd_path, snd_lst_main[i])
                        
                        # Move to "Main" in the consolidation.
                        shutil.move(snd_orig, snd_dest)
                        
                        # Instantiate the File class.
                        snd_file = features.File(is_new=True, uuid=None, dbfile=None)
                        snd_file.material = mat_uuid
                        snd_file.consolidation = con_uuid
                        snd_file.filename = general.getRelativePath(snd_dest, "Consolidation")
                        snd_file.created_date = now
                        snd_file.modified_date = now
                        snd_file.file_type = "audio"
                        snd_file.alias = "Recording"
                        snd_file.status = "Original"
                        snd_file.lock = True
                        snd_file.public = False
                        snd_file.source = "Nothing"
                        snd_file.operation = "Audio Recording"
                        snd_file.operating_application = "This system"
                        snd_file.caption = "Original audio"
                        snd_file.description = ""
                        
                        # Insert the new entry into the database.
                        snd_file.dbInsert(DATABASE)
                        
                        # Add the image to the boject.
                        sop_object.sounds.insert(0, snd_file)
                else:
                    print("There are no resultants.")
                    return(None)
                
                # Remove tethered path from the temporal directory.
                shutil.rmtree(recording_path)
                
                # Refresh the file list.
                self.refreshFileList(sop_object)
            else:
                print("The result is not accepted.")
                return(None)
        except Exception as e:
            self.errorUnknown("recordWithPhoto(self)", e)
           
            # Returns nothing.
            return(None)
    
    def tetheredShooting(self):
        print("main::tetheredShooting(self)")
        
        global CUR_CAM
        global TMP_DIR
        global CON_DIR
        
        # Exit if the root directory is not loaded.
        if ROOT_DIR == None: self.errorProjectNotOpened(); return(None)
        
        # Get the item of the material.
        selected = self.tre_prj_item.selectedItems()
        
        # Exit if selected item is 0.
        if len(selected) == 0: self.errorTreeItemNotSelected("self.tre_prj_item.selectedItems() == 0"); return(None)
        
        # Initialyze the uuid for the consolidation and the material.
        sop_object = None
        
        # Initialyze the variables.
        con_uuid = None
        mat_uuid = None
        item_path = None
        
        # Get the current object from the selected tab index.
        if self.tab_target.currentIndex() == 0:
            # Get the current consolidaiton uuid.
            con_uuid = self.tbx_con_uuid.text()
            
            # Instantiate the consolidation.
            sop_object = features.Consolidation(is_new=False, uuid=con_uuid, dbfile=DATABASE)
            
            # Get the item path of the selected consolidaiton.
            item_path = os.path.join(CON_DIR, con_uuid)
        elif self.tab_target.currentIndex() == 1:
            # Get the current material uuid.
            mat_uuid = self.tbx_mat_uuid.text()
            
            # Instantiate the material.
            sop_object = features.Material(is_new=False, uuid=mat_uuid, dbfile=DATABASE)
            
            # Instantiate the consolidation.
            con_uuid = sop_object.consolidation
            con_path = os.path.join(CON_DIR, sop_object.consolidation)
            item_path = os.path.join(os.path.join(con_path, "Materials"), mat_uuid) 
        else:
            return(None)
        
        # Exit if none of objecs are instantiated.
        if sop_object == None: return(None)
        
        if sop_object.images == None: sop_object.images = list()
        
        # Initialyze the temporal directory.
        tethered_path = os.path.join(TMP_DIR, "tethered")
        
        if not os.path.exists(tethered_path):
            # Create the temporal directory if not exists.
            os.mkdir(tethered_path)
        else:
            # Delete the existing temporal directory before create.
            shutil.rmtree(tethered_path)
            os.mkdir(tethered_path)
        
        # Define the path for saving images.
        img_path = os.path.join(item_path, "Images")
        
        # Generate the GUID for the consolidation
        pht_uuid = str(uuid.uuid4())
        
        try:
            if CUR_CAM == None:
                if imageProcessing.detectCamera() == None:
                    # Returns nothing.
                    return(None)
            else:
                # Define the temporal path for the tethered shooting.
                tmp_path = os.path.join(tethered_path, pht_uuid)
                
                # Take a imge by using imageProcessing library.
                imageProcessing.takePhoto(tmp_path)
                
                # Define the output directory.
                img_lst_main = general.getFilesWithExtensionList(tethered_path, IMG_EXT)
                img_lst_raw = general.getFilesWithExtensionList(tethered_path, RAW_EXT)
                
                # Check the result of the tethered image.
                self.dialogTetheredShooting = CheckImageDialog(parent=self, path=tethered_path)
                isAccepted = self.dialogTetheredShooting.exec_()
                
                now = datetime.datetime.utcnow().isoformat()
                
                if isAccepted == 1:
                    # Define the path for images.
                    img_main = os.path.join(img_path, "Main")
                    img_raw = os.path.join(img_path, "Raw")
                    
                    # Move main images from the temporal directory to the object's directory.
                    if len(img_lst_main) > 0:
                        for i in range(0, len(img_lst_main)):
                            main_orig = os.path.join(tethered_path, img_lst_main[i])
                            main_dest = os.path.join(img_main, img_lst_main[i])
                            
                            # Move to "Main" in the consolidation.
                            shutil.move(main_orig, main_dest)
                            
                            # Instantiate the File class.
                            img_file = features.File(is_new=True, uuid=None, dbfile=None)
                            img_file.material = mat_uuid
                            img_file.consolidation = con_uuid
                            img_file.filename = general.getRelativePath(main_dest, "Consolidation")
                            img_file.created_date = now
                            img_file.modified_date = now
                            img_file.file_type = "image"
                            img_file.alias = "Tethered Shooting"
                            img_file.status = "Original"
                            img_file.lock = True
                            img_file.public = False
                            img_file.source = "Nothing"
                            img_file.operation = "Tethered Shooting"
                            img_file.operating_application = "This system"
                            img_file.caption = "Original image"
                            img_file.description = ""
                            
                            # Execute the SQL script.
                            img_file.dbInsert(DATABASE)
                            
                            # Add the image to the boject.
                            sop_object.images.insert(0, img_file)
                    else:
                        print("There are no main images.")
                    
                    # Move raw images from the temporal directory to the object's directory.
                    if len(img_lst_raw) > 0:
                        for j in range(0, len(img_lst_raw)):
                            raw_orig = os.path.join(tethered_path, img_lst_raw[j])
                            raw_dest = os.path.join(img_raw, img_lst_raw[j])
                            
                            # Move to "Raw" in the consolidation.
                            shutil.move(raw_orig, raw_dest)
                            
                            # Instantiate the File class.
                            raw_file = features.File(is_new=True, uuid=None, dbfile=None)
                            raw_file.material = mat_uuid
                            raw_file.consolidation = con_uuid
                            raw_file.filename = general.getRelativePath(raw_dest, "Consolidation")
                            raw_file.created_date = now
                            raw_file.modified_date = now
                            raw_file.file_type = "image"
                            raw_file.alias = "Tethered Shooting (RAW)"
                            raw_file.status = "Original"
                            raw_file.lock = True
                            raw_file.public = False
                            raw_file.source = "Nothing"
                            raw_file.operation = "Tethered Shooting"
                            raw_file.operating_application = "This system"
                            raw_file.caption = "Original image"
                            raw_file.description = ""
                            
                            # Execute the SQL script.
                            raw_file.dbInsert(DATABASE)
                            
                            # Add the image to the boject.
                            sop_object.images.insert(0, raw_file)
                    else:
                        print("There are no raw images.")
                
                # Remove tethered path from the temporal directory.
                shutil.rmtree(tethered_path)
                
                # Refresh the file list.
                self.refreshFileList(sop_object)
        except:
            self.errorUnknown("main::tetheredShooting(self)")
            return(None)
    
    # ==========================
    # Error messages
    # ==========================
    def errorProjectNotOpened(self):
        print("errorProjectNotOpened(self)")
        
        # Create error messages.
        error_title = "プロジェクトのエラー"
        error_msg = "プロジェクトが開かれていません。"
        error_info = "プロジェクトのディレクトリを参照し、指定ください。"
        error_icon = QMessageBox.Critical
        error_detailed = None
        
        # Handle error.
        general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
    
    def errorUnknown(self, module, e=None):
        print("errorUnknown(self)")
        
        # Create error messages.
        error_title = "エラーが発生しました"
        error_msg = "不明なエラーです。"
        error_info = "Error occurs in " + module
        error_icon = QMessageBox.Critical
        error_detailed = str(e)
        
        # Handle error.
        general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
    
    def errorTreeItemNotSelected(self, treeView):
        print("errorProjectNotOpened(self)")
        
        # Create error messages.
        error_title = "オブジェクトの選択エラー"
        error_msg = "オブジェクトを再選択し、実行しなおして下さい。"
        error_info = "ツリービューのオブジェクトが選択されていません。"
        error_icon = QMessageBox.Critical
        error_detailed = treeView
        
        # Handle error.
        general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
    
    
    def exportAsHtml(self):
        # Exit if the root directory is not loaded.
        if ROOT_DIR == None: self.errorProjectNotOpened(); return(None)
        
        try:
            output = os.path.join(ROOT_DIR,"project.html")
            
            features.exportAsHtml(DATABASE, output)
        except Exception as e:
            self.errorUnknown("main::exportAsHtml(self)", e)

def main():
    app = QApplication(sys.argv)
    form = mainPanel()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
