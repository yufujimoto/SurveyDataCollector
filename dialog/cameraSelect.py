#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Import PyQt5 libraries for generating the GUI application.
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Import camera and image processing library.
import gphoto2 as gp
import dialog.cameraSelectDialog as cameraSelectDialog
import modules.camera as camera


class SelectCameraDialog(QDialog, cameraSelectDialog.Ui_CameraSelectDialog):
    @property
    def camera_name(self): return self._camera_name
    @property
    def camera_port(self): return self._camera_port

    @camera_name.setter
    def camera_name(self, value): self._camera_name = value
    @camera_port.setter
    def camera_port(self, value): self._camera_port = value

    #def __init__(self, parent=None, cameras=None):
    def __init__(self, parent=None):
        print("cameraSelect::__init__(self, parent=None)")
        super(SelectCameraDialog, self).__init__(parent)
        self.setupUi(self)

        # Initialyze the porperties.
        self._camera_name = None
        self._camera_port = None

        # Connect the functions to the UI objects.
        self.tre_cam.itemSelectionChanged.connect(self._getSelectedNumber)
        self.btn_cam_detect.clicked.connect(self._detectCamera)

    def _detectCamera(self):
        print("Start -> cameraSelect::_detectCamera(self)")
        print("## Please wait for a minute...")
        try:
            # Get the list of connected cameras.
            camera_list = list(gp.Camera.autodetect())
            if not camera_list:
                print('No camera detected')
            else:
                camera_list.sort(key=lambda x: x[0])

                # Add each camera to the camera list.
                for index, (name, addr) in enumerate(camera_list):
                    print("### Detected... : " + name)
                    tre_cam_item_ = QTreeWidgetItem(self.tre_cam)
                    tre_cam_item_.setText(0, addr)
                    tre_cam_item_.setText(1, name)

                # Resize the header width with contents.
                self.tre_cam.resizeColumnToContents(0)
                self.tre_cam.resizeColumnToContents(1)

                # Select the top object as the default selection.
                self.tre_cam.setCurrentItem(self.tre_cam.topLevelItem(0))
        except Exception as e:
            print("Error occured in cameraSelect::detectCamera(self)")
            print(str(e))
            error.ErrorMessageCameraDetection(details=str(e), show=True, language=self._language)
        finally:
            print("End -> cameraSelect::_detectCamera")

    def _getSelectedNumber(self):
        print("cameraSelect::_getSelectedNumber(self)")

        # Get address and name of camera by selection.
        selected = self.tre_cam.currentItem()
        addr, name = [selected.text(0), selected.text(1)]

        self._camera_name = name
        self._camera_port = addr
        #
        # gp.gp_camera_exit(gp_camera, gp_context)
        #
