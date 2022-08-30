#!/usr/bin/python
# -*- coding: UTF-8 -*-

# import the necessary packages
import cv2, imutils, argparse, uuid, numpy, six, gphoto2 as gp, colorcorrect.algorithm as cca
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
    
    def __init__(self, cam_name, cam_port):
        self._camera_name = cam_name
        self._port = cam_port
        
        self._imagesize = None
        self._iso = None
        self._whitebalance = None
        self._exposurecompensation = None
        self._f_number = None
        self._imagequality = None
        self._focusmode = None
        self._expprogram = None
        self._capturemode = None
        self._exposuremetermode = None
            
        if self._setCamera(cam_name):
            params = [  "imagesize",
                        "iso",
                        "whitebalance",
                        "exposurecompensation",
                        "f-number",
                        "imagequality",
                        "focusmode",
                        "expprogram",
                        "capturemode",
                        "exposuremetermode"]
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                camera_params = {executor.submit(self._getCameraSetting, param): param for param in params}
                for future in concurrent.futures.as_completed(camera_params):
                    label = camera_params[future]
                    data = future.result()
                    
                    if label == "imagesize": self._imagesize = data
                    if label == "iso": self._iso = data
                    if label == "whitebalance": self._whitebalance = data
                    if label == "exposurecompensation": self._exposurecompensation = data
                    if label == "f-number": self._f_number = data
                    if label == "imagequality": self._imagequality = data
                    if label == "focusmode": self._focusmode = data
                    if label == "expprogram": self._expprogram = data
                    if label == "capturemode": self._capturemode = data
                    if label == "exposuremetermode": self._exposuremetermode = data
            
    def _getCameraSetting(self, param):
        result = dict()
        
        try:
            proc = subprocess.run(["gphoto2","--quiet","--get-config",param], capture_output=True)
            
            # Get camera parameters from  printed messages.
            params = proc.stdout.decode().split("\n")
            
            # Exit if none of messages printed.
            if params == None or params == "": return(None)
            
            # Define variables for storing entries.
            label = ""
            current = ""
            choice = list()
            
            for param in params:
                item = param.split(":")
                label = item[0]
                
                if label == "Label":
                    entry = item[1].strip()
                    result["label"] = entry
                elif label == "Current":
                    entry = item[1].strip()
                    result["current"] = entry
                elif label == "Choice":
                    # Split the text with white space.
                    entry = item[1].strip().split(" ")
                    
                    # Get the first item as the value.
                    entry_val = entry[0]
                    
                    # Remove the first item from the entry.
                    entry_txt = str(entry.pop(0))
                    
                    # Append the entry to the choice list.
                    choice.append({str(entry.pop(0)):entry_val})
                
                result["choice"] = choice
                
            # Returns configuration list.
            if len(result) == None or len(result) == 0:
                return(None)
            else:
                return(result)
        except Exception as e:
            print("Error occured in Camera::getCameraConfig(cam_parameter)")
            print(str(e))
            
            return(None)
    
    def _setCamera(self, cam_name):
        print("Camera::_setCamera(" + cam_name + ")")
        try:
            # Define the subprocess for detecting connected camera.
            cmd_setting = ["gphoto2", "--camera", cam_name]
            
            # Execute the gphoto2 command.
            subprocess.run(cmd_setting, capture_output=True)
            
            return(True)
        except Exception as e:
            print("Error occured in Camera::setCamera(name, addr)")
            print(str(e))
            
            return(None)

def detectCamera():
    print("Camera::detectCamera()")
    
    try:
        cams = list()
        
        # Get the context of the camera.
        context = gp.Context()
        
        if hasattr(gp, 'gp_camera_autodetect'):
            # gphoto2 version 2.5+
            cameras = context.camera_autodetect()
        else:
            port_info_list = gp.PortInfoList()
            port_info_list.load()
            abilities_list = gp.CameraAbilitiesList()
            abilities_list.load(context)
            cameras = abilities_list.detect(port_info_list, context)
        
        for name, port in cameras:
            cams.append({"name" : name, "port" : port})
        
        return(cams)
    except Exception as e:
        print("Error occured in Camera::detectCamera()")
        print(str(e))
    
def takePhoto(output):
    print("Camera::takePhoto(output)")
    
    try:
        # Define the subprocess for tethered shooting by using gphoto2
        cmd_taking = [    "gphoto2", 
                        "--quiet",
                        "--capture-image-and-download",
                        "--filename=" + output + ".%C"]
        
        # Execute the command.
        print("Hi,Cheez!!")
        pop = subprocess.run(cmd_taking, capture_output=True)
        
        print(output)
        return(0)
    except Exception as e:
        print("Error occured in Camera::takePhoto(output)")
        print(str(e))
        
        return(None)
