# Summary
 This tethered shooting system provides various kinds of digital archiving tasks: Taking photo, recording and database managing.
 In addion to these tasks, this system provides other extra tools for simplified image processing, optical character recognition,
 exporting data. These functions are implemented by thanks to open source software and/or libraries listed below.
 The database schema of this system is comforming to ISO 19109, which is the international standard based on the idea of Object
 Oriented GIS (OOGIS). This standard is complecated, and it is not easy to understand and/or implement as a independent system.
 Because of this reason, The author of this system previously proposed "The Simple Object Profile (SOP)", which is simple and
 versatile implementation of the ISO 19109. This system implements the SOP on the one hand. 

# This tethered shooting system requires following softwares. These are easily installed by the "apt-get" command.
    + gphoto2       : The open source software, which provides tethered shooting function on this system.
    + dcraw         : The open source software handling RAW images on this system.
    + tesseract-ocr : The open source library of the Optical Character Recognition(OCR).
    + gimp          : The open source photo retouch software providing advanced image editing.
    + rawtherapee   : The open source RAW image processing software.
    + Sqlite        : The open source light weight DataBase Management System.

# In addition to above softwares, this system requires python libraries as below:
 [GUI libraries]
    + PyQt5
    
 [Generic libraries]
    + sys, stat, os, shutil, subprocess, pipes, getopt,
      argparse, optparse, uuid, time, math, tempfile, logging,

 [DataBase Management System libraries]
    + sqlite3

 [Image processing libraries]
    + PIL, cv2, imutils, numpy, pyexiv2
    
 Most of these libraries can be installed by using "pip" or "easy_install" commands for python. But some libraries are not provided
 officially. These libraries should be installed from GitHub. 

 [Sound managing libraries] 
    + Queue, sounddevice, soundfile

