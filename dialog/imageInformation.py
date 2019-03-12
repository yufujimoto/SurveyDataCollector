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
import modules.skin as skin

# Import camera and image processing library.
import modules.imageProcessing as imageProcessing
import dialog.imageInformationDialog as imageInformationDialog

# Import image viewer object.
import viewer.imageViewer as viewer

class imageInformationDialog(QDialog, imageInformationDialog.Ui_imageInformationDialog):
    @property
    def source_directory(self): return self._source_directory
    @property
    def database(self): return self._database
    @property
    def config_file(self): return self._config_file
    @property
    def siggraph_directory(self): return self._siggraph_directory
    @property
    def icon_directory(self): return self._icon_directory
    @property
    def temporal_directory(self): return self._temporal_directory
    @property
    def root_directory(self): return self._root_directory
    
    @source_directory.setter
    def source_directory(self, value): self._source_directory = value
    @database.setter
    def database(self, value): self._database = value
    @config_file.setter
    def config_file(self, value): self._config_file = value
    @siggraph_directory.setter
    def siggraph_directory(self, value): self._siggraph_directory = value
    @icon_directory.setter
    def icon_directory(self, value): self._icon_directory = value
    @temporal_directory.setter
    def temporal_directory(self, value): self._temporal_directory = value
    @root_directory.setter
    def root_directory(self, value): self._root_directory = value
    @property
    def qt_image(self): return self._qt_image
    @property
    def language(self): return self._language
    
    @qt_image.setter
    def qt_image(self, value): self._qt_image = value
    @language.setter
    def language(self, value): self._language = value
    
    def __init__(self, parent=None, sop_file=None):
        # Get the path of the tethered image.
        self._sop_file = sop_file
        self._qt_image = parent.qt_image
        self._language = parent.language
        self._source_directory = parent.source_directory
        self._root_directory = parent.root_directory
        self._database  = parent.database
        
        # Set the source directory which this program located.
        super(imageInformationDialog, self).__init__(parent)
        self.setupUi(self)
        
        # Initialize the window.
        self.setWindowTitle(self.tr("File Information Dialog"))
        
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
            icon_path = os.path.join(parent.icon_directory, "white")
            
            # Set the default background and front color.
            back_color = 'background-color: #2C2C2C;'
            font_style_color = 'color: #FFFFFF;'
            font_style = font_style_color + font_style_size
            
            # Set the default skin for all components.
            self.setStyleSheet(back_color + font_style + 'border-style: none; border-color: #4C4C4C;')
            self.frame.setStyleSheet(back_color + font_style + 'border-style: none; border-color: #4C4C4C;')
            
            # Set the default skin for text boxes.
            text_border = 'border-style: outset; border-width: 0.5px; border-color: #4C4C4C;'
            text_background = "background-color: #6C6C6C;"
            self.cmb_fil_stts.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            self.tbx_fil_ali.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            
            self.dte_fil_dt_cre.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            self.dte_fil_dt_mod.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            self.cmb_fil_eope.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            self.tbx_fil_ope_app.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            self.tbx_fil_dsc.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            self.tbx_fil_capt.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        elif skin == "white":
            # Set the icon path.
            icon_path = os.path.join(parent.icon_directory, "black")
            
            # Set the icon path.
            parent.icon_directory = os.path.join(parent.icon_directory, "black")
        
        
        # Add the text label to the tab
        if self._language == "ja":
            self.cbx_fil_pub.setText("公開設定")
            self.cbx_fil_edit.setText("削除可能")
            self.lab_fil_sta.setText("ステータス")
            self.lab_fil_ali.setText("別　名 :")
            self.lab_fil_dt_cr.setText("作成日時 :")
            self.lab_fil_dt_mod.setText("編集日時 :")
            self.lab_fil_ope.setText("操　作 :")
            self.lab_fil_ope_app.setText("操作アプリ :")
            self.lab_fil_cap.setText("キャプション :")
            self.lbl_fil_dsc.setText("備　考 :")
            self.btn_fil_dt_cre_exif.setText("Exifから取得")
            self.btn_fil_dt_mod_exif.setText("Exifから取得")
            self.box_fil_ope.buttons()[0].setText("OK")
            self.box_fil_ope.buttons()[1].setText("キャンセル")
        elif self._language == "en":
            self.cbx_fil_pub.setText("Public")
            self.cbx_fil_edit.setText("Erasable")
            self.lab_fil_sta.setText("Status")
            self.lab_fil_ali.setText("Alias :")
            self.lab_fil_dt_cr.setText("Date of Create :")
            self.lab_fil_dt_mod.setText("Date of Edit :")
            self.lab_fil_ope.setText("Operation :")
            self.lab_fil_ope_app.setText("Application :")
            self.lab_fil_cap.setText("Caption :")
            self.lbl_fil_dsc.setText("Description :")
            self.btn_fil_dt_cre_exif.setText("Get from Exif")
            self.btn_fil_dt_mod_exif.setText("Get from Exif")
            self.box_fil_ope.buttons()[0].setText("OK")
            self.box_fil_ope.buttons()[1].setText("Cancel")
        
        # Change the default icons for dialoc button box.
        self.box_fil_ope.buttons()[0].setFlat(True)
        self.box_fil_ope.buttons()[1].setFlat(True)
        
        # Set the dialog button size.
        dlg_btn_size = QSize(125, 30)
        self.box_fil_ope.buttons()[0].setMinimumSize(dlg_btn_size)
        self.box_fil_ope.buttons()[1].setMinimumSize(dlg_btn_size)
        
        # Set the skin and icon.
        self.box_fil_ope.buttons()[0].setIcon(skin.getIconFromPath(os.path.join(icon_path, 'check.png')))
        self.box_fil_ope.buttons()[1].setIcon(skin.getIconFromPath(os.path.join(icon_path, 'close.png')))
        
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
        
        # Set the operation of the file object and option values.
        self.cmb_fil_eope.addItem(self._sop_file.operation)
        self.cmb_fil_eope.addItem("Editing on GIMP")
        self.cmb_fil_eope.addItem("Rotating")
        self.cmb_fil_eope.addItem("Grayscaling")
        self.cmb_fil_eope.addItem("White balance adjusting")
        self.cmb_fil_eope.addItem("Normalizing")
        self.cmb_fil_eope.addItem("Cropping")
        self.cmb_fil_eope.addItem("Color inverting")
        self.cmb_fil_eope.addItem("Removing")
        self.cmb_fil_eope.addItem("Colorlizing")
        self.cmb_fil_eope.addItem("Unknown")
        self.cmb_fil_eope.addItem("Other")
        
        if self._sop_file.file_type == "image":
            # Get the path from selected image object.
            img_file_path = os.path.join(parent.root_directory, self._sop_file.filename)
            
            if self.imageIsValid(img_file_path) == True:
                # Add a tab for the thumbnail.
                self.tab_img_thumb = QWidget()
                self.tab_img_thumb.setLayoutDirection(Qt.LeftToRight)
                self.tab_img_thumb.setObjectName("tab_img_thumb")
                
                # Add a tab for the image viewer
                self.tab_img_view = QWidget()
                self.tab_img_view.setLayoutDirection(Qt.LeftToRight)
                self.tab_img_view.setObjectName("tab_img_view")
                self.tab_img_view.setAccessibleName("tab_img_view")
                
                # Add the layout for image viewer.
                self.lay_img_view = QVBoxLayout(self.tab_img_view)
                self.lay_img_view.setContentsMargins(0, 0, 0, 0)
                self.lay_img_view.setObjectName("lay_thm")
                
                # Add the layout for image viewer.
                self.lay_img_thumb = QVBoxLayout(self.tab_img_thumb)
                self.lay_img_thumb.setContentsMargins(0, 0, 0, 0)
                self.lay_img_thumb.setObjectName("lay_thm")
                
                self.lbl_img_thumb = QLabel()
                self.lbl_img_thumb.setAlignment(Qt.AlignCenter)
                self.lbl_img_thumb.setObjectName("lbl_img_thumb")
                
                self.lay_img_thumb.addWidget(self.lbl_img_thumb)
                
                # Add the layout to the tab.
                self.tab_src.addTab(self.tab_img_thumb, "")
                
                # Add the layout to the tab.
                self.tab_src.addTab(self.tab_img_view, "")
                
                # Create the graphic view item.        
                self.graphicsView = viewer.ImageViewer()
                self.graphicsView.setObjectName("graphicsView")
                self.lay_img_view.addWidget(self.graphicsView)
                
                
                # Add the text label to the tab
                if self._language == "ja":
                    self.tab_src.setTabText(self.tab_src.indexOf(self.tab_img_thumb),"サムネイル")
                    self.tab_src.setTabText(self.tab_src.indexOf(self.tab_img_view),"画像ビューア")
                elif self._language == "en":
                    self.tab_src.setTabText(self.tab_src.indexOf(self.tab_img_thumb),"Thumbnail")
                    self.tab_src.setTabText(self.tab_src.indexOf(self.tab_img_view),"Image Viewer")
                
                if parent.skin == "grey":
                    # Set the icon path.
                    icon_path = os.path.join(parent.icon_directory, "white")
                    
                    # Set the default skin for tabs.
                    back_color_tab = 'QTabBar::tab {background-color: #2C2C2C; }'
                    back_color_tab_act = 'QTabBar::tab::selected {background-color: #4C4C4C;}'
                    self.tab_src.setStyleSheet(back_color_tab + back_color_tab_act)
                    
                
                # Get the image file.
                self.showImage()
        
    def toggleTab(self):
        print("information::toggleTab(self)")
        try:
            # Get the currently selected tab name.
            current_tab = self.tab_src.tabText(self.tab_src.currentIndex())
            
            if self._language == "ja":
                if current_tab == u"画像ビューア":
                    self.setViewer()
                
            elif self._language == "en":
                if current_tab == u"Image Viewer":
                    self.setViewer()
        except Exception as e:
            print(str(e))
    
    def showImage(self):
        print("imageInformationDialog::showImage(self)")
        
        try:
            # Get the full path of the image.
            if not os.path.exists(os.path.join(self._root_directory, self._sop_file.filename)):
                img_file_path = os.path.join(os.path.join(self._source_directory, "images"),"noimage.jpg")
            else:
                img_file_path = os.path.join(self._root_directory, self._sop_file.filename)
            
            # Get container size.
            panel_w = self.lbl_img_thumb.width()
            panel_h = self.lbl_img_thumb.height()
            
            # Check whether the image is Raw image or not.
            if not self.imageIsValid(img_file_path) == True:
                # Extract the thumbnail image from the RAW image by using "dcraw".
                imageProcessing.getThumbnail(img_file_path)
                
                # Get the extracted thumbnail image.
                img_file_path = os.path.splitext(img_file_path)[0] + ".thumb.jpg"
            
            if os.path.exists(img_file_path):
                
                # Create the container for displaying the image
                org_pixmap = QPixmap(img_file_path)
                scl_pixmap = org_pixmap.scaled(panel_w, panel_h, Qt.KeepAspectRatio)
                
                # Set the image file to the image view container.
                self.lbl_img_thumb.setPixmap(scl_pixmap)
                
                # Show the selected image.
                self.lbl_img_thumb.show()
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
        except Exception as e:
            print("Error occurs in imageInformationDialog::showImage(self)")
            
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
            print("Error occurs in imageInformationDialog::setViewer(self)")
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
            print("Error occurs in imageProcessing::getMetaInfo(img_input)")
            print(str(e))
            
            return(None)
