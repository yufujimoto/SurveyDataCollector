#!/usr/bin/python
# -*- coding: UTF-8 -*-

# import the necessary packages
import cv2, imutils, argparse, uuid, numpy, six, gphoto2 as gp, colorcorrect.algorithm as cca
import os, sys, subprocess, tempfile, pipes, getopt, colorsys

from sys import argv
from optparse import OptionParser
from imutils import perspective, contours
from PIL import Image, ImageDraw
from PIL.ExifTags import TAGS, GPSTAGS
from colorcorrect.util import from_pil, to_pil

#====================================
#          Camera Operation
#====================================
def setCamera(cam_name):
    print("imageProcessing::setCamera(cam_name, cam_address)")
    
    try:
        # Define the subprocess for detecting connected camera.
        cmd_setting = ["gphoto2"]
        
        # Define parameters for the subprocess.
        cmd_setting.append("--camera")
        cmd_setting.append(cam_name)
        
        # Execute the gphoto2 command.
        subprocess.check_output(cmd_setting)
        
        return(True)
    except Exception as e:
        print("Error occurs in imageProcessing::setCamera(name, addr)")
        print(str(e))
        
        return(None)

def detectCamera():
    print("imageProcessing::detectCamera()")
    
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
        print("Error occurs in imageProcessing::detectCamera()")
        print(str(e))
    
def getCameraConfig(cam_parameter):
    print("imageProcessing::getCameraConfig(cam_parameter, cam_name, cam_address)")
    
    result = dict()
    
    try:
        # Define the subprocess for getting camera parameters.
        cmd_setting = ["gphoto2"]
        
        # Define parameters for the subprocess.
        cmd_setting.append("--get-config")
        cmd_setting.append(cam_parameter)
        
        # Execute the subprocess.
        stdout_data = subprocess.check_output(cmd_setting)
        
        # Exit if none of messages printed.
        if stdout_data == None or stdout_data == "": return(None)
        
        # Get camera parameters from  printed messages.
        params = stdout_data.split("\n")
        
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
        print("Error occurs in imageProcessing::getCameraConfig(cam_parameter, cam_name, cam_address)")
        print(str(e))
        
        return(None)
    
def takePhoto(output):
    print("imageProcessing::takePhoto(output)")
    
    try:
        # Define the subprocess for tethered shooting by using gphoto2
        cmd_taking = ["gphoto2"]
        
        # Define the parameters for the command.
        cmd_taking.append("--quiet")
        cmd_taking.append("--capture-image-and-download")
        cmd_taking.append("--filename=" + output + ".%C")
        
        # Execute the command.
        result = subprocess.check_output(cmd_taking)
        
        return(result)
    except Exception as e:
        print("Error occurs in imageProcessing::takePhoto(output)")
        print(str(e))
        
        return(None)
