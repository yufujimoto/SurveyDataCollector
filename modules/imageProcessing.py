#!/usr/bin/python
# -*- coding: UTF-8 -*-

# import the necessary packages
import cv2, imutils, argparse, uuid, math, numpy, operator, gphoto2 as gp, colorcorrect.algorithm as cca
import os, sys, subprocess, tempfile, pipes, getopt, colorsys, exifread, rawpy, imageio
import pyexiv2, piexif

from sys import argv
from optparse import OptionParser
from imutils import perspective, contours
from PIL import Image, ImageDraw
from PIL.ExifTags import TAGS
from colorcorrect.util import from_pil, to_pil
from focus_stack import FocusStacker

import modules.error as error

def imread(fl_input, flags=cv2.IMREAD_COLOR, dtype=numpy.uint8):
    print("## Reading a image as cv2 object:" + fl_input + " imageProcessing::imread")

    try:
        img_numpy = numpy.fromfile(fl_input, dtype)
        fl_output = cv2.imdecode(img_numpy, flags)

        return fl_output
    except Exception as e:
        print("Error occured in imageProcessing::imread(fl_input, flags=cv2.IMREAD_COLOR, dtype=numpy.uint8)")
        print((str(e)))
        error.ErrorMessageImageProcessing(details=str(e), show=True, language="en")
        return None

def imwrite(fl_input, fl_output, params=None):
    print("## Rewrite the "+ fl_input+" with the cv2 object: imageProcessing::imwrite")

    try:
        ext = os.path.splitext(fl_input)[1]
        img_enc, img_numpy = cv2.imencode(ext, fl_output, params)

        if img_enc:
            with open(fl_input, mode='w+b') as f:
                img_numpy.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print("Error occured in imageProcessing::colorize(src_dir, imgfile, output)")
        print((str(e)))
        error.ErrorMessageImageProcessing(details=str(e), show=True, language="en")
        return False

def colorize(dir_source, fl_input, fl_output, col_model="colornet.t7"):
    print("imageProcessing::imwrite(fl_input, img, params=None)")

    try:
        # Get the full path to the bash script command.
        script_siggraph = ["th"]

        # Define the parameters for the command.
        script_siggraph.append(str(os.path.join(dir_source, "colorize.lua")))
        script_siggraph.append(str(fl_input.encode("utf-8"),"utf-8"))     # Input grey scaled image file.
        script_siggraph.append(str(fl_output.encode("utf-8"),"utf-8"))     # Output colorized image.
        script_siggraph.append(str(os.path.join(dir_source, col_model)))

        # Execute the colorize function.
        subprocess.check_output(script_siggraph)

        return(True)
    except Exception as e:
        print("Error occured in imageProcessing::colorize(src_dir, imgfile, output)")
        print((str(e)))
        error.ErrorMessageImageProcessing(details=str(e), show=True, language="en")
        return(None)

def openWithGimp(fl_input):
    print("Start -> imageProcessing::openWithGimp(" + fl_input + ")")

    try:
        # Define the subprocess for tethered shooting by using gphoto2
        cmd_gimp = ["gimp"]
        cmd_gimp.append(fl_input)

        # Execute the subprocess.
        subprocess.check_output(cmd_gimp)

        # Return the result as Boolean.
        return(True)
    except Exception as e:
        print("Error occured in imageProcessing::openWithGimp(fl_input)")
        print((str(e)))
        error.ErrorMessageImageProcessing(details=str(e), show=True, language="en")
        return(None)
    finally:
        print("End -> imageProcessing::openWithGimp")

def getMetaInfo(fl_input):
    print("Start -> imageProcessing::getMetaInfo(" + fl_input + ")")

    try:
        # Open the image object with read only mode.

        img_input = open(fl_input, 'rb')

        # Get EXIF tags and their values.
        org_tags = exifread.process_file(img_input)

        # Prepare new tags object.
        new_tags = dict()

        for org_tag in sorted(org_tags.keys()):
            key = str(org_tag).replace("EXIF ","")
            value = str(org_tags[org_tag])

            if org_tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote', 'EXIF UserComment', 'Image PrintIM'):
                print("### Exif Info:" + key + ":" + value)

                if str(org_tag) == "EXIF Tag 0x9010":
                    key = "OffsetTime"
                elif str(org_tag) == "EXIF Tag 0x9011":
                    key = "OffsetTimeOriginal"
                elif str(org_tag) == "EXIF Tag 0x9012":
                    key = "OffsetTimeDigitized"
                elif str(org_tag) == "EXIF Tag 0x9400":
                    key = "AmbientTemperature"
                    value = exifRational(str(org_tags[org_tag]))
                elif str(org_tag) == "EXIF Tag 0x9402":
                    key = "Pressure"
                elif str(org_tag) == "EXIF Tag 0x9403":
                    key = "WaterDepth"
                    value = exifRational(str(org_tags[org_tag]))
                elif str(org_tag) == "EXIF Tag 0x9404":
                    key = "Acceleration"
                elif str(org_tag) == "EXIF BrightnessValue":
                    value = exifRational(str(org_tags[org_tag]))
                elif str(org_tag) == "EXIF ExifVersion":
                    entry = str(org_tags[org_tag])
                    value = float(entry) / 100
                elif str(org_tag) == "EXIF FNumber":
                    value = exifRational(str(org_tags[org_tag]))
                elif str(org_tag) == "EXIF MaxApertureValue":
                    value = exifRational(str(org_tags[org_tag]))
                elif str(org_tag) == "EXIF FocalLength":
                    value = exifRational(str(org_tags[org_tag]))
            new_tags[key]=value
        return(new_tags)
    except Exception as e:
        print("Error occured in imageProcessing::getMetaInfo(fl_input)")
        print((str(e)))
        error.ErrorMessageImageProcessing(details=str(e), show=True, language="en")
        return(None)

    finally:
        print("End -> imageProcessing::getMetaInfo")

def exifRational(exifTag):
    print("## EXIF tag to string:" + exifTag + ": imageProcessing::exifRational")

    try:
        value = None

        # Convert the rational tag value to float number.
        if not exifTag.find('/') == -1:
            entry = exifTag.split("/")
            value = round(float(entry[0]) / float(entry[1]),2)
        else:
            value = round(float(exifTag),2)

        return(value)
    except Exception as e:
        print("Error occured in imageProcessing::exifRational(exifTag)")
        print((str(e)))
        error.ErrorMessageImageProcessing(details=str(e), show=True, language="en")
        return(None)

def getThumbnail(fl_input):
    print("## Getting a thubnail of the RAW: imageProcessing::getThumbnail")
    try:
        # Define the output thumbnail file.
        fl_output = os.path.splitext(fl_input)[0] + ".thumb" + ".jpg"

        # Extract the thumbnail image from raw image file.
        with rawpy.imread(fl_input) as raw:
            thumb = raw.extract_thumb()
        if thumb.format == rawpy.ThumbFormat.JPEG:
            # thumb.data is already in JPEG format, save as-is
            with open(fl_output, 'wb') as f:
                f.write(thumb.data)
        elif thumb.format == rawpy.ThumbFormat.BITMAP:
            # thumb.data is an RGB numpy array, convert with imageio
            imageio.imsave(fl_output, thumb.data)

        # Return the result.
        return(fl_output)

    except Exception as e:
        print("Error occured in imageProcessing::getThumbnail(fl_input)")
        print((str(e)))
        error.ErrorMessageImageProcessing(details=str(e), show=True, language="en")
        return(None)

def enhance(fl_input, fl_output):
    print("Start -> imageProcessing::enhance(" + fl_input + "," + fl_output + ")")

    try:
        # Load input image, and create the output file name.
        img_cv2_input = imread(fl_input)

        # Split RGB channels into single channels.
        b,g,r = cv2.split(img_cv2_input)

        # Define the histogram normalization algorithm
        # CLAHE (Contrast Limited Adaptive Histogram Equalization).
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

        # Apply the histogram normalization algorithm to each channel.
        norm_b = clahe.apply(b)
        norm_r = clahe.apply(r)
        norm_g = clahe.apply(g)

        # Merge single channels into one image.
        img_cv2_output = cv2.merge((norm_b,norm_g,norm_r))

        # Save the result.
        imwrite(fl_output, img_cv2_output)

        # Return the output file name.
        return(fl_output)
    except Exception as e:
        print("Error occured in imageProcessing::enhance(fl_input)")
        print((str(e)))
        error.ErrorMessageImageProcessing(details=str(e), show=True, language="en")
        return(None)
    finally:
        print("End -> imageProcessing::enhance")

def makeMono(fl_input, fl_output):
    print("imageProcessing::makeMono(fl_input, fl_output)")

    try:
        # Load input image, and create the output file name.
        img_cv2_input = imread(fl_input)

        # Convert color image to gray scale image.
        gry_cv2_img = cv2.cvtColor(img_cv2_input, cv2.COLOR_BGR2GRAY)

        # Save the result.
        imwrite(fl_output, gry_cv2_img)

        # Return the output file name.
        return(fl_output)
    except Exception as e:
        print("Error occured in imageProcessing::makeMono(fl_input, fl_output)")
        print((str(e)))
        error.ErrorMessageImageProcessing(details=str(e), show=True, language="en")
        return(None)

def negaToPosi(fl_input, fl_output):
    print("imageProcessing::negaToPosi(fl_input, fl_output)")

    try:
        # Load input image, and create the output file name.
        img_cv2_input = imread(fl_input)

        # Split RGB channels into single channels.
        b,g,r = cv2.split(img_cv2_input)

        # Invert color in each channel.
        conv_b = 255 - b
        conv_g = 255 - g
        conv_r = 255 - r

        # Merge single channels into one image.
        img_cv2_output = cv2.merge((conv_b, conv_g, conv_r))

        # Save the result.
        imwrite(fl_output, img_cv2_output)

        # Return the output file name.
        return(fl_output)
    except Exception as e:
        print("Error occured in imageProcessing::negaToPosi(fl_input, fl_output)")
        print((str(e)))
        error.ErrorMessageImageProcessing(details=str(e), show=True, language="en")
        return(None)

def extractInnerFrame(fl_input, fl_output, ratio):
    print("imageProcessing::extractInnerFrame(in_file fl_output, ratio)")

    try:
        # Load input image, and create the output file name.
        org_img = imread(fl_input)

        # Shrink the image for extracting contour.
        h, w = org_img.shape[:2]
        img_cv2_resize = cv2.resize(org_img,(int(w * ratio), int(h * ratio)), interpolation=cv2.INTER_CUBIC)

        # Convert the image to grayscale and make it blur.
        img_cv2_gray = cv2.cvtColor(img_cv2_resize, cv2.COLOR_BGR2GRAY)
        img_cv2_gray = cv2.GaussianBlur(img_cv2_gray, (7, 7), 0)

        # Detect the edge.
        img_cv2_edged = cv2.Canny(img_cv2_gray, 50, 100)

        # Perform dilation and erosion.
        img_cv2_edged = cv2.dilate(img_cv2_edged, None, iterations=1)
        img_cv2_edged = cv2.erode(img_cv2_edged, None, iterations=1)

        # Find contours in the edge map.
        img_cv2_cnts = cv2.findContours(img_cv2_edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        img_cv2_cnts = img_cv2_cnts[0] if imutils.is_cv2() else img_cv2_cnts[1]

        # Get the largest contour.
        cnts_areas = list()
        for c in img_cv2_cnts:
            cnts_areas.append(cv2.contourArea(c))

        # Exstract the biggest area.
        rect_index = cnts_areas.index(max(cnts_areas))
        cnt = img_cv2_cnts[rect_index]

        # Get the bounding rectangle for the largest rectangle.
        x,y,w,h = cv2.boundingRect(cnt)

        # Rescale to apply the crop area to original image.
        x = int(x / ratio)
        y = int(y / ratio)
        w = int(w / ratio)
        h = int(h / ratio)

        # Finally extract interior of the original image and save it.
        img_cv2_crop = org_img[y:(y+h),x:(x+w)]
        imwrite(fl_output, img_cv2_crop)

        # Returns saved file path.
        return(fl_output)
    except Exception as e:
        print("Error occured in imageProcessing::extractInnerFrame(in_file fl_output, ratio)")
        print((str(e)))
        error.ErrorMessageImageProcessing(details=str(e), show=True, language="en")
        return(None)

def correctRotaion(fl_input):
    print("Start -> imageProcessing::correctRotaion(fl_input)")

    try:
        # Get the metadata infomation.
        tags = getMetaInfo(fl_input)

        # Get the information about the rotation.
        if not len(tags) == 0:
            # Open the image as a PIL object.
            img = Image.open(fl_input)
            if "exif" in img.info:
                # Get the exif object and load them.
                exif_dict = piexif.load(img.info["exif"])

                if piexif.ImageIFD.Orientation in exif_dict["0th"]:
                    # Get the orientation property.
                    orientation = exif_dict["0th"].pop(piexif.ImageIFD.Orientation)

                    # Modify the bug(or error??) to work correctly.
                    exif_dict['Exif'][41729] = b'1'

                    # Rewrite the exif information to "No rotation".
                    exif_dict['0th'][piexif.ImageIFD.Orientation] = 1

                    # Dump the exif tags to update.
                    exif_bytes = piexif.dump(exif_dict)

                    # Rotate image to match with EXIF information.
                    if orientation == 2:
                        img = img.transpose(Image.FLIP_LEFT_RIGHT)
                    elif orientation == 3:
                        img = img.rotate(180)
                    elif orientation == 4:
                        img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
                    elif orientation == 5:
                        img = img.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
                    elif orientation == 6:
                        img = img.rotate(-90, expand=True)
                    elif orientation == 7:
                        img = img.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
                    elif orientation == 8:
                        img = img.rotate(90, expand=True)

                    # Rewrite the image with the new image file.
                    img.save(fl_input, exif=exif_bytes)
        else:
            print("### There are no exif information.")

    except Exception as e:
        print("Error occured in imageProcessing::correctRotaion(in_file)")
        print((str(e)))
        error.ErrorMessageImageProcessing(details=str(e), show=True, language="en")
        return(None)

    finally:
        print("End -> imageProcessing::correctRotaion(fl_input)")

def rotation(fl_input, fl_output, angle):
    print("imageProcessing::rotation(fl_input, fl_output, angle)")
    # Load input image, and create the output file name.

    try:
        img_cv2_input = imread(fl_input)

        # grab the dimensions of the image and then determine the center
        (w, h) = img_cv2_input.shape[1::-1]
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
        img_cv2_rot = cv2.warpAffine(img_cv2_input, M, dsize=(nW, nH))

        # Save the result.
        imwrite(fl_output, img_cv2_rot)

        # Return the output file name.
        return(fl_output)
    except Exception as e:
        print("Error occured in imageProcessing::rotation(in_file, fl_output, angle)")
        print((str(e)))
        error.ErrorMessageImageProcessing(details=str(e), show=True, language="en")
        return(None)

def makeThumbnail(fl_input, fl_output, basewidth):
    print("imageProcessing::makeThumbnail(fl_input, output, basewidth)")

    try:
        img = Image.open(fl_input).convert("RGB")
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
        new.save(fl_output)

        # Return the output file name.
        return(fl_output)
    except Exception as e:
        print("Error occured in mageProcessing::makeThumbnail(fl_input, output, basewidth)")
        print((str(e)))
        error.ErrorMessageImageProcessing(details=str(e), show=True, language="en")
        return(None)

def autoWhiteBalance(fl_input, fl_output, method = "automatic"):
    print("imageProcessing::autoWhiteBalance(fl_input, fl_output, method = 'automatic'")

    try:
        # Open the image object to be adjusted.
        img_pil_input = Image.open(fl_input)

        # Define the empty image object.
        img_pil_adj = None

        if method == "stretch": img_pil_adj = to_pil(cca.stretch(from_pil(img_pil_input)))
        elif method == "gray_world": img_pil_adj = to_pil(cca.gray_world(from_pil(img_pil_input)))
        elif method == "max_white": img_pil_adj = to_pil(cca.max_white(from_pil(img_pil_input)))
        elif method == "retinex": img_pil_adj = to_pil(cca.cca.retinex(from_pil(img_pil_input)))
        elif method == "retinex_adjusted": img_pil_adj = to_pil(cca.retinex_with_adjust(from_pil(img_pil_input)))
        elif method == "stdev_luminance": img_pil_adj = to_pil(cca.standard_deviation_and_luminance_weighted_gray_world(from_pil(img_pil_input)))
        elif method == "stdev_grey_world": img_pil_adj = to_pil(cca.standard_deviation_weighted_grey_world(from_pil(img_pil_input)))
        elif method == "luminance_weighted": img_pil_adj = to_pil(cca.luminance_weighted_gray_world(from_pil(img_pil_input)))
        elif method == "automatic": img_pil_adj = to_pil(cca.automatic_color_equalization(from_pil(img_pil_input)))

        # Save the adjusted image.
        img_pil_adj.save(fl_output)

        # Return the output file name.
        return(fl_output)
    except Exception as e:
        print("Error occured in imageProcessing::autoWhiteBalance(fl_input, fl_output, method = 'automatic'")
        print((str(e)))
        error.ErrorMessageImageProcessing(details=str(e), show=True, language="en")
        return(None)

def pansharpen(thumbnail, fl_input, fl_output, method="ihsConvert"):
    print("imageProcessing::pansharpen(thumbnail, fl_input, fl_output, method='ihsConvert')")

    try:
        # Open the colorized image and the original image.
        img_pil_thm = Image.open(thumbnail)
        img_pil_input = Image.open(fl_input)

        # Rescale the colorized image to original image size.
        img_pil_col = img_pil_thm.resize(img_pil_input.size, Image.ANTIALIAS)

        # Define the empty image object to be converted.
        img_pil_output = None

        if method == "ihsConvert":
            # IHS conversion.
            img_pil_output = ihsConvert(img_pil_col, img_pil_input)
        elif method =="simpleMeanConvert":
            # Simple Mean conversion.
            img_pil_output = simpleMeanConvert(img_pil_col, img_pil_input)
        elif method == "broveyConvert":
            #BroveyConvert
            img_pil_output = broveyConvert(img_pil_col, img_pil_input)

        # Save the result
        img_pil_output.save(fl_output)

        # Return the output file name.
        return(fl_output)
    except Exception as e:
        print("Error occured in imageProcessing::pansharpen(thumbnail, fl_input, fl_output, method='ihs')")
        print((str(e)))
        error.ErrorMessageImageProcessing(details=str(e), show=True, language="en")
        return(None)

def normalize(npy_array):
    try:
        npy_array = npy_array.astype('float')

        for i in range(3):
            minval = npy_array[...,i].min()
            maxval = npy_array[...,i].max()
            if minval != maxval:
                npy_array[...,i] -= minval
                npy_array[...,i] *= (255.0/(maxval-minval))
        return npy_array
    except Exception as e:
        print("Error occured in imageProcessing::normalize(npy_array)")
        print((str(e)))
        error.ErrorMessageImageProcessing(details=str(e), show=True, language="en")
        return(None)

def broveyConvert(img_pil_input, height):
    print("broveyConvert(img, height)")
    # Red_out = Red_in / [(blue_in + green_in + red_in) * Pan]
    # Greem_out = green_in / [(blue_in + green_in + red_in) * Pan]
    # Blue_out = blue_in / [(blue_in + green_in + red_in) * Pan]

    try:
        # Split the colorized image into red, green and blue bands.
        img_pil_r, img_pil_g, img_pil_b=img_pil_input.split()
        height = height.convert("L")

        # Calculate Brovey convert values.
        img_pil_r_conv = ImageMath.eval("convert(int(((float(r)/(float(b)+float(g)+float(r)))*float(h))),'L')", img_pil_r, img_pil_g, img_pil_b, h=height)
        img_pil_g_conv = ImageMath.eval("convert(int(((float(g)/(float(b)+float(g)+float(r)))*float(h))),'L')", img_pil_r, img_pil_g, img_pil_b, h=height)
        img_pil_b_conv = ImageMath.eval("convert(int(((float(b)/(float(b)+float(g)+float(r)))*float(h))),'L')", img_pil_r, img_pil_g, img_pil_b, h=height)

        # Normalize the image
        img_pil_rgb = Image.merge("RGB",(img_pil_r_conv,img_pil_g_conv,img_pil_b_conv))
        rgb_npy_arr = numpy.array(img_pil_rgb)

        # Generate a RGB image.
        img_pil_output = Image.fromarray(normalize(rgb_npy_arr).astype('uint8'),'RGB')

        # Return converted image.
        return(img_pil_output)
    except Exception as e:
        print("Error occured in broveyConvert(img, height)")
        print((str(e)))
        error.ErrorMessageImageProcessing(details=str(e), show=True, language="en")
        return(None)

def simpleMeanConvert(img_pil_input, height):
    print("simpleMeanConvert(img, height)")
    # Red_out= 0.5 * (Red_in + Pan_in)
    # Green_out = 0.5 * (Green_in + Pan_in)
    # Blue_out= 0.5 * (Blue_in + Pan_in)

    try:
        # Split the colorized image into red, green and blue bands.
        img_pil_r, img_pil_g, img_pil_b=img_pil_input.split()
        height = height.convert("L")

        # Calculate simple mean values.
        img_pil_r_conv = ImageMath.eval("convert((r+h)/2),'L')", img_pil_r, height)
        img_pil_g_conv = ImageMath.eval("convert((g+h)/2),'L')", img_pil_g, height)
        img_pil_b_conv= ImageMath.eval("convert((b+h)/2),'L')", img_pil_b, height)

        # Generate a RGB image.
        img_pil_output = Image.merge("RGB",(img_pil_r_conv,img_pil_g_conv,img_pil_b_conv))

        # Return converted image.
        return(img_pil_output)
    except Exception as e:
        print("Error occured in simpleMeanConvert(img, height)")
        print((str(e)))
        error.ErrorMessageImageProcessing(details=str(e), show=True, language="en")
        return(None)

def ihsConvert(img_pil_input, values):
    print("ihsConvert(img_pil_input, values)")

    try:
        # Convert the original image into single band image.
        values = values.convert("L")

        # Split the colorized image into red, green and blue bands.
        img_pil_input_r, img_pil_input_g, img_pil_input_b = img_pil_input.split()

        # Initialize arrays for Hue, Saturation and Value.
        img_list_hue = []
        img_list_saturation = []
        img_list_value = []

        # Convert RGB to HSV, and swap the Value band with original image.
        for pix_org_red, pix_org_green, pix_org_blue, pix_new_value in zip(img_pil_input_r.getdata(),img_pil_input_g.getdata(),img_pil_input_b.getdata(),values.getdata()):
            # Convert RGB values to HSV values.
            pix_org_hue, pix_org_saturation, pix_org_value = colorsys.rgb_to_hsv(pix_org_red/255.,pix_org_green/255.,pix_org_blue/255.)

            # Append pixcel value to the list.
            img_list_hue.append(int(pix_org_hue * 255.))
            img_list_saturation.append(int(pix_org_saturation * 255.))
            img_list_value.append(pix_new_value)

        # Initialize arrays for new red, green and pix_org_blueue bands.
        img_list_red = []
        img_list_green = []
        img_list_pix_org_blueue = []

        # Convert HSV to RGB.
        for pix_org_hue, pix_org_saturation, pix_org_value in zip(img_list_hue,img_list_saturation,img_list_value):
            # Get HSV pixcel values.
            pix_new_r, pix_new_g, pix_new_b = colorsys.hsv_to_rgb(pix_org_hue / 255., pix_org_saturation / 255., pix_org_value/255.)

            img_list_red.append(int(pix_new_r * 255.))
            img_list_green.append(int(pix_new_g * 255.))
            img_list_pix_org_blueue.append(int(pix_new_b * 255.))

        # Rewrite the original pixels by new RGB values.
        img_pil_input_r.putdata(img_list_red)
        img_pil_input_g.putdata(img_list_green)
        img_pil_input_b.putdata(img_list_pix_org_blueue)

        # Return converted image.
        img_pil_output = Image.merge('RGB',(img_pil_input_r,img_pil_input_g,img_pil_input_b))

        # Return converted image.
        return(img_pil_output)
    except Exception as e:
        print("Error occured in ihsConvert(img, height)")
        print((str(e)))
        error.ErrorMessageImageProcessing(details=str(e), show=True, language="en")
        return(None)

def focusStack(img_file_list):
    stacker = FocusStacker()
    stucked = stacker.focus_stack(image_files=img_file_list)
    return(stucked)
