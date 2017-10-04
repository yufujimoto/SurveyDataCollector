#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Import general libraries.
import sys, os, uuid, shutil, time, math, tempfile, logging, pyexiv2

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
LAB_CON = "統合体"
LAB_MAT = "資料"

# Define the default extensions.
QT_IMG = [".BMP", ".GIF", ".JPG", ".JPEG", ".PNG", ".PBM", ".PGM", ".PPM", ".XBM", ".XPM"]
IMG_EXT = [".JPG", ".TIF", ".JPEG", ".TIFF", ".PNG", ".JP2", ".J2K", ".JPF", ".JPX", ".JPM"]
RAW_EXT = [".RAW", ".ARW"]
SND_EXT = [".WAV"]

class RecordThreading(QThread):
    def __init__(self, path):
        QThread.__init__(self)
        self.path_snd = path

    def __del__(self):
        self.wait()

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
    def __init__(self, parent=None, path=None):
        # Get the root directory for this script.
        global SRC_DIR
        global TMP_DIR
        
        # Set the source directory which this program located.
        SRC_DIR = os.path.dirname(os.path.abspath(__file__))
        
        icon_path = os.path.join(SRC_DIR, "icon")
        
        super(RecordWithImage, self).__init__(parent)
        self.setupUi(self)
        
        # Initialize the window.
        self.setWindowTitle(self.tr("Check Tethered Image"))
        self.setWindowState(Qt.WindowMaximized)
        
        # Get the path of the tethered image.
        self.path_img = os.path.join(os.path.join(path, "Images"),"Main")
        self.path_snd = os.path.join(path, "Sounds")
        
        # Initialyze the sound file control objects.
        self.btn_refresh.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'ic_sync_black_24dp_1x.png'))))
        self.btn_refresh.setIconSize(QSize(24,24))
        self.btn_refresh.clicked.connect(self.getSoundFiles)
        
        # Initialyze the play button.
        self.btn_play.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'ic_play_circle_filled_black_24dp_1x.png'))))
        self.btn_play.setIconSize(QSize(24,24))
        self.btn_play.clicked.connect(self.playing)
        
        # Initialyze the record button.
        self.btn_rec_start.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'ic_fiber_manual_record_black_24dp_1x.png'))))
        self.btn_rec_start.setIconSize(QSize(24,24))
        self.btn_rec_start.clicked.connect(self.recording)
        
        # Initialyze the stop button.
        self.btn_rec_stop.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'ic_pause_circle_filled_black_24dp_1x.png'))))
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
    
    def recording(self):
        # Start the recording thread.
        self.recThread.start()
        
        # Stop the threading.
        self.btn_rec_stop.clicked.connect(self.recThread.terminate)
    
    def playing(self):
        # Get the path to the sound path.
        if not self.lst_snd_fls.currentItem() == None:
            snd_file_name = self.lst_snd_fls.currentItem().text()
            snd_path = os.path.join(self.path_snd, snd_file_name)
        
        data, fs = sf.read(snd_path, dtype='float32')
        sd.play(data, fs)
        
        self.btn_rec_stop.clicked.connect(self.stopping)
    
    def stopping(self):
        sd.stop()
        
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

class CheckImageDialog(QDialog, checkTetheredImageDialog.Ui_testDialog):
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
        self.lst_fls.itemSelectionChanged.connect(self.showImage)
        
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
                
                self.getImageFileInfo()
                
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
        icon_path = os.path.join(SRC_DIR, "icon")
        
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
        self.act_prj_open.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'ic_folder_open_black_24dp_1x.png'))))
        
        # Handle current selection of consolidations and materials.
        self.tre_prj_item.itemSelectionChanged.connect(self.toggleSelectedItem)
        self.tre_prj_item.itemDoubleClicked.connect(self.test)
        
        # Activate the tab for grouping manupilating consolidations and materials.
        self.tab_target.setTabIcon(0, QIcon(QPixmap(os.path.join(icon_path, 'ic_apps_black_24dp_1x.png'))))
        self.tab_target.setTabIcon(1, QIcon(QPixmap(os.path.join(icon_path, 'ic_insert_photo_black_24dp_1x.png'))))
        self.tab_target.setCurrentIndex(0)
        
        # Activate the tab for grouping manupilating consolidations and materials.
        self.tab_control.setTabIcon(0, QIcon(QPixmap(os.path.join(icon_path, 'ic_view_list_black_24dp_1x.png'))))
        self.tab_control.setTabIcon(1, QIcon(QPixmap(os.path.join(icon_path, 'ic_add_a_photo_black_24dp_1x.png'))))
        self.tab_control.setCurrentIndex(0)
        
        #========================================
        # Initialyze objects for consolidation
        #========================================
        
        self.tab_mat_src.setTabIcon(0, QIcon(QPixmap(os.path.join(icon_path, 'ic_collections_black_24dp_1x.png'))))
        self.tab_mat_src.setTabIcon(1, QIcon(QPixmap(os.path.join(icon_path, 'ic_library_music_black_24dp_1x.png'))))
        self.tab_mat_src.setCurrentIndex(0)
        
        # Activate the adding a consolidation button.
        self.btn_con_add.clicked.connect(self.addConsolidation)
        self.btn_con_add.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'ic_add_box_black_24dp_1x.png'))))
        self.btn_con_add.setIconSize(QSize(24,24))
        
        # Activate the updating the selected consolidation button.
        self.btn_con_update.clicked.connect(self.updateConsolidation)
        self.btn_con_update.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'ic_check_box_black_24dp_1x.png'))))
        self.btn_con_update.setIconSize(QSize(24,24))
        
        # Activate the deleting the selected consolidation button.
        self.btn_con_del.clicked.connect(self.deleteConsolidation)
        self.btn_con_del.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'ic_indeterminate_check_box_black_24dp_1x.png'))))
        self.btn_con_del.setIconSize(QSize(24,24))
        
        # Activate the taking a image of the consolidation button.
        self.btn_con_take.clicked.connect(self.tetheredShooting)
        self.btn_con_take.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'ic_local_see_black_24dp_1x.png'))))
        self.btn_con_take.setIconSize(QSize(24,24))
        
        # Activate the opening recording dialog button.
        self.btn_con_rec.clicked.connect(self.recordWithPhoto)
        self.btn_con_rec.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'ic_keyboard_voice_black_24dp_1x.png'))))
        self.btn_con_rec.setIconSize(QSize(24,24))
        
        # Handle current selection of files for consolidations.
        self.lst_con_fls.itemSelectionChanged.connect(self.getImageFileInfo)
        
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
        self.btn_mat_add.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'ic_add_circle_black_24dp_1x.png'))))
        self.btn_mat_add.setIconSize(QSize(24,24))
        
        # Activate the updating the selected material button.
        self.btn_mat_update.clicked.connect(self.updateMaterial)
        self.btn_mat_update.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'ic_check_circle_black_24dp_1x.png'))))
        self.btn_mat_update.setIconSize(QSize(24,24))
        
        # Activate the consolidation delete button.
        self.btn_mat_del.clicked.connect(self.deleteMaterial)
        self.btn_mat_del.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'ic_remove_circle_black_24dp_1x.png'))))
        self.btn_mat_del.setIconSize(QSize(24,24))
        
        # Activate the taking a image of the material button.
        self.btn_mat_take.clicked.connect(self.tetheredShooting)
        self.btn_mat_take.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'ic_local_see_black_24dp_1x.png'))))
        self.btn_mat_take.setIconSize(QSize(24,24))
        
        # Activate the opening recording dialog button.
        self.btn_mat_rec.clicked.connect(self.recordWithPhoto)
        self.btn_mat_rec.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'ic_keyboard_voice_black_24dp_1x.png'))))
        self.btn_mat_rec.setIconSize(QSize(24,24))
        
        # Activate image proccessing tool buttons.
        self.btn_mat_img_cnt.clicked.connect(self.extractContour)
        self.btn_mat_img_cnt.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'ic_crop_black_24dp_1x.png'))))
        self.btn_mat_img_cnt.setIconSize(QSize(24,24))
        
        self.btn_mat_img_inv.clicked.connect(self.negativeToPositive)
        self.btn_mat_img_inv.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'ic_compare_black_24dp_1x.png'))))
        self.btn_mat_img_inv.setIconSize(QSize(24,24))
        
        self.btn_mat_img_del.clicked.connect(self.deleteSelectedImage)
        self.btn_mat_img_del.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'ic_delete_forever_black_24dp_1x.png'))))
        self.btn_mat_img_del.setIconSize(QSize(24,24))
        
        self.btn_mat_img_rot_r.clicked.connect(self.rotateImageRight)
        self.btn_mat_img_rot_r.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'ic_rotate_right_black_24dp_1x.png'))))
        self.btn_mat_img_rot_r.setIconSize(QSize(24,24))
        
        self.btn_mat_img_rot_l.clicked.connect(self.rotateImageLeft)
        self.btn_mat_img_rot_l.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'ic_rotate_left_black_24dp_1x.png'))))
        self.btn_mat_img_rot_l.setIconSize(QSize(24,24))
        
        self.btn_mat_img_rot_u.clicked.connect(self.rotateImageInvert)
        self.btn_mat_img_rot_u.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'ic_sync_black_24dp_1x.png'))))
        self.btn_mat_img_rot_u.setIconSize(QSize(24,24))
        
        self.btn_mat_img_mno.clicked.connect(self.makeMonoImage)
        self.btn_mat_img_mno.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'ic_monochrome_photos_black_24dp_1x.png'))))
        self.btn_mat_img_mno.setIconSize(QSize(24,24))
        
        self.btn_mat_img_enh.clicked.connect(self.enhanceImage)
        self.btn_mat_img_enh.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'ic_photo_filter_black_24dp_1x.png'))))
        self.btn_mat_img_enh.setIconSize(QSize(24,24))
        
        self.btn_mat_gimp.clicked.connect(self.openWithGimp)
        self.btn_mat_gimp.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'gimp-icon.png'))))
        self.btn_mat_gimp.setIconSize(QSize(24,24))
        
        self.btn_mat_img_sav.clicked.connect(self.saveImageAs)
        self.btn_mat_img_sav.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'ic_move_to_inbox_black_24dp_1x.png'))))
        self.btn_mat_img_sav.setIconSize(QSize(24,24))
        
        # Handle current selection of files for consolidations.
        self.lst_mat_fls.itemSelectionChanged.connect(self.getImageFileInfo)
        
        # Activate selecting operation mode button.
        self.grp_mat_ope = QButtonGroup()
        self.grp_mat_ope.addButton(self.rad_mat_new, 0)
        self.grp_mat_ope.addButton(self.rad_mat_mod, 1)
        self.grp_mat_ope.buttonClicked.connect(self.toggleEditModeForMaterial)
        
        # Initialyze the edit material mode as modifying.
        self.rad_mat_mod.setChecked(True)
        self.toggleEditModeForMaterial()
        
        #========================================
        # Initialyze objects for camera & images
        #========================================
        
        # Activate detecting a connected camera button.
        self.btn_cam_detect.clicked.connect(self.detectCamera)
        self.btn_cam_detect.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'ic_party_mode_black_24dp_1x.png'))))
        self.btn_cam_detect.setIconSize(QSize(24,24))
        
        # Detect the camera automatically.
        self.detectCamera()
        
    def test(self):
        itm = self.tre_prj_item.itemFromIndex(self.tree.selectedIndexes()[0])
        column = self.tre_prj_item.currentColumn()
        edit = QtWidgets.QLineEdit()
        edit.returnPressed.connect(lambda*_:self.project.setData(column,edit.text(),itm,column,self.tre_prj_item))
        edit.returnPressed.connect(lambda*_:self.update())
        self.tre_prj_item.setItemWidget(itm,column,edit)
    
    # ==========================
    # Image processing tools
    # ==========================
    def getCurrentImage(self):
        global CON_DIR
        
        # Check the selection status.
        check_select = self.checkSelection()
        
        # Get the selection status.
        if not check_select == None:
            # Translate resultants.
            select_type = check_select["selection"][0]
            select_uuid = check_select["selection"][1]
            select_item = check_select["selection"][2]
        else:
            # Exit if something happened in checking the selection status on tree view.
            return(None)
        
        # Get uuid of the consolidation or the material.
        item_uuid = select_uuid
        
        if select_type == "consolidation":
            if not self.lst_con_fls.currentItem() == None:
                # Get the path to the consolidation.
                con_path = os.path.join(CON_DIR,item_uuid)
                
                # Get the path to the image directory of the consolidation.
                img_path = os.path.join(con_path, "Images")
                
                # Get the selected image file.
                lst_fls = self.lst_con_fls.currentItem().text()
            else:
                return(None)
        elif select_type == "material":
            if not self.lst_mat_fls.currentItem() == None:
                # Get uuid of the consolidation.
                con_uuid = select_item.parent().text(0)
                
                # Get the consolidation path.
                con_path = os.path.join(CON_DIR, con_uuid)
                mat_path = os.path.join(os.path.join(con_path, "Materials"), select_uuid)
                
                # Get the path to the image directory of the consolidation.
                img_path = os.path.join(mat_path, "Images")
                
                # Get the selected image file.
                lst_fls = self.lst_mat_fls
            else:
                return(None)
        else:
            return(None)
        
        # Get the file name which is currently selected.
        img_file_name = lst_fls.currentItem().text()
        
        # Make the full path of the selected image file.
        img_file_path = os.path.join(img_path,img_file_name)
        
        # Return values.
        return([select_type, select_uuid, img_path, img_file_path, lst_fls])
        
    def openWithGimp(self):
        # Make the full path of the selected image file.
        if not self.getCurrentImage() == None:
            select_type, select_uuid, img_path, img_file_path_org, lst_fls = self.getCurrentImage()
        else:
            return(None)
        
        # Get the image path.
        img_path = os.path.dirname(os.path.dirname(img_file_path_org))
        
        if os.path.exists(img_file_path_org):
            # Get the parent directory of the original image.
            out_dir = os.path.dirname(img_file_path_org)
            
            # Make a copy of the original.
            img_file_path_new = os.path.join(out_dir, str(uuid.uuid4())+'.jpg')
            shutil.copy(img_file_path_org, img_file_path_new)
            
            # Invert the negative image.
            imageProcessing.openWithGimp(img_file_path_new)
            
            # Refresh the image file list.
            self.refreshImageFileList(img_path, select_uuid, lst_fls)
        
    def rotateImageLeft(self):
        self.rotateImage(-90)
    
    def rotateImageRight(self):
        self.rotateImage(90)
    
    def rotateImageInvert(self):
        self.rotateImage(180)
    
    def rotateImage(self, angle):
        global TMP_DIR
        
        # Initialyze the temporal directory.
        imgproc_path = os.path.join(TMP_DIR, "imgproc")
        
        if not os.path.exists(imgproc_path):
            # Create the temporal directory if not exists.
            os.mkdir(imgproc_path)
        else:
            # Delete the existing temporal directory before create.
            shutil.rmtree(imgproc_path)
            os.mkdir(imgproc_path)
        
        # Make the full path of the selected image file.
        if not self.getCurrentImage() == None:
            select_type, select_uuid, img_path, img_file_path_in, lst_fls = self.getCurrentImage()
        else:
            return(None)
        
        # Exit if the mime type is not match.
        img_file_ext = os.path.splitext(img_file_path_in)[1]
        
        if not img_file_ext.lower() == ".jpg" or img_file_ext == "jpeg":
            # Create error messages.
            error_title = "エラーが発生しました"
            error_msg = "対応していないファイル形式です"
            error_info = "RAWデータはRawtherapee等のツールで編集してください。"
            error_icon = QMessageBox.Critical
            error_detailed = None
            
            # Handle error.
            general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
           
            # Returns nothing.
            return(None)
        
        # Get the image path.
        img_path = os.path.dirname(os.path.dirname(img_file_path_in))
        
        if os.path.exists(img_file_path_in):
            # Get the parent directory of the original image.
            out_dir = os.path.dirname(img_file_path_in)
            
            # Rotate the image 90 degree.
            img_file_path_out = imageProcessing.rotation(img_file_path_in, imgproc_path, angle)
            
            # Copy exif information.
            self.copyExif(img_file_path_in, img_file_path_out)
            
            # Over write original image with rotated image.
            shutil.copy(img_file_path_out, img_file_path_in)
            os.remove(img_file_path_out)
            
            # Refresh the image file list.
            self.refreshImageFileList(img_path, select_uuid, lst_fls)
            self.showImage(select_type, img_file_path_in)
    
    def makeMonoImage(self):
        # Make the full path of the selected image file.
        if not self.getCurrentImage() == None:
            select_type, select_uuid, img_path, img_file_path_in, lst_fls = self.getCurrentImage()
        else:
            return(None)
        
        # Exit if the mime type is not match.
        img_file_ext = os.path.splitext(img_file_path_in)[1]
        if not img_file_ext.lower() == ".jpg" or img_file_ext == "jpeg":
            # Create error messages.
            error_title = "エラーが発生しました"
            error_msg = "対応していないファイル形式です"
            error_info = "RAWデータはRawtherapee等のツールで編集してください。"
            error_icon = QMessageBox.Critical
            error_detailed = None
            
            # Handle error.
            general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
           
            # Returns nothing.
            return(None)
        
        # Get the image path.
        img_path = os.path.dirname(os.path.dirname(img_file_path_in))
        
        if os.path.exists(img_file_path_in):
            # Get the parent directory of the original image.
            out_dir = os.path.dirname(img_file_path_in)
            
            # Invert the negative image.
            img_file_path_out = imageProcessing.makeMono(img_file_path_in, out_dir)
            
            # Copy exif information.
            self.copyExif(img_file_path_in, img_file_path_out)
            
            # Refresh the image file list.
            self.refreshImageFileList(img_path, select_uuid, lst_fls)
    
    def enhanceImage(self):
        # Make the full path of the selected image file.
        if not self.getCurrentImage() == None:
            select_type, select_uuid, img_path, img_file_path_in, lst_fls = self.getCurrentImage()
        else:
            return(None)
        
        # Exit if the mime type is not match.
        img_file_ext = os.path.splitext(img_file_path_in)[1]
        if not img_file_ext.lower() == ".jpg" or img_file_ext == "jpeg":
            # Create error messages.
            error_title = "エラーが発生しました"
            error_msg = "対応していないファイル形式です"
            error_info = "RAWデータはRawtherapee等のツールで編集してください。"
            error_icon = QMessageBox.Critical
            error_detailed = None
            
            # Handle error.
            general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
           
            # Returns nothing.
            return(None)
        
        # Get the image path.
        img_path = os.path.dirname(os.path.dirname(img_file_path_in))
        
        if os.path.exists(img_file_path_in):
            # Get the parent directory of the original image.
            out_dir = os.path.dirname(img_file_path_in)
            
            # Invert the negative image.
            img_file_path_out = imageProcessing.enhance(img_file_path_in, out_dir)
            
            # Copy exif information.
            self.copyExif(img_file_path_in, img_file_path_out)
            
            # Refresh the image file list.
            self.refreshImageFileList(img_path, select_uuid, lst_fls)
    
    def extractContour(self):
        # Make the full path of the selected image file.
        if not self.getCurrentImage() == None:
            select_type, select_uuid, img_path, img_file_path_in, lst_fls = self.getCurrentImage()
        else:
            return(None)
        
        # Exit if the mime type is not match.
        img_file_ext = os.path.splitext(img_file_path_in)[1]
        if not img_file_ext.lower() == ".jpg" or img_file_ext == "jpeg":
            # Create error messages.
            error_title = "エラーが発生しました"
            error_msg = "対応していないファイル形式です"
            error_info = "RAWデータはRawtherapee等のツールで編集してください。"
            error_icon = QMessageBox.Critical
            error_detailed = None
            
            # Handle error.
            general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
           
            # Returns nothing.
            return(None)
        
        # Get the image path.
        img_path = os.path.dirname(os.path.dirname(img_file_path_in))
        
        if os.path.exists(img_file_path_in):
            # Get the parent directory of the original image.
            out_dir = os.path.dirname(img_file_path_in)
            
            # Extract contour and save the inner frame of the contour.
            img_file_path_out = imageProcessing.extractInnerFrame(img_file_path_in, out_dir, ratio = 0.05)
            
            # Copy exif information.
            self.copyExif(img_file_path_in, img_file_path_out)
            
            # Refresh the image file list.
            self.refreshImageFileList(img_path, select_uuid, lst_fls)
    
    def negativeToPositive(self):
        # Make the full path of the selected image file.
        if not self.getCurrentImage() == None:
            select_type, select_uuid, img_path, img_file_path_in, lst_fls = self.getCurrentImage()
        else:
            return(None)
        
        # Exit if the mime type is not match.
        img_file_ext = os.path.splitext(img_file_path_in)[1]
        if not img_file_ext.lower() == ".jpg" or img_file_ext == "jpeg":
            # Create error messages.
            error_title = "エラーが発生しました"
            error_msg = "対応していないファイル形式です"
            error_info = "RAWデータはRawtherapee等のツールで編集してください。"
            error_icon = QMessageBox.Critical
            error_detailed = None
            
            # Handle error.
            general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
           
            # Returns nothing.
            return(None)
        
        # Get the image path.
        img_path = os.path.dirname(os.path.dirname(img_file_path_in))
        
        if os.path.exists(img_file_path_in):
            # Get the parent directory of the original image.
            out_dir = os.path.dirname(img_file_path_in)
            
            # Invert the negative image.
            img_file_path_out = imageProcessing.negaToPosi(img_file_path_in, out_dir)
            
            # Copy exif information.
            self.copyExif(img_file_path_in, img_file_path_out)
            
            # Refresh the image file list.
            self.refreshImageFileList(img_path, select_uuid, lst_fls)
    
    def copyExif(self, org_file, dst_file):
        # Get the exif information for the original image.
        meta_org = pyexiv2.ImageMetadata(org_file)
        meta_org.read()
        meta_org.modified = True
        
        # Get the exif information for the cropped image.
        meta_dst = pyexiv2.metadata.ImageMetadata(dst_file)
        meta_dst.read()
        
        # Copy the original exif information to the cropped image.
        meta_org.copy(meta_dst)
        meta_dst.write()
    
    def saveImageAs(self):
        # Make the full path of the selected image file.
        if not self.getCurrentImage() == None:
            select_type, select_uuid, img_path, img_file_path_in, lst_fls = self.getCurrentImage()
        else:
            return(None)
        
        # Get the output file name by using file save dialog.
        img_file_path_out, img_file_type = QFileDialog.getSaveFileName(self, "保存先の選択", "output.jpg","Images (*.jpg)")
        
        if img_file_path_out:
            if not os.path.exists(img_file_path_out):
                print(img_file_path_out)
                shutil.copyfile(img_file_path_in, img_file_path_out)
    
    # ==========================
    # General operation
    # ==========================
    def deleteSelectedImage(self):
        global CON_DIR
        
        # Check the selection status.
        check_select = self.checkSelection()
        
        # Get the selection status.
        if not check_select == None:
            # Translate resultants.
            select_type = check_select["selection"][0]
            select_uuid = check_select["selection"][1]
            select_item = check_select["selection"][2]
        else:
            # Exit if something happened in checking the selection status on tree view.
            return(None)
        
        # Get uuid of the consolidation or the material.
        item_uuid = select_uuid
        
        if select_type == "consolidation":
            if not self.lst_con_fls.currentItem() == None:
                # Get the path to the consolidation.
                con_path = os.path.join(CON_DIR,item_uuid)
                
                # Get the path to the image directory of the consolidation.
                img_path = os.path.join(con_path, "Images")
                
                # Get the selected image file.
                lst_fls = self.lst_con_fls.currentItem().text()
            else:
                return(None)
        elif select_type == "material":
            if not self.lst_mat_fls.currentItem() == None:
                # Get uuid of the consolidation.
                con_uuid = select_item.parent().text(0)
                
                # Get the consolidation path.
                con_path = os.path.join(CON_DIR, con_uuid)
                mat_path = os.path.join(os.path.join(con_path, "Materials"), select_uuid)
                
                # Get the path to the image directory of the consolidation.
                img_path = os.path.join(mat_path, "Images")
                
                # Get the selected image file.
                lst_fls = self.lst_mat_fls
            else:
                return(None)
        else:
            return(None)
        
        # Get the file name which is currently selected.
        img_file_name = lst_fls.currentItem().text()
        
        # Make the full path of the selected image file.
        img_file_path = os.path.join(img_path,img_file_name)
        
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
        
        # Delete the selected file.
        os.remove(img_file_path)
        
        # Refresh the image file list.
        self.refreshImageFileList(img_path, select_uuid, self.lst_mat_fls)
    
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
                    # Create the SQL query for selecting consolidation.
                    sql_con_sel = """SELECT 
                                    uuid,
                                    name,
                                    description
                                FROM consolidation"""
                    
                    # Create the SQL query for selecting the consolidation.
                    sql_mat_sel = """SELECT 
                                        uuid,
                                        name,
                                        descriptions
                                    FROM material WHERE con_id=?"""
                    
                    # Instantiate the cursor for query.
                    cur_con = conn.cursor()
                    rows_con = cur_con.execute(sql_con_sel)
                    
                    # Execute the query and get consolidation recursively
                    for row_con in rows_con:
                        # Get attributes from the row.
                        con_uuid = row_con[0]
                        con_name = row_con[1]
                        con_description = row_con[2]
                        
                        # Update the tree view.
                        tre_prj_con_items = QTreeWidgetItem(self.tre_prj_item)
                        tre_prj_con_items.setText(0, con_uuid)
                        tre_prj_con_items.setText(1, con_name)
                        tre_prj_con_items.setText(2, con_description)
                        
                        # Instantiate the cursor for query.
                        cur_mat = conn.cursor()
                        rows_mat = cur_mat.execute(sql_mat_sel, [con_uuid])
                            
                        for row_mat in rows_mat:
                            # Get attributes from the row.
                            mat_uuid = row_mat[0]
                            mat_name = row_mat[1]
                            mat_description = row_mat[2]
                            
                            # Update the tree view.
                            tre_prj_mat_items = QTreeWidgetItem(tre_prj_con_items)
                            
                            tre_prj_mat_items.setText(0, mat_uuid)
                            tre_prj_mat_items.setText(1, mat_name)
                            tre_prj_mat_items.setText(2, mat_description)
                        
                        # Refresh the tree view.
                        self.tre_prj_item.show()
                        
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
    
    def getImageFileInfo(self):
        global CON_DIR
        
        # Check the selection status.
        check_select = self.checkSelection()
        
        # Get the selection status.
        if not check_select == None:
            # Translate resultants.
            select_type = check_select["selection"][0]
            select_uuid = check_select["selection"][1]
            select_item = check_select["selection"][2]
        else:
            # Exit if something happened in checking the selection status on tree view.
            return(None)
        
        # Get uuid of the consolidation or the material.
        item_uuid = select_uuid
        
        if select_type == "consolidation":
            if not self.lst_con_fls.currentItem() == None:
                # Get the path to the consolidation.
                con_path = os.path.join(CON_DIR,item_uuid)
                
                # Get the path to the image directory of the consolidation.
                img_path = os.path.join(con_path, "Images")
                
                # Get the tree view for the metadata of consolidation.
                tre_fl = self.tre_con_fl
                
                # Get the selected image file.
                lst_fls = self.lst_con_fls.currentItem().text()
            else:
                return(None)
        elif select_type == "material":
            if not self.lst_mat_fls.currentItem() == None:
                # Get uuid of the consolidation.
                con_uuid = select_item.parent().text(0)
                
                # Get the consolidation path.
                con_path = os.path.join(CON_DIR, con_uuid)
                mat_path = os.path.join(os.path.join(con_path, "Materials"), select_uuid)
                
                # Get the path to the image directory of the consolidation.
                img_path = os.path.join(mat_path, "Images")
                
                # Get the tree view for the metadata of material.
                tre_fl = self.tre_mat_fl
                
                # Get the selected image file.
                lst_fls = self.lst_mat_fls.currentItem().text()
            else:
                return(None)
        else:
            return(None)
        
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
            
            # Show preview.
            self.showImage(select_type, img_file_path)
        else:
            # Deselect the item.
            tre_fl.clearSelection()
            tre_fl.clear()
    
    def showImage(self, select_type, img_file_path):
        if select_type == "consolidation":
            lbl_img_preview = self.lbl_con_img_preview
            
        elif select_type == "material":
            lbl_img_preview = self.lbl_mat_img_preview
            
        else:
            return(None)
        
        # Get the file path to show.
        img_path = img_file_path
        
        # Check the image file can be displayed directry.
        img_base, img_ext = os.path.splitext(img_path)
        img_valid = False
        
        # Get container size.
        panel_w = lbl_img_preview.width()
        panel_h = lbl_img_preview.height()
        
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
            img_path = img_base + ".thumb.jpg"
        
        if os.path.exists(img_path):
            # Create the container for displaying the image
            org_pixmap = QPixmap(img_path)
            scl_pixmap = org_pixmap.scaled(panel_w, panel_h, Qt.KeepAspectRatio)
            
            # Set the image file to the image view container.
            lbl_img_preview.setPixmap(scl_pixmap)
                        
            # Show the selected image.
            lbl_img_preview.show()
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
    
    def toggleSelectedItem(self):
        # Check the selection status.
        check_select = self.checkSelection()
        
        # Get the selection status.
        if not check_select == None:
            # Translate resultants.
            select_type = check_select["selection"][0]
            select_uuid = check_select["selection"][1]
            select_item = check_select["selection"][2]
        else:
            # Exit if something happened in checking the selection status on tree view.
            return(None)
        
        if select_type == "consolidation":
            self.getConsolidation()
        elif select_type == "material":
            self.getMaterial()
    
    def checkSelection(self):
        global DATABASE
        global CON_DIR
        
        # Initialyze the value for the result.
        result = dict()
        
        if not ROOT_DIR == None:
            # Get the item of the material.
            selected = self.tre_prj_item.selectedItems()
            
            # Exit if selected item is 0.
            if len(selected) == 0:
                result["selection"] = [None, None, None]
                return(result)
            
            elif len(selected) > 0:
                if not selected[0].parent() == None:
                    result["selection"] = ["material", selected[0].text(0), selected[0]]
                    return(result)
                    
                    return(result)
                if selected[0].parent() == None:
                    result["selection"] = ["consolidation", selected[0].text(0), selected[0]]
                    return(result)
            else:
                # Create error messages.
                error_title = "統合体の取得エラー"
                error_msg = "統合体が選択されていません。"
                error_info = "ツリービューから統合体を再度選択してください。"
                error_icon = QMessageBox.Information
                error_detailed = None
                
                # Handle error.
                general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
                
                # Returns nothing.
                result["selection"] = [None, None, None]
                return(result)
        else:
            # Create error messages.
            error_title = "プロジェクトのエラー"
            error_msg = "プロジェクトが開かれていません。"
            error_info = "プロジェクトのディレクトリを参照し、指定ください。"
            error_icon = QMessageBox.Critical
            error_detailed = None
            
            # Handle error.
            general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
            
            # Returns nothing.
            result["selection"] = [None, None, None]
            return(result)
    
    def refreshImageFileList(self, search_dir, uuid, lst_fls):
        global CON_DIR
        global IMG_EXT
        global RAW_EXT
        
        # Clear the item list.
        lst_fls.clear()
        
        # Define the search path to the medium.
        path_img_main = os.path.join(search_dir, "Main")
        path_img_raw = os.path.join(search_dir, "Raw")
        path_img_thumb = os.path.join(search_dir, "Thumbs")
        
        # Get image files from the given directory.
        img_fls = general.getFilesWithExtensionList(path_img_main, IMG_EXT)
        raw_fls = general.getFilesWithExtensionList(path_img_raw, RAW_EXT)
        
        # Get general files from "Main".
        if img_fls > 0:
            for img_file in img_fls:
                img_item = QListWidgetItem(os.path.join("Main", img_file))
                lst_fls.addItem(img_item)
        
        # Get RAW files from "Raw".
        if raw_fls > 0:
            for raw_file in raw_fls:
                raw_item = QListWidgetItem(os.path.join("Raw", raw_file))
                lst_fls.addItem(raw_item)
    
    def refreshItemInfo(self):
        self.tre_mat_fl.clear()
        self.lst_mat_fls.clear()
        self.lbl_mat_img_preview.setText("")
        
        self.tre_con_fl.clear()
        self.lst_con_fls.clear()
        self.lbl_con_img_preview.setText("")
        
        return(None)
        
    # ==========================
    # object operation
    # ==========================
    def toggleEditModeForConsolidation(self):
        global ROOT_DIR
        
        try:
            if self.grp_con_ope.checkedId() == 0:
                # Clear the file list for consolidation.
                self.lst_con_fls.clearSelection()
                self.lst_con_fls.clear()
                
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
                
            elif self.grp_con_ope.checkedId() == 1:
                # Get the attributes of the selected consolidation.
                #if not ROOT_DIR == None: self.getConsolidation()
                
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
        except:
                # Connection error.
                error_title = "エラーが発生しました"
                error_msg = "統合体の編集モードを変更できません。"
                error_info = "不明のエラーです。"
                error_icon = QMessageBox.Critical
                error_detailed = None
                
                # Handle error.
                general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
                
                # Returns nothing.
                return(None)
    
    def toggleEditModeForMaterial(self):
        try:
            if self.grp_mat_ope.checkedId() == 0:
                # Clear the file list for consolidation.
                self.lst_mat_fls.clearSelection()
                self.lst_mat_fls.clear()
                
                # Only the add new material button enabled.
                self.btn_mat_add.setDisabled(False)
                self.btn_mat_del.setDisabled(True)
                self.btn_mat_take.setDisabled(True)
                self.btn_mat_update.setDisabled(True)
                
                # Text boxes for attributes are enabled.
                self.tbx_mat_name.setDisabled(False)
                self.tbx_mat_geo_lat.setDisabled(False)
                self.tbx_mat_geo_lon.setDisabled(False)
                self.tbx_mat_geo_alt.setDisabled(False)
                self.tbx_mat_tmp_bgn.setDisabled(False)
                self.tbx_mat_tmp_end.setDisabled(False)
                self.tbx_mat_description.setDisabled(False)
                
                # Change text color for text boxes.
                self.tbx_mat_name.setStyleSheet("color: rgb(255, 0, 0);")
                self.tbx_mat_geo_lat.setStyleSheet("color: rgb(255, 0, 0);")
                self.tbx_mat_geo_lon.setStyleSheet("color: rgb(255, 0, 0);")
                self.tbx_mat_geo_alt.setStyleSheet("color: rgb(255, 0, 0);")
                self.tbx_mat_tmp_bgn.setStyleSheet("color: rgb(255, 0, 0);")
                self.tbx_mat_tmp_end.setStyleSheet("color: rgb(255, 0, 0);")
                self.tbx_mat_description.setStyleSheet("color: rgb(255, 0, 0);")
                
                # Clear text boxes for attributes.
                self.tbx_mat_name.setText("")
                self.tbx_mat_geo_lat.setText("")
                self.tbx_mat_geo_lon.setText("")
                self.tbx_mat_geo_alt.setText("")
                self.tbx_mat_tmp_bgn.setText("")
                self.tbx_mat_tmp_end.setText("")
                self.tbx_mat_description.setText("")
                
            elif self.grp_mat_ope.checkedId() == 1:
                # Get the attributes of the selected material.
                # if not ROOT_DIR == None: self.getMaterial()
                
                # Only the add new consolidation button is disabled.
                self.btn_mat_add.setDisabled(True)
                self.btn_mat_update.setDisabled(False)
                self.btn_mat_take.setDisabled(False)
                self.btn_mat_del.setDisabled(False)
                
                # All text boxes for attributes of material is enabled.
                self.tbx_mat_name.setDisabled(False)
                self.tbx_mat_geo_lat.setDisabled(False)
                self.tbx_mat_geo_lon.setDisabled(False)
                self.tbx_mat_geo_alt.setDisabled(False)
                self.tbx_mat_tmp_bgn.setDisabled(False)
                self.tbx_mat_tmp_end.setDisabled(False)
                self.tbx_mat_description.setDisabled(False)
                
                # Change text color for text boxes.
                self.tbx_mat_name.setStyleSheet("color: rgb(0, 0, 0);")
                self.tbx_mat_geo_lat.setStyleSheet("color: rgb(0, 0, 0);")
                self.tbx_mat_geo_lon.setStyleSheet("color: rgb(0, 0, 0);")
                self.tbx_mat_geo_alt.setStyleSheet("color: rgb(0, 0, 0);")
                self.tbx_mat_tmp_bgn.setStyleSheet("color: rgb(0, 0, 0);")
                self.tbx_mat_tmp_end.setStyleSheet("color: rgb(0, 0, 0);")
                self.tbx_mat_description.setStyleSheet("color: rgb(0, 0, 0);")
        except:
                # Connection error.
                error_title = "エラーが発生しました"
                error_msg = "資料の編集モードを変更できません。"
                error_info = "不明のエラーです。"
                error_icon = QMessageBox.Critical
                error_detailed = None
                
                # Handle error.
                general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
                
                # Returns nothing.
                return(None)
    
    def getConsolidation(self):
        global DATABASE
        
        # Reflesh the last selection.
        self.refreshItemInfo()
        
        # Set active control tab for consolidation.
        self.tab_target.setCurrentIndex(0)
        
        # Deselect the file information for consolidations and materials.
        self.lst_con_fls.clearSelection()
        self.lst_mat_fls.clearSelection()
        
        # Clear the file list for consolidations and materials.
        self.lst_con_fls.clear()
        self.lst_mat_fls.clear()
        
        # Initialyze the edit consolidation mode as modifying.
        self.rad_con_mod.setChecked(True)
        self.toggleEditModeForConsolidation()
        
        # Check the selection status.
        check_select = self.checkSelection()
        
        # Get the selection status.
        if not check_select == None:
            # Translate resultants.
            select_type = check_select["selection"][0]
            select_uuid = check_select["selection"][1]
            select_item = check_select["selection"][2]
        else:
            # Exit if something happened in checking the selection status on tree view.
            return(None)
        
        if select_type == "consolidation":
            try:
                # Instantiate by the DB record.
                con = features.Consolidation(is_new=False, uuid=select_uuid, dbfile=DATABASE)
                
                # Set attributes to text boxes.
                self.tbx_con_name.setText(con.name)
                self.tbx_con_geoname.setText(con.geographic_annotation)
                self.tbx_con_temporal.setText(con.temporal_annotation)
                self.tbx_con_description.setText(con.description)
                
                # Refresh the consolidation files.
                con_img_path = os.path.join(os.path.join(CON_DIR, con.uuid), "Images")
                self.refreshImageFileList(con_img_path, con.uuid, self.lst_con_fls)
                
                # Set the first image for the preview image.
                self.lst_con_fls.setCurrentRow(0)
            except Error as e:
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
    
    def getMaterial(self):
        global DATABASE
        
        # Reflesh the last selection.
        self.refreshItemInfo()
        
        # Set active control tab for consolidation.
        self.tab_target.setCurrentIndex(1)
        
        # Deselect the file information for consolidations and materials.
        self.lst_con_fls.clearSelection()
        self.lst_mat_fls.clearSelection()
        
        # Clear the file list for consolidations and materials.
        self.lst_con_fls.clear()
        self.lst_mat_fls.clear()
        
        # Initialyze the edit material mode as modifying.
        self.rad_mat_mod.setChecked(True)
        self.toggleEditModeForMaterial()
        
        # Check the selection status.
        check_select = self.checkSelection()
        
        # Get the selection status.
        if not check_select == None:
            # Translate resultants.
            select_type = check_select["selection"][0]
            select_uuid = check_select["selection"][1]
            select_item = check_select["selection"][2]
        else:
            # Exit if something happened in checking the selection status on tree view.
            return(None)
        
        if select_type == "material":
            try:
                # Instantiate by the DB record.
                mat = features.Material(is_new=False, uuid=select_uuid, dbfile=DATABASE)
                
                # Set attributes to text boxes.
                self.tbx_mat_name.setText(mat.name)
                self.tbx_mat_tmp_bgn.setText(mat.estimated_period_beginning)
                self.tbx_mat_tmp_end.setText(mat.estimated_period_ending)
                self.tbx_mat_geo_lat.setText(mat.latitude)
                self.tbx_mat_geo_lon.setText(mat.longitude)
                self.tbx_mat_geo_alt.setText(mat.altitude)
                # self.tbx_mat_num.setText(mat_num)
                self.tbx_mat_description.setText(mat.description)
                
                # Refresh the material image files.
                con_path = os.path.join(CON_DIR, mat.consolidation)
                con_mat = os.path.join(os.path.join(con_path, "Materials"), mat.uuid)
                mat_img_path = os.path.join(con_mat,"Images")
                
                self.refreshImageFileList(mat_img_path, mat.uuid, self.lst_mat_fls)
                
                # Set the first image for the preview image.
                self.lst_mat_fls.setCurrentRow(0)
            except Error as e:
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
    
    def addConsolidation(self):
        global CON_DIR
        
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
            tre_prj_item_items.setText(2, con.description)
            
            # Refresh the tree view.
            self.tre_prj_item.show()
            
            # Change edit mode to modifying.
            self.rad_con_mod.setChecked(True)
            self.toggleEditModeForConsolidation()
        except:
            # Create error messages.
            error_title = "統合体の作成エラー"
            error_msg = "統合体の作成に失敗しました。"
            error_info = "不明なエラーです。"
            error_icon = QMessageBox.Information
            error_detailed = None
            
            # Handle error.
            general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
            
            # Returns nothing.
            return(None)
    
    def addMaterial(self):
        global CON_DIR
        
        # Check the selection state.
        check_select = self.checkSelection()
        
        if not check_select == None:
            # Translate resultants.
            select_type = check_select["selection"][0]
            select_uuid = check_select["selection"][1]
            select_item = check_select["selection"][2]
        else:
            # Exit if something happened in checking the selection status on tree view.
            # Create error messages.
            error_title = "資料の作成エラー"
            error_msg = "資料の作成ができません。"
            error_info = "資料を包括する統合体を選択してください。"
            error_icon = QMessageBox.Information
            error_detailed = None
            
            # Handle error.
            general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
            
            return(None)
        
        if select_type == "material":
            # Initialize the Consolidation Class.
            con_uuid = select_item.parent().text(0)
            
            # Confirm whether select the parent consolidations.
            reply = QMessageBox.question(
                    self, 
                    '資料を内包する統合体が指定されていません。', 
                    u"現在の統合体（" + con_uuid + u"）に新規資料を追加しますか？", 
                    QMessageBox.Yes, 
                    QMessageBox.No
                )
            # Handle the return value.
            if reply == QMessageBox.Yes:
                # Set tree view item from parent node.
                tre_prj_item_items = QTreeWidgetItem(select_item.parent())
            else:
                return(None)
        elif select_type == "consolidation":
            # Get the current consolidation from the selection.
            con_uuid = select_uuid
            
            # Get the current consolidation from the selection.
            tre_prj_item_items = QTreeWidgetItem(select_item)
        else:
            return(None)
        
        try:
            # Generate the GUID for the material
            mat = features.Material(is_new=True, uuid=None, dbfile=None)
            
            # Get attributes from text boxes.
            mat.consolidation = con_uuid
            mat.name = self.tbx_mat_name.text()
            mat.estimated_period_beginning = self.tbx_mat_tmp_bgn.text()
            mat.estimated_period_ending = self.tbx_mat_tmp_end.text()
            mat.latitude = self.tbx_mat_geo_lat.text()
            mat.longitude = self.tbx_mat_geo_lon.text()
            mat.altitude = self.tbx_mat_geo_alt.text()
            # mat.material_number = 
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
            tre_prj_item_items.setText(2, mat.description)
            
            self.tre_prj_item.show()
        except:
            # Create error messages.
            error_title = "資料の作成エラー"
            error_msg = "資料の作成に失敗しました。"
            error_info = "不明なエラーです。"
            error_icon = QMessageBox.Information
            error_detailed = None
            
            # Handle error.
            general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
            
            # Returns nothing.
            return(None)
    
    def updateConsolidation(self):
        # Check the selection state.
        check_select = self.checkSelection()
        
        if not check_select == None:
            # Translate resultants.
            select_type = check_select["selection"][0]
            select_uuid = check_select["selection"][1]
            select_item = check_select["selection"][2]
        else:
            # Exit if something happened in checking the selection status on tree view.
            return(None)
        
        if select_type == "consolidation":
            try:
                # Initialize the Consolidation Class.
                con = features.Consolidation(is_new=False, uuid=select_uuid, dbfile=DATABASE)
                
                # Instantiate the consolidation class
                con.name = self.tbx_con_name.text()
                con.geographic_annotation = self.tbx_con_geoname.text()
                con.temporal_annotation = self.tbx_con_temporal.text()
                con.description = self.tbx_con_description.text()
                
                # Update the instance into DBMS.
                con.dbUpdate(DATABASE)
                
                # Update the tree view.
                select_item.setText(1, con.name)
                select_item.setText(2, con.description)
                
                # Refresh the tree view.
                self.tre_prj_item.show()
            except:
                # Create error messages.
                error_title = "統合体の更新エラー"
                error_msg = "統合体の更新に失敗しました。"
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
    
    def updateMaterial(self):
        # Check the selection state.
        check_select = self.checkSelection()
        
        if not check_select == None:
            # Translate resultants.
            select_type = check_select["selection"][0]
            select_uuid = check_select["selection"][1]
            select_item = check_select["selection"][2]
        else:
            # Exit if something happened in checking the selection status on tree view.
            # Create error messages.
            error_title = "資料の更新エラー"
            error_msg = "資料の更新ができません。"
            error_info = "資料を包括する統合体を選択してください。"
            error_icon = QMessageBox.Information
            error_detailed = None
            
            # Handle error.
            general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
            
            # Returns nothing.
            return(None)
        
        if select_type == "material":
            try:
                # Generate the GUID for the material
                mat = features.Material(is_new=False, uuid=select_uuid, dbfile=DATABASE)
                
                # Get attributes from text boxes.
                mat.name = self.tbx_mat_name.text()
                mat.estimated_period_beginning = self.tbx_mat_tmp_bgn.text()
                mat.estimated_period_ending = self.tbx_mat_tmp_end.text()
                mat.latitude = self.tbx_mat_geo_lat.text()
                mat.longitude = self.tbx_mat_geo_lon.text()
                mat.altitude = self.tbx_mat_geo_alt.text()
                # mat.material_number = 
                mat.description = self.tbx_mat_description.text()
                
                # Create the SQL query for updating the new consolidation.
                mat.dbUpdate(DATABASE)
                
                # Update the tree view.
                select_item.setText(1, mat.name)
                select_item.setText(2, mat.description)
                
                # Refresh the tree view.
                self.tre_prj_item.show()
            except:
                # Create error messages.
                error_title = "資料の更新エラー"
                error_msg = "資料の更新に失敗しました。"
                error_info = "不明なエラーです。"
                error_icon = QMessageBox.Information
                error_detailed = None
                
                # Handle error.
                general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
                
                # Returns nothing.
                return(None)
        else:
            # Create error messages.
            error_title = "資料の更新エラー"
            error_msg = "資料の更新に失敗しました。"
            error_info = "更新対象の資料が選択されていません。"
            error_icon = QMessageBox.Information
            error_detailed = None
            
            # Handle error.
            general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
            
            # Returns nothing.
            return(None)
    
    def deleteConsolidation(self):
        global CON_DIR
        
        # Check the selection status.
        check_select = self.checkSelection()
        
        # Get the selection status.
        if not check_select == None:
            # Translate resultants.
            select_type = check_select["selection"][0]
            select_uuid = check_select["selection"][1]
            select_item = check_select["selection"][2]
        else:
            # Exit if something happened in checking the selection status on tree view.
            return(None)
        
        if select_type == "consolidation":
            # Confirm deletion.
            reply = QMessageBox.question(
                    self, 
                    '統合体の削除', 
                    '統合体が内包する全ての資料およびデータが削除されます。本当に削除しますか？', 
                    QMessageBox.Yes, 
                    QMessageBox.No
                )
            
            # Confirm deleting the consolidation.
            if not reply == QMessageBox.Yes:
                return(None)
            
            try:
                # Remove the consolidation from the tree view.
                root = self.tre_prj_item.invisibleRootItem()
                
                # Update the tree view.
                root.removeChild(select_item)
                
                # Clear selection.
                self.tre_prj_item.clearSelection()
                
                # Refresh the tree view.
                self.tre_prj_item.show()
                
                # Delete all files from consolidation directory.
                shutil.rmtree(os.path.join(CON_DIR,select_uuid))
                
                # Initialize the Consolidation Class.
                con = features.Consolidation(is_new=False, uuid=select_uuid, dbfile=DATABASE)
                
                # Drop the consolidation from the DB table.
                con.dbDrop(DATABASE)
                
                # Reflesh the last selection.
                self.refreshItemInfo()
            except:
                # Create error messages.
                error_title = "統合体の削除エラー"
                error_msg = "統合体の削除に失敗しました。"
                error_info = "不明なエラーです。"
                error_icon = QMessageBox.Information
                error_detailed = None
                
                # Handle error.
                general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
                
                # Returns nothing.
                return(None)
    
    def deleteMaterial(self):
        global CON_DIR
        
        # Check the selection status.
        check_select = self.checkSelection()
        
        # Get the selection status.
        if not check_select == None:
            # Translate resultants.
            select_type = check_select["selection"][0]
            select_uuid = check_select["selection"][1]
            select_item = check_select["selection"][2]
        else:
            # Exit if something happened in checking the selection status on tree view.
            return(None)
        
        if select_type == "material":
            # Confirm deleting the consolidation.
            reply = QMessageBox.question(
                    self, 
                    '資料の削除', 
                    '資料が内包する全てのデータが削除されます。本当に削除しますか？', 
                    QMessageBox.Yes, 
                    QMessageBox.No
                )
            if not reply == QMessageBox.Yes:
                return(None)
            
            try:
                # Get the directory storing information about the material
                con_uuid = select_item.parent().text(0)
                
                # Update the tree view.
                select_item.parent().removeChild(select_item)
                
                # Clear selection.
                self.tre_prj_item.clearSelection()
                
                # Refresh the tree view.
                self.tre_prj_item.show()
                
                # Delete all files from consolidation directory.
                con_mat_path = os.path.join(os.path.join(CON_DIR,con_uuid),"Materials")
                mat_path = os.path.join(con_mat_path, select_uuid)
                
                # Delete files.
                shutil.rmtree(mat_path)
                
                # Generate the GUID for the material
                mat = features.Material(is_new=False, uuid=select_uuid, dbfile=DATABASE)
                
                # Drop the consolidation from the DB table.
                mat.dbDrop(DATABASE)
                
                # Reflesh the last selection.
                self.refreshItemInfo()
            except:
                # Create error messages.
                error_title = "資料の削除エラー"
                error_msg = "資料の削除に失敗しました。"
                error_info = "不明なエラーです。"
                error_icon = QMessageBox.Information
                error_detailed = None
                
                # Handle error.
                general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
                
                # Returns nothing.
                return(None)
    
    # ==========================
    # Cemera operation
    # ==========================
    def detectCamera(self):
        # Detect the connected camera.
        cams = imageProcessing.detectCam()
        
        for cam in cams:
            print(cam)
        
        cam = cam[0]
        
        # Display the camera information.
        if not cam == None:
            # Set the connected camera to the header.
            self.lbl_cam_detected.setStyleSheet("color: rgb(0, 0, 0);")
            self.lbl_cam_detected.setText(cam)
            
            # Get camera parameter for the image size. 
            cam_size = imageProcessing.getConfig("imagesize")
            cam_iso = imageProcessing.getConfig("iso")
            cam_wht = imageProcessing.getConfig("whitebalance")
            cam_exp = imageProcessing.getConfig("exposurecompensation")
            cam_fval = imageProcessing.getConfig("f-number")
            cam_qoi = imageProcessing.getConfig("imagequality")
            cam_fmod = imageProcessing.getConfig("focusmode")
            cam_epg = imageProcessing.getConfig("expprogram")
            cam_cpt = imageProcessing.getConfig("capturemode")
            cam_met = imageProcessing.getConfig("exposuremetermode")
            
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
            
            # Returns the current camera.
            return(cam)
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
                cbx.addItem(opt_val + " : " + opt_txt)
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
        global TMP_DIR
        global CON_DIR
        global TETHERED
                
        # Check the selection status.
        check_select = self.checkSelection()
        
        # Get the selection status.
        if not check_select == None:
            # Translate resultants.
            select_type = check_select["selection"][0]
            select_uuid = check_select["selection"][1]
            select_item = check_select["selection"][2]
        else:
            # Exit if something happened in checking the selection status on tree view.
            return(None)
        
        # Get the current consolidation.
        item_uuid = select_uuid
        
        if select_type == "consolidation":
            # Define the path to the consolidation.
            item_path = os.path.join(CON_DIR, item_uuid)
            lst_fls = self.lst_con_fls
            
        elif select_type == "material":
            # Get the consolidation uuid.
            con_uuid = select_item.parent().text(0)
            con_path = os.path.join(CON_DIR, con_uuid)
            
            # Get the item path under the consolidaiton path.
            item_path = os.path.join(os.path.join(con_path, "Materials"),item_uuid)
            lst_fls = self.lst_mat_fls
        else:
            return(None)
        
        # Check the result of the tethered image.
        print(os.path.exists(item_path))
        
        self.dialogRecording = RecordWithImage(parent=self, path=item_path)
        
        isAccepted = self.dialogRecording.exec_()
    
    def tetheredShooting(self):
        global TMP_DIR
        global CON_DIR
        global TETHERED
        
        # Initialyze the temporal directory.
        tethered_path = os.path.join(TMP_DIR, "tethered")
        if not os.path.exists(tethered_path):
            # Create the temporal directory if not exists.
            os.mkdir(tethered_path)
        else:
            # Delete the existing temporal directory before create.
            shutil.rmtree(tethered_path)
            os.mkdir(tethered_path)
        
        # Check the selection status.
        check_select = self.checkSelection()
        
        # Get the selection status.
        if not check_select == None:
            # Translate resultants.
            select_type = check_select["selection"][0]
            select_uuid = check_select["selection"][1]
            select_item = check_select["selection"][2]
        else:
            # Exit if something happened in checking the selection status on tree view.
            return(None)
        
        # Get the current consolidation.
        item_uuid = select_uuid
        
        if select_type == "consolidation":
            # Define the path to the consolidation.
            item_path = os.path.join(CON_DIR, item_uuid)
            lst_fls = self.lst_con_fls
            
        elif select_type == "material":
            # Get the consolidation uuid.
            con_uuid = select_item.parent().text(0)
            con_path = os.path.join(CON_DIR, con_uuid)
            
            # Get the item path under the consolidaiton path.
            item_path = os.path.join(os.path.join(con_path, "Materials"),item_uuid)
            lst_fls = self.lst_mat_fls
        else:
            return(None)
        
        # Define the path for saving images.
        img_path = os.path.join(item_path, "Images")
        
        # Generate the GUID for the consolidation
        pht_uuid = str(uuid.uuid4()) 
        
        if not imageProcessing.detectCam() == None:
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
            
            if isAccepted == 1:
                # Define the path for images.
                img_main = os.path.join(img_path, "Main")
                img_raw = os.path.join(img_path, "Raw")
                
                # Move to proper directory.
                if len(img_lst_main) > 0:
                    for i in range(0, len(img_lst_main)):
                        main_orig = os.path.join(tethered_path, img_lst_main[i])
                        main_dest = os.path.join(img_main, img_lst_main[i])
                        
                        # Move to "Main" in the consolidation.
                        shutil.move(main_orig, main_dest)
                
                if len(img_lst_raw) > 0:
                    for j in range(0, len(img_lst_raw)):
                        raw_orig = os.path.join(tethered_path, img_lst_raw[j])
                        raw_dest = os.path.join(img_raw, img_lst_raw[j])
                        
                        # Move to "Raw" in the consolidation.
                        shutil.move(raw_orig, raw_dest)
            
            # Remove tethered path from the temporal directory.
            shutil.rmtree(tethered_path)
            
            # Refresh the consolidation file list view.
            self.refreshImageFileList(img_path, item_uuid, lst_fls)
        else:
            # Create error messages.
            error_title = "エラーが発生しました"
            error_msg = "カメラが接続されていません。"
            error_info = "カメラの接続を確認し、再度、撮影ボタンを押下してください。"
            error_icon = QMessageBox.Critical
            error_detailed = None
            
            # Handle error.
            general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
           
            # Returns nothing.
            return(None)

def main():
    app = QApplication(sys.argv)
    form = mainPanel()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
