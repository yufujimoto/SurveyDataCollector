#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Import general libraries.
import sys, os, uuid, shutil, time, math, tempfile, logging, pyexiv2, datetime, exifread
import pytesseract

# Import the library for acquiring file information.
from stat import *
from dateutil.parser import parse

# Import the library for camera operations.
import gphoto2 as gp

# Import PyQt5 libraries for generating the GUI application.
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QThread, pyqtSignal

# Import general operations.
import modules.general as general
import modules.features as features
import modules.error as error
import modules.setupConfigSkin as setupConfigSkin
import modules.camera as camera

# Import camera and image processing library.
import dialog.configurationDialog as configurationDialog

class configurationDialog(QDialog, configurationDialog.Ui_configurationDialog):
    @property
    def main(self): return self._main
    @property
    def language(self): return self._language
    @property
    def skin(self): return self._skin
    @property
    def proxy(self): return self._proxy

    @main.setter
    def main(self, value): self._main = value
    @language.setter
    def language(self, value): self._language = value
    @skin.setter
    def skin(self, value): self._skin = value
    @proxy.setter
    def proxy(self, value): self._proxy = value

    def __init__(self, parent=None):
        print("Start -> configuration::__init__(self, parent=None)")

        try:
            super(configurationDialog, self).__init__(parent)
            self.setupUi(self)

            # Initialize the window.
            self.setWindowTitle(self.tr("Configuration"))

            # Get the parent.
            self._main = parent

            # ========================
            # General Tab
            # ========================
            # Language setting.
            self._language = parent.language
            print("## Set the UI language as" + parent.language)
            if self._language == "ja":
                self.cbx_thm_lang.setCurrentIndex(0)
            elif self._language == "en":
                self.cbx_thm_lang.setCurrentIndex(1)

            # Skin color setting.
            self._skin = parent.skin
            print("## Set the UI theme as" + self._skin)
            if self._skin == "grey":
                self.cbx_skin.setCurrentIndex(0)
            elif self._skin == "white":
                self.cbx_skin.setCurrentIndex(1)
            # Apply skin to the window.
            self.setSkin(parent.icon_directory)

            # Set default auto white balance algorithms.
            print("## Set the algorithm for Auto White Balance as " + parent._awb_algo)
            if parent._awb_algo == "retinex_adjusted": self.cbx_tool_awb.setCurrentIndex(0)
            elif parent._awb_algo == "stretch": self.cbx_tool_awb.setCurrentIndex(1)
            elif parent._awb_algo == "gray_world": self.cbx_tool_awb.setCurrentIndex(2)
            elif parent._awb_algo == "max_white": self.cbx_tool_awb.setCurrentIndex(3)
            elif parent._awb_algo == "retinex": self.cbx_tool_awb.setCurrentIndex(4)
            elif parent._awb_algo == "stdev_luminance": self.cbx_tool_awb.setCurrentIndex(5)
            elif parent._awb_algo == "stdev_grey_world": self.cbx_tool_awb.setCurrentIndex(6)
            elif parent._awb_algo == "luminance_weighted": self.cbx_tool_awb.setCurrentIndex(7)
            elif parent._awb_algo == "automatic": self.cbx_tool_awb.setCurrentIndex(8)
            else: print("### Invalid AWB algorithm"); self.cbx_tool_awb.setCurrentIndex(0)

            # Set default pan-sharpening algorithms.
            print("## Set the algorithm for Pan-Sharpening as " + parent.psp_algo)
            if parent.psp_algo == "ihsConvert": self.cbx_tool_psp.setCurrentIndex(0)
            elif parent.psp_algo == "simpleMeanConvert": self.cbx_tool_psp.setCurrentIndex(1)
            elif parent.psp_algo == "broveyConvert": self.cbx_tool_psp.setCurrentIndex(2)
            else: print("### Invalid PSP algorithm"); self.cbx_tool_psp.setCurrentIndex(0)

            #Default application setting.
            print("## Set the default text editor as " + parent.app_textEdit)
            self.tbx_exe_textedit.setText(parent.app_textEdit)

            # Set the Proxy setting.
            self._proxy = parent.proxy

            if parent.proxy == "No Proxy":
                self.proxySettingsFalse()
                print("## No Proxy settings")
            else:
                self.proxySettingsTrue()
                self.txt_proxy.setText(self._proxy)
                print("## HTTP_PROXY: " + self._proxy)

            # ========================
            # Camera setting Tab
            # ========================
            # Initialize camera parameters.
            print("## Set the camera")
            if not parent.current_camera == None:
                # Set the current camera.
                cam_nam = parent.current_camera.camera_name
                cam_prt = parent.current_camera.port

                # Set the current camera name.
                self.lbl_cur_cam_nam.setText(cam_nam + " (" + cam_prt + ")")
                print('### Currently ' + cam_nam + " (" + cam_prt + ")" + " is connected.")

                # Set parameters to comboboxes.
                if not parent.current_camera.imagesize == None:
                    self.setCamParamCbx(self.cbx_cam_size, parent.current_camera.imagesize)
                if not parent.current_camera.iso == None:
                    self.setCamParamCbx(self.cbx_cam_iso, parent.current_camera.iso)
                if not parent.current_camera.whitebalance == None:
                    self.setCamParamCbx(self.cbx_cam_wht, parent.current_camera.whitebalance)
                if not parent.current_camera.exposuremetermode == None:
                    self.setCamParamCbx(self.cbx_cam_exp, parent.current_camera.exposuremetermode)
                if not parent.current_camera.f_number == None:
                    self.setCamParamCbx(self.cbx_cam_fval, parent.current_camera.f_number)
                if not parent.current_camera.imagequality == None:
                    self.setCamParamCbx(self.cbx_cam_qoi, parent.current_camera.imagequality)
                if not parent.current_camera.focusmode == None:
                    self.setCamParamCbx(self.cbx_cam_fmod, parent.current_camera.focusmode)
                if not parent.current_camera.expprogram == None:
                    self.setCamParamCbx(self.cbx_cam_epg, parent.current_camera.expprogram)
                if not parent.current_camera.capturemode == None:
                    self.setCamParamCbx(self.cbx_cam_cpt, parent.current_camera.capturemode)
            else:
                # Refresh camera parameters.
                self.refreshCameraParameters()

                # Set no camear informaiton.
                self.lbl_cur_cam_nam.setText("Currently, no camera is connected...")
                print("### Currently, no camera is connected...")

                # Resize the header width with contents.
                self.tre_cam.resizeColumnToContents(0)
                self.tre_cam.resizeColumnToContents(1)

            # ========================
            # OCR setting Tab
            # ========================
            # Set the Page Segmentation Mode.
            print("## Set the OCR parameter of the Page Segmentation Mode as " + str(int(parent.ocr_psm)+1))
            self.cbx_psm.setCurrentIndex(int(parent.ocr_psm)+1)

            # Get OCR languages.
            print("## Set the OCR languages")
            ocr_langs_ave = parent.ocr_lang_available.split("+")
            ocr_langs_use = parent.ocr_lang.split("+")

            for ocr_lang_use in ocr_langs_use:
                print("### Currently " + ocr_lang_use + " is selected as OCR language...")
                ocr_langs_ave.remove(ocr_lang_use)

                ocr_lng_use_item = QListWidgetItem(ocr_lang_use)
                self.lst_lang_selected.addItem(ocr_lng_use_item)
            for ocr_lang_ave in ocr_langs_ave:
                print("### Currently " + ocr_lang_ave + " is available...")
                ocr_lng_ave_item = QListWidgetItem(ocr_lang_ave)
                self.lst_lang_available.addItem(ocr_lng_ave_item)

            # ========================
            # Third party service setting Tab
            # ========================
            print("## Set the back gound map for Geospatial data.")
            if parent.map_tile == "OpenStreetMap": self.cbx_map_tile.setCurrentIndex(0)
            elif parent.map_tile == "Google Streets": self.cbx_map_tile.setCurrentIndex(1)
            elif parent.map_tile == "Google Hybrid": self.cbx_map_tile.setCurrentIndex(2)
            elif parent.map_tile == "Google Satellite": self.cbx_map_tile.setCurrentIndex(3)
            elif parent.map_tile == "Google Terrain": self.cbx_map_tile.setCurrentIndex(4)
            elif parent.map_tile == u"地理院タイル": self.cbx_map_tile.setCurrentIndex(5)
            else: parent.map_tile = "OpenStreetMap"
            print("### " + parent.map_tile + " is set to the default.")

            # Set Flickr API and Secret Key.
            if not parent.flickr_apikey == None:
                print("## Set the Flickr API: " + parent.flickr_apikey)
                self.txt_flc_api.setText(parent.flickr_apikey)
            if not parent.flickr_secret == None:
                print("## Set the Flickr API: **********")
                self.txt_flc_sec.setText(parent.flickr_secret)

            # ========================
            # Activate UI objects.
            # ========================
            self.rbtn_proxy.clicked.connect(self.proxySettingsTrue)
            self.rbtn_no_proxy.clicked.connect(self.proxySettingsFalse)
            self.btn_cam_conn.clicked.connect(self.connectCamera)
            self.btn_cam_detect.clicked.connect(self.detectCamera)
            self.btn_ocr_lang_on.clicked.connect(self.addOcrLanguage)
            self.btn_ocr_lang_off.clicked.connect(self.removeOcrLanguage)

            # Set the dialog button size.
            dlg_btn_size = QSize(125, 30)
            self.bbx_conf_res.buttons()[0].setMinimumSize(dlg_btn_size)
            self.bbx_conf_res.buttons()[1].setMinimumSize(dlg_btn_size)

        except Exception as e:
            print("Error occured in configuration::__init__(self, parent=None)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

        finally:
            print("End -> configuration::__init__")

    def refreshCameraParameters(self):
        print("## configuration::refreshCameraParameters(self)")

        try:
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
        except Exception as e:
            print("Error occured in configuration::refreshCameraParameters(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def setSkin(self, icon_path):
        print("Start -> configuration::setSkin(self, icon_path)")
        try:
            # Apply the new skin.
            setupConfigSkin.applyConfigWindowSkin(self, icon_path, skin=self._skin)
            setupConfigSkin.setConfigWindowButtonText(self)

        except Exception as e:
            print("Error occured in configuration::setSkin(self, icon_path)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

        finally:
            print("End -> configuration::setSkin")

    def proxySettingsTrue(self):
        print("# Set Proxy as True.")

        try:
            self.rbtn_proxy.setChecked(True)
            self.rbtn_no_proxy.setChecked(False)

            self.txt_proxy.setEnabled(True)
            self.txt_proxy.setText("")

        except Exception as e:
            print("Error occured in configuration::proxySettingsTrue(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def proxySettingsFalse(self):
        print("# Set Proxy as False.")

        try:
            self.rbtn_no_proxy.setChecked(True)
            self.rbtn_proxy.setChecked(False)

            self.txt_proxy.setEnabled(False)
            self.txt_proxy.setText("No Proxy")

        except Exception as e:
            print("Error occured in configuration::proxySettingsFalse(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def addOcrLanguage(self):
        try:
            selected = self.lst_lang_available.selectedItems()
            for selection in selected:
                ocr_lng_use_item = QListWidgetItem(selection)
                self.lst_lang_selected.addItem(ocr_lng_use_item)
                self.lst_lang_available.takeItem(self.lst_lang_available.row(selection))
        except Exception as e:
            print("Error occured in configuration::addOcrLanguage")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)
        finally:
            print("## Add an OCR language.")

    def removeOcrLanguage(self):
        try:
            selected = self.lst_lang_selected.selectedItems()
            for selection in selected:
                ocr_lng_ave_item = QListWidgetItem(selection)
                self.lst_lang_available.addItem(ocr_lng_ave_item)
                self.lst_lang_selected.takeItem(self.lst_lang_selected.row(selection))
        except Exception as e:
            print("Error occured in configuration::removeOcrLanguage")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)
        finally:
            print("## Remove an OCR language.")

    def detectCamera(self):
        print("Start -> configuration::detectCamera(self)")

        # Clear Camera list.
        self.tre_cam.clear()

        # Refresh camera parameters.
        self.refreshCameraParameters()

        try:
            # Detect the cameras automatically and listing up them.
            camera_list = list(gp.Camera.autodetect())
            if not camera_list:
                print('### None of camera detected')
            else:
                # Get the list of connected cameras.
                camera_list.sort(key=lambda x: x[0])

                # Add each camera to the camera list.
                for index, (name, addr) in enumerate(camera_list):
                    print("#### New Camera, " + name + "(" + addr + ") is detected...")
                    tre_cam_item_ = QTreeWidgetItem(self.tre_cam)
                    tre_cam_item_.setText(0, addr)
                    tre_cam_item_.setText(1, name)
        except Exception as e:
            print("Error occured in configuration::detectCamera(self)")
            print(str(e))
            error.ErrorMessageCameraDetection(details=str(e), show=True, language=self._language)
            return(None)

        finally:
            print("End -> configuration::connectCamera")

    def connectCamera(self):
        print("Start -> configuration::connectCamera(self)")

        try:
            parent = self._main

            # Stop the gp_context and gp_camera.
            gp.gp_camera_exit(parent.gp_camera, parent.gp_context)

            # Restart the gp_context and gp_camera.
            parent.gp_context = gp.Context()
            parent.gp_camera = gp.Camera()

            # Get address and name of camera by selection.
            selected = self.tre_cam.currentItem()

            if not selected == None:
                cam_port, cam_name = [selected.text(0), selected.text(1)]

                print(cam_name, cam_port)

                # search ports for camera port name
                port_info_list = gp.PortInfoList()
                port_info_list.load()
                idx = port_info_list.lookup_path(cam_port)

                parent.gp_camera.set_port_info(port_info_list[idx])
                parent.gp_camera.init(parent.gp_context)

                parent.current_camera = camera.Camera(cam_name, cam_port, parent.gp_context, parent.gp_camera)

                # Set parameters to comboboxes.
                if not parent.current_camera.imagesize == None:
                    self.setCamParamCbx(self.cbx_cam_size, parent.current_camera.imagesize)
                if not parent.current_camera.iso == None:
                    self.setCamParamCbx(self.cbx_cam_iso, parent.current_camera.iso)
                if not parent.current_camera.whitebalance == None:
                    self.setCamParamCbx(self.cbx_cam_wht, parent.current_camera.whitebalance)
                if not parent.current_camera.exposuremetermode == None:
                    self.setCamParamCbx(self.cbx_cam_exp, parent.current_camera.exposuremetermode)
                if not parent.current_camera.f_number == None:
                    self.setCamParamCbx(self.cbx_cam_fval, parent.current_camera.f_number)
                if not parent.current_camera.imagequality == None:
                    self.setCamParamCbx(self.cbx_cam_qoi, parent.current_camera.imagequality)
                if not parent.current_camera.focusmode == None:
                    self.setCamParamCbx(self.cbx_cam_fmod, parent.current_camera.focusmode)
                if not parent.current_camera.expprogram == None:
                    self.setCamParamCbx(self.cbx_cam_epg, parent.current_camera.expprogram)
                if not parent.current_camera.capturemode == None:
                    self.setCamParamCbx(self.cbx_cam_cpt, parent.current_camera.capturemode)

                print("## Camera successfully connected.")

                # Set the current camera name.
                self.lbl_cur_cam_nam.setText(cam_name + " (" + cam_port + ")")
                print('## Currently ' + cam_name + " (" + cam_port + ")" + " is connected.")

            else:
                error_title = "No camera is selected."
                error_msg = "No camera is selected."
                error_info = "Please select valid camera from the list."
                error_icon = QMessageBox.Critical
                error_detailed = "Please select valid camera from the list."

                # Handle error.
                general.alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)

        except Exception as e:
            print("Error occured in configuration::connectCamera(self)")
            print(str(e))
            error.ErrorMessageCameraDetection(details=str(e), show=True, language=self._language)
            return(None)

        finally:
            print("End -> configuration::connectCamera")

    def setCamParamCbx(self, cbx, param):
        # Clear the combobox.
        cbx.clear()

        current = "Not selected..."

        try:
            # Add the first position for the combobox as the current value.
            current = param.get_value()
            cbx.addItem(current)

            # Add the options into the combobox.
            for n in range(gp.check_result(gp.gp_widget_count_choices(param))):
                choice = gp.check_result(gp.gp_widget_get_choice(param, n))
                opt_txt = str(n) + ":" + choice

                cbx.addItem(opt_txt)
        except Exception as e:
            print("Error occured in configuration::setCamParamCbx(self)")
            print(str(e))
            error.ErrorMessageCameraDetection(details=str(e), show=True, language=self._language)
            return(None)

        finally:
            print("#### Camera Prameter:" + current + ": configuration::setCamParamCbx")
