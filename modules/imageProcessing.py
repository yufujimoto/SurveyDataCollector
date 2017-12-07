#!/usr/bin/python
# -*- coding: UTF-8 -*-

# import the necessary packages
import cv2, imutils, argparse, uuid, numpy, six, gphoto2 as gp, colorcorrect.algorithm as cca
import os, sys, subprocess, tempfile, pipes, getopt, colorsys, autocolorize

from sys import argv
from optparse import OptionParser
from imutils import perspective, contours
from PIL import Image, ImageDraw
from PIL.ExifTags import TAGS, GPSTAGS
from colorcorrect.util import from_pil, to_pil

def colorize(dir_source, img_input, img_output):
    print("imageProcessing::colorize(dir_source, img_input, img_output)")
    
    try:
        # Get the full path to the bash script command.
        script_siggraph = [os.path.join(dir_source, "siggraph_run.sh")]
        
        # Define the parameters for the command.
        script_siggraph.append(str(dir_source))     # Source directory for siggraph.
        script_siggraph.append(str(img_input))      # Input grey scaled image file.
        script_siggraph.append(str(img_output))     # Output colorized image.
        
        # Execute the colorize function.
        subprocess.check_output(script_siggraph)
    except Exception as e:
        print("Error occurs in imageProcessing::colorize(src_dir, imgfile, output)")
        print(str(e))
        
        return(None)

def openWithGimp(img_input):
    print("imageProcessing::openWithGimp(img_input)")
    
    try:
        # Define the subprocess for tethered shooting by using gphoto2
        cmd_gimp = ["gimp"]
        cmd_gimp.append(img_input)
        
        # Execute the subprocess. 
        subprocess.check_output(cmd_gimp)
    except Exception as e:
        print("Error occurs in imageProcessing::openWithGimp(img_input)")
        print(str(e))
        
        return(None)

def getMetaInfo(img_input):
    print("imageProcessing::getMetaInfo(img_input)")
    
    try:
        # Define the subprocess for getting the camera configuration by using gphoto2.
        cmd_getMetaInfo = ["dcraw"]
        
        # Define the parameters for the command.
        cmd_getMetaInfo.append("-i")
        cmd_getMetaInfo.append("-v")
        cmd_getMetaInfo.append("'" + img_input + "'")
        
        # Execute the command.
        proc = subprocess.Popen(" ".join(cmd_getMetaInfo), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        buf = []
        
        while True:
            line = proc.stdout.readline()
            buf.append(line)
            sys.stdout.write(line)
            
            if not line and proc.poll() is not None: break
        
        # Returns configuration list.
        return ''.join(buf)
    except Exception as e:
        print("Error occurs in imageProcessing::getMetaInfo(img_input)")
        print(str(e))
        
        return(None)

def getThumbnail(img_input):
    print("imageProcessing::getThumbnail(img_input)")
    
    try:
        # Define the subprocess for getting the camera configuration by using gphoto2.
        cmd_getThumb = ["dcraw"]
        
        # Define the parameters for the command.
        cmd_getThumb.append("-e")
        cmd_getThumb.append(img_input)
        
        # Execute the command.
        result = subprocess.check_output(cmd_getThumb)
        
        # Returns configuration list.
        return(result)
    except Exception as e:
        print("Error occurs in imageProcessing::getThumbnail(img_input)")
        print(str(e))

def enhance(img_input, img_output):
    print("imageProcessing::enhance(img_input, img_output)")
    
    try:
        # Load input image, and create the output file name.
        org_cv2_img = cv2.imread(img_input)
        
        # Split RGB channels into single channels.
        b,g,r = cv2.split(org_cv2_img)
        
        # Define the histogram normalization algorithm.
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        
        # Apply the histogram normalization algorithm to each channel.
        norm_b = clahe.apply(b)
        norm_r = clahe.apply(r)
        norm_g = clahe.apply(g)
        
        # Merge single channels into one image.
        cnv_cv2_img = cv2.merge((norm_b,norm_g,norm_r))
        
        # Save the result.
        cv2.imwrite(img_output, cnv_cv2_img)
        
        # Return the output file name.
        return(img_output)
    except Exception as e:
        print("Error occurs in imageProcessing::enhance(img_input)")
        print(str(e))
        
        return(None)
    
def makeMono(img_input, img_output):
    print("imageProcessing::makeMono(img_input, img_output)")
    
    try:
        # Load input image, and create the output file name.
        org_cv2_img = cv2.imread(img_input)
        
        # Convert color image to gray scale image.
        gry_cv2_img = cv2.cvtColor(org_cv2_img, cv2.COLOR_BGR2GRAY)
        
        # Save the result.
        cv2.imwrite(img_output, gry_cv2_img)
        
        # Return the output file name.
        return(img_output)
    except Exception as e:
        print("Error occurs in imageProcessing::makeMono(img_input, img_output)")
        print(str(e))
        
        return(None)

def negaToPosi(img_input, img_output):
    print("imageProcessing::negaToPosi(img_input, img_output)")
    
    try:
        # Load input image, and create the output file name.
        org_cv2_img = cv2.imread(img_input)
        
        # Split RGB channels into single channels.
        b,g,r = cv2.split(org_cv2_img)
        
        # Invert color in each channel.
        conv_b = 255 - b
        conv_g = 255 - g
        conv_r = 255 - r
        
        # Merge single channels into one image.
        cnv_cv2_img = cv2.merge((conv_b, conv_g, conv_r))
        
        # Save the result.
        cv2.imwrite(img_output, cnv_cv2_img)
        
        # Return the output file name.
        return(img_output)
    except Exception as e:
        print("Error occurs in imageProcessing::negaToPosi(img_input, img_output)")
        print(str(e))
        
        return(None)

def extractInnerFrame(in_file, dst_img, ratio):
    # Load input image, and create the output file name.
    org_img = cv2.imread(in_file)
    
    # Shrink the image for extracting contour.
    h, w = org_img.shape[:2]
    image = cv2.resize(org_img,(int(w * ratio), int(h * ratio)), interpolation=cv2.INTER_CUBIC)
    
    # Convert the image to grayscale and make it blur.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    
    # Detect the edge.
    edged = cv2.Canny(gray, 50, 100)
    
    # Perform dilation and erosion.
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)
    
    # Find contours in the edge map.
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    
    # Get the largest contour.
    cnts_areas = list()
    for c in cnts:
        cnts_areas.append(cv2.contourArea(c))

    rect_index = cnts_areas.index(max(cnts_areas))
    cnt = cnts[rect_index]
    
    # Get the bounding rectangle for the largest rectangle.
    x,y,w,h = cv2.boundingRect(cnt)
    
    # Rescale to apply the crop area to original image.
    x = int(x / ratio)
    y = int(y / ratio)
    w = int(w / ratio)
    h = int(h / ratio)
    
    # Finally extract interior of the original image and save it.
    crop = org_img[y:(y+h),x:(x+w)]
    cv2.imwrite(dst_img, crop)
    
    # Returns saved file path.
    return(dst_img)

def rotation(in_file, dst_img, angle):
    # Load input image, and create the output file name.
    org_img = cv2.imread(in_file)
    
    # grab the dimensions of the image and then determine the center
    (h, w) = org_img.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    
    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = numpy.abs(M[0, 0])
    sin = numpy.abs(M[0, 1])
    
    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
    
    # perform the actual rotation and return the image
    rot_img = cv2.warpAffine(org_img, M, (nW, nH))
    
    # Save the result.
    cv2.imwrite(dst_img, rot_img)
    
    # Return the output file name.
    return(dst_img)

def makeThumbnail(imgfile, output, basewidth):
    img = Image.open(imgfile).convert("RGB")
    scale = 0
    wsize = 0
    hsize = 0
        
    if img.size[0]>=img.size[1]:
        scale=(float(basewidth)/float(img.size[0]))
        wsize = basewidth
        hsize = int((float(img.size[1])*float(scale)))
    else:
        scale=(float(basewidth)/float(img.size[1]))
        wsize = int((float(img.size[0])*float(scale)))
        hsize = basewidth
    
    new = img.resize((int(wsize), int(hsize)), Image.ANTIALIAS)
    new.save(output)

def autoWhiteBalance(imgfile, output, method = "automatic"):
    img = Image.open(imgfile)
    
    adj_img = None
    
    if method == "stretch": adj_img = to_pil(cca.stretch(from_pil(img)))
    elif method == "gray_world": adj_img = to_pil(cca.gray_world(from_pil(img)))
    elif method == "max_white": adj_img = to_pil(cca.max_white(from_pil(img)))
    elif method == "retinex": adj_img = to_pil(cca.cca.retinex(from_pil(img)))
    elif method == "retinex_adjusted": adj_img = to_pil(cca.retinex_with_adjust(from_pil(img)))
    elif method == "stdev_luminance": adj_img = to_pil(cca.standard_deviation_and_luminance_weighted_gray_world(from_pil(img)))
    elif method == "stdev_grey_world": adj_img = to_pil(cca.standard_deviation_weighted_grey_world(from_pil(img)))
    elif method == "luminance_weighted": adj_img = to_pil(cca.luminance_weighted_gray_world(from_pil(img)))
    elif method == "automatic": adj_img = to_pil(cca.automatic_color_equalization(from_pil(img)))
    
    adj_img.save(output)
    
def pansharpen(thumbnail, original, output, method="ihs"):
    # Open the colorized image and the original image.
    thm = Image.open(thumbnail)
    org = Image.open(original)
    
    # Rescale the colorized image to original image size.
    col = thm.resize(org.size, Image.ANTIALIAS)
    
    if method == "ihs":
        # IHS conversion.
        img = ihsConvert(img=col, high=org)
        img.save(output)
    elif method =="sm":
        # Simple Mean conversion.
        img = simpleMeanConvert(img=col, high=org)
        img.save(output)
    elif method == "br":
        #BroveyConvert
        img = broveyConvert(img=col, high=org)
        img.save(output)

def normalize(arr):
    arr = arr.astype('float')
    
    for i in range(3):
        minval = arr[...,i].min()
        maxval = arr[...,i].max()
        if minval != maxval:
            arr[...,i] -= minval
            arr[...,i] *= (255.0/(maxval-minval))
    return arr

def broveyConvert(img, high):
    # Red_out = Red_in / [(blue_in + green_in + red_in) * Pan]
    # Greem_out = green_in / [(blue_in + green_in + red_in) * Pan]
    # Blue_out = blue_in / [(blue_in + green_in + red_in) * Pan]
    
    # Split the colorized image into red, green and blue bands.
    r, g, b=img.split()
    high = high.convert("L")
    
    # Calculate Brovey convert values.
    r = ImageMath.eval("convert(int(((float(r)/(float(b)+float(g)+float(r)))*float(h))),'L')", r=r, g=g, b=b, h=high)
    g = ImageMath.eval("convert(int(((float(g)/(float(b)+float(g)+float(r)))*float(h))),'L')", r=r, g=g, b=b, h=high)
    b = ImageMath.eval("convert(int(((float(b)/(float(b)+float(g)+float(r)))*float(h))),'L')", r=r, g=g, b=b, h=high)
    
    # Normalize the image
    rgb = Image.merge("RGB",(r,g,b))
    rgb_arr = numpy.array(rgb)
    
    # Return converted image.
    return Image.fromarray(normalize(rgb_arr).astype('uint8'),'RGB')

def simpleMeanConvert(img, high):
    # Red_out= 0.5 * (Red_in + Pan_in) 
    # Green_out = 0.5 * (Green_in + Pan_in) 
    # Blue_out= 0.5 * (Blue_in + Pan_in)
    
    # Split the colorized image into red, green and blue bands.
    r, g, b=img.split()
    high = high.convert("L")
    
    # Calculate simple mean values.
    r = ImageMath.eval("convert((r+h)/2),'L')", r=r, h=high)
    g = ImageMath.eval("convert((g+h)/2),'L')", g=g, h=high)
    b = ImageMath.eval("convert((b+h)/2),'L')", b=b, h=high)
    
    # Return converted image.
    return Image.merge("RGB",(r,g,b))

def ihsConvert(img, high):
    # Convert the original image into single band image.
    high = high.convert("L")
    
    # Split the colorized image into red, green and blue bands.
    r,g,b = img.split()
    
    # Initialize arrays for Hue, Saturation and Value.
    Hdat = []
    Sdat = []
    Vdat = []
    
    # Convert RGB to HSV, and swap the Value band with original image.
    for rd,gn,bl,pv in zip(r.getdata(),g.getdata(),b.getdata(),high.getdata()):
        h,s,v = colorsys.rgb_to_hsv(rd/255.,gn/255.,bl/255.)
        
        Hdat.append(int(h*255.))
        Sdat.append(int(s*255.))
        Vdat.append(pv)
    
    # Initialize arrays for new red, green and blue bands.
    Rdat = []
    Gdat = []
    Bdat = []
    
    # Convert HSV to RGB.
    for dr,ng,lb in zip(Hdat,Sdat,Vdat):
        new_r,new_g,new_b = colorsys.hsv_to_rgb(dr/255.,ng/255.,lb/255.)
        Rdat.append(int(new_r*255.))
        Gdat.append(int(new_g*255.))
        Bdat.append(int(new_b*255.))
    
    # Rewrite the original pixels by new RGB values.
    r.putdata(Rdat)
    g.putdata(Gdat)
    b.putdata(Bdat)
    
    # Return converted image.
    return Image.merge('RGB',(r,g,b))

