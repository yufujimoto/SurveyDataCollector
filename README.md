# Summary
 The Survey Data Collector (SDC) is a digital archiving system for various kinds of cultural and/or natural assets. This system based on the “Simple Object Profile”, which is a well structured information management model in comforming to ISO 19100 series, the International Standards for Geographic Information System (GIS).

# Requirements
The SDC is developed by Python. It means SDC would be run on Windows and Mac platform. However, in some essential function of tethered shooting and colorlization wouldn't work on Windows and Mac. These problems will be improved in the future update. In current situations, Linux is strongly recommended.
The SDC requires following softwares. These are easily installed by the "apt" command.

    + gphoto2       : The open source software under GPL, which provides tethered shooting function on this system.
    + Sqlite        : The open source light weight DataBase Management System.

In addition to above softwares, this system requires python libraries as below:

## GUI libraries

    + PyQt5
    + Queue
    + pyqtgraph

## Generic libraries

    + os
    + sys
    + gc
    + stat
    + mimetypes
    + tempfile
    + shutil
    + subprocess
    + pipes
    + getopt
    + argparse
    + optparse
    + operator
    + uuid
    + math
    + logging
    + xml
    + lxml

## Temporal data handling libraries

    + time
    + datetime
    + dateutil

## DataBase Management System libraries

    + sqlite3

## Sound libraries

    + sounddevice
    + soundfile

## Image processing libraries

    + PIL
    + cv2
    + numpy
    + six
    + gphoto2
    + rawkit
    + imutils
    + colorcorrect
    + colorsys
    + pyexiv2
    + pexif
    + exifread

## Sound managing libraries

    + sounddevice
    + soundfile

## Additional Libraries

    + cartopy
    + flickrapi

 Most of these libraries can be installed by using "pip" or "easy_install" commands for python. But some libraries are not provided
 officially. These libraries should be installed from GitHub. 

# Reccomendations
The SDC dynamically linked to other softwares so that users can edit precisely with specific softwares. Representative softwares are listed below. SDC would work even though you wouldn't install these softwares.

    + dcraw         : The open source software handling RAW images on this system.
    + gimp          : The open source photo retouch software under GPL Ver.3 providing advanced image editing.

# General Functions
## Image Processing Tools

    + Rotation           : A generic function.
    + Automatic Cropping : A contour function provided by OpenCV. The function automalicaly remove mergines.
    + Auto Enhancing     : A CLAHE (Contrast Limited Adaptive Histogram Equalization) Algolithm provided by OpenCV.
    + Auto White Balance : A generic function provided by OpenCV.
    + Color Inversion    : In each RGB channel, the value is converted to 255-R, 255-G and 255-B.
    + Greyscaling        : A generic function provided by OpenCV.
    + Auto Colorizing    : An automatic colorization of grayscale images package "SIGGRAPH", which is developed by Dr.Satoshi Iizuka is used. Please refer to http://hi.cs.waseda.ac.jp/~iizuka/projects/colorization/ for the detail.
    + Open with GIMP     : You can edit each image by GIMP if you want. 
