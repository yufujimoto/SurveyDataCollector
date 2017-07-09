#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os, sys, subprocess, tempfile, pipes, getopt
from optparse import OptionParser

def detectCam():
    # Define the subprocess for detecting connected camera.
    cmd_detect = ["gphoto2"]
    
    # Define the parameters for the command.
    cmd_detect.append("--auto-detect")
    cmd_detect.append("--quiet")
    
    # Execute the subprocess. 
    cam = subprocess.check_output(cmd_detect)
    
    # Edit the output strings.
    cam = cam.replace("-","")
    cam = cam.replace("\n","")
    cam = cam.replace("\t",",")
    cam = cam.replace("  "," ")
    cam = cam.replace("Model","")
    cam = cam.replace("Port","")
    cam = cam.strip()
    
    # Returns camera information if succusessfully detected.
    # Otherwise, returns nothing. 
    if cam == "":
        print("Error: No Camera detected")
        return(None)
    else:
        return(cam)

def takePhoto(output):
    # Define the subprocess for tethered shooting by using gphoto2
    cmd_taking = ["gphoto2"]
    
    # Define the parameters for the command.
    cmd_taking.append("--quiet")
    cmd_taking.append("--capture-image-and-download")
    cmd_taking.append("--filename="+output+".%C")
    
    # Execute the command.
    result = subprocess.check_output(cmd_taking)
    
    return(result)

def getConfig(param):
    # Define the subprocess for getting the camera configuration by using gphoto2.
    cmd_getConfig = ["gphoto2"]
    
    # Define the parameters for the command.
    cmd_getConfig.append("--get-config")
    cmd_getConfig.append(param)
    
    # Execute the command.
    params = subprocess.check_output(cmd_getConfig)
    params = params.split("\n")
    
    result = dict()
    
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
    return(result)

def getConfigurations():
    # Define the subprocess for getting the camera configuration by using gphoto2.
    cmd_getConfig = ["gphoto2"]
    
    # Define the parameters for the command.
    cmd_getConfig.append("--quiet")
    cmd_getConfig.append("--list-config")
    
    # Execute the command.
    result = subprocess.check_output(cmd_getConfig)
    
    # Returns configuration list.
    return(result)

def getMetaInfo(imgFile):
    # Define the subprocess for getting the camera configuration by using gphoto2.
    cmd_getMetaInfo = ["dcraw"]
    
    # Define the parameters for the command.
    cmd_getMetaInfo.append("-i")
    cmd_getMetaInfo.append("-v")
    cmd_getMetaInfo.append("'" + imgFile + "'")
    
    # Execute the command.
    proc = subprocess.Popen(" ".join(cmd_getMetaInfo), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    buf = []

    while True:
        line = proc.stdout.readline()
        buf.append(line)
        sys.stdout.write(line)
        
        if not line and proc.poll() is not None:
            break
    
    # Returns configuration list.
    return ''.join(buf)

def getThumbnail(raw_image):
    # Define the subprocess for getting the camera configuration by using gphoto2.
    cmd_getThumb = ["dcraw"]
    
    # Define the parameters for the command.
    cmd_getThumb.append("-e")
    cmd_getThumb.append(raw_image)
    
    # Execute the command.
    result = subprocess.check_output(cmd_getThumb)
    
    # Returns configuration list.
    return(result)

def showImage(rawfile):
    cmd_show = ["geeqie"]
    cmd_show.append(rawfile)
    
    subprocess.call(cmd_show)