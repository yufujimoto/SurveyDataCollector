# Summary
 This tethered shooting system provides various kinds of digital archiving tasks: Taking photo, recording and database managing.
 In addion to these tasks, this system provides other extra tools for simplified image processing, optical character recognition,
 exporting data. These functions are implemented by thanks to open source software and/or libraries listed below.
 The database schema of this system is comforming to ISO 19109, which is the international standard based on the idea of Object
 Oriented GIS (OOGIS). This standard is complecated, and it is not easy to understand and/or implement as a independent system.
 Because of this reason, The author of this system previously proposed "The Simple Object Profile (SOP)", which is simple and
 versatile implementation of the ISO 19109. This system implements the SOP on the one hand. 

# Requirements
This tethered shooting system requires following softwares. These are easily installed by the "apt-get" command.

    + gphoto2       : The open source software under GPL, which provides tethered shooting function on this system.
    + dcraw         : The open source software handling RAW images on this system.
    + gimp          : The open source photo retouch software under GPL providing advanced image editing.
    + rawtherapee   : The open source RAW image processing software.
    + Sqlite        : The open source light weight DataBase Management System.

In addition to above softwares, this system requires python libraries as below:

 [GUI libraries]
    + PyQt5
    + Queue
    + pyqtgraph

 [Generic libraries]
    + sys, stat, os, shutil, subprocess, pipes, getopt, xml, operator, math, getopt
      argparse, optparse, uuid, time, math, tempfile, logging, mimetypes, lxml, datetime, dateutil

 [DataBase Management System libraries]
    + sqlite3

 [Sound libraries]
    + sounddevice, soundfile

 [Image processing libraries]
    + gphoto2, PIL, cv2, imutils, numpy, pyexiv2, six, rawkit, pexif, exifread, colorcorrect, colorsys

 [Sound managing libraries] 
    + sounddevice, soundfile

 [Additional Libraries]
    +	cartopy
    +	flickrapi

 Most of these libraries can be installed by using "pip" or "easy_install" commands for python. But some libraries are not provided
 officially. These libraries should be installed from GitHub. 

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