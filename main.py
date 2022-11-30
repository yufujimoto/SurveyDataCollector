#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Import general libraries.
import sys, os, uuid, shutil, time, math, tempfile, logging, datetime, gc, json
import xml.etree.cElementTree as ET
import geodaisy.converters as convert
import gphoto2 as gp

from os.path import expanduser

# Import PyQt5 libraries for generating the GUI application.
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QThread, pyqtSignal
#from PyQt5.QtWebKit import *
#from PyQt5.QtWebKitWidgets import *
from PyQt5.QtWebEngine import *

from PyQt5.QtNetwork import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

# Import GIS libraries for showing geographic data.
import numpy as np

# Import DB libraries
import sqlite3 as sqlite
from sqlite3 import Error as dbError

# Import general operations.
import modules.camera as camera
import modules.general as general
import modules.features as features
import modules.media as sop_media
import modules.error as error
import modules.setupMainUi as setupMainUi
import modules.setupMainSkin as setupMainSkin
import modules.imageProcessing as imageProcessing
import modules.writeHtml as htmlWriter
import modules.geospatial as geospatial
import modules.flickr_upload as flickr

# Import GUI window.
import dialog.mainWindow as mainWindow
import dialog.configuration as configurationDialog
import dialog.consolidation as consolidationDialog
import dialog.material as materialDialog
import dialog.checkTetheredImage as checkTetheredImageDialog
import dialog.recordWithPhoto as recordWithPhotoDiaolog
import dialog.fileInformation as fileInformationDialog
import dialog.fileToObjects as fileToObjectsDialog
import dialog.textEditWithPhoto as textEditWithPhoto
import dialog.cameraSelect as cameraSelectDialog
import dialog.flickr as flickrDialog

# Import libraries for sound recording.
import queue
import sounddevice as sd
import soundfile as sf

# Labels for Consolidation and Material
LAB_CON = u"統合体"
LAB_MAT = u"資料"

# Connected devices.
CUR_CAM = None

class mainPanel(QMainWindow, mainWindow.Ui_MainWindow):
    @property
    def source_directory(self): return self._source_directory
    @property
    def config_file(self): return self._config_file
    @property
    def siggraph_directory(self): return self._siggraph_directory
    @property
    def map_directory(self): return self._map_directory
    @property
    def icon_directory(self): return self._icon_directory
    @property
    def temporal_directory(self): return self._temporal_directory
    @property
    def root_directory(self): return self._root_directory
    @property
    def lib_directory(self): return self._lib_directory
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
    @property
    def current_consolidation(self): return self._current_consolidation
    @property
    def current_material(self): return self._current_material
    @property
    def current_file(self): return self._current_file
    @property
    def current_camera(self): return self._current_camera
    @property
    def gp_camera(self): return self._gp_camera
    @property
    def gp_context(self): return self._gp_context
    @property
    def awb_algo(self): return self._awb_algo
    @property
    def psp_algo(self): return self._psp_algo
    @property
    def ocr_lang_available(self): return self._ocr_lang_available
    @property
    def ocr_lang(self): return self._ocr_lang
    @property
    def ocr_psm(self): return self._ocr_psm
    @property
    def language(self): return self._language
    @property
    def skin(self): return self._skin
    @property
    def proxy(self): return self._proxy
    @property
    def flickr_apikey(self): return self._flickr_apikey
    @property
    def flickr_secret(self): return self._flickr_secret
    @property
    def map_tile(self): return self._map_tile
    @property
    def app_textEdit(self): return self._app_textEdit
    @property
    def image_file_operation(self): return self._image_file_operation
    @property
    def text_file_operation(self): return self._text_file_operation

    @source_directory.setter
    def source_directory(self, value): self._source_directory = value
    @config_file.setter
    def config_file(self, value): self._config_file = value
    @siggraph_directory.setter
    def siggraph_directory(self, value): self._siggraph_directory = value
    @map_directory.setter
    def map_directory(self, value): self._map_directory = value
    @icon_directory.setter
    def icon_directory(self, value): self._icon_directory = value
    @temporal_directory.setter
    def temporal_directory(self, value): self._temporal_directory = value
    @root_directory.setter
    def root_directory(self, value): self._root_directory = value
    @lib_directory.setter
    def lib_directory(self, value): self._lib_directory = value
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
    @current_consolidation.setter
    def current_consolidation(self, value): self._current_consolidation = value
    @current_material.setter
    def current_material(self, value): self._current_material = value
    @current_file.setter
    def current_file(self, value): self._current_file = value
    @current_camera.setter
    def current_camera(self, value): self._current_camera = value
    @gp_camera.setter
    def gp_camera(self, value): self._gp_camera = value
    @gp_context.setter
    def gp_context(self, value): self._gp_context = value
    @awb_algo.setter
    def awb_algo(self, value): self._awb_algo = value
    @psp_algo.setter
    def psp_algo(self, value): self._psp_algo = value
    @ocr_lang_available.setter
    def ocr_lang_available(self, value): self._ocr_lang_available = value
    @ocr_lang.setter
    def ocr_lang(self, value): self._ocr_lang = value
    @ocr_psm.setter
    def ocr_psm(self, value): self._ocr_psm = value
    @language.setter
    def language(self, value): self._language = value
    @skin.setter
    def skin(self, value): self._skin = value
    @proxy.setter
    def proxy(self, value): self._proxy = value
    @flickr_apikey.setter
    def flickr_apikey(self, value): self._flickr_apikey = value
    @flickr_secret.setter
    def flickr_secret(self, value): self._flickr_secret = value
    @map_tile.setter
    def map_tile(self, value): self._map_tile = value
    @app_textEdit.setter
    def app_textEdit(self, value): self._app_textEdit = value
    @image_file_operation.setter
    def image_file_operation(self, value): self._image_file_operation = value
    @text_file_operation.setter
    def text_file_operation(self, value): self._text_file_operation = value

    def __init__(self, parent=None):
        print("Start -> main::__init__(self, parent=None)")

        try:
            # Clear memory
            gc.collect()

            # Make this class as the super class and initialyze the class.
            super(mainPanel, self).__init__(parent)
            self.setupUi(self)

            # Initialyze the window.
            self.setWindowState(Qt.WindowMaximized)     # Show as maximized.

            # Hide uuid columns from tree widgets.
            #self.tre_prj_item.hideColumn(0)
            self.tre_fls.hideColumn(0)

            # Activate modules.
            print("## Initialize UI objects and functions.")
            setupMainUi.activate(self)

            # Initialyze the source paths.
            print("## Initialize parameters.")
            print("### Paths for souces...")
            dir_src = os.path.dirname(os.path.abspath(__file__))
            dir_lib = os.path.join(dir_src, "lib")
            dir_sig = os.path.join(os.path.expanduser("~"),"siggraph")
            dir_map = os.path.join(dir_src, "map")
            dir_tmp = os.path.join(dir_src, "temp")
            dir_icn = os.path.join(dir_src, "icon")
            fil_cnf = os.path.join(dir_src, "config.xml")

            # Initialyze properties.
            print("### Parameters...")
            general.initAll(self, dir_src, dir_lib, dir_sig, dir_map, dir_tmp, dir_icn, fil_cnf)

            # Initialyze the proxy setting
            print("### Proxy...")
            self.setProxy()

            # Initialyze the map viewer
            print("### Map...")
            self.setDefaultMap()

            # Set the default skin.
            print("### UI Skin...")
            self.setSkin(lang=self._language, theme=self._skin)

            # Detect the camera automatically
            print("## Set Camera...")
            self.detectCamera()

            # Open the previous project.
            print("## Now opening the project...")
            if not self._database == None:
                if os.path.exists(self._database):
                    self.openProject()

        except Exception as e:
            print("Error occured in main::__init__(self, parent=None)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

        finally:
            print("End -> main::__init__(self, parent=None)")

    # ==========================
    # General operation
    # ==========================
    def openProject(self):
        print("Start -> main::openProject(self)")

        try:
            # Establish the connection to the self._database file.
            conn = sqlite.connect(self._database)

            if conn is not None:
                # Check whether table exists or not.
                general.checkExistenceOfTables(self._database)

                # Check wether columns exists or not.
                general.checkFieldsOfTables(self.database)

                # Reconstruct the tree view for project items.
                self.retriveProjectItems()

                # Update the configuration file.
                general.changeConfig(self)

                # Set the top item.
                if self.tre_prj_item.topLevelItemCount() > 0:
                    self.tre_prj_item.setCurrentItem(self.tre_prj_item.topLevelItem(0))
        except sqlite.DatabaseError as e:
            print("Error occured in main::openProject(self)")
            print(str(e))
            error.ErrorMessageDbConnection(details=str(e), language=self._language)
            return(None)

        finally:
            # Finally set the root path to the text box.
            if not self.root_directory == None:
                self.lbl_prj_path.setText(self._root_directory)
            print("End -> main::openProject(self)")

    def retriveProjectItems(self):
        print("Start -> main::retriveProjectItems(self)")

        # Create a sqLite file if not exists.
        try:
            # Establish the connection to the self._database file.
            conn = sqlite.connect(self._database)

            # Exit if connection is not established.
            if conn == None: return(None)

            # Create the SQL query for selecting consolidation.
            sql_con_sel = """SELECT uuid, name, description, id FROM consolidation ORDER BY id"""

            # Create the SQL query for selecting the consolidation.
            sql_mat_sel = """SELECT uuid, name, description, id FROM material WHERE con_id=? ORDER by id"""

            # Instantiate the cursor for query.
            cur_con = conn.cursor()
            rows_con = cur_con.execute(sql_con_sel)

            # Execute the query and get consolidation recursively
            for row_con in rows_con:
                # Get attributes from the row.
                con_uuid = row_con[0]
                con_name = row_con[1]
                con_description = row_con[2]

                print("# Get the consolidation:" + con_uuid)

                # Convert the NULL value to the empty entry.
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

                    print("# Get the material:" + mat_uuid)

                    # Convert the NULL value to the empty entry.
                    if mat_uuid == None or mat_uuid == "NULL": mat_uuid = ""
                    if mat_name == None or mat_name == "NULL": mat_name = ""
                    if mat_description == None or mat_description == "NULL": mat_description = ""

                    # Update the tree view.
                    tre_prj_mat_items = QTreeWidgetItem(tre_prj_con_items)
                    tre_prj_mat_items.setText(0, mat_uuid)
                    tre_prj_mat_items.setText(1, mat_name)

            # Refresh the tree view.
            self.tre_prj_item.show()

            # Resize the column header by text length.
            self.tre_prj_item.resizeColumnToContents(0)
            self.tre_prj_item.resizeColumnToContents(1)

        except sqlite.DatabaseError as e:
            print("Error occured in main::retriveProjectItems(self)")
            print(staticmethod(e))
            error.ErrorMessageDbConnection(str(e.args[0]))
            return(None)

        finally:
            print("End -> main::retriveProjectItems")

    def openConfigDialog(self):
        print("main::openConfigDialog(self)")

        try:
            # Exit if the root directory is not loaded.
            if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

            # Initialize the configuration dialog.
            self.dialog_Config = configurationDialog.configurationDialog(parent=self)

            # Open the configuration dialog.
            if self.dialog_Config.exec_() == True:
                # Apply language setting.
                lang = self.dialog_Config.cbx_thm_lang.currentText()
                if lang == u"日本語":
                    self._language = "ja"
                elif lang == "English":
                    self._language = "en"

                # Apply theme of the UI
                self._skin = self.dialog_Config.cbx_skin.currentText().lower()
                self.setSkin(lang=self._language, theme=self._skin)

                # Apply auto white balance algorithm
                self._awb_algo = self.dialog_Config.cbx_tool_awb.currentText()

                # Apply pansharpening algorithm
                self._psp_algo = self.dialog_Config.cbx_tool_psp.currentText()

                # Apply default text editor.
                self._app_textEdit = self.dialog_Config.tbx_exe_textedit.text()

                # Apply proxy setting.
                proxy_setting = self.dialog_Config.txt_proxy.text()
                if proxy_setting == "No Proxy" or proxy_setting == "":
                    proxy_setting = "No Proxy"
                self._proxy = proxy_setting
                self.setProxy()

                # Apply OCR page Segmentation Mode.
                self._ocr_psm = str(int(self.dialog_Config.cbx_psm.currentText().split(":")[0])-1)

                # Apply OCR languages.
                if not self.dialog_Config.lst_lang_selected == None:
                    if self.dialog_Config.lst_lang_selected.count() > 0:
                        ocr_langs = [str(self.dialog_Config.lst_lang_selected.item(i).text()) for i in range(self.dialog_Config.lst_lang_selected.count())]
                        self._ocr_lang = "+".join(ocr_langs)
                print(self._ocr_lang)

                # Apply Flickr setting.
                self._flickr_apikey = self.dialog_Config.txt_flc_api.text()
                self._flickr_secret = self.dialog_Config.txt_flc_sec.text()

                # Apply map tile source.
                self._map_tile = self.dialog_Config.cbx_map_tile.currentText()
                self.setDefaultMap()

                # Save the current setting.
                general.changeConfig(self)
        except Exception as e:
            print("Error occured in main::openConfigDialog(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def setProxy(self):
        print("main::setProxy(self)")

        try:
            if not self._proxy == "No Proxy":
                proxy_url = QUrl(self._proxy)

                if unicode(proxy_url.scheme()).startswith('http'):
                    protocol = QNetworkProxy.HttpProxy
                else:
                    protocol = QNetworkProxy.Socks5Proxy
                QNetworkProxy.setApplicationProxy(
                    QNetworkProxy(
                        protocol,
                        proxy_url.host(),
                        proxy_url.port(),
                        proxy_url.userName(),
                        proxy_url.password())
                    )
        except Exception as e:
            self._proxy = "No Proxy"
            print("Error occured in main::setProxy(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def setSkin(self, lang, theme):
        print("main::setSkin(self, lang, theme)")

        try:
            # Reset values.
            self._language = lang
            self._skin = theme

            # Apply the new skin.
            setupMainSkin.applyMainWindowSkin(self, self._icon_directory, skin=self._skin)
            setupMainSkin.setMainWindowButtonText(self)

            # Set the tool tips with the specific language.
            setupMainSkin.setMainWindowToolTips(self)
        except Exception as e:
            print("Error occured in main::setSkin(self, lang, theme)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def setLangEn(self):
        print("main::setLangEn(self)")

        try:
            # Define language and skin theme.
            self._language = "en"

            # Set the default skin.
            setupMainSkin.setMainWindowButtonText(self)
            setupMainSkin.setMainWindowToolTips(self)
        except Exception as e:
            print("Error occured in main::setLangEn(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def setLangJa(self):
        print("main::setLangJa(self)")

        try:
            # Define language and skin theme.
            self._language = "ja"

            # Set the default skin.
            setupMainSkin.setMainWindowButtonText(self)
            setupMainSkin.setMainWindowToolTips(self)
        except Exception as e:
            print("Error occured in main::setLangEn(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def importExternalData(self):
        print("main::importExternalData(self)")

        # Set the dialog tile message.
        msg_title = ""

        if self._language == "ja":
            msg_title = "ファイルの選択"
        elif self._language == "en":
            msg_title = "Select files to import"

        try:
            # Exit if the root directory is not loaded.
            if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

            # Exit if the tree object is not selected.
            selected = self.tre_prj_item.selectedItems()
            if (selected == None or len(selected) == 0): error.ErrorMessageCurrentConsolidation(language=self._language); return(None)

            if self.tab_target.currentIndex() == 0:
                # Exit if the current consolidation is not selected.
                if self._current_consolidation == None: error.ErrorMessageCurrentConsolidation(language=self._language); return(None)
            elif self.tab_target.currentIndex()==1:
                # Exit if the current consolidation is not selected.
                if self._current_consolidation == None: error.ErrorMessageCurrentConsolidation(language=self._language); return(None)

                # Exit if the current consolidation is not selected.
                if self._current_material == None: error.ErrorMessageCurrentMaterial(language=self._language); return(None)

            # Define directories for storing files.
            in_dir = QFileDialog.getOpenFileNames(self, msg_title)

            # Initialyze the uuid for the consolidation and the mateselfrial.
            sop_object = None

            # Initialyze the variables.
            con_uuid = None
            mat_uuid = None
            item_path = None

            # Get the current object from the selected tab index.
            if self.tab_target.currentIndex() == 0:
                # Instantiate the consolidation.
                sop_object = self._current_consolidation

                # Get the current consolidaiton uuid.
                con_uuid = sop_object.uuid

                # Get the item path of the selected consolidaiton.
                item_path = os.path.join(self._consolidation_directory, con_uuid)
            elif self.tab_target.currentIndex() == 1:
                # Instantiate the material.
                sop_object = self._current_material

                # Instantiate the consolidation.
                mat_uuid = sop_object.uuid
                con_uuid = sop_object.consolidation
                con_path = os.path.join(self._consolidation_directory, sop_object.consolidation)
                item_path = os.path.join(os.path.join(con_path, "Materials"), mat_uuid)
            else:
                return(None)

            # Exit if none of objecs are instantiated.
            if sop_object == None: return(None)

            # Import medias in selected path.
            sop_media.mediaImporter(sop_object, item_path, in_dir[0], mat_uuid, con_uuid, self._database)

            # Refresh the file list.
            self.refreshFileList(sop_object)
        except Exception as e:
            print("Error occured in main::importExternalData(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def getTheRootDirectory(self):
        print("main::getTheRootDirectory(self)")

        # Set the dialog title message.
        msg_dialog = ""
        if self._language == "en":
            msg_dialog = "Select the project directory"
        elif self._language == "ja":
            msg_dialog = "プロジェクトディレクトリの選択"

        try:
            # Initialyze the tree view.
            self.tre_prj_item.clear()

            # Reflesh the last selection.
            self.refreshConsolidationInfo()
            self.refreshMaterialInfo()
            self.refreshImageInfo()

            # Get the current directories and save as previous entries.
            prev_root_directory = self._root_directory
            prev_table_directory = self._table_directory
            prev_consolidation_directory = self._consolidation_directory
            prev_database = self._database
            prev_consolidation = self._current_consolidation
            prev_material = self._current_material

            # Define directories for storing files.
            self._root_directory = QFileDialog.getExistingDirectory(self, msg_dialog)

            # Return nothing and exit this process if direcotry is not selected.
            if not os.path.exists(self.root_directory):
                self._root_directory = prev_root_directory
                self._table_directory = prev_table_directory
                self._consolidation_directory = prev_consolidation_directory
                self._database = prev_database
                self._current_consolidation = prev_consolidation
                self._current_material = prev_material

                # Exit this process.
                return(None)

            # Some essential directories are created under the root directory if they are not existed.
            self._table_directory = os.path.join(self._root_directory, "Table")
            self._consolidation_directory = os.path.join(self._root_directory, "Consolidation")

            # Reset the current consolidation and the current material.
            self._current_consolidation = None
            self._current_material = None

            # Define the DB file.
            self._database = os.path.join(self._table_directory, "project.db")

            # Check Flickr API Key File.
            self.checkFlickrKey()

            # Show the project creation dialog if the path is not existed.
            if not os.path.exists(self._database):
                createNewProject = general.askNewProject(self)
                if createNewProject == None:
                    # Set initial settings by previously loaded.
                    self._root_directory = prev_root_directory
                    self._table_directory = prev_table_directory
                    self._consolidation_directory = prev_consolidation_directory
                    self._database = prev_database
                    self._current_consolidation = prev_consolidation
                    self._current_material  = prev_material

                    # Exit this process.
                    return(None)

            # Open the project.
            self.openProject()
        except Exception as e:
            print("main::getTheRootDirectory(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def showImage(self, img_file_path):
        print("Start -> main::showImage(self," + img_file_path + ")")

        try:
            # Check the image file can be displayed directry.
            img_base, img_ext = os.path.splitext(img_file_path)
            img_valid = False

            for qt_ext in self._qt_image:
                # Exit loop if extension is matched with Qt supported image.
                if img_ext.lower() == qt_ext.lower():
                    img_valid = True
                    break

            # Check whether the image is Raw image or not.
            if not img_valid == True:
                # Extract the thumbnail image from the RAW image by using "dcraw".
                imageProcessing.getThumbnail(img_file_path)

                # Get the extracted thumbnail image.
                if not img_ext.lower() == "jpg":
                    img_file_path = img_base + ".thumb.jpg"

            if os.path.exists(img_file_path):
                # Check the exif rotation information.
                imageProcessing.correctRotaion(img_file_path)

                # Show the image on graphic view.
                self.graphicsView.setFile(img_file_path)
            else:
                error.ErrorMessageImagePreview(details=str(e), language=self._language)

                # Returns nothing.
                return(None)
        except Exception as e:
            print("Error occured in main::showImage(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

        finally:
            print("End -> main::showImage")

    def toggleCurrentObjectTab(self):
        print("main::toggleCurrentObjectTab(self)")

        try:
            if self.tab_target.currentIndex() == 0:
                if not self._current_consolidation == None:
                    # Set file information of material images.
                    self.refreshFileList(self._current_consolidation)
                else:
                    self.refreshConsolidationInfo()
                    self.refreshMaterialInfo()
            elif self.tab_target.currentIndex() == 1:
                if not self._current_consolidation == None:
                    if not self._current_material == None:
                        # Set file information of material images.
                        self.refreshFileList(self._current_material)
                    else:
                        self.refreshMaterialInfo()
                else:
                    self.refreshConsolidationInfo()

        except Exception as e:
            print("Error occured in main::toggleCurrentObjectTab(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def toggleCurrentTreeObject(self):
        print("Start -> main::toggleCurrentTreeObject(self)")

        # Exit if the root directory is not loaded.
        if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

        # Get the item of the material.
        selected = self.tre_prj_item.selectedItems()

        # Exit if selected item is 0.
        if (selected == None or len(selected) == 0): return(None)

        # Clear the information of the previously selected objects.
        self._current_consolidation = None
        self._current_material = None

        # To clear current view of the material info...
        self.refreshMaterialInfo()

        try:
            if selected[0].parent() == None:
                # Get the Consolidation if the node have no parent.
                selected_uuid = selected[0].text(0)

                # Set current objects.
                self._current_consolidation = features.Consolidation(is_new=False, uuid=selected_uuid, dbfile=self._database)

                # Set attributes of the consolidation to input boxes.
                self.setConsolidationInfo(self._current_consolidation)

                # Set active control tab for consolidation.
                self.tab_target.setCurrentIndex(0)

                # Set file information of material images.
                self.refreshFileList(self._current_consolidation)
                self.toggleCurrentSourceTab()

            elif selected[0].parent() != None:
                self.tre_prj_item.setCurrentItem(selected[0])

                # Get the Materil if the node have a parent.
                selected_uuid = selected[0].text(0)

                # Set current material.
                self._current_material = features.Material(is_new=False, uuid=selected_uuid, dbfile=self._database)
                self._current_consolidation = features.Consolidation(is_new=False, uuid=self._current_material.consolidation, dbfile=self._database)

                # Set attributes of the consolidation and the material to the input boxes.
                self.setConsolidationInfo(self._current_consolidation)
                self.setMaterialInfo()
                # Set active control tab for consolidation.
                self.tab_target.setCurrentIndex(1)

                # Set file information of material images.
                self.refreshFileList(self._current_material)
                self.toggleCurrentSourceTab()
        except Exception as e:
            print("Error occured in main::toggleCurrentTreeObject(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)
        finally:
            print("End -> main::toggleCurrentTreeObject")

    def toggleCurrentSourceTab(self):
        print("main::toggleCurrentSource(self)")

        # Exit if the root directory is not loaded.
        if self._root_directory == None: return(None)

        # Get the item of the material.
        selected = self.tre_prj_item.selectedItems()

        # Exit if selected item is 0.
        if (selected == None or len(selected) == 0): return(None)

        try:
            if self.tab_src.currentIndex() == 3:
                self.refreshMap()
        except Exception as e:
            print("Error occured in main::toggleCurrentSource(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def toggleShowFileMode(self):
        print("main::toggleShowFileMode(self)")

        try:
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
                sop_object = features.Consolidation(is_new=False, uuid=con_uuid, dbfile=self._database)
            elif self.tab_target.currentIndex() == 1:
                # Get the current material uuid.
                mat_uuid = self.tbx_mat_uuid.text()

                # Instantiate the material.
                sop_object = features.Material(is_new=False, uuid=mat_uuid, dbfile=self._database)
            else:
                return(None)

            # Refresh the file list.
            if not sop_object == None: self.refreshFileList(sop_object)
        except Exception as e:
            print("Error occured in main::toggleShowFileMode(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def refreshFileList(self, sop_object):
        print("main::refreshFileList(self, sop_object)")

        try:
            # "Clear the file list view"
            self.tre_fls.clear()

            # Clear current file.
            self._current_file = None

            # Get images from the given class.
            images = sop_object.images
            sounds = sop_object.sounds
            movies = sop_object.movies
            texts = sop_object.texts
            geometries = sop_object.geometries

            if not images == None and len(images) > 0:
                for image in images: self.setFileInfo(image)
            if not sounds == None and len(sounds) > 0:
                for sound in sounds: self.setFileInfo(sound)
            if not movies == None and len(movies) > 0:
                for movie in movies: self.setFileInfo(movie)
            if not texts == None and len(texts) > 0:
                for text in texts: self.setFileInfo(text)
            if not geometries == None and len(geometries) > 0:
                for geometry in geometries: self.setFileInfo(geometry)

            # Refresh the tree view.
            self.tre_fls.resizeColumnToContents(0)
            self.tre_fls.resizeColumnToContents(1)
            self.tre_fls.resizeColumnToContents(2)

            # Selct the top item as the default.
            self.tre_fls.setCurrentItem(self.tre_fls.topLevelItem(0))
            self.tre_fls.show()
        except Exception as e:
            print("Error occured in mainPanel::refreshFileList")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def importFileToObjects(self):
        print("Start -> main::importFileToObjects(self)")

        try:
            # Exit if the root directory is not loaded.
            if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

            self.dialogFileToObjects = fileToObjectsDialog.fileToObjectsDialog(parent=self)

            if self.dialogFileToObjects.exec_():
                dir_fls = self.dialogFileToObjects.tbx_fnam.text()

                # Check whether import directory is empty or not.
                if dir_fls == "" or dir_fls == None: return(False)

                # Create a new consolidation.
                con_uuid = str(uuid.uuid4())

                sop_consolidation = features.Consolidation(is_new=True, uuid=None, dbfile=None)
                sop_consolidation.uuid = con_uuid
                sop_consolidation.name = os.path.basename(dir_fls)

                # Insert the consolidation.
                sop_consolidation.dbInsert(self._database)

                # Create a directory to store consolidation.
                con_dir = os.path.join(self._consolidation_directory, sop_consolidation.uuid)
                general.createDirectories(con_dir, True)

                bgn = self.dialogFileToObjects.spn_pos_bgn.value()
                end = self.dialogFileToObjects.spn_pos_end.value()

                fl_nams = self.dialogFileToObjects.importedFiles
                obj_dict = dict()

                for fl_nam in fl_nams:
                    obj_dict[fl_nam] = fl_nam[bgn:end]

                for fl_nam in fl_nams:
                    find = fl_nam[bgn:end]
                    keys = [k for k, v in obj_dict.items() if v == find]

                    if len(keys) > 0:
                        # Create and insert Material.
                        sop_material = features.Material(is_new=True, uuid=None, dbfile=None)
                        sop_material.uuid = str(uuid.uuid4())
                        sop_material.consolidation = con_uuid
                        sop_material.name =find
                        sop_material.material_number = find

                        # Create a directory to store material
                        mat_dir = os.path.join(con_dir, "Materials")
                        itm_dir = os.path.join(mat_dir, sop_material.uuid)

                        if self.dialogFileToObjects.cbx_ftyp.currentText() == "Image":
                            # Define file type.
                            fl_typ = "image"

                            # Define the path for saving files.
                            img_path = os.path.join(itm_dir, "Images")
                            fl_path = os.path.join(img_path, "Main")

                        elif self.dialogFileToObjects.cbx_ftyp.currentText() == "Text":
                            # Define file type.
                            fl_typ = "text"

                            # Define the path for saving files.
                            fl_path = os.path.join(itm_dir, "Texts")

                        # Create a materials folder.
                        mat_dir = os.path.join(con_dir, "Materials")

                        # Create a directory for storing objects.
                        general.createDirectories(os.path.join(mat_dir, sop_material.uuid), False)

                        for key in keys:
                            # Add file and insert the file.
                            # Get the original image path.
                            fl_org = os.path.join(dir_fls, key)
                            fl_ext = os.path.splitext(key)[1]

                            # Generate the GUID for the consolidation
                            fl_uuid = str(uuid.uuid4())

                            # Get current time.
                            now = datetime.datetime.utcnow().isoformat()

                            # Define the destination file path.
                            fl_dest = os.path.join(fl_path, fl_uuid + fl_ext)

                            # Copy the original file.
                            shutil.copy(fl_org, fl_dest)

                            # Instantiate the File class.
                            sop_file = features.File(is_new=True, uuid=None, dbfile=None)

                            sop_file.material = sop_material.uuid
                            sop_file.consolidation = sop_material.consolidation
                            sop_file.filename = general.getRelativePath(fl_dest, "Consolidation")
                            sop_file.created_date = now
                            sop_file.modified_date = now
                            sop_file.file_type = fl_typ
                            sop_file.alias = "Imported"
                            sop_file.status = "Original"
                            sop_file.lock = False
                            sop_file.public = False
                            sop_file.source = "Nothing"
                            sop_file.operation = "Imported"
                            sop_file.operating_application = "Survey Data Collector"
                            sop_file.caption = "Imported"
                            sop_file.description = ""

                            sop_file.dbInsert(self._database)

                            # Add the image to the boject.
                            sop_material.images.append(sop_file)

                            obj_dict.pop(key)

                        # Insert the consolidation.
                        sop_material.dbInsert(self._database)

            # Initialyze the tree view.
            self.tre_prj_item.clear()

            # Reflesh the last selection.
            self.refreshConsolidationInfo()
            self.refreshMaterialInfo()
            self.refreshImageInfo()

            # Refresh the tree view.
            self.retriveProjectItems()

        except Exception as e:
            print("Error occured in main::importFileToObjects(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

        finally:
            print("End -> main::importFileToObjects")

    # ==========================
    # Consolidation
    # ==========================
    def importConsolidationCSV(self):
        print("main::importConsolidationCSV(self)")

        try:
            # Exit if the root directory is not loaded.
            if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

            # Define directories for storing files.
            in_file = QFileDialog.getOpenFileName(self, "Select the consolidation file")

            # Open and read the imported csv file.
            with open(in_file[0]) as table:
                # Initialyze the counter for reading line.
                cnt_line = 0

                # Initialyze the variables.
                feat_type = dict()
                con_head = dict()
                mat_head = dict()

                for line in table:
                    line = line.strip()

                    # Parsing each line.
                    if cnt_line == 0:
                        # The case of header line.
                        cnt_haeder = 0

                        # Read the header line with comma.
                        headers = line.split(",")

                        for header in headers:
                            # Separate the class name and the attribute name with a period.
                            cls, item = header.split(".")

                            # If the class is consolidation.
                            if cls == "consolidation":
                                # Create a dictionary for parsing each entry.
                                feat_type[cnt_haeder] = "consolidation"

                                print(item)

                                if item == "uuid": con_head[cnt_haeder] = "uuid"
                                elif item == "name": con_head[cnt_haeder] = "name"
                                elif item == "geographic_annotation": con_head[cnt_haeder] = "geographic_annotation"
                                elif item == "temporal_annotation": con_head[cnt_haeder] = "temporal_annotation"
                                elif item == "description": con_head[cnt_haeder] = "description"
                                elif item == "main": con_head[cnt_haeder] = "main"
                                elif item == "raw": con_head[cnt_haeder] = "raw"
                                elif item == "sound": con_head[cnt_haeder] = "sound"
                                elif item == "text": con_head[cnt_haeder] = "text"
                                elif item == "movie": con_head[cnt_haeder] = "movie"
                                else: con_head[cnt_haeder] = item

                                cnt_haeder += 1
                    else:
                        # The case of entry lines.
                        entries = line.split(",")

                        # Create a new SOP object of consolidation.
                        sop_consolidation = features.Consolidation(is_new=True, uuid=None, dbfile=None)

                        for i in range(len(entries)):
                            # Give a NULL value if the entry is empty.
                            if entries[i] == "" : entries[i] = "NULL"

                            # Convert the string to the unicode.
                            if isinstance(entries[i], str): entries[i] = entries[i].decode('utf-8')

                            # Check the class of the current entry.
                            if feat_type[i] == "consolidation":
                                if con_head[i] == "uuid":
                                    if entries[i] != None:
                                        sop_consolidation.uuid = entries[i]
                                    else:
                                        sop_consolidation.uuid = str(uuid.uuid4())
                                elif con_head[i] == "name": sop_consolidation.name = entries[i]
                                elif con_head[i] == "geographic_annotation": sop_consolidation.geographic_annotation = entries[i]
                                elif con_head[i] == "temporal_annotation": sop_consolidation.temporal_annotation = entries[i]
                                elif con_head[i] == "description": sop_consolidation.description = entries[i]
                                else:
                                    sop_additional_attribute = features.AdditionalAttribute(is_new=True, uuid=None, dbfile=None)
                                    sop_additional_attribute.key = con_head[i]
                                    sop_additional_attribute.value = entries[i]
                                    sop_additional_attribute.datatype = "CharacterString"
                                    sop_additional_attribute.description = ""
                                    sop_consolidation.additionalAttributes.append(sop_additional_attribute)
                        # Insert the consolidation.
                        sop_consolidation.dbInsert(self._database)

                        # Create a directory to store consolidation.
                        general.createDirectories(os.path.join(self._consolidation_directory,sop_consolidation.uuid), True)
                    cnt_line += 1
            # Initialyze the tree view.
            self.tre_prj_item.clear()

            # Reflesh the last selection.
            self.refreshConsolidationInfo()
            self.refreshMaterialInfo()
            self.refreshImageInfo()

            # Refresh the tree view.
            self.retriveProjectItems()
        except Exception as e:
            print("Error occured in main::importConsolidationCSV(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def exportConsolidationCSV(self):
        print("main::exportConsolidationCSV(self)")

         # Create a sqLite file if not exists.
        try:
            # Exit if the root directory is not loaded.
            if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

            # Exit if the current consolidation is not selected.
            if self._current_consolidation == None: error.ErrorMessageCurrentConsolidation(language=self._language); return(None)

            # Exit if the tree object is not selected.
            selected = self.tre_prj_item.selectedItems()
            if (selected == None or len(selected) == 0): error.ErrorMessageTreeItemNotSelected(language=self._language); return(None)

            # Get the output file name by using file save dialog.
            output, output_type = QFileDialog.getSaveFileName(self, "Export to", "output.csv","Images (*.csv)")

            if not output: return(None)

            # Open the file stream
            output_csv = open(output,"w")

            # Establish the connection to the self._database file.
            conn = sqlite.connect(self._database)

            if conn is not None:
                header_line = ""

                # Create a header.
                headers = [
                    "consolidation.uuid",
                    "consolidation.name",
                    "consolidation.geographic_annotation",
                    "consolidation.temporal_annotation",
                    "consolidation.description",
                    "consolidation.additional_attributes"
                ]
                # Write the header
                for header in headers:
                    header_line = header_line + header + ","

                # Write the hader line.
                output_csv.writelines(header_line.rstrip(",") + "\n")

                # Create the SQL query for selecting consolidation.
                sql_con_sel = """SELECT uuid FROM consolidation"""

                # Instantiate the cursor for query.
                cur_con = conn.cursor()
                rows_con = cur_con.execute(sql_con_sel)

                # Execute the query and get consolidation recursively
                for row_con in rows_con:
                    # Get attributes from the row.
                    con_uuid = row_con[0]

                    # Instantiate the consolidation.
                    sop_consolidation = features.Consolidation(is_new=False, uuid=con_uuid, dbfile=self._database)

                    con_values = [
                        sop_consolidation.uuid,
                        sop_consolidation.name,
                        sop_consolidation.geographic_annotation,
                        sop_consolidation.temporal_annotation,
                        sop_consolidation.description
                    ]

                    con_generic_values = ""
                    con_additional_values = ","

                    for con_value in con_values:
                        if isinstance(con_value, unicode) : con_value = con_value.encode('utf-8')

                        con_generic_values = con_generic_values + "," + str(con_value).encode('utf-8')

                    if not sop_consolidation.additionalAttributes == None:
                        if not len(sop_consolidation.additionalAttributes) <= 0:
                            con_additional_values = "{"

                            for additionalAttribute in sop_consolidation.additionalAttributes:
                                con_add_key = additionalAttribute.key
                                con_add_val = additionalAttribute.value

                                if isinstance(con_add_key, unicode) : con_add_key = con_add_key.encode('utf-8')
                                if isinstance(con_add_val, unicode) : con_add_val = con_add_val.encode('utf-8')

                                con_additional_values = "(" + con_add_key + ":" + con_add_val + ")"

                            # Close the bracket.
                            con_additional_values = con_additional_values + "}"

                    # Writet the attribute lines.
                    output_csv.writelines(con_generic_values.lstrip(",") + con_additional_values + "\n")
        except Exception as e:
            print("Error occured in main::exportConsolidationCSV(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def addConsolidation(self):
        print("main::addConsolidation(self)")

        try:
            # Exit if the root directory is not loaded.
            if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)
            print(1)
            # Initialize the Consolidation Class.
            self._current_consolidation = features.Consolidation(is_new=True, uuid=None, dbfile=None)
            print(2)
            # Show the dialog.
            dlg_con = consolidationDialog.consolidationDialog(parent=self)
            print(3)
            isAccepted = dlg_con.exec_()
            print(4)
            if isAccepted == 1:
                # Instantiate the consolidation class
                self._current_consolidation.name = dlg_con.tbx_con_name.text()
                self._current_consolidation.geographic_annotation = dlg_con.tbx_con_geoname.text()
                self._current_consolidation.temporal_annotation = dlg_con.tbx_con_temporal.text()
                self._current_consolidation.description = dlg_con.tbx_con_description.text()

                # Insert the instance into DBMS.
                self._current_consolidation.dbInsert(self._database)

                # Create a directory to store consolidation.
                general.createDirectories(os.path.join(self._consolidation_directory,self._current_consolidation.uuid), True)

                # Update the tree view.
                tre_prj_item_items = QTreeWidgetItem(self.tre_prj_item)

                # Set text item to the tree widget.
                tre_prj_item_items.setText(0, self._current_consolidation.uuid)
                tre_prj_item_items.setText(1, self._current_consolidation.name)

                # Refresh the tree view.
                self.tre_prj_item.show()

                # Adjust columns width.
                self.tre_prj_item.resizeColumnToContents(0)
                self.tre_prj_item.resizeColumnToContents(1)

                # Select the new consolidation from the tree.
                self.tre_prj_item.setCurrentItem(tre_prj_item_items)

                # Set new values
                self.setConsolidationInfo(self._current_consolidation)

                # Set file information of material images.
                self.refreshFileList(self._current_consolidation)
        except Exception as e:
            print("Error occured in main::addConsolidation(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def updateConsolidation(self):
        print("main::updateConsolidation(self)")

        try:
           # Exit if the root directory is not loaded.
            if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

            # Exit if the current consolidation is not selected.
            if self._current_consolidation == None: error.ErrorMessageCurrentConsolidation(language=self._language); return(None)

            # Exit if the tree object is not selected.
            selected = self.tre_prj_item.selectedItems()
            if (selected == None or len(selected) == 0): error.ErrorMessageTreeItemNotSelected(language=self._language); return(None)

            # Show the dialog.
            dlg_con = consolidationDialog.consolidationDialog(parent=self)

            isAccepted = dlg_con.exec_()

            if isAccepted == 1:
                # Instantiate the consolidation class
                self._current_consolidation.name = dlg_con.tbx_con_name.text()
                self._current_consolidation.geographic_annotation = dlg_con.tbx_con_geoname.text()
                self._current_consolidation.temporal_annotation = dlg_con.tbx_con_temporal.text()
                self._current_consolidation.description = dlg_con.tbx_con_description.text()

                # Update the instance into DBMS.
                self._current_consolidation.dbUpdate(self._database)

                # Get the item of the material.
                selected = self.tre_prj_item.selectedItems()[0]

                # Update the tree view.
                if selected.text(0) == self._current_consolidation.uuid:
                    selected.setText(1, self._current_consolidation.name)

                # Refresh the tree view.
                self.tre_prj_item.show()
                self.tre_prj_item.resizeColumnToContents(0)
                self.tre_prj_item.resizeColumnToContents(1)

                # Set new values
                self.setConsolidationInfo(self._current_consolidation)

                # Set file information of material images.
                self.refreshFileList(self._current_consolidation)

                # Refresh the map.
                self.refreshMap()
        except Exception as e:
            print("Error occured in main::updateConsolidation(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def deleteConsolidation(self):
        print("main::deleteConsolidation(self)")

        try:
            # Exit if the root directory is not loaded.
            if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

            # Exit if the current consolidation is not selected.
            if self._current_consolidation == None: error.ErrorMessageCurrentConsolidation(language=self._language); return(None)

            # Exit if the tree object is not selected.
            selected = self.tre_prj_item.selectedItems()
            if (selected == None or len(selected) == 0): error.ErrorMessageTreeItemNotSelected(language=self._language); return(None)

            # Confirm deleting the consolidation.
            if not general.askDeleteConsolidation(self) == QMessageBox.Yes: return(None)

            con_uuid = self.tbx_con_uuid.text()

            # Initialize the Consolidation Class.
            con = features.Consolidation(is_new=False, uuid=con_uuid, dbfile=self._database)

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
            shutil.rmtree(os.path.join(self._consolidation_directory, con.uuid))

            # Drop the consolidation from the DB table.
            con.dbDrop(self._database)

            # Reflesh the last consolidation and material.
            self.current_consolidation = None
            self.current_material = None

            # Reflesh the last selection.
            self.refreshConsolidationInfo()
            self.refreshMaterialInfo()
            self.refreshImageInfo()
        except Exception as e:
            print("Error occured in main::deleteConsolidation(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def setConsolidationInfo(self, consolidation):
        print("main::setConsolidationInfo(self, consolidation)")

        try:
            # Initialyze the consolidation and the material info.
            self.refreshConsolidationInfo()

            # Set attributes to text boxes.
            self.tbx_con_uuid.setText(consolidation.uuid)
            self.tbx_con_name.setText(consolidation.name)
            self.tbx_con_geoname.setText(consolidation.geographic_annotation)
            self.tbx_con_temporal.setText(consolidation.temporal_annotation)
            self.tbx_con_description.setText(consolidation.description)
        except Exception as e:
            print("Error occors in main::setConsolidationInfo(self, consolidation)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def refreshConsolidationInfo(self):
        print("main::refreshConsolidationInfo(self)")

        try:
            # Change text color for text boxes.
            setupMainSkin.setDefaultConsolidationText(self, status="default", skin=self._skin)

            # Refresh preview image.
            self.refreshImageInfo()

            # Clear the file list for consolidation.
            self.tre_fls.clear()

            # Set the thumbnail No Image as the default.
            img_file_path = os.path.join(os.path.join(self._source_directory, "images"),"noimage.jpg")
            self.showImage(img_file_path)

            # Clear text boxes for attributes.
            self.tbx_con_uuid.setText("")
            self.tbx_con_name.setText("")
            self.tbx_con_geoname.setText("")
            self.tbx_con_temporal.setText("")
            self.tbx_con_description.setText("")
        except Exception as e:
            print("Error occured in main::refreshConsolidationInfo(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    # ==========================
    # Material
    # ==========================
    def importMaterialCSV(self):
        print("main::importMaterialCSV(self)")

        try:
            # Exit if the root directory is not loaded.
            if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

            # Define directories for storing files.
            in_file = QFileDialog.getOpenFileName(self, "Select material file.")

            # Open and read the imported csv file.
            with open(in_file[0]) as table:
                # Initialyze the counter for reading line.
                cnt_line = 0

                # Initialyze the variables.
                feat_type = dict()
                mat_head = dict()

                for line in table:
                    line = line.strip()

                    # Parsing each line.
                    if cnt_line == 0:
                        # The case of header line.
                        cnt_haeder = 0

                        # Read the header line with comma.
                        headers = line.split(",")

                        for header in headers:
                            # Separate the class name and the attribute name with a period.
                            cls, item = header.split(".")

                            if cls == "material":
                                feat_type[cnt_haeder] = "material"
                                if  item == "uuid": mat_head[cnt_haeder] = "uuid"
                                elif item == "consolidation": mat_head[cnt_haeder] = "consolidation"
                                elif item == "name": mat_head[cnt_haeder] = "name"
                                elif item == "material_number": mat_head[cnt_haeder] = "material_number"
                                elif item == "estimated_period_beginning": mat_head[cnt_haeder] = "estimated_period_beginning"
                                elif item == "estimated_period_peak": mat_head[cnt_haeder] = "estimated_period_peak"
                                elif item == "estimated_period_ending": mat_head[cnt_haeder] = "estimated_period_ending"
                                elif item == "latitude": mat_head[cnt_haeder] = "latitude"
                                elif item == "longitude": mat_head[cnt_haeder] = "longitude"
                                elif item == "altitude": mat_head[cnt_haeder] = "altitude"
                                elif item == "description": mat_head[cnt_haeder] = "description"
                                elif item == "main": mat_head[cnt_haeder] = "main"
                                elif item == "raw": mat_head[cnt_haeder] = "raw"
                                elif item == "sound": mat_head[cnt_haeder] = "sound"
                                elif item == "text": mat_head[cnt_haeder] = "text"
                                elif item == "movie": mat_head[cnt_haeder] = "movie"
                                else: mat_head[cnt_haeder] = item

                                cnt_haeder += 1
                    else:
                        entries = line.split(",")

                        sop_material = features.Material(is_new=True, uuid=None, dbfile=None)

                        con_dir = ""
                        mat_dir = ""

                        for i in range(len(entries)):
                            # Give a NULL value if the entry is empty.
                            if entries[i] == "" : entries[i] = "NULL"

                            # Convert the string to the unicode.
                            if isinstance(entries[i], str): entries[i] = entries[i].decode('utf-8')

                            # Check the class of the current entry.
                            if feat_type[i] == "material":
                                if mat_head[i] == "uuid":
                                    if entries[i] == "NULL":
                                        sop_material.uuid = str(uuid.uuid4())
                                    else:
                                        sop_material.uuid = entries[i]
                                elif mat_head[i] == "consolidation":
                                    sop_material.consolidation = entries[i]

                                    con_dir = os.path.join(self._consolidation_directory, sop_material.consolidation)
                                    mat_dir = os.path.join(con_dir, "Materials")

                                    # Create a directory for storing objects.
                                    createPathIfNotExists(mat_dir)
                                    general.createDirectories(os.path.join(mat_dir, sop_material.uuid), False)
                                elif mat_head[i] == "name": sop_material.name = entries[i]
                                elif mat_head[i] == "material_number": sop_material.material_number = entries[i]
                                elif mat_head[i] == "estimated_period_beginning": sop_material.estimated_period_beginning = entries[i]
                                elif mat_head[i] == "estimated_period_peak": sop_material.estimated_period_peak = entries[i]
                                elif mat_head[i] == "estimated_period_ending": sop_material.estimated_period_ending = entries[i]
                                elif mat_head[i] == "latitude": sop_material.latitude = entries[i]
                                elif mat_head[i] == "longitude": sop_material.longitude = entries[i]
                                elif mat_head[i] == "altitude": sop_material.altitude = entries[i]
                                elif mat_head[i] == "description": sop_material.description = entries[i]
                                elif mat_head[i] == "main":
                                    con_dir = os.path.join(self._consolidation_directory, sop_material.consolidation)
                                    itm_dir = os.path.join(mat_dir, sop_material.uuid)

                                    # Define the path for saving files.
                                    img_path = os.path.join(itm_dir, "Images")
                                    img_path_main = os.path.join(img_path, "Main")

                                    # Get the original image path.
                                    main_org = os.path.join(os.path.dirname(in_file[0]), entries[i])

                                    # Generate the GUID for the consolidation
                                    img_uuid = str(uuid.uuid4())

                                    # Get current time.
                                    now = datetime.datetime.utcnow().isoformat()

                                    # Define the destination file path.
                                    main_dest = os.path.join(img_path_main, img_uuid+".jpg")

                                    if os.path.exists(main_org):
                                        # Copy the original file.
                                        shutil.copy(main_org, main_dest)

                                        # Instantiate the File class.
                                        sop_img_file = features.File(is_new=True, uuid=None, dbfile=None)

                                        sop_img_file.material = sop_material.uuid
                                        sop_img_file.consolidation = sop_material.consolidation
                                        sop_img_file.filename = general.getRelativePath(main_dest, "Consolidation")
                                        sop_img_file.created_date = now
                                        sop_img_file.modified_date = now
                                        sop_img_file.file_type = "image"
                                        sop_img_file.alias = "Imported"
                                        sop_img_file.status = "Original"
                                        sop_img_file.lock = False
                                        sop_img_file.public = False
                                        sop_img_file.source = "Nothing"
                                        sop_img_file.operation = "Imported"
                                        sop_img_file.operating_application = "Survey Data Collector"
                                        sop_img_file.caption = "Imported image"
                                        sop_img_file.description = ""

                                        # Add the image to the boject.
                                        sop_material.images.append(sop_img_file)
                                    else:
                                        print("File not found:" + main_org)
                                elif mat_head[i] == "raw":
                                    con_dir = os.path.join(self._consolidation_directory, sop_material.consolidation)
                                    itm_dir = os.path.join(mat_dir, sop_material.uuid)

                                    # Define the path for saving files.
                                    img_path = os.path.join(itm_dir, "Images")
                                    img_path_raw = os.path.join(img_path, "Raw")

                                    # Get the original image path.
                                    raw_org = os.path.join(os.path.dirname(in_file[0]), entries[i])
                                    ext = os.path.splitext(raw_org)[1]

                                    # Generate the GUID for the consolidation
                                    raw_uuid = str(uuid.uuid4())

                                    # Get current time.
                                    now = datetime.datetime.utcnow().isoformat()

                                    # Define the destination file path.
                                    raw_dest = os.path.join(img_path_raw, raw_uuid + ext)

                                    if os.path.exists(raw_org):
                                        # Copy the original file.
                                        shutil.copy(raw_org, raw_dest)

                                        # Instantiate the File class.
                                        sop_raw_file = features.File(is_new=True, uuid=None, dbfile=None)
                                        sop_raw_file.material = sop_material.uuid
                                        sop_raw_file.consolidation = sop_material.consolidation
                                        sop_raw_file.filename = general.getRelativePath(raw_dest, "Consolidation")
                                        sop_raw_file.created_date = now
                                        sop_raw_file.modified_date = now
                                        sop_raw_file.file_type = "image"
                                        sop_raw_file.alias = "Imported"
                                        sop_raw_file.status = "Original"
                                        sop_raw_file.lock = False
                                        sop_raw_file.public = False
                                        sop_raw_file.source = "Nothing"
                                        sop_raw_file.operation = "Imported"
                                        sop_raw_file.operating_application = "Survey Data Collector"
                                        sop_raw_file.caption = "Imported image"
                                        sop_raw_file.description = ""

                                        # Add the image to the boject.
                                        sop_material.images.append(sop_raw_file)
                                    else:
                                        print("File not found:" + raw_org)
                                else:
                                    sop_additional_attribute = features.AdditionalAttribute(is_new=True, uuid=None, dbfile=None)
                                    sop_additional_attribute.key = mat_head[i]
                                    sop_additional_attribute.value = entries[i]
                                    sop_additional_attribute.datatype = "CharacterString"
                                    sop_additional_attribute.description = ""
                                    sop_material.additionalAttributes.append(sop_additional_attribute)
                        # Insert the consolidation.
                        sop_material.dbInsert(self._database)
                    cnt_line += 1
            # Initialyze the tree view.
            self.tre_prj_item.clear()

            # Reflesh the last selection.
            self.refreshConsolidationInfo()
            self.refreshMaterialInfo()
            self.refreshImageInfo()

            # Refresh the tree view.
            self.retriveProjectItems()
        except Exception as e:
            print("Error occured in main::importMaterialCSV(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def exportMaterialCSV(self):
        print("main::exportMaterialCSV(self)")

         # Create a sqLite file if not exists.
        try:
            # Exit if the root directory is not loaded.
            if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

            # Exit if the current consolidation is not selected.
            if self._current_consolidation == None: error.ErrorMessageCurrentConsolidation(language=self._language); return(None)

            # Exit if the current consolidation is not selected.
            if self._current_material == None: error.ErrorMessageCurrentMaterial(language=self._language); return(None)

            # Exit if the tree object is not selected.
            selected = self.tre_prj_item.selectedItems()
            if (selected == None or len(selected) == 0): error.ErrorMessageTreeItemNotSelected(language=self._language); return(None)

            # Get the output file name by using file save dialog.
            output, output_type = QFileDialog.getSaveFileName(self, "Export to", "output.csv","Commna Separation Values(*.csv)")

            if not output: return(None)

            # Open the file stream
            output_csv = open(output,"w")

            # Establish the connection to the self._database file.
            conn = sqlite.connect(self._database)

            if conn is not None:
                header_line = ""

                # Create a header.
                headers = [
                    "material.consolidation",
                    "material.uuid",
                    "material.name",
                    "material.material_number",
                    "material.estimated_period_beginning",
                    "material.estimated_period_peak",
                    "material.estimated_period_ending",
                    "material.latitude",
                    "material.longitude",
                    "material.altitude",
                    "material.description",
                    "material.additional_attributes"
                ]
                # Write the header
                for header in headers:
                    header_line = header_line + header + ","

                # Write the hader line.
                output_csv.writelines(header_line.rstrip(",") + "\n")

                # Create the SQL query for selecting the Materials.
                sql_mat_sel = """SELECT uuid FROM material"""

                # Instantiate the cursor for query.
                cur_mat = conn.cursor()
                rows_mat = cur_mat.execute(sql_mat_sel)

                # Execute the query and get material recursively
                for row_mat in rows_mat:
                    # Get attributes from the row.
                    mat_uuid = row_mat[0]

                    # Instantiate the material.
                    sop_material = features.Material(is_new=False, uuid=mat_uuid, dbfile=self._database)

                    mat_values = [
                        sop_material.consolidation,
                        sop_material.uuid,
                        sop_material.name,
                        sop_material.material_number,
                        sop_material.estimated_period_beginning,
                        sop_material.estimated_period_peak,
                        sop_material.estimated_period_ending,
                        sop_material.latitude,
                        sop_material.longitude,
                        sop_material.altitude,
                        sop_material.description
                    ]

                    mat_generic_values = ""
                    mat_additional_values = ","

                    for mat_value in mat_values:
                        if isinstance(mat_value, unicode) : mat_value = mat_value.encode('utf-8')

                        mat_generic_values = mat_generic_values + "," + str(mat_value)
                    if not sop_material.additionalAttributes == None:
                        if not len(sop_material.additionalAttributes) <= 0:
                            mat_additional_values = "{"
                            for additionalAttribute in sop_material.additionalAttributes:
                                mat_add_key = additionalAttribute.key
                                mat_add_val = additionalAttribute.value

                                if isinstance(mat_add_key, unicode) : mat_add_key = mat_add_key.encode('utf-8')
                                if isinstance(mat_add_val, unicode) : mat_add_val = mat_add_val.encode('utf-8')

                                mat_additional_values = "(" + mat_add_key + ":" + mat_add_val + ")"

                            # Close the bracket.
                            mat_additional_values = mat_additional_values + "}"

                    # Writet the attribute lines.
                    output_csv.writelines(mat_generic_values.lstrip(",") + mat_additional_values + "\n")
        except Exception as e:
            print("Error occured in main::exportMaterialCSV(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def addMaterial(self):
        print("main::addMaterial(self)")

        try:
            # Exit if the root directory is not loaded.
            if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

            # Exit if the current consolidation is not selected.
            if self._current_consolidation == None: error.ErrorMessageCurrentConsolidation(language=self._language); return(None)

            # Exit if the tree object is not selected.
            selected = self.tre_prj_item.selectedItems()
            if (selected == None or len(selected) == 0): error.ErrorMessageCurrentMaterial(language=self._language); return(None)

            # Initialyze the consolidation tree item.
            consolidation_tree_item = None

            # Check the selected object is consolidation or not.
            if not self.tre_prj_item.selectedItems()[0].parent() == None:
                # Confirm whether select the parent consolidations.
                reply = general.askNewMaterial(self)

                # Handle the return value.
                if reply == QMessageBox.Yes:
                    consolidation_tree_item = self.tre_prj_item.selectedItems()[0].parent()
                else:
                    return(None)
            else:
                consolidation_tree_item = self.tre_prj_item.selectedItems()[0]

            # Generate the GUID for the material
            self._current_material = features.Material(is_new=True, uuid=None, dbfile=None)

            # Show the dialog.
            dlg_mat = materialDialog.materialDialog(parent=self)

            isAccepted = dlg_mat.exec_()

            if isAccepted == 1:
                # Get attributes from text boxes.
                self._current_material.consolidation = self._current_consolidation.uuid
                self._current_material.material_number = dlg_mat.tbx_mat_number.text()
                self._current_material.name = dlg_mat.tbx_mat_name.text()
                self._current_material.estimated_period_beginning = dlg_mat.tbx_mat_tmp_bgn.text()
                self._current_material.estimated_period_peak = dlg_mat.tbx_mat_tmp_mid.text()
                self._current_material.estimated_period_ending = dlg_mat.tbx_mat_tmp_end.text()
                self._current_material.latitude = dlg_mat.tbx_mat_geo_lat.text()
                self._current_material.longitude = dlg_mat.tbx_mat_geo_lon.text()
                self._current_material.altitude = dlg_mat.tbx_mat_geo_alt.text()
                self._current_material.description = dlg_mat.tbx_mat_description.text()

                # Create the SQL query for inserting the new consolidation.
                self._current_material.dbInsert(self._database)

                # Create a directory to store consolidation.
                con_dir = os.path.join(self._consolidation_directory, self._current_consolidation.uuid)
                mat_dir = os.path.join(con_dir, "Materials")

                # Create Materials directory if not exists.
                if not os.path.exists(mat_dir): os.mkdir(mat_dir)

                # Create material directory.
                general.createDirectories(os.path.join(mat_dir, self._current_material.uuid), False)

                # Update the tree view.
                tree_item_new_material = QTreeWidgetItem([self._current_material.uuid,self._current_material.name])
                consolidation_tree_item.addChild(tree_item_new_material)

                # Show tree view.
                self.tre_prj_item.show()

                # Adjust columns width.
                self.tre_prj_item.resizeColumnToContents(0)
                self.tre_prj_item.resizeColumnToContents(1)
                self.tre_prj_item.setCurrentItem(tree_item_new_material)

                # Set the new values.
                self.setMaterialInfo()

                # Set file information of material images.
                self.refreshFileList(self._current_material)

                # Clear current file object.
                self._current_file = None
        except Exception as e:
            print("Error occured in main::addMaterial(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def updateMaterial(self):
        print("main::updateMaterial(self)")

        try:
            # Exit if the root directory is not loaded.
            if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

            # Exit if the current consolidation is not selected.
            if self._current_consolidation == None: error.ErrorMessageCurrentConsolidation(language=self._language); return(None)

            # Exit if the current consolidation is not selected.
            if self._current_material == None: error.ErrorMessageCurrentMaterial(language=self._language); return(None)

            # Exit if the tree object is not selected.
            selected = self.tre_prj_item.selectedItems()
            if (selected == None or len(selected) == 0): error.ErrorMessageCurrentMaterial(language=self._language); return(None)

            # Show the dialog.
            dlg_mat = materialDialog.materialDialog(parent=self)

            isAccepted = dlg_mat.exec_()

            if isAccepted == 1:
                # Get attributes from text boxes.
                self._current_material.name = dlg_mat.tbx_mat_name.text()
                self._current_material.material_number = dlg_mat.tbx_mat_number.text()
                self._current_material.estimated_period_beginning = dlg_mat.tbx_mat_tmp_bgn.text()
                self._current_material.estimated_period_peak = dlg_mat.tbx_mat_tmp_mid.text()
                self._current_material.estimated_period_ending = dlg_mat.tbx_mat_tmp_end.text()
                self._current_material.latitude = dlg_mat.tbx_mat_geo_lat.text()
                self._current_material.longitude = dlg_mat.tbx_mat_geo_lon.text()
                self._current_material.altitude = dlg_mat.tbx_mat_geo_alt.text()
                self._current_material.description = dlg_mat.tbx_mat_description.text()

                # Create the SQL query for updating the new consolidation.
                self._current_material.dbUpdate(self._database)

                # Get the item of the material.
                selected = self.tre_prj_item.selectedItems()[0]

                # Update the tree view.
                if selected.text(0) == self._current_material.uuid:
                    selected.setText(1, self._current_material.name)

                # Refresh the tree view.
                self.tre_prj_item.show()

                self.tre_prj_item.resizeColumnToContents(0)
                self.tre_prj_item.resizeColumnToContents(1)

                # Set the new values.
                self.setMaterialInfo()

                # Set file information of material images.
                self.refreshFileList(self._current_material)

                # Refresh map with given coordinates.
                self.refreshMap()
        except Exception as e:
            print("Error occured in main::updateMaterial(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def deleteMaterial(self):
        print("main::deleteMaterial(self)")

        try:
            # Exit if the root directory is not loaded.
            if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

            # Exit if the current consolidation is not selected.
            if self._current_consolidation == None: error.ErrorMessageCurrentConsolidation(language=self._language); return(None)

            # Exit if the current consolidation is not selected.
            if self._current_material == None: error.ErrorMessageCurrentMaterial(language=self._language); return(None)

            # Exit if the tree object is not selected.
            selected = self.tre_prj_item.selectedItems()
            if (selected == None or len(selected) == 0): error.ErrorMessageCurrentMaterial(language=self._language); return(None)

            # Confirm deleting the material.
            if not general.askDeleteMaterial(self) == QMessageBox.Yes: return(None)

            # Generate the GUID for the material
            mat_uuid = self.tbx_mat_uuid.text()

            # Generate the GUID for the material
            mat = features.Material(is_new=False, uuid=mat_uuid, dbfile=self._database)
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

            # Refresh the current material.
            self.current_material = None

            # Refresh the tree view.
            self.tre_prj_item.show()
            self.tre_prj_item.resizeColumnToContents(0)
            self.tre_prj_item.resizeColumnToContents(1)

            # Delete all files from consolidation directory.
            con_mat_path = os.path.join(os.path.join(self._consolidation_directory,con_uuid),"Materials")
            mat_path = os.path.join(con_mat_path, mat.uuid)

            # Delete files.
            shutil.rmtree(mat_path)

            # Drop the consolidation from the DB table.
            mat.dbDrop(self._database)

            # Reflesh the last selection.
            self.refreshMaterialInfo()
            self.refreshImageInfo()
            self._current_file = None
        except Exception as e:
            print("Error occured in main::deleteMaterial(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def setMaterialInfo(self):
        print("main::setMaterialInfo(self)")

        try:
            # Initialyze the material info.
            self.refreshMaterialInfo()

            # Set attributes to text boxes.
            self.tbx_mat_uuid.setText(self._current_material.uuid)
            self.tbx_mat_number.setText(self._current_material.material_number)
            self.tbx_mat_name.setText(self._current_material.name)
            self.tbx_mat_tmp_bgn.setText(self._current_material.estimated_period_beginning)
            self.tbx_mat_tmp_mid.setText(self._current_material.estimated_period_peak)
            self.tbx_mat_tmp_end.setText(self._current_material.estimated_period_ending)
            self.tbx_mat_geo_lat.setText(str(self._current_material.latitude))
            self.tbx_mat_geo_lon.setText(str(self._current_material.longitude))
            self.tbx_mat_geo_alt.setText(str(self._current_material.altitude))
            self.tbx_mat_description.setText(self._current_material.description)

            # Returns the value.
            return(True)
        except Exception as e:
            print("Error occors in main::setMaterialInfo(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def refreshMaterialInfo(self):
        print("Start -> main::refreshMaterialInfo(self)")

        try:
            # Change text color for text boxes.
            setupMainSkin.setDefaultMaterialText(self, status="default", skin=self._skin)

            # Refresh preview image.
            self.refreshImageInfo()

            # Clear the file list for consolidation.
            self.tre_fls.clear()

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
        except Exception as e:
            print("Error occcurs in main::refreshMaterialInfo(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)
        print("End -> main::refreshMaterialInfo(self)")

    # ==========================
    # File
    # ==========================
    def getCurrentFile(self):
        print("Start -> main::getCurrentFile(self)")

        # Exit if the root directory is not loaded.
        if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

        # Get the current tree view item.
        selected = self.tre_fls.selectedItems()

        try:
            if not selected == None:
                if not len(selected) == 0:
                    # Get the uuid of the selected file.
                    fil_uuid = selected[0].text(0)

                    # Instantiate the file object of SOP.
                    self._current_file = features.File(is_new=False, uuid=fil_uuid, dbfile=self._database)

                    # Get the image properties from the instance.
                    if self._current_file.public == "1":
                        self.cbx_fil_pub.setChecked(True)
                    else:
                        self.cbx_fil_pub.setChecked(False)

                    if self._current_file.lock == "1":
                        self.cbx_fil_edit.setChecked(False)
                        self.cbx_fil_edit.setDisabled(True)
                    else:
                        self.cbx_fil_edit.setChecked(True)
                        self.cbx_fil_edit.setDisabled(False)

                    if self._current_file.file_type == "image":
                        # Set active control tab for material.
                        self.tab_src.setCurrentIndex(0)
                        self.getImageFileInfo(self._current_file)
                    if self._current_file.file_type == "audio":
                        # Set active control tab for material.
                        self.tab_src.setCurrentIndex(1)
                        self.getSoundFileInfo(self._current_file)
                        self.openMultimediaFile()
                    if self._current_file.file_type == "movie":
                        # Set active control tab for material.
                        self.tab_src.setCurrentIndex(1)
                        self.getSoundFileInfo(self._current_file)
                        self.openMultimediaFile()
                    if self._current_file.file_type == "text":
                        # Set active control tab for material.
                        self.tab_src.setCurrentIndex(2)
                        self.getTextFileInfo(self._current_file)
                    if self._current_file.file_type == "geometry":
                        # Set active control tab for material.
                        self.tab_src.setCurrentIndex(3)
                        self.refreshMap()
                else:
                    print("main::getCurrentFile(self)")
        except Exception as e:
            print("Error occured in main::getCurrentFile(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

        finally:
           print("End -> main::getCurrentFile")

    def editFileInformation(self):
        print("main::editFileInformation(self)")

        # Exit if the root directory is not loaded.
        if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

        # Exit if the current file is not existed.
        if self._current_file == None: return(None)

        try:
            # Exit if the none of a file is selected.
            if self.tre_fls.selectedItems() == None: return(None)

            # Check and edit file information.
            dlg_img_fil = fileInformationDialog.fileInformationDialog(parent=self, sop_file=self._current_file)

            # Show the dialog.
            isAccepted = dlg_img_fil.exec_()

            if isAccepted == 1:
                # Get attributes from text boxes.
                self._current_file.status = str(dlg_img_fil.cmb_fil_stts.currentText())
                self._current_file.operation = str(dlg_img_fil.cmb_fil_eope.currentText())
                self._current_file.alias = str(dlg_img_fil.tbx_fil_ali.text())                             # Alias
                self._current_file.operating_application = str(dlg_img_fil.tbx_fil_ope_app.text())         # Operating application
                self._current_file.caption = str(dlg_img_fil.tbx_fil_capt.text())                          # Caption
                self._current_file.description = str(dlg_img_fil.tbx_fil_dsc.text())                       # Description
                self._current_file.created_date = str(dlg_img_fil.dte_fil_dt_cre.text())
                self._current_file.modified_date = str(dlg_img_fil.dte_fil_dt_mod.text())
                self._current_file.public = int(dlg_img_fil.cbx_fil_pub.isChecked())
                self._current_file.lock = int(dlg_img_fil.cbx_fil_edit.isChecked())

                # Update the file information.
                self._current_file.dbUpdate(self._database)

                # Get the tree item index of currently selected.
                cur_tree_index = self.tre_fls.currentIndex().row()

                # Refresh image file list.
                self.refreshImageInfo()

                if self.tab_target.currentIndex() == 0:
                    if not self._current_consolidation == None:
                        # Get the uuid of the current consolidation.
                        con_uuid = self._current_consolidation.uuid

                        # Reset the current consolidation.
                        self._current_consolidation = features.Consolidation(is_new=False, uuid=con_uuid, dbfile=self._database)

                        # Set file information of consolidation images.
                        self.refreshFileList(self._current_consolidation)
                elif self.tab_target.currentIndex() == 1:
                    if not self._current_consolidation == None:
                        if not self._current_material == None:
                            # Get the uuid of the current material.
                            mat_uuid = self.current_material.uuid

                            # Reset the current consolidation.
                            self._current_material = features.Material(is_new=False, uuid=mat_uuid, dbfile=self._database)

                            # Set file information of material images.
                            self.refreshFileList(self._current_material)

                self.tre_fls.setCurrentItem(self.tre_fls.topLevelItem(cur_tree_index))
        except Exception as e:
            print("Error occured in main::editFileInformation(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def importFileCSV(self):
        print("main::importFileCSV(self)")

         # Exit if the root directory is not loaded.
        if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

        try:
            # Define directories for storing files.
            in_file = QFileDialog.getOpenFileName(self, "ファイルの選択")

            # Open and read the imported csv file.
            with open(in_file[0]) as table:
                # Initialyze the counter for reading line.
                cnt_line = 0

                # Initialyze the variables.
                feat_type = dict()
                fil_head = dict()

                for line in table:
                    line = line.strip()

                    # Parsing each line.
                    if cnt_line == 0:
                        # The case of header line.
                        cnt_haeder = 0

                        # Read the header line with comma.
                        headers = line.split(",")

                        for header in headers:
                            # Separate the class name and the attribute name with a period.
                            cls, item = header.split(".")

                            if cls == "file":
                                feat_type[cnt_haeder] = "file"

                                if item == "uuid": fil_head[cnt_haeder] = "uuid"
                                elif item == "consolidation": fil_head[cnt_haeder] = "consolidation"
                                elif item == "material": fil_head[cnt_haeder] = "material"
                                elif item == "created_date": fil_head[cnt_haeder] = "created_date"
                                elif item == "modified_date": fil_head[cnt_haeder] = "modified_date"
                                elif item == "file_name": fil_head[cnt_haeder] = "file_name"
                                elif item == "file_type": fil_head[cnt_haeder] = "file_type"
                                elif item == "alias_name": fil_head[cnt_haeder] = "alias_name"
                                elif item == "status": fil_head[cnt_haeder] = "status"
                                elif item == "make_public": fil_head[cnt_haeder] = "make_public"
                                elif item == "is_locked": fil_head[cnt_haeder] = "is_locked"
                                elif item == "source": fil_head[cnt_haeder] = "source"
                                elif item == "file_operation": fil_head[cnt_haeder] = "file_operation"
                                elif item == "operating_application": fil_head[cnt_haeder] = "operating_application"
                                elif item == "caption": fil_head[cnt_haeder] = "caption"
                                elif item == "description": fil_head[cnt_haeder] = "description"
                                elif item == "path": fil_head[cnt_haeder] = "path"

                                cnt_haeder += 1
                    else:
                        # The case of entry lines.
                        entries = line.split(",")

                        # Create a new SOP object of consolidation.
                        self._current_file = features.File(is_new=True, uuid=None, dbfile=None)

                        con_dir = ""
                        mat_dir = ""

                        for i in range(len(entries)):
                            # Give a NULL value if the entry is empty.
                            if entries[i] == "" : entries[i] = "NULL"

                            # Convert the string to the unicode.
                            if isinstance(entries[i], str): entries[i] = entries[i].decode('utf-8')

                            # Check the class of the current entry.

                            if feat_type[i] == "file":
                                print(fil_head[i])

                                if fil_head[i] == "uuid":
                                    if not entries[i] == "NULL":self._current_file.uuid = entries[i]
                                    else:self._current_file.uuid = str(uuid.uuid4())
                                elif fil_head[i] == "consolidation":
                                    if not entries[i] == "NULL": self._current_file.consolidation = entries[i]
                                    else: self._current_file.consolidation = None
                                elif fil_head[i] == "material":
                                    if not entries[i] == "NULL": sop_file.material = entries[i]
                                    else: sop_file.material = None
                                elif fil_head[i] == "created_date": sop_file.created_date = entries[i]
                                elif fil_head[i] == "modified_date":
                                    if entries[i] == "NULL":
                                        # Get current date and time.
                                        sop_file.modified_date = datetime.datetime.utcnow().isoformat()
                                    else:
                                        sop_file.modified_date = entries[i]
                                elif fil_head[i] == "file_name": sop_file.filename = entries[i]
                                elif fil_head[i] == "file_type": sop_file.file_type = entries[i]
                                elif fil_head[i] == "alias_name": sop_file.alias = entries[i]
                                elif fil_head[i] == "status": sop_file.status = entries[i]
                                elif fil_head[i] == "make_public": sop_file.public = entries[i]
                                elif fil_head[i] == "is_locked": sop_file.lock = entries[i]
                                elif fil_head[i] == "source": sop_file.source = entries[i]
                                elif fil_head[i] == "file_operation": sop_file.operation = entries[i]
                                elif fil_head[i] == "operating_application": sop_file.operating_application = entries[i]
                                elif fil_head[i] == "caption": sop_file.caption = entries[i]
                                elif fil_head[i] == "description": sop_file.description = entries[i]
                                elif fil_head[i] == "path":
                                    # Get the original image path.
                                    fil_org = entries[i]

                                    con_dir = None
                                    mat_dir = None
                                    itm_dir = None

                                    if sop_file.material != None:
                                        con_dir = os.path.join(self._consolidation_directory, sop_file.consolidation)
                                        mat_dir = os.path.join(con_dir, "Materials")
                                        itm_dir = os.path.join(mat_dir, sop_file.material)

                                    if sop_file.file_type == "image":
                                        # Define the path for saving files.
                                        img_path = os.path.join(itm_dir, "Images")
                                        img_ext = os.path.splitext(fil_org)[1]

                                        if img_ext.lower() == ".jpg":
                                            img_path_main = os.path.join(img_path, "Main")
                                            print(img_path_main)
                                            # Generate the GUID for the consolidation
                                            img_uuid = str(uuid.uuid4())
                                            print(img_uuid)
                                            # Define the destination file path.
                                            main_dest = os.path.join(img_path_main, img_uuid + ".jpg")
                                            print(main_dest)
                                            sop_file.filename =  general.getRelativePath(main_dest, "Consolidation")
                                            print(fil_org)
                                            if os.path.exists(fil_org):
                                                # Copy the original file.
                                                shutil.copy(fil_org, main_dest)
                                            else:
                                                print("File not found:" + fil_org)
                                        else:
                                            # Define the path for saving files.
                                            img_path = os.path.join(itm_dir, "Images")
                                            img_path_raw = os.path.join(img_path, "Raw")

                                            # Get the original image path.
                                            raw_ext = os.path.splitext(fil_org)[1]

                                            # Generate the GUID for the consolidation
                                            raw_uuid = str(uuid.uuid4())

                                            # Define the destination file path.
                                            raw_dest = os.path.join(img_path_raw, raw_uuid + raw_ext)

                                            sop_file.filename =  general.getRelativePath(raw_dest, "Consolidation")

                                            if os.path.exists(fil_org):
                                                # Copy the original file.
                                                shutil.copy(fil_org, raw_dest)
                                            else:
                                                print("File not found:" + fil_org)
                                    elif sop_file.file_type == "audio":
                                        # Define the path for saving files.
                                        snd_path = os.path.join(itm_dir, "Sounds")
                                        snd_ext = os.path.splitext(fil_org)[1]

                                        # Generate the GUID for the consolidation
                                        snd_uuid = str(uuid.uuid4())

                                        # Define the destination file path.
                                        snd_dest = os.path.join(snd_path, snd_uuid + snd_ext)

                                        sop_file.filename =  general.getRelativePath(snd_dest, "Consolidation")

                                        if os.path.exists(fil_org):
                                            # Copy the original file.
                                            shutil.copy(fil_org, snd_dest)
                                        else:
                                            print("File not found:" + fil_org)
                        # Insert the consolidation.
                        sop_file.dbInsert(self._database)
                    cnt_line += 1
            # Initialyze the tree view.
            self.tre_prj_item.clear()

            # Reflesh the last selection.
            self.refreshImageInfo()

            # Refresh the tree view.
            self.retriveProjectItems()
        except Exception as e:
            print("main::importFileCSV(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def exportFileCSV(self):
        print("main::exportFileCSV(self)")

         # Create a sqLite file if not exists.
        try:
            # Exit if the root directory is not loaded.
            if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

            # Get the output file name by using file save dialog.
            output, output_type = QFileDialog.getSaveFileName(self, "Export to", "output.csv","CSV File (*.csv)")

            if not output: return(None)

            # Open the file stream
            output_csv = open(output,"w")

            # Establish the connection to the self._database file.
            conn = sqlite.connect(self._database)

            if conn is not None:
                header_line = ""

                # Create a header.
                headers = [
                    "file.uuid",
                    "file.consolidation",
                    "file.material",
                    "file.created_date",
                    "file.modified_date",
                    "file.file_name",
                    "file.file_type",
                    "file.alias_name",
                    "file.status",
                    "file.make_public",
                    "file.is_locked",
                    "file.source",
                    "file.file_operation",
                    "file.operating_application",
                    "file.caption",
                    "file.description"
                ]
                # Write the header
                for header in headers:
                    header_line = header_line + header + ","

                # Write the hader line.
                output_csv.writelines(header_line.rstrip(",") + "\n")

                # Create the SQL query for selecting consolidation.
                sql_fil_sel = """SELECT uuid FROM file"""

                # Instantiate the cursor for query.
                cur_fil = conn.cursor()
                rows_fil = cur_fil.execute(sql_fil_sel)

                # Execute the query and get consolidation recursively
                for row_fil in rows_fil:
                    # Get attributes from the row.
                    fil_uuid = row_fil[0]

                    # Instantiate the consolidation.
                    sop_file = features.File(is_new=False, uuid=fil_uuid, dbfile=self._database)

                    fil_values = [
                        sop_file.uuid,
                        sop_file.consolidation,
                        sop_file.material,
                        sop_file.created_date,
                        sop_file.modified_date,
                        sop_file.filename,
                        sop_file.file_type,
                        sop_file.alias,
                        sop_file.status,
                        sop_file.public,
                        sop_file.lock,
                        sop_file.source,
                        sop_file.operation,
                        sop_file.operating_application,
                        sop_file.caption,
                        sop_file.description
                    ]

                    fil_generic_values = ""

                    for fil_value in fil_values:
                        if isinstance(fil_value, unicode) : fil_value = fil_value.encode('utf-8')

                        fil_generic_values = fil_generic_values + "," + str(fil_value).encode('utf-8')

                    # Writet the attribute lines.
                    output_csv.writelines(fil_generic_values.lstrip(",") + "\n")
        except Exception as e:
            print("main::exportFileCSV(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def getImageFileInfo(self, sop_image):
        print("main::getImageFileInfo(self, sop_image)")

        try:
            # Clear.
            self.tre_img_prop.clear()

            # Get the full path of the image.
            if sop_image.filename == "":
                img_file_path = os.path.join(os.path.join(self._source_directory, "images"),"noimage.jpg")
            else:
                if not os.path.exists(os.path.join(self._root_directory, sop_image.filename)):
                    img_file_path = os.path.join(os.path.join(self._source_directory, "images"),"noimage.jpg")
                else:
                    img_file_path = os.path.join(self._root_directory, sop_image.filename)

                    # Get file information by using "dcraw" library.
                    tags = imageProcessing.getMetaInfo(img_file_path)

                    # Show EXIF tags on the tree item view.
                    for tag in sorted(tags.keys()):
                        self.tre_img_prop.addTopLevelItem(QTreeWidgetItem([str(tag), str(tags[tag])]))

            # Refresh the tree view.
            self.tre_img_prop.show()

            # Show preview.
            self.showImage(img_file_path)

            # Adjust columns width.
            self.tre_img_prop.resizeColumnToContents(0)
            self.tre_img_prop.resizeColumnToContents(1)
        except Exception as e:
            print("Error occured in main::getImageFileInfo(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def getSoundFileInfo(self, sop_sound):
        print("main::getSoundFileInfo(self, sop_sound)")

    def getTextFileInfo(self, sop_text):
        print("main::getTextFileInfo(self, sop_text)")
        try:
            # Get the file path of the text.
            if not sop_text.filename == "":
                txt_file_path = os.path.join(self._root_directory, sop_text.filename)

                # Read the text file and show contexts on the text browser.
                if os.path.exists(txt_file_path):
                    # Open the text file.
                    txt_file_stream = open(txt_file_path, "r")

                    # Show text contents.
                    self.textBrowser.setText(txt_file_stream.read())

                    # Close the text file object.
                    txt_file_stream.close()
                else:
                    # Set empty text to the text browser.
                    self.textBrowser.setText("")
            else:
                # Set empty text to the text browser.
                self.textBrowser.setText("")
        except Exception as e:
            print("Error occured in main::getTextFileInfo(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def setFileInfo(self, sop_object):
        print("main::setFileInfo(self, sop_object)")

        try:
            # Check whether the object can be published or not.
            if sop_object.public == "1":
                self.cbx_fil_pub.setChecked(True)
            else:
                self.cbx_fil_pub.setChecked(False)

            # Check whether the object is locked or not.
            if sop_object.lock == "1":
                self.cbx_fil_edit.setChecked(False)
                self.cbx_fil_edit.setDisabled(True)
            else:
                self.cbx_fil_edit.setChecked(True)
                self.cbx_fil_edit.setDisabled(False)
                self.cbx_fil_edit.setEnabled(True)

            # Get get the status of the object.
            fil_status = sop_object.status

            if fil_status == "Original":
                if self.cbx_fil_original.isChecked() == True:
                    # Update the tree view.

                    tre_fls_item = QTreeWidgetItem(self.tre_fls)

                    tre_fls_item.setText(0, sop_object.uuid)
                    tre_fls_item.setText(1, sop_object.alias)
                    tre_fls_item.setText(2, sop_object.file_type)

                    setupMainSkin.setDefaultFileText(tre_fls_item, status="original", skin=self._skin)
            elif fil_status == "Removed":
                if self.cbx_fil_deleted.isChecked() == True:

                    # Update the tree view.
                    tre_fls_item = QTreeWidgetItem(self.tre_fls)

                    tre_fls_item.setText(0, sop_object.uuid)
                    tre_fls_item.setText(1, sop_object.alias)
                    tre_fls_item.setText(2, sop_object.file_type)

                    setupMainSkin.setDefaultFileText(tre_fls_item, status="removed", skin=self._skin)
            else:
                # Update the tree view.
                tre_fls_item = QTreeWidgetItem(self.tre_fls)

                tre_fls_item.setText(0, sop_object.uuid)
                tre_fls_item.setText(1, sop_object.alias)
                tre_fls_item.setText(2, sop_object.file_type)
        except Exception as e:
            print("Error occured in setFileInfo(self, sop_object)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def updateFile(self):
        print("main::updateFile(self)")

        # Exit if the root directory is not loaded.
        if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

        try:
            selected = self.tre_fls.selectedItems()

            if (selected != None) and (len(selected) != 0):
                fil_uuid = selected[0].text(0)

                cur_file = features.File(is_new=False, uuid=fil_uuid, dbfile=self._database)
                cur_file.public = int(self.cbx_fil_pub.isChecked())

                # Update the file information.
                cur_file.dbUpdate(self._database)
        except Exception as e:
            print("Error occured in updateFile(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def refreshImageInfo(self):
        print("Start -> main::refreshImageInfo(self)")

        try:
            # Clear the file list tree view..
            self.tre_fls.clear()

            # Initialyze the checkboxes.
            self.cbx_fil_pub.setChecked(False)
            self.cbx_fil_edit.setChecked(False)

            # Define the no image avatar for preview panel.
            noimage_path = os.path.join(os.path.join(self._source_directory, "images"),"noimage.jpg")

            self.showImage(noimage_path)

            # Clear entries on image properties view.
            self.tre_img_prop.clear()

            # Initialyze checkboxes.
            self.cbx_fil_pub.setChecked(False)
            self.cbx_fil_edit.setChecked(True)
            self.cbx_fil_edit.setDisabled(False)

            # Clear the text brower content.
            self.textBrowser.setText("")
        except Exception as e:
            print("Error occured in main::refreshImageInfo(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)
        finally:
            print("End -> main::refreshImageInfo(self)")

    def deleteSelectedFile(self):
        print("main::deleteSelectedFile(self)")

        try:
            # Exit if the root directory is not loaded.
            if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

            # Exit if the tree object is not selected.
            selected = self.tre_fls.selectedItems()
            if (selected == None or len(selected) == 0): return(None)

            # Exit if the selected file is locked.
            if not self.cbx_fil_edit.isChecked():
                error.ErrorMessageFileLocked()
                return(None)

            # Confirm deletion.
            if self._language == "ja":
                reply = QMessageBox.question(
                        self,
                        'ファイルの削除',
                        '選択されたファイルを本当に削除しますか？',
                        QMessageBox.Yes,
                        QMessageBox.No
                )
            elif self._language == "en":
                reply = QMessageBox.question(
                        self,
                        'Delete the selected file.',
                        'Would you delete the selected file?',
                        QMessageBox.Yes,
                        QMessageBox.No
                )

            # Confirm deleting the consolidation.
            if not reply == QMessageBox.Yes: return(None)

            # Instantiate the file object of SOP.
            self.getCurrentFile()
            if self._current_file == None: return(None)

            # Get the time for closing GIMP.
            time_delete = datetime.datetime.utcnow().isoformat()

            self._current_file.alias = "Already Removed."
            self._current_file.modified_date = time_delete
            self._current_file.status = "Removed"
            self._current_file.lock = True
            self._current_file.public = False
            self._current_file.operation = "Removed"
            self._current_file.operating_application = "Survey Data Collector"
            self._current_file.caption = "Removed"

            # Get the path of the selected file.
            if self._current_file.file_type == "geometry":
                geo_path = os.path.splitext(self._current_file.filename)[0]

                wkt_path = os.path.join(self._root_directory, geo_path + ".wkt")
                htm_path = os.path.join(self._root_directory, geo_path + ".html")

                print(wkt_path)

                if os.path.exists(wkt_path): os.remove(wkt_path)
                if os.path.exists(htm_path): os.remove(htm_path)

                # Set the file name blank.
                self._current_file.filename = ""

                # Update DB table.
                self._current_file.dbUpdate(self._database)
            else:
                fil_path = os.path.join(self._root_directory, self._current_file.filename)

                if os.path.exists(fil_path): os.remove(fil_path)

                # Set the file name blank.
                self._current_file.filename = ""

                # Update DB table.
                self._current_file.dbUpdate(self._database)

            # Refresh the image file list.
            sop_object = None
            if self._current_file.material == "":
                sop_object = features.Consolidation(is_new=False, uuid=self._current_file.consolidation, dbfile=self._database)
            else:
                sop_object = features.Material(is_new=False, uuid=self._current_file.material, dbfile=self._database)

            # Refresh the image file list.
            self.refreshFileList(sop_object)
        except Exception as e:
            print("Error occured in main::deleteSelectedFile(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    # ==========================
    # Sound Play
    # ==========================
    def openMultimediaFile(self):
        print("main::openMultimediaFile(self)")

        try:
            if not self.mediaPlayer.state() == QMediaPlayer.PlayingState:
                setupMainSkin.setPlayingIcon(icon_path=self._icon_directory, btn_play=self.mlt_btn_play, skin=self._skin)
                fileName = os.path.join(self._root_directory, self._current_file.filename)

                if fileName != '':
                    if self._current_file.file_type == "audio" or self._current_file.file_type == "movie":
                        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
                        self.mlt_btn_play.setEnabled(True)
            else:
                setupMainSkin.setPauseButtonIcon(icon_path=self._icon_directory, btn_pause=self.mlt_btn_play, skin=self._skin)
        except Exception as e:
            print("Error occured in main::openMultimediaFile(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def playMedia(self):
        print("main::playMedia(self)")

        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        print("main::mediaStateChanged(self, state)")
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            setupMainSkin.setPauseButtonIcon(icon_path=self._icon_directory, btn_pause=self.mlt_btn_play, skin=self._skin)
        else:
            setupMainSkin.setPlayingIcon(icon_path=self._icon_directory, btn_play=self.mlt_btn_play, skin=self._skin)

    def positionChanged(self, position):
        print("main::positionChanged(self, state)")
        self.mlt_sld_play.setValue(position)

    def durationChanged(self, duration):
        print("main::durationChanged(self, duration)")
        self.mlt_sld_play.setRange(0, duration)

    def setPosition(self, position):
        print("main::setPosition(self, position)")
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        print("main::setPosition(self, handleError)")
        self.mlt_btn_play.setEnabled(False)
        e = self.mediaPlayer.errorString()

        print("Error occured in main::openMultimediaFile(self)")
        print(str(e))
        error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
        return(None)

    # ==========================
    # Text processing tools
    # ==========================
    def textEditWithPhoto(self):
        print("main::textEditWithPhoto(self)")

        try:
            # Exit if the root directory is not loaded.
            if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

            # Exit if the tree object is not selected.
            selected = self.tre_prj_item.selectedItems()
            if (selected == None or len(selected) == 0): error.ErrorMessageCurrentConsolidation(language=self._language); return(None)

            # Exit if current object is not set.
            if self.tab_target.currentIndex() == 0:
                # Exit if the current consolidation is not selected.
                if self._current_consolidation == None: error.ErrorMessageCurrentConsolidation(language=self._language); return(None)
            elif self.tab_target.currentIndex()==1:
                # Exit if the current consolidation is not selected.
                if self._current_consolidation == None: error.ErrorMessageCurrentConsolidation(language=self._language); return(None)

                # Exit if the current consolidation is not selected.
                if self._current_material == None: error.ErrorMessageCurrentMaterial(language=self._language); return(None)

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
                sop_object = self._current_consolidation

                # Get the item path of the selected consolidaiton.
                item_path = os.path.join(self._consolidation_directory, sop_object.uuid)
            elif self.tab_target.currentIndex() == 1:
                # Get the current material uuid.
                mat_uuid = self.tbx_mat_uuid.text()

                # Instantiate the material.
                sop_object = self._current_material

                # Instantiate the consolidation.
                con_uuid = sop_object.consolidation
                con_path = os.path.join(self._consolidation_directory, sop_object.consolidation)
                item_path = os.path.join(os.path.join(con_path, "Materials"), sop_object.uuid)
            else:
                return(None)

            # Exit if none of objecs are instantiated.
            if sop_object == None: return(None)

            if sop_object.texts == None: sop_object.texts = list()

            # Define the path for saving images.
            txt_path = os.path.join(item_path, "Texts"); general.createPathIfNotExists(txt_path)
            img_path = os.path.join(os.path.join(item_path, "Images"),"Main")

            # Check the result of the tethered image.
            self.dialogJotting = textEditWithPhoto.jottingWithImage(parent=self,
                                                                    img_path=img_path,
                                                                    txt_path=txt_path,
                                                                    sop=sop_object,
                                                                    con_uuid=con_uuid,
                                                                    mat_uuid=mat_uuid)
            isAccepted = self.dialogJotting.exec_()

        except Exception as e:
            print("Error occured in main::textEditWithPhoto(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

        finally:
            # Refresh the file list.
            if sop_object.__class__.__name__ == "Consolidation":
                # Get the Consolidation if the node have no parent.
                selected_uuid = self._current_consolidation.uuid

                # Set current objects.
                self._current_consolidation = features.Consolidation(is_new=False, uuid=selected_uuid, dbfile=self._database)

                # Set attributes of the consolidation to input boxes.
                self.setConsolidationInfo(self._current_consolidation)

                # Set active control tab for consolidation.
                self.tab_target.setCurrentIndex(0)

                # Set file information of material images.
                self.refreshFileList(self._current_consolidation)
                self.toggleCurrentSourceTab()
            elif sop_object.__class__.__name__ == "Material":
                # Get the Materil if the node have a parent.
                selected_uuid = self._current_material.uuid

                # Set current material.
                self._current_material = features.Material(is_new=False, uuid=selected_uuid, dbfile=self._database)
                self._current_consolidation = features.Consolidation(is_new=False, uuid=self._current_material.consolidation, dbfile=self._database)

                # Set attributes of the consolidation and the material to the input boxes.
                self.setConsolidationInfo(self._current_consolidation)
                self.setMaterialInfo()
                # Set active control tab for consolidation.
                self.tab_target.setCurrentIndex(1)

                # Set file information of material images.
                self.refreshFileList(self._current_material)
                self.toggleCurrentSourceTab()

    # ==========================
    # Map processing tools
    # ==========================
    def checkLeafletLibrary(self, item_path):
        print("checkLeafletLibrary(self)")

        # Generate the GUID for the consolidation
        geo_dir = os.path.join(item_path, 'Geometries')
        if not os.path.exists(geo_dir):
            os.mkdir(geo_dir)
            print("The directory for geometries is created.")
        # Check library of leaflet path.
        geo_lib = os.path.join(self._map_directory,"lib")
        if not  os.path.exists(os.path.join(geo_dir,"lib")):
            shutil.copytree(geo_lib, os.path.join(geo_dir,"lib"))
            print("Libraries for leaflet is copied.")
        return(True)

    def setDefaultMap(self):
        print("main::setDefaultMap(self)")

        try:
            location = os.path.join(self._map_directory,"defaul.html")
            geospatial.writeHtml(self, location)
            self.geo_view.setUrl(QUrl("file:///" + location))
        except Exception as e:
            print("Error occured in main::refreshMap(self)")
            print(str(e))

    def refreshMap(self):
        print("main::refreshMap(self)")

        try:
            location = os.path.join(self._map_directory,"location.html")
            geospatial.writeHtml(self, location)
            self.geo_view.setUrl(QUrl("file:///" + location))

            if self.tab_target.currentIndex() == 0:
                if not self._current_file == None:
                    if self._current_file.file_type == "geometry":
                        con_dir = os.path.join(self._consolidation_directory, self._current_consolidation.uuid)
                        geo_dir = os.path.join(con_dir, "Geometries")

                        # Check whether the geometry directory is exists or not.
                        if not os.path.exists(geo_dir):
                            # Create a directory for storing geometries.
                            os.mkdir(geo_dir)

                            # Set the default map.
                            self.setDefaultMap()

                            # Exit this proces
                            return(None)

                        wkt_path = os.path.join(self._root_directory, self._current_file.filename)

                        # Check whether the output file is exists or not.
                        if not os.path.exists(wkt_path):
                            # Set the default map.
                            self.setDefaultMap()

                            # Exit this proces
                            return(None)
                        else:
                            print(wkt_path)

                            output = self.publishMap(wkt_path)
                            # Load a map.
                            self.geo_view.setUrl(QUrl("file:///" + output))
                    else:
                        self.setDefaultMap()
                else:
                    self.setDefaultMap()
            elif self.tab_target.currentIndex() == 1:
                lat = self._current_material.latitude
                lon = self._current_material.longitude

                if not (lat == "" or lat == None):
                    if not (lon == "" or lon == None):
                        marker = geospatial.mapMarker(geom=[lat, lon])
                        location = os.path.join(self._map_directory,"location.html")
                        geospatial.writeHtml(self, output = location, map_zoom = 15, map_center = [lat, lon], markers = [marker])
                        self.geo_view.setUrl(QUrl("file:///" + location))
                    else:
                        self.setDefaultMap()
                else:
                    self.setDefaultMap()
        except Exception as e:
            print("Error occured in main::refreshMap(self)")
            print(str(e))

            # Set the default map.
            self.setDefaultMap()

            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def publishMap(self, wkt_path):
        print("main::publishMap(self, wkt_path)")

        dbl_Markers = []
        map_Markers = []
        markers = open(wkt_path, "r")

        for marker in markers:
            geojson = convert.wkt_to_geojson(marker)
            coords = json.loads(geojson).get("coordinates")

            dbl_Markers.append(coords)

            map_Marker = geospatial.mapMarker(geom = coords, desc = "")
            map_Markers.append(map_Marker)

        map_center = np.mean(np.array(dbl_Markers), axis=0)

        geo_name, ext = os.path.splitext(wkt_path)
        map_path = geo_name + ".html"

        geospatial.writeHtml(self, output=map_path, map_zoom = 10, map_center = map_center, markers = map_Markers)

        return(map_path)

    def addGeometryByGeocoding(self):
        print("main::addGeometryByGeocoding(self)")

        # Exit if the root directory is not loaded.
        if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

        # Exit if the tree object is not selected.
        selected = self.tre_prj_item.selectedItems()
        if (selected == None or len(selected) == 0): error.ErrorMessageTreeItemNotSelected(language=self._language); return(None)

        # Initialyze the variables.
        sop_object = None
        item_path = None
        con_uuid = ""
        mat_uuid = ""
        geo_name = ""

        try:
            # Get the geoname from the text box.
            geo_name = self.tbx_con_geoname.text()

            if geo_name == None or geo_name == "":
                if self._language == "en":
                    # Create error messages.
                    error_title = "Geocoding error"
                    error_msg = "Location is not defined in consolidation"
                    error_info = "Location is not defined in consolidation"
                    error_icon = QMessageBox.Critical
                    error_detailed = "Geocoding function is applied for location entry of the consolidation."

                    general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
                elif self._language == "ja":
                    # Create error messages.
                    error_title = "ジオコーディングのエラー"
                    error_msg = "検索するべき地名が「地理識別子」にセットされていません。"
                    error_info = "この機能は統合体の「地理識別子」に適用されます。"
                    error_icon = QMessageBox.Critical
                    error_detailed = "この機能は統合体の「地理識別子」に適用されます。"

                    general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
                return(none)

            # Get item path of the current object.
            if self.tab_target.currentIndex() == 0:
                # Exit if the current consolidation is not selected.
                if self._current_consolidation == None: error.ErrorMessageCurrentObject(language=self._language); return(None)

                # Get the current object.
                sop_object = self._current_consolidation

                # Get uuids.
                con_uuid = sop_object.uuid
                mat_uuid = ""

                # Get the item path of the selected consolidaiton.
                item_path = os.path.join(self._consolidation_directory, sop_object.uuid)

            elif self.tab_target.currentIndex() == 1:
                # Exit if the current material is not selected.
                if self._current_material == None: error.ErrorMessageCurrentObject(language=self._language); return(None)

                # Get the current object.
                sop_object = self._current_material

                # Get uuids.
                con_uuid = sop_object.consolidation
                mat_uuid = sop_object.uuid

                # Define the path for saving images.
                con_path = os.path.join(self._consolidation_directory, sop_object.consolidation)
                item_path = os.path.join(os.path.join(con_path, "Materials"), sop_object.uuid)

            # Check whether current object has images.
            if sop_object.geometries == None: sop_object.geometries = list()

            # Check the path to the leaflet library.
            self.checkLeafletLibrary(item_path)

            # Get the current date and time.
            now = datetime.datetime.utcnow().isoformat()

            # Find the file of geometry which is acquired by geocoded.
            geo_uuid = None
            for geometry in sop_object.geometries:
                if geometry.operation == "Geocoding":
                    # Get the uuid from the existing object.
                    geo_uuid = geometry.uuid

                    # Instantiate the File class.
                    wkt_file = features.File(is_new=False, uuid=geo_uuid, dbfile=self._database)
                    wkt_file.modified_date = now

                    # Update the file information
                    wkt_file.dbUpdate(self._database)

                    # Update the existing file.
                    geo_path = os.path.join(self._root_directory, self._current_file.filename)
                    self.createMapByLocationName(geo_name, geo_path)

            # If geocoded is existed geocoded file is updated else new file is created.
            if geo_uuid == None:
                # Generate new UUID.
                geo_uuid = str(uuid.uuid4())

                # Generate the WKT file path.
                geo_dir = os.path.join(item_path, 'Geometries')
                geo_path = os.path.join(geo_dir, geo_uuid + ".wkt")

                # Instantiate the File class.
                wkt_file = features.File(is_new=True, uuid=geo_uuid, dbfile=None)
                wkt_file.material = mat_uuid
                wkt_file.consolidation = con_uuid
                wkt_file.filename = general.getRelativePath(geo_path, "Consolidation")
                wkt_file.created_date = now
                wkt_file.modified_date = now
                wkt_file.file_type = "geometry"
                wkt_file.alias = "Geocoded"
                wkt_file.status = "Automatically Generated"
                wkt_file.lock = False
                wkt_file.public = False
                wkt_file.source = "Nothing"
                wkt_file.operation = "Geocoding"
                wkt_file.operating_application = "Survey Data Collector"
                wkt_file.caption = "Geocoded Location"
                wkt_file.description = ""

                # Execute the SQL script.
                wkt_file.dbInsert(self._database)

                # Add the image to the object.
                sop_object.geometries.insert(0, wkt_file)

                # Create a wkt file and its corresponding leaflet file.
                self.createMapByLocationName(geo_name, geo_path)
            # Refresh the map
            self.refreshMap()

            # Refresh the file list.
            if sop_object.__class__.__name__ == "Consolidation":
                self._current_consolidation = sop_object
                self.refreshFileList(self._current_consolidation)
            elif sop_object.__class__.__name__ == "Material":
                self._current_material = sop_object
                self.refreshFileList(self._current_material)
        except Exception as e:
            print("Error occured in main::addGeometryByGeocoding(self)")
            print(str(e))

            # Set the default map.
            self.setDefaultMap()

            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def createMapByLocationName(self, geo_name, wkt_path):
        print("main::createMapByLocationName(self, wkt_path)")

        try:
            if not self._proxy == "No Proxy":
                proxy = {'https': self._proxy}
                latlon = geospatial.geoCoding(geo_name, proxy)
            else:
                latlon = geospatial.geoCoding(geo_name)

            latitude = latlon[0]
            longitude = latlon[1]

            wkt_pt = "POINT (%s %s)\n" % (latitude, longitude)

            marker = open(wkt_path, "w")
            marker.write(wkt_pt)
            marker.close()

            self.publishMap(wkt_path)

            return(wkt_path)
        except Exception as e:
            print("Error occured in main::createMapByLocationName(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def searchLocationOnMap(self):
        print("main::searchLocationOnMap(self)")

        try:
            geo_name = self.txt_map_search.text()
            output = os.path.join(self._map_directory,"location.html")

            if not self._proxy == "No Proxy":
                proxy = {'https': self._proxy}
                geospatial.moveMapTo(self, geo_name, output, proxies=proxy)
            else:
                geospatial.moveMapTo(self, geo_name, output)
            self.geo_view.setUrl(QUrl("file:///" + output))
        except Exception as e:
            print("Error occured in main::searchLocationOnMap(self)")
            print(str(e))

            # Set the default map.
            self.setDefaultMap()

            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)
    # ==========================
    # Image processing tools
    # ==========================
    def openWithGimp(self):
        print("main::openWithGimp(self)")

        try:
            # Instantiate the file object of SOP.
            if self._current_file == None: return(None)

            if self._current_file.file_type == "image":
                # Set active control tab for material.
                self.tab_src.setCurrentIndex(0)
                self.getImageFileInfo(self._current_file)

                # Get the image path.
                img_path = os.path.join(self._root_directory, self._current_file.filename)

                if os.path.exists(img_path):
                    # Chec the extension of the file.
                    ext = os.path.splitext(img_path)[1].lower()

                    # Cancel if the file extension is not JPEG.
                    if not (ext == ".jpg" or ext == ".jpeg"):
                        # Create error messages.
                        error.ErrorMessageEditImageFile()

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
                    img_gimp = imageProcessing.openWithGimp(new_file)

                    if not img_gimp == None:
                        # Get the time for closing GIMP.
                        time_close = datetime.datetime.utcnow().isoformat()

                        # Instantiate the File class.
                        img_file = features.File(is_new=True, uuid=new_uuid, dbfile=None)
                        img_file.material = self._current_file.material
                        img_file.consolidation = self._current_file.consolidation
                        img_file.filename = general.getRelativePath(new_file, "Consolidation")
                        img_file.created_date = time_open
                        img_file.modified_date = time_close
                        img_file.file_type = "image"
                        img_file.alias = "Edited by GIMP"
                        img_file.status = "Edited"
                        img_file.lock = False
                        img_file.public = False
                        img_file.source = self._current_file.uuid
                        img_file.operation = "Edited by GIMP"
                        img_file.operating_application = "GIMP"
                        img_file.caption = "Edited by GIMP"
                        img_file.description = "This file is edited by GIMP."

                        img_file.dbInsert(self._database)

                        sop_object = None
                        if img_file.material == "":
                            sop_object = features.Consolidation(is_new=False, uuid=img_file.consolidation, dbfile=self._database)
                        else:
                            sop_object = features.Material(is_new=False, uuid=img_file.material, dbfile=self._database)

                        # Refresh the image file list.
                        self.refreshFileList(sop_object)
            else:
                error.ErrorMessageFileNotExist()

                # Returns nothing.
                return(None)
        except Exception as e:
            print("Error occured in main::openWithGimp(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def rotateImageLeft(self):
        print("rotateImageLeft(self)")

        # Exit if the root directory is not loaded.
        if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

        # Rotate the image -90 degree.
        self.rotateImage(-90)

    def rotateImageRight(self):
        print("rotateImageRight(self)")

        # Exit if the root directory is not loaded.
        if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

        # Rotate the image 90 degree.
        self.rotateImage(90)

    def rotateImageInvert(self):
        print("rotateImageInvert(self)")

        # Exit if the root directory is not loaded.
        if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

        # Rotate the image 180 degree.
        self.rotateImage(180)

    def rotateImage(self, angle):
        print("main::rotateImage(self, angle)")

        try:
            # Exit if SOP object is not instantiated.
            if self._current_file == None: return(None)

            # Get the image path.
            img_path = os.path.join(self._root_directory, self._current_file.filename)

            # Exit if selected file is not exists.
            if not os.path.exists(img_path): error.ErrorMessageFileNotExist(); return(None)

            if self._current_file.file_type == "image":
                # Set active control tab for material.
                self.tab_src.setCurrentIndex(0)
                self.getImageFileInfo(self._current_file)

                # Chec the extension of the file.
                ext = os.path.splitext(img_path)[1].lower()

                # Cancel if the file extension is not JPEG.
                if not (ext == ".jpg" or ext == ".jpeg"):
                    # Create error messages.
                    error.ErrorMessageEditImageFile()

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
                img_rot = imageProcessing.rotation(img_path, new_file, angle)
                if img_rot == None: return(None)

                # Copy the exif information.
                general.copyExif(img_path, new_file)

                # Get the time for closing GIMP.
                time_close = datetime.datetime.utcnow().isoformat()

                # Instantiate the File class.
                img_file = features.File(is_new=True, uuid=new_uuid, dbfile=None)
                img_file.material = self._current_file.material
                img_file.consolidation = self._current_file.consolidation
                img_file.filename = general.getRelativePath(new_file, "Consolidation")
                img_file.created_date = time_open
                img_file.modified_date = time_close
                img_file.file_type = "image"
                img_file.alias = "Rotated(" + str(angle) + " degree)"
                img_file.status = "Edited"
                img_file.lock = False
                img_file.public = False
                img_file.source = self._current_file.uuid
                img_file.operation = "Rotating " + str(angle) + " degree"
                img_file.operating_application = "Survey Data Collector"
                img_file.caption = "Rotated(" + str(angle) + " degree)"
                img_file.description = "Rotated(" + str(angle) + " degree) by this system."

                img_file.dbInsert(self._database)

                sop_object = None
                if img_file.material == "":
                    sop_object = features.Consolidation(is_new=False, uuid=img_file.consolidation, dbfile=self._database)
                else:
                    sop_object = features.Material(is_new=False, uuid=img_file.material, dbfile=self._database)

                # Refresh the image file list.
                self.refreshFileList(sop_object)
        except Exception as e:
            print("Error occured in main::rotateImage(self, angle)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def makeMonoImage(self):
        print("main::makeMonoImage(self, angle)")

        try:
            # Exit if SOP object is not instantiated.
            if self._current_file == None: return(None)

            # Get the image path.
            img_path = os.path.join(self._root_directory, self._current_file.filename)

            # Exit if selected file is not exists.
            if not os.path.exists(img_path): error.ErrorMessageFileNotExist(); return(None)

            if self._current_file.file_type == "image":
                # Set active control tab for material.
                self.tab_src.setCurrentIndex(0)
                self.getImageFileInfo(self._current_file)

                # Chec the extension of the file.
                ext = os.path.splitext(img_path)[1].lower()

                # Cancel if the file extension is not JPEG.
                if not (ext == ".jpg" or ext == ".jpeg"):
                    # Create error messages.
                    error.ErrorMessageEditImageFile()

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
                img_file.material = self._current_file.material
                img_file.consolidation = self._current_file.consolidation
                img_file.filename = general.getRelativePath(new_file, "Consolidation")
                img_file.created_date = time_open
                img_file.modified_date = time_close
                img_file.file_type = "image"
                img_file.alias = "Grayscale version"
                img_file.status = "Edited"
                img_file.lock = False
                img_file.public = False
                img_file.source = self._current_file.uuid
                img_file.operation = "Grayscale"
                img_file.operating_application = "Survey Data Collector"
                img_file.caption = "Grayscale version"
                img_file.description = "Make grayscale by this system."

                img_file.dbInsert(self._database)

                # Initialize the SOP osbject.
                sop_object = None
                if img_file.material == "":
                    sop_object = features.Consolidation(is_new=False, uuid=img_file.consolidation, dbfile=self._database)
                else:
                    sop_object = features.Material(is_new=False, uuid=img_file.material, dbfile=self._database)

                # Refresh the image file list.
                self.refreshFileList(sop_object)
            else:
                error.ErrorMessageEditImageFile()
        except Exception as e:
            print("Error occured in main::makeMonoImage(self, angle)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def adjustWhiteBalance(self):
        print("main::adjustWhiteBalance(self)")

        try:
            # Exit if SOP object is not instantiated.
            if self._current_file == None: return(None)

            # Get the image path.
            img_path = os.path.join(self._root_directory, self._current_file.filename)

            # Exit if selected file is not exists.
            if not os.path.exists(img_path): error.ErrorMessageFileNotExist(); return(None)

            if self._current_file.file_type == "image":
                # Set active control tab for material.
                self.tab_src.setCurrentIndex(0)
                self.getImageFileInfo(self._current_file)

                # Chec the extension of the file.
                ext = os.path.splitext(img_path)[1].lower()

                # Cancel if the file extension is not JPEG.
                if not (ext == ".jpg" or ext == ".jpeg"):
                    # Create error messages.
                    error.ErrorMessageEditImageFile()

                    # Returns nothing.
                    return(None)

                # Define the new uuid for the image.
                new_uuid = str(uuid.uuid4())

                # Get the time for opening GIMP.
                time_open = datetime.datetime.utcnow().isoformat()

                # Get the parent directory of the original image.
                out_dir = os.path.dirname(img_path)
                new_file = os.path.join(out_dir, new_uuid+".jpg")

                # Adjust the white balance.
                imageProcessing.autoWhiteBalance(img_path, new_file, method = self._awb_algo)

                # Copy exif information.
                general.copyExif(img_path, new_file)

                # Get the time for closing GIMP.
                time_close = datetime.datetime.utcnow().isoformat()

                # Instantiate the File class.
                img_file = features.File(is_new=True, uuid=new_uuid, dbfile=None)
                img_file.material = self._current_file.material
                img_file.consolidation = self._current_file.consolidation
                img_file.filename = general.getRelativePath(new_file, "Consolidation")
                img_file.created_date = time_open
                img_file.modified_date = time_close
                img_file.file_type = "image"
                img_file.alias = "Automatic white balance adjusting"
                img_file.status = "Edited"
                img_file.lock = False
                img_file.public = False
                img_file.source = self._current_file.uuid
                img_file.operation = "White Balance Adjustment"
                img_file.operating_application = "Survey Data Collector"
                img_file.caption = "White balance adjusted"
                img_file.description = "Make Auto White Balance with " + self._awb_algo +" by this system."

                # Insert the new entry to the database.
                img_file.dbInsert(self._database)

                # Initialize the SOP object.
                sop_object = None
                if img_file.material == "":
                    sop_object = features.Consolidation(is_new=False, uuid=img_file.consolidation, dbfile=self._database)
                else:
                    sop_object = features.Material(is_new=False, uuid=img_file.material, dbfile=self._database)

                # Refresh the image file list.
                self.refreshFileList(sop_object)
            else:
                error.ErrorMessageEditImageFile()
        except Exception as e:
            print("Error occured in main::adjustWhiteBalance(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def enhanceImage(self):
        print("main::enhanceImage(self)")

        try:
            # Exit if SOP object is not instantiated.
            if self._current_file == None: return(None)

            # Get the image path.
            img_path = os.path.join(self._root_directory, self._current_file.filename)

            # Exit if selected file is not exists.
            if not os.path.exists(img_path): error.ErrorMessageFileNotExist(); return(None)

            if self._current_file.file_type == "image":
                # Set active control tab for material.
                self.tab_src.setCurrentIndex(0)
                self.getImageFileInfo(self._current_file)

                # Chec the extension of the file.
                ext = os.path.splitext(img_path)[1].lower()

                # Cancel if the file extension is not JPEG.
                if not (ext == ".jpg" or ext == ".jpeg"):
                    # Create error messages.
                    error.ErrorMessageEditImageFile()

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
                img_file.material = self._current_file.material
                img_file.consolidation = self._current_file.consolidation
                img_file.filename = general.getRelativePath(new_file, "Consolidation")
                img_file.created_date = time_open
                img_file.modified_date = time_close
                img_file.file_type = "image"
                img_file.alias = "Normalized version"
                img_file.status = "Edited"
                img_file.lock = False
                img_file.public = False
                img_file.source = self._current_file.uuid
                img_file.operation = "Normalized"
                img_file.operating_application = "Survey Data Collector"
                img_file.caption = "Normalized version"
                img_file.description = "Make normalized by this system."

                img_file.dbInsert(self._database)

                # Initialize the SOP object.
                sop_object = None
                if img_file.material == "":
                    sop_object = features.Consolidation(is_new=False, uuid=img_file.consolidation, dbfile=self._database)
                else:
                    sop_object = features.Material(is_new=False, uuid=img_file.material, dbfile=self._database)

                # Refresh the image file list.
                self.refreshFileList(sop_object)
            else:
                error.ErrorMessageEditImageFile()
        except Exception as e:
            print("Error occured in main::enhanceImage(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def extractContour(self):
        print("main::extractContour(self)")

        try:
            # Exit if SOP object is not instantiated.
            if self._current_file == None: return(None)

            # Get the image path.
            img_path = os.path.join(self._root_directory, self._current_file.filename)

            # Exit if selected file is not exists.
            if not os.path.exists(img_path): error.ErrorMessageFileNotExist(); return(None)

            if self._current_file.file_type == "image":
                # Set active control tab for material.
                self.tab_src.setCurrentIndex(0)
                self.getImageFileInfo(self._current_file)

                # Chec the extension of the file.
                ext = os.path.splitext(img_path)[1].lower()

                # Cancel if the file extension is not JPEG.
                if not (ext == ".jpg" or ext == ".jpeg"):
                    error.ErrorMessageEditImageFile()

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
                img_file.material = self._current_file.material
                img_file.consolidation = self._current_file.consolidation
                img_file.filename = general.getRelativePath(new_file, "Consolidation")
                img_file.created_date = time_open
                img_file.modified_date = time_close
                img_file.file_type = "image"
                img_file.alias = "Automatically cropped"
                img_file.status = "Edited"
                img_file.lock = False
                img_file.public = False
                img_file.source = self._current_file.uuid
                img_file.operation = "Cropped"
                img_file.operating_application = "Survey Data Collector"
                img_file.caption = "Cropped version"
                img_file.description = "Make cropped by this system."

                img_file.dbInsert(self._database)

                sop_object = None
                if img_file.material == "":
                    sop_object = features.Consolidation(is_new=False, uuid=img_file.consolidation, dbfile=self._database)
                else:
                    sop_object = features.Material(is_new=False, uuid=img_file.material, dbfile=self._database)

                # Refresh the image file list.
                self.refreshFileList(sop_object)
            else:
                error.ErrorMessageEditImageFile()
        except Exception as e:
            print("Error occured in main::extractContour(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def negativeToPositive(self):
        print("main::negativeToPositive(self)")

        try:
            # Exit if SOP object is not instantiated.
            if self._current_file == None: return(None)

            # Get the image path.
            img_path = os.path.join(self._root_directory, self._current_file.filename)

            # Exit if selected file is not exists.
            if not os.path.exists(img_path): error.ErrorMessageFileNotExist(); return(None)

            if self._current_file.file_type == "image":
                # Set active control tab for material.
                self.tab_src.setCurrentIndex(0)
                self.getImageFileInfo(self._current_file)

                # Chec the extension of the file.
                ext = os.path.splitext(img_path)[1].lower()

                # Cancel if the file extension is not JPEG.
                if not (ext == ".jpg" or ext == ".jpeg"):
                    # Create error messages.
                    print(ext)
                    error.ErrorMessageEditImageFile()

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
                img_file.material = self._current_file.material
                img_file.consolidation = self._current_file.consolidation
                img_file.filename = general.getRelativePath(new_file, "Consolidation")
                img_file.created_date = time_open
                img_file.modified_date = time_close
                img_file.file_type = "image"
                img_file.alias = "Automatic color inverting"
                img_file.status = "Edited"
                img_file.lock = False
                img_file.public = False
                img_file.source = self._current_file.uuid
                img_file.operation = "Color invert"
                img_file.operating_application = "Survey Data Collector"
                img_file.caption = "Color inverted version"
                img_file.description = "Make color inverting by this system."

                img_file.dbInsert(self._database)

                sop_object = None
                if img_file.material == "":
                    sop_object = features.Consolidation(is_new=False, uuid=img_file.consolidation, dbfile=self._database)
                else:
                    sop_object = features.Material(is_new=False, uuid=img_file.material, dbfile=self._database)

                # Refresh the image file list.
                self.refreshFileList(sop_object)
            else:
                error.ErrorMessageEditImageFile()
        except Exception as e:
            print("Error occured in main::negativeToPositive(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def saveImageAs(self):
        print("main::saveImageAs(self)")

        # Exit if the root directory is not loaded.
        if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

        # Exit if the tree object is not selected.
        selected = self.tre_fls.selectedItems()
        if (selected == None or len(selected) == 0): return(None)

        try:
            # Check the file type.
            print(self._current_file._file_type)

            # Set the default output file name.
            fil_out = self._current_file.uuid + ".jpg"

            # Exit if SOP object is not instantiated.
            if self._current_file == None: return(None)

            # Get the image path.
            img_path = os.path.join(self._root_directory, self._current_file.filename)

            # Exit if selected file is not exists.
            if not os.path.exists(img_path): error.ErrorMessageFileNotExist(); return(None)

            if self._current_file.file_type == "image":
                # Set active control tab for material.
                self.tab_src.setCurrentIndex(0)
                self.getImageFileInfo(self._current_file)

                # Chec the extension of the file.
                ext = os.path.splitext(img_path)[1].lower()

                # Cancel if the file extension is not JPEG.
                if not (ext == ".jpg" or ext == ".jpeg"):
                    error.ErrorMessageEditImageFile()

                    # Returns nothing.
                    return(None)

                # Get the output file name by using file save dialog.
                new_file, img_file_type = QFileDialog.getSaveFileName(self, "Export to", fil_out,"Images (*.jpg)")

                if new_file:
                    if not os.path.exists(new_file):
                        # Export the original file into given path.
                        shutil.copyfile(img_path, new_file)

                        # Export file info by XML.
                        sop_xml = self._current_file.writeAsXml()
                        if not sop_xml == None:
                            xml_image_info = open(new_file+'.xml', "w")
                            xml_image_info.write(sop_xml)
                            xml_image_info.close()
                    else:
                        # Display the error message.
                        error.ErrorMessageFileExport()

                        # Returns nothing.
                        return(None)
            else:
                error.ErrorMessageEditImageFile()
        except Exception as e:
            print("Error occured in main::negativeToPositive(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def colorlize(self):
        print("main::colorlize(self, angle)")

        try:
            item_path = None
            img_path = None
            thm_path = None

            # Exit if SOP object is not instantiated.
            if self._current_file == None: return(None)

            # Exit if the selected file is not image.
            if not self._current_file.file_type == "image": return(None)

            # Get the image path.
            img_file = os.path.join(self._root_directory, self._current_file.filename)

            # Exit if the selected file is not exists.
            if not os.path.exists(img_file): error.ErrorMessageFileNotExist(); return(None)

            # Get the current object from the selected tab index.
            if self._current_file.material == "":
                # Get the item path of the selected consolidaiton.
                item_path = os.path.join(self._consolidation_directory, self._current_file.consolidation)
                img_path = os.path.join(item_path, "Images")
                thm_path = os.path.join(img_path, "Thumbs")
            else:
                con_path = os.path.join(self._consolidation_directory, self._current_file.consolidation)
                item_path = os.path.join(os.path.join(con_path, "Materials"), self._current_file.material)
                img_path = os.path.join(item_path, "Images")
                thm_path = os.path.join(img_path, "Thumbs")

            # Set active control tab for file.
            self.tab_src.setCurrentIndex(0)
            self.getImageFileInfo(self._current_file)

            # Chec the extension of the file.
            filename = os.path.splitext(os.path.basename(img_file))[0]
            ext = os.path.splitext(img_file)[1]

            # Cancel if the file extension is not JPEG.
            if not (ext.lower() == ".jpg" or ext == ".jpeg"):
                # Create error messages.
                error.ErrorMessageEditImageFile()

                # Returns nothing.
                return(None)

            # Define the new uuid for the image.
            new_uuid = str(uuid.uuid4())

            # Get the time for opening GIMP.
            time_open = datetime.datetime.utcnow().isoformat()

            # Get the parent directory of the original image.
            out_dir = os.path.dirname(img_file)
            thm_file = os.path.join(thm_path, filename + ".jpg")
            col_file = os.path.join(thm_path, filename + "_colorized.jpg")

            new_file = os.path.join(out_dir, new_uuid + ".jpg")

            # Make a thumbnail.
            thumb = imageProcessing.makeThumbnail(img_file, thm_file, 400)
            if thumb == None: print("Error occured in thumbnail generation."); raise

            # Colorize.
            col = imageProcessing.colorize(self._siggraph_directory, thm_file, col_file)
            if col == None: print("Error occured in colorize generation."); raise

            # Make pansharpened image.
            psp = imageProcessing.pansharpen(col_file, img_file, new_file, self._psp_algo)
            if psp == None: print("Error occured in pansharpening."); raise

            # Copy the exif information.
            general.copyExif(img_file, new_file)

            # Get the time for closing GIMP.
            time_close = datetime.datetime.utcnow().isoformat()

            # Instantiate the File class.
            img_file = features.File(is_new=True, uuid=new_uuid, dbfile=None)
            img_file.material = self._current_file.material
            img_file.consolidation = self._current_file.consolidation
            img_file.filename = general.getRelativePath(new_file, "Consolidation")
            img_file.created_date = time_open
            img_file.modified_date = time_close
            img_file.file_type = "image"
            img_file.alias = "Colorlized Image"
            img_file.status = "Edited"
            img_file.lock = False
            img_file.public = False
            img_file.source = self._current_file.uuid
            img_file.operation = "Colorlized"
            img_file.operating_application = "siggraph 2016 Colorization"
            img_file.caption = "Colorlized by machine learning"
            img_file.description = "Colorlized by machine learning algorithm."

            # Insert the new image into the DB.
            img_file.dbInsert(self._database)

            sop_object = None
            if img_file.material == "":
                sop_object = features.Consolidation(is_new=False, uuid=img_file.consolidation, dbfile=self._database)
            else:
                sop_object = features.Material(is_new=False, uuid=img_file.material, dbfile=self._database)

            # Refresh the image file list.
            self.refreshFileList(sop_object)

        except Exception as e:
            print("Error occured in main::colorlize(self, angle)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    # ==========================
    # Cemera operation
    # ==========================
    def detectCamera(self):
        print("main::detectCamera(self)")

        try:
            # Display the camera select dialog.
            self.dialog_camera = cameraSelectDialog.SelectCameraDialog(self)
            if self.dialog_camera.exec_() == True:
                # Set the selected camera as the current
                self._gp_context = gp.Context()
                self._gp_camera = gp.Camera()

                cam_name = self.dialog_camera.camera_name
                cam_port = self.dialog_camera.camera_port

                if not cam_name == None and not cam_port == None:
                    print(cam_name, cam_port)

                    # search ports for camera port name
                    port_info_list = gp.PortInfoList()
                    port_info_list.load()
                    idx = port_info_list.lookup_path(cam_port)

                    self._gp_camera.set_port_info(port_info_list[idx])
                    self._gp_camera.init(self._gp_context)

                    self._current_camera = camera.Camera(cam_name, cam_port, self._gp_context, self._gp_camera)
                    print("Camera successfully detected.")
                else:
                    print("Any cameras are not detected... Please check the connection.")
                    self._current_camera = None
        except Exception as e:
            print("Error occured in main::detectCamera(self)")
            print(str(e))
            error.ErrorMessageCameraDetection(details=str(e), show=True, language=self._language)
            return(None)

    def recordWithPhoto(self):
        print("main::recordWithPhoto(self)")

        try:
            # Exit if the root directory is not loaded.
            if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

            # Exit if the tree object is not selected.
            selected = self.tre_prj_item.selectedItems()
            if (selected == None or len(selected) == 0): error.ErrorMessageCurrentConsolidation(language=self._language); return(None)

            # Exit if current object is not set.
            if self.tab_target.currentIndex() == 0:
                # Exit if the current consolidation is not selected.
                if self._current_consolidation == None: error.ErrorMessageCurrentConsolidation(language=self._language); return(None)
            elif self.tab_target.currentIndex()==1:
                # Exit if the current consolidation is not selected.
                if self._current_consolidation == None: error.ErrorMessageCurrentConsolidation(language=self._language); return(None)

                # Exit if the current consolidation is not selected.
                if self._current_material == None: error.ErrorMessageCurrentMaterial(language=self._language); return(None)
        except Exception as e:
            print("Error occured in main::recordWithPhoto(self)")
            print(str(e))
            return(None)

        try:
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
                sop_object = self._current_consolidation

                # Get the item path of the selected consolidaiton.
                item_path = os.path.join(self._consolidation_directory, sop_object.uuid)
            elif self.tab_target.currentIndex() == 1:
                # Get the current material uuid.
                mat_uuid = self.tbx_mat_uuid.text()

                # Instantiate the material.
                sop_object = self._current_material

                # Instantiate the consolidation.
                con_uuid = sop_object.consolidation
                con_path = os.path.join(self._consolidation_directory, sop_object.consolidation)
                item_path = os.path.join(os.path.join(con_path, "Materials"), sop_object.uuid)
            else:
                return(None)

            # Exit if none of objecs are instantiated.
            if sop_object == None: return(None)

            if sop_object.sounds == None: sop_object.sounds = list()

            # Initialyze the temporal directory.
            recording_path = os.path.join(self._temporal_directory, "recording")

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
        except Exception as e:
            print("Error occured in main::recordWithPhoto(self)")
            print(str(e))
            return(None)

        try:
            # Check the result of the tethered image.
            self.dialogRecording = recordWithPhotoDiaolog.RecordWithImage(parent=self, img_path=img_path, snd_path=recording_path)
            isAccepted = self.dialogRecording.exec_()

            if isAccepted == 1:
                # Get the current date and time from accepted timing.
                now = datetime.datetime.utcnow().isoformat()

                # Define the output directory.
                snd_lst_main = general.getFilesWithExtensionList(recording_path, self._sound_extensions)

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
                        snd_file.operating_application = "Survey Data Collector"
                        snd_file.caption = "Original audio"
                        snd_file.description = ""

                        # Insert the new entry into the self._database.
                        snd_file.dbInsert(self._database)

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
            error.ErrorMessageUnknown(details=str(e))
            # Returns nothing.
            return(None)

    def tetheredShooting(self):
        print("main::tetheredShooting(self)")

        # Exit if the root directory is not loaded.
        if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

        # Exit if the tree object is not selected.
        selected = self.tre_prj_item.selectedItems()
        if (selected == None or len(selected) == 0): error.ErrorMessageTreeItemNotSelected(language=self._language); return(None)

        try:
            # Initialyze the variables.
            sop_object = None
            item_path = None
            con_uuid = ""
            mat_uuid = ""

            # Get item path of the current object.
            if self.tab_target.currentIndex() == 0:
                # Exit if the current consolidation is not selected.
                if self._current_consolidation == None: error.ErrorMessageCurrentObject(language=self._language); return(None)

                # Get the current object.
                sop_object = self._current_consolidation

                # Get uuids.
                con_uuid = sop_object.uuid
                mat_uuid = ""

                # Get the item path of the selected consolidaiton.
                item_path = os.path.join(self._consolidation_directory, sop_object.uuid)
            elif self.tab_target.currentIndex() == 1:
                # Exit if the current consolidation is not selected.
                if self._current_material == None: error.ErrorMessageCurrentObject(language=self._language); return(None)

                # Get the current object.
                sop_object = self._current_material

                # Get uuids.
                con_uuid = sop_object.consolidation
                mat_uuid = sop_object.uuid

                # Define the path for saving images.
                con_path = os.path.join(self._consolidation_directory, sop_object.consolidation)
                item_path = os.path.join(os.path.join(con_path, "Materials"), sop_object.uuid)
            # Check whether current object has images.
            if sop_object.images == None: sop_object.images = list()

            # Exit if the root directory is not loaded.
            if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

            # Exit if the current camera is not loaded.
            if self._current_camera == None: error.ErrorMessageCameraDetection(); return(None)

            # Initialyze the temporal directory.
            tethered_path = os.path.join(self._temporal_directory, "tethered")

            if not os.path.exists(tethered_path):
                # Create the temporal directory if not exists.
                os.mkdir(tethered_path)
            else:
                # Delete the existing temporal directory before create.
                shutil.rmtree(tethered_path)
                os.mkdir(tethered_path)

            # Generate the GUID for the consolidation
            pht_uuid = str(uuid.uuid4())

            # Define the temporal path for the tethered shooting.
            tmp_path = os.path.join(tethered_path, pht_uuid)
            img_quality = self._current_camera.imagequality.get_value()

            # Take a imge by using imageProcessing library.
            self._current_camera._do_capture(self._gp_context,self._gp_camera, tmp_path)

            # Check the result of the tethered image.
            self.dialogTetheredShooting = checkTetheredImageDialog.CheckImageDialog(parent=self, path=tethered_path)

            if self.dialogTetheredShooting.exec_():
                # Get the current date and time.
                now = datetime.datetime.utcnow().isoformat()

                # Define the output directory.
                img_lst_main = general.getFilesWithExtensionList(tethered_path, self._image_extensions)
                img_lst_raw = general.getFilesWithExtensionList(tethered_path, self._raw_image_extensions)

                # Define the path for images.
                img_path = os.path.join(item_path, "Images")
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
                        img_file.operating_application = "Survey Data Collector"
                        img_file.caption = "Original image"
                        img_file.description = ""

                        # Execute the SQL script.
                        img_file.dbInsert(self._database)

                        # Add the image to the object.
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
                        raw_file.operating_application = "Survey Data Collector"
                        raw_file.caption = "Original image"
                        raw_file.description = ""

                        # Execute the SQL script.
                        raw_file.dbInsert(self._database)

                        # Add the image to the boject.
                        sop_object.images.insert(0, raw_file)
                else:
                    print("There are no raw images.")

            # Remove tethered path from the temporal directory.
            shutil.rmtree(tethered_path)

            # Refresh the file list.
            if sop_object.__class__.__name__ == "Consolidation":
                self._current_consolidation = sop_object
                self.refreshFileList(self._current_consolidation)
            elif sop_object.__class__.__name__ == "Material":
                self._current_material = sop_object
                self.refreshFileList(self._current_material)
        except Exception as e:
            print("Error occured in main::tetheredShooting(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    # ==========================
    # Flickr operation
    # ==========================
    def checkFlickrKey(self):
        print("main::checkFlickrKey(self)")

        try:
            self._flickr_apikey = "Empty"
            self._flickr_secret = "Empty"

            keyfile_path = os.path.join(self._root_directory,".flickr")

            if not os.path.exists(keyfile_path):
                keyfile = open(keyfile_path,"w")
                keyfile.write("Empty,Empty")
                keyfile.close()
            else:
                keyfile = open(keyfile_path,"r")
                api_params = keyfile.readline().split(",")

                self._flickr_apikey = api_params[0]
                self._flickr_secret = api_params[1]

                keyfile.close()
        except Exception as e:
            print("Error occured in main::checkFlickrKey(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def regFlickrKey(self):
        print("main::regFrickrKey(self)")

        # Create a sqLite file if not exists.
        try:
            # Exit if the root directory is not loaded.
            if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

            keyfile_path = os.path.join(self._root_directory,".flickr")

            self.checkFlickrKey()

            # Display the camera select dialog.
            self.dialog_flickr = flickrDialog.FlickrAPIDialog(self, self._flickr_apikey, self._flickr_secret)

            if self.dialog_flickr.exec_() == True:
                self._flickr_apikey = self.dialog_flickr.tbx_flickr_key.text()
                self._flickr_secret = self.dialog_flickr.tbx_flickr_sec.text()

                keyfile = open(keyfile_path,"w")
                keyfile.write(self._flickr_apikey + "," + self._flickr_secret)
        except Exception as e:
            print("Error occured in main::regFlickrKey(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    # ==========================
    # Exporting operation
    # ==========================
    def uploadToFlickr(self):
        print("uploadToFrickr(self)")

        # Create a sqLite file if not exists.
        try:
            # Exit if the root directory is not loaded.
            if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

            # Establish the connection to the self._database file.
            conn = sqlite.connect(self._database)

            # Exit if connection is not established.
            if conn == None: return(None)

            # Create the SQL query for selecting consolidation.
            sql_con_sel = """SELECT uuid, id, flickr_photosetid FROM consolidation ORDER BY id"""
            sql_mat_sel = """SELECT uuid, id FROM material WHERE con_id=? ORDER by id"""

            # Create the SQL query for selecting image files
            sql_con_fil_sel = """SELECT flickr_photoid FROM material WHERE uuid=?"""
            sql_mat_fil_sel = """SELECT flickr_photoid FROM material WHERE uuid=?"""

            # Instantiate the cursor for query.
            cur_con = conn.cursor()
            rows_con = cur_con.execute(sql_con_sel)

            # Execute the query and get consolidation recursively
            for row_con in rows_con:
                time.sleep(10)

                photoset_ids = []

                # Initialyze the photoset id.
                con_photoset_id = None

                # Get attributes from the row.
                consolidation = features.Consolidation(
                    is_new=False,
                    uuid = row_con[0],
                    dbfile = self._database)

                # Get the current photoset id.
                con_photoset_id = row_con[2]

                # Set attributes to text boxes.
                con_uuid = consolidation.uuid
                con_cnid = consolidation.id
                con_name = consolidation.name
                con_geog = consolidation.geographic_annotation
                con_temp = consolidation.temporal_annotation
                con_desc = consolidation.description
                con_imgs = consolidation.images

                if isinstance(con_uuid, unicode) : con_uuid = con_uuid.encode('utf-8')
                if isinstance(con_cnid, unicode) : con_cnid = con_cnid.encode('utf-8')
                if isinstance(con_name, unicode) : con_name = con_name.encode('utf-8')
                if isinstance(con_geog, unicode) : con_geog = con_geog.encode('utf-8')
                if isinstance(con_temp, unicode) : con_temp = con_temp.encode('utf-8')
                if isinstance(con_desc, unicode) : con_desc = con_desc.encode('utf-8')

                for image in con_imgs:
                    time.sleep(5)

                    con_img_uuid = image.uuid
                    con_img_flid = image.id
                    con_img_alas = image.alias
                    con_img_capt = image.caption
                    con_img_cdat = image.created_date
                    con_img_mdat = image.modified_date
                    con_img_fnam = os.path.join(self._root_directory,image.filename)
                    con_img_ftyp = image.file_type
                    con_img_opap = image.operating_application
                    con_img_oper = image.operation
                    con_img_publ = image.public
                    con_img_lock = image.lock
                    con_img_srce = image.source
                    con_img_stat = image.status
                    con_img_desc = image.description
                    con_img_exts = os.path.splitext(con_img_fnam)[1].upper()

                    if isinstance(con_img_uuid, unicode) : con_img_uuid = con_img_uuid.encode('utf-8')
                    if isinstance(con_img_flid, unicode) : con_img_flid = con_img_flid.encode('utf-8')
                    if isinstance(con_img_alas, unicode) : con_img_alas = con_img_alas.encode('utf-8')
                    if isinstance(con_img_capt, unicode) : con_img_capt = con_img_capt.encode('utf-8')
                    if isinstance(con_img_cdat, unicode) : con_img_cdat = con_img_cdat.encode('utf-8')
                    if isinstance(con_img_mdat, unicode) : con_img_mdat = con_img_mdat.encode('utf-8')
                    if isinstance(con_img_fnam, unicode) : con_img_fnam = con_img_fnam.encode('utf-8')
                    if isinstance(con_img_ftyp, unicode) : con_img_ftyp = con_img_ftyp.encode('utf-8')
                    if isinstance(con_img_opap, unicode) : con_img_opap = con_img_opap.encode('utf-8')
                    if isinstance(con_img_oper, unicode) : con_img_oper = con_img_oper.encode('utf-8')
                    if isinstance(con_img_publ, unicode) : con_img_publ = con_img_publ.encode('utf-8')
                    if isinstance(con_img_lock, unicode) : con_img_lock = con_img_lock.encode('utf-8')
                    if isinstance(con_img_srce, unicode) : con_img_srce = con_img_srce.encode('utf-8')
                    if isinstance(con_img_stat, unicode) : con_img_stat = con_img_stat.encode('utf-8')
                    if isinstance(con_img_desc, unicode) : con_img_desc = con_img_desc.encode('utf-8')

                    if con_img_publ == "1":
                        if con_img_exts == ".JPG":
                            con_img_path = con_img_fnam

                            # Define the SQL query for get the photo id of the Flickr.
                            sql_con_fil_sel = """SELECT flickr_photoid FROM file WHERE uuid=?"""
                            cur_con_fil = conn.cursor()
                            rows_con_fil = cur_con_fil.execute(sql_con_fil_sel, [image.uuid])

                            # Get the Flickr photo id from the DB.
                            flickr_pht_id = rows_con_fil.fetchone()

                            # Create the HTML description for Flickr.
                            con_flickr_desc = """
                                <b>%s</b>
                                <u>Geography:</u>
                                <blockquote>%s</blockquote>
                                <u>Period:</u>
                                <blockquote>%s</blockquote>
                                <u>Dscriptions:</u>
                                <blockquote>%s</blockquote>
                                """ % (con_name, con_geog, con_temp, con_desc)

                            con_flickrPhoto = flickr.FlickrPhoto(
                                api_key = self._flickr_apikey,
                                secret_key = self._flickr_secret,
                                photo_id = flickr_pht_id,
                                title = con_name,
                                description = con_flickr_desc,
                                path = con_img_path)

                            # Check the photo.
                            res = con_flickrPhoto.getInfo()

                            if res is not None:
                                con_flickrPhoto.replace()
                                photoset_ids.append(con_flickrPhoto.photo_id)
                            else:
                                con_flickrPhoto.upload()

                                # Update the flickr id column.
                                sql_update = """UPDATE file SET flickr_photoid = ? WHERE uuid = ?"""
                                cur_con_fil = conn.cursor()
                                cur_con_fil.execute(sql_update, [con_img_uuid,con_flickrPhoto.photo_id])
                                photoset_ids.append(con_flickrPhoto.photo_id)

                cur_mat = conn.cursor()
                rows_mat = cur_mat.execute(sql_mat_sel, [con_uuid])

                for row_mat in rows_mat:
                    time.sleep(10)
                    material = features.Material(is_new=False, uuid = row_mat[0], dbfile=self._database)

                    # Set attributes to text boxes.
                    mat_uuid = material.uuid
                    mat_mtid = material.id
                    mat_mnum = material.material_number
                    mat_mnam = material.name
                    mat_mbgn = material.estimated_period_beginning
                    mat_mpek = material.estimated_period_peak
                    mat_mend = material.estimated_period_ending
                    mat_mlat = material.latitude
                    mat_mlon = material.longitude
                    mat_malt = material.altitude
                    mat_desc = material.description
                    mat_imgs = material.images

                    if isinstance(mat_uuid, unicode) : mat_uuid = mat_uuid.encode('utf-8')
                    if isinstance(mat_mtid, unicode) : mat_mtid = mat_uuid.encode('utf-8')
                    if isinstance(mat_mnum, unicode) : mat_mnum = mat_mnum.encode('utf-8')
                    if isinstance(mat_mnam, unicode) : mat_mnam = mat_mnam.encode('utf-8')
                    if isinstance(mat_mbgn, unicode) : mat_mbgn = mat_mbgn.encode('utf-8')
                    if isinstance(mat_mpek, unicode) : mat_mpek = mat_mpek.encode('utf-8')
                    if isinstance(mat_mend, unicode) : mat_mend = mat_mend.encode('utf-8')
                    if isinstance(mat_mlat, unicode) : mat_mlat = mat_mlat.encode('utf-8')
                    if isinstance(mat_mlon, unicode) : mat_mlon = mat_mlon.encode('utf-8')
                    if isinstance(mat_malt, unicode) : mat_malt = mat_malt.encode('utf-8')
                    if isinstance(mat_desc, unicode) : mat_desc = mat_desc.encode('utf-8')

                    for image in mat_imgs:
                        time.sleep(5)

                        mat_img_uuid = image.uuid
                        mat_img_flid = image.id
                        mat_img_alas = image.alias
                        mat_img_capt = image.caption
                        mat_img_cdat = image.created_date
                        mat_img_mdat = image.modified_date
                        mat_img_fnam = os.path.join(self._root_directory,image.filename)
                        mat_img_ftyp = image.file_type
                        mat_img_opap = image.operating_application
                        mat_img_oper = image.operation
                        mat_img_publ = image.public
                        mat_img_lock = image.lock
                        mat_img_srce = image.source
                        mat_img_stat = image.status
                        mat_img_desc = image.description
                        mat_img_exts = os.path.splitext(mat_img_fnam)[1].upper()

                        if isinstance(mat_img_uuid, unicode) : mat_img_uuid = mat_img_uuid.encode('utf-8')
                        if isinstance(mat_img_flid, unicode) : mat_img_flid = mat_img_flid.encode('utf-8')
                        if isinstance(mat_img_alas, unicode) : mat_img_alas = mat_img_alas.encode('utf-8')
                        if isinstance(mat_img_capt, unicode) : mat_img_capt = mat_img_capt.encode('utf-8')
                        if isinstance(mat_img_cdat, unicode) : mat_img_cdat = mat_img_cdat.encode('utf-8')
                        if isinstance(mat_img_mdat, unicode) : mat_img_mdat = mat_img_mdat.encode('utf-8')
                        if isinstance(mat_img_fnam, unicode) : mat_img_fnam = mat_img_fnam.encode('utf-8')
                        if isinstance(mat_img_ftyp, unicode) : mat_img_ftyp = mat_img_ftyp.encode('utf-8')
                        if isinstance(mat_img_opap, unicode) : mat_img_opap = mat_img_opap.encode('utf-8')
                        if isinstance(mat_img_oper, unicode) : mat_img_oper = mat_img_oper.encode('utf-8')
                        if isinstance(mat_img_publ, unicode) : mat_img_publ = mat_img_publ.encode('utf-8')
                        if isinstance(mat_img_lock, unicode) : mat_img_lock = mat_img_lock.encode('utf-8')
                        if isinstance(mat_img_srce, unicode) : mat_img_srce = mat_img_srce.encode('utf-8')
                        if isinstance(mat_img_stat, unicode) : mat_img_stat = mat_img_stat.encode('utf-8')
                        if isinstance(mat_img_desc, unicode) : mat_img_desc = mat_img_desc.encode('utf-8')

                        if mat_img_publ == "1":
                            if mat_img_exts == ".JPG":
                                mat_img_path = mat_img_fnam

                                # Define the SQL query for get the photo id of the Flickr.
                                sql_mat_fil_sel = """SELECT flickr_photoid FROM file WHERE uuid=?"""
                                cur_mat_fil = conn.cursor()
                                rows_mat_fil = cur_mat_fil.execute(sql_mat_fil_sel, [image.uuid])

                                # Get the Flickr photo id from the DB.
                                flickr_pht_id = rows_mat_fil.fetchone()

                                # Create the HTML description for Flickr.
                                mat_flickr_desc = """
                                <b>%s</b>
                                <u><b>General Information<b></u>
                                <u>id:</u>
                                <blockquote>%s</blockquote>
                                <u>Dscriptions:</u>
                                <blockquote>%s</blockquote>
                                <u><b>Temporal Annotation</b></u>
                                <blockquote>Start:%s</blockquote>
                                <blockquote>Peak:%s</blockquote>
                                <blockquote>End:%s</blockquote>
                                <u><b>Geographic Annotation</b></u>
                                <blockquote>latitude:%s</blockquote>
                                <blockquote>longitude:%s</blockquote>
                                <blockquote>altitude:%s</blockquote>
                                """ % (mat_mnam, mat_mnum, mat_desc, mat_mbgn, mat_mpek, mat_mend, mat_mlat, mat_mlon, mat_malt)

                                mat_flickrPhoto = flickr.FlickrPhoto(
                                    api_key = self._flickr_apikey,
                                    secret_key = self._flickr_secret,
                                    photo_id = flickr_pht_id,
                                    title = mat_mnam,
                                    description = mat_flickr_desc,
                                    path = mat_img_path)

                                # Check the photo.
                                res = mat_flickrPhoto.getInfo()

                                if res is not None:
                                    mat_flickrPhoto.replace()
                                    photoset_ids.append(mat_flickrPhoto.photo_id)
                                    print("replaced")
                                else:
                                    mat_flickrPhoto.upload()

                                    # Update the flickr id column.
                                    sql_update = """UPDATE file SET flickr_photoid = ? WHERE uuid = ?"""
                                    cur_con_fil = conn.cursor()
                                    cur_con_fil.execute(sql_update, [mat_flickrPhoto.photo_id, mat_img_uuid])
                                    photoset_ids.append(mat_flickrPhoto.photo_id)
                                    print("uploaded")

                prime_photo = photoset_ids[0]
                photoset_ids.pop(0)

                con_photoset = flickr.FlickrPhotoSet(
                    api_key = self._flickr_apikey,
                    secret_key = self._flickr_secret,
                    photoset_id = con_photoset_id,
                    title = con_name,
                    description = con_flickr_desc,
                    primary_photo_id = prime_photo,
                    photos = photoset_ids)

                if con_photoset_id is None: con_photoset.createPhotoset()
                con_photoset.addPhotosToPhotoset()

        except Exception as e:
            print("Error occured in uploading process:")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def exportAsXML(self):
        print("exportAsXML(self)")

        # Create a sqLite file if not exists.
        try:
            # Exit if the root directory is not loaded.
            if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

            # Define directories for storing files.
            output = QFileDialog.getExistingDirectory(self, "Select the output directory")

            # Open the file stream
            output_xml = open(os.path.join(output,"output.xml"),"w")

            output_xml.write("<dataset>\n")

            # Establish the connection to the self._database file.
            conn = sqlite.connect(self._database)

            # Exit if connection is not established.
            if conn == None: return(None)

            # Create the SQL query for selecting consolidation.
            sql_con_sel = """SELECT uuid, id FROM consolidation ORDER BY id"""
            sql_mat_sel = """SELECT uuid, id FROM material WHERE con_id=? ORDER by id"""

            # Instantiate the cursor for query.
            cur_con = conn.cursor()
            rows_con = cur_con.execute(sql_con_sel)

            # Execute the query and get consolidation recursively
            for row_con in rows_con:
                output_xml.write("\t<consolidation>\n")

                # Get attributes from the row.
                consolidation = features.Consolidation(is_new=False, uuid = row_con[0], dbfile=self._database)

                # Set attributes to text boxes.
                con_uuid = consolidation.uuid
                con_cnid = consolidation.id
                con_name = consolidation.name
                con_geog = consolidation.geographic_annotation
                con_temp = consolidation.temporal_annotation
                con_desc = consolidation.description

                if isinstance(con_uuid, unicode) : con_uuid = con_uuid.encode('utf-8')
                if isinstance(con_cnid, unicode) : con_cnid = con_cnid.encode('utf-8')
                if isinstance(con_name, unicode) : con_name = con_name.encode('utf-8')
                if isinstance(con_geog, unicode) : con_geog = con_geog.encode('utf-8')
                if isinstance(con_temp, unicode) : con_temp = con_temp.encode('utf-8')
                if isinstance(con_desc, unicode) : con_desc = con_desc.encode('utf-8')

                output_xml.write("\t\t<uuid>%s</uuid>\n" % con_uuid)
                output_xml.write("\t\t<id>%s</id>\n" % con_cnid)
                output_xml.write("\t\t<name>%s</name>\n" % con_name)
                output_xml.write("\t\t<geographic_annotation>%s</geographic_annotation>\n" %(con_geog))
                output_xml.write("\t\t<temporal_annotation>%s</temporal_annotation>\n" %(con_temp))
                output_xml.write("\t\t<description>%s</description>\n" %(con_desc))
                output_xml.write("\t\t<materials>\n")

                cur_mat = conn.cursor()
                rows_mat = cur_mat.execute(sql_mat_sel, [con_uuid])

                for row_mat in rows_mat:
                    material = features.Material(is_new=False, uuid = row_mat[0], dbfile=self._database)

                    # Set attributes to text boxes.
                    mat_uuid = material.uuid
                    mat_mtid = material.id
                    mat_mnum = material.material_number
                    mat_mnam = material.name
                    mat_mbgn = material.estimated_period_beginning
                    mat_mpek = material.estimated_period_peak
                    mat_mend = material.estimated_period_ending
                    mat_mlat = material.latitude
                    mat_mlon = material.longitude
                    mat_malt = material.altitude
                    mat_desc = material.description
                    mat_imgs = material.images

                    if isinstance(mat_uuid, unicode) : mat_uuid = mat_uuid.encode('utf-8')
                    if isinstance(mat_mtid, unicode) : mat_mtid = mat_uuid.encode('utf-8')
                    if isinstance(mat_mnum, unicode) : mat_mnum = mat_mnum.encode('utf-8')
                    if isinstance(mat_mnam, unicode) : mat_mnam = mat_mnam.encode('utf-8')
                    if isinstance(mat_mbgn, unicode) : mat_mbgn = mat_mbgn.encode('utf-8')
                    if isinstance(mat_mpek, unicode) : mat_mpek = mat_mpek.encode('utf-8')
                    if isinstance(mat_mend, unicode) : mat_mend = mat_mend.encode('utf-8')
                    if isinstance(mat_mlat, unicode) : mat_mlat = mat_mlat.encode('utf-8')
                    if isinstance(mat_mlon, unicode) : mat_mlon = mat_mlon.encode('utf-8')
                    if isinstance(mat_malt, unicode) : mat_malt = mat_malt.encode('utf-8')
                    if isinstance(mat_desc, unicode) : mat_desc = mat_desc.encode('utf-8')

                    output_xml.write("\t\t\t<material>\n")
                    output_xml.write("\t\t\t\t<uuid>%s</uuid>\n" % mat_uuid)
                    output_xml.write("\t\t\t\t<id>%s</id>\n" % mat_mtid)
                    output_xml.write("\t\t\t\t<number>%s</number>\n" % mat_mnum)
                    output_xml.write("\t\t\t\t<name>%s</name>\n" % mat_mnam)
                    output_xml.write("\t\t\t\t<date_begin>%s</date_begin>\n" % mat_mbgn)
                    output_xml.write("\t\t\t\t<date_peak>%s</date_peak>\n" % mat_mpek)
                    output_xml.write("\t\t\t\t<date_end>%s</date_end>\n" % mat_mend)
                    output_xml.write("\t\t\t\t<latitude>%s</latitude>\n" % mat_mlat)
                    output_xml.write("\t\t\t\t<longitude>%s</longitude>\n" % mat_mlon)
                    output_xml.write("\t\t\t\t<altitude>%s</altitude>\n" % mat_malt)
                    output_xml.write("\t\t\t\t<description>%s</description>\n" % mat_desc)
                    output_xml.write("\t\t\t\t<images>\n")

                    for image in mat_imgs:
                        img_uuid = image.uuid
                        img_flid = image.id
                        img_alas = image.alias
                        img_capt = image.caption
                        img_cdat = image.created_date
                        img_mdat = image.modified_date
                        img_fnam = os.path.join(self._root_directory,image.filename)
                        img_ftyp = image.file_type
                        img_opap = image.operating_application
                        img_oper = image.operation
                        img_publ = image.public
                        img_lock = image.lock
                        img_srce = image.source
                        img_stat = image.status
                        img_desc = image.description

                        if isinstance(img_uuid, unicode) : img_uuid = img_uuid.encode('utf-8')
                        if isinstance(img_flid, unicode) : img_flid = img_flid.encode('utf-8')
                        if isinstance(img_alas, unicode) : img_alas = img_alas.encode('utf-8')
                        if isinstance(img_capt, unicode) : img_capt = img_capt.encode('utf-8')
                        if isinstance(img_cdat, unicode) : img_cdat = img_cdat.encode('utf-8')
                        if isinstance(img_mdat, unicode) : img_mdat = img_mdat.encode('utf-8')
                        if isinstance(img_fnam, unicode) : img_fnam = img_fnam.encode('utf-8')
                        if isinstance(img_ftyp, unicode) : img_ftyp = img_ftyp.encode('utf-8')
                        if isinstance(img_opap, unicode) : img_opap = img_opap.encode('utf-8')
                        if isinstance(img_oper, unicode) : img_oper = img_oper.encode('utf-8')
                        if isinstance(img_publ, unicode) : img_publ = img_publ.encode('utf-8')
                        if isinstance(img_lock, unicode) : img_lock = img_lock.encode('utf-8')
                        if isinstance(img_srce, unicode) : img_srce = img_srce.encode('utf-8')
                        if isinstance(img_stat, unicode) : img_stat = img_stat.encode('utf-8')
                        if isinstance(img_desc, unicode) : img_desc = img_desc.encode('utf-8')

                        output_xml.write("\t\t\t\t\t<image>\n")
                        output_xml.write("\t\t\t\t\t\t<uuid>%s</uuid>\n" % img_uuid)
                        output_xml.write("\t\t\t\t\t\t<id>%s</id>\n" % img_flid)
                        output_xml.write("\t\t\t\t\t\t<alias>%s</alias>\n" % img_alas)
                        output_xml.write("\t\t\t\t\t\t<caption>%s</caption>\n" % img_capt)
                        output_xml.write("\t\t\t\t\t\t<created>%s</created>\n" % img_cdat)
                        output_xml.write("\t\t\t\t\t\t<modified>%s</modified>\n" % img_mdat)
                        output_xml.write("\t\t\t\t\t\t<filename>%s</filename>\n" % img_fnam)
                        output_xml.write("\t\t\t\t\t\t<filetype>%s</filetype>\n" % img_ftyp)
                        output_xml.write("\t\t\t\t\t\t<application>%s</application>\n" % img_opap)
                        output_xml.write("\t\t\t\t\t\t<operation>%s</operation>\n" % img_oper)
                        output_xml.write("\t\t\t\t\t\t<public>%s</public>\n" % img_publ)
                        output_xml.write("\t\t\t\t\t\t<lock>%s</lock>\n" % img_lock)
                        output_xml.write("\t\t\t\t\t\t<source>%s</source>\n" % img_srce)
                        output_xml.write("\t\t\t\t\t\t<status>%s</status>\n" % img_stat)
                        output_xml.write("\t\t\t\t\t\t<description>%s</description>\n" % img_desc)
                        output_xml.write("\t\t\t\t\t</image>\n")
                    output_xml.write("\t\t\t\t</images>\n")
                    output_xml.write("\t\t\t</material>\n")
                output_xml.write("\t\t</materials>\n")
                output_xml.write("\t</consolidation>\n")
            output_xml.write("</dataset>")
        except Exception as e:
            print("Error occured in exportAsXML(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def exportAsHtml(self):
        print("exportAsHtml(self)")

        try:
            # Exit if the root directory is not loaded.
            if self._root_directory == None: error.ErrorMessageProjectOpen(language=self._language); return(None)

            bootstrap = os.path.join(self._lib_directory, "bootstrap")
            bootstrap_css = os.path.join(bootstrap, "css")
            bootstrap_js = os.path.join(bootstrap, "js")

            # Define directories for storing files.
            output = QFileDialog.getExistingDirectory(self, "Select the output directory")

            # Define the directory for putting css and js.
            html_theme = os.path.join(output, "theme")
            html_images = os.path.join(output, "images")

            # Make directory for putting bootstrap themes.
            if not os.path.exists(html_theme): os.makedirs(html_theme)
            if not os.path.exists(html_images): os.makedirs(html_images)
            if not os.path.exists(os.path.join(html_theme,"css")): shutil.copytree(bootstrap_css, os.path.join(html_theme,"css"))
            if not os.path.exists(os.path.join(html_theme,"js")): shutil.copytree(bootstrap_js, os.path.join(html_theme,"js"))

            org_noimage = os.path.join(os.path.join(self._source_directory, "images"),"noimage.jpg")
            dst_noimage = os.path.join(html_images, "noimage.jpg")

            if not os.path.exists(dst_noimage): shutil.copy(org_noimage, dst_noimage)

            # Open the file stream
            output_html = open(os.path.join(output,"index.html"),"w")

            # Define the pages
            pages = dict()
            pages['home'] = "index.html"

            output_html.write(htmlWriter.startHtml(title="Home"))
            output_html.write(htmlWriter.startBody())
            output_html.write(htmlWriter.setMenuBar(pages=pages))
            output_html.write(htmlWriter.startContents())

            # Establish the connection to the self._database file.
            conn = sqlite.connect(self._database)

            # Exit if connection is not established.
            if conn == None: return(None)

            # Create the SQL query for selecting consolidation.
            sql_con_sel = """SELECT uuid FROM consolidation"""

            # Create the SQL query for selecting the consolidation.
            sql_mat_sel = """SELECT uuid FROM material WHERE con_id=?"""

            # Instantiate the cursor for query.
            cur_con = conn.cursor()
            rows_con = cur_con.execute(sql_con_sel)

            # Execute the query and get consolidation recursively
            for row_con in rows_con:
                # Get attributes from the row.
                con_uuid = row_con[0]
                consolidation = features.Consolidation(is_new=False, uuid=con_uuid, dbfile=self._database)

                if not  consolidation.images == None:
                    if not len(consolidation.images) == 0:
                        for image in consolidation.images:
                            org_img = os.path.join(self._root_directory, image.filename)
                            dst_img = os.path.join(html_images, image.uuid + ".jpg")

                            if os.path.exists(org_img): shutil.copy(org_img, dst_img)

                output_html.write(htmlWriter.setConsolidation(consolidation))

            output_html.write(htmlWriter.endContents())
            output_html.write(htmlWriter.endBody())
            output_html.write(htmlWriter.endHtml())

            output_html.close()
        except Exception as e:
            print("Error occured in exportAsHtml(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)
            pass

    # ==========================
    # Geodata operation
    # ==========================


def main():
    app = QApplication(sys.argv)

    form = mainPanel()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
