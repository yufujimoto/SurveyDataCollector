#!/usr/bin/python
# -*- coding: UTF-8 -*-

# import the necessary packages
import cv2, imutils, argparse, uuid, numpy, time, six, pathlib, gphoto2 as gp, colorcorrect.algorithm as cca
import os, sys, subprocess, tempfile, pipes, getopt, colorsys
import concurrent.futures

from sys import argv
from optparse import OptionParser
from imutils import perspective, contours
from PIL import Image, ImageDraw
from PIL.ExifTags import TAGS, GPSTAGS
from colorcorrect.util import from_pil, to_pil

#====================================
#          Camera Operation
#====================================
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

class Camera(object):
    @property
    def camera_name(self): return self._camera_name
    @property
    def port(self): return self._port
    @property
    def imagesize(self): return self._imagesize
    @property
    def iso(self): return self._iso
    @property
    def shutterspeed(self): return self._shutterspeed
    @property
    def whitebalance(self): return self._whitebalance
    @property
    def exposurecompensation(self): return self._exposurecompensation
    @property
    def f_number(self): return self._f_number
    @property
    def imagequality(self): return self._imagequality
    @property
    def focusmode(self): return self._focusmode
    @property
    def expprogram(self): return self._expprogram
    @property
    def capturemode(self): return self._capturemode
    @property
    def exposuremetermode(self): return self._exposuremetermode

    @camera_name.setter
    def camera_name(self, value): self._camera_name = value
    @port.setter
    def port(self, value): self._port = value
    @imagesize.setter
    def imagesize(self, value): self._imagesize = value
    @iso.setter
    def iso(self, value): self._iso = value
    @shutterspeed.setter
    def shutterspeed(self, value): self._shutterspeed = value
    @whitebalance.setter
    def whitebalance(self, value): self._whitebalance = value
    @exposurecompensation.setter
    def exposurecompensation(self, value): self._exposurecompensation = value
    @f_number.setter
    def f_number(self, value): self._f_number = value
    @imagequality.setter
    def imagequality(self, value): self._imagequality = value
    @focusmode.setter
    def focusmode(self, value): self._focusmode = value
    @expprogram.setter
    def expprogram(self, value): self._expprogram = value
    @capturemode.setter
    def capturemode(self, value): self._capturemode = value
    @exposuremetermode.setter
    def exposuremetermode(self, value): self._exposuremetermode = value

    def __init__(self, name, addr, gp_context, gp_camera):
        gp_config = gp_camera.get_config(gp_context)
        cnt = gp_config.count_children()

        self._camera_name = name
        self._port = addr
        self._imagesize = None
        self._iso = None
        self._shutterspeed = None
        self._whitebalance = None
        self._exposurecompensation = None
        self._f_number = None
        self._imagequality = None
        self._focusmode = None
        self._expprogram = None
        self._capturemode = None
        self._exposuremetermode = None

        self._imagesize = gp.check_result(gp.gp_widget_get_child_by_name(gp_config,'imagesize'))
        self._iso = gp.check_result(gp.gp_widget_get_child_by_name(gp_config,'iso'))
        self._shutterspeed = gp.check_result(gp.gp_widget_get_child_by_name(gp_config,'shutterspeed'))
        self._whitebalance = gp.check_result(gp.gp_widget_get_child_by_name(gp_config,'whitebalance'))
        self._exposurecompensation = gp.check_result(gp.gp_widget_get_child_by_name(gp_config,'exposurecompensation'))
        self._f_number = gp.check_result(gp.gp_widget_get_child_by_name(gp_config,'f-number'))
        self._imagequality = gp.check_result(gp.gp_widget_get_child_by_name(gp_config,'imagequality'))
        self._focusmode = gp.check_result(gp.gp_widget_get_child_by_name(gp_config,'focusmode'))
        self._expprogram = gp.check_result(gp.gp_widget_get_child_by_name(gp_config,'expprogram'))
        self._capturemode = gp.check_result(gp.gp_widget_get_child_by_name(gp_config,'capturemode'))
        self._exposuremetermode = gp.check_result(gp.gp_widget_get_child_by_name(gp_config,'exposuremetermode'))

    def _do_capture(self, gp_context, gp_camera, save_path):
        print("camera::_do_capture(self)")

        # Take two shots per one capture. The fisrt shot.
        self._capture(gp_context, gp_camera, save_path)

        # Wait a second.
        time.sleep(1)

        # The second shot.
        self._capture(gp_context, gp_camera, save_path)

        # Wait a second.
        time.sleep(1)

    def _capture(self, gp_context, gp_camera, save_path):
        print("camera::_capture(self)")

        timeout = 20
        starttime = time.time()

        try:
            # capture actual image
            gp.check_result(gp.gp_camera_trigger_capture(gp_camera, gp_context))
            filefound = [False, False]

            while filefound[1] != gp.GP_EVENT_FILE_ADDED:
                filefound = gp.gp_camera_wait_for_event(gp_camera, 10000, gp_context)
                if time.time() - starttime > timeout:
                    print ('operation timed out')
                    return False

            campath = '/'
            filelist = self.list_files(gp_camera, gp_context, campath)

            for f in filelist:
                filename = f.strip(campath)
                camfile = gp.check_result(gp.gp_file_new())

                camfile = gp.gp_camera_file_get(gp_camera, campath, filename, gp.GP_FILE_TYPE_NORMAL, gp_context)

                ext = pathlib.Path(f).suffix

                gp.gp_file_save(camfile[1], save_path + ext)
                #gp.gp_file_unref(camfile)
                gp.gp_camera_file_delete(gp_camera, campath, filename, gp_context)

            endtime = round(time.time() - starttime, 2)
            print ('capture complete in {}s'.format(endtime))

        except Exception as e:
            print("Error occured in camera::_capture(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

    def list_files(self, camera, context, path='/'):
        result = []
        # get files
        for name, value in gp.check_result(gp.gp_camera_folder_list_files(camera, path, context)):
            result.append(os.path.join(path, name))

        # read folders
        folders = []

        for name, value in gp.check_result(gp.gp_camera_folder_list_folders(camera, path, context)):
            folders.append(name)

        # recurse over subfolders
        for name in folders:
            result.extend(list_files(camera, context, os.path.join(path, name)))
        return result
