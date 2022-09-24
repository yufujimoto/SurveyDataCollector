====================================
# New Commands for Python 3 Series
====================================
sudo port install geos
sudo port install qt5-qtwebkit

# Install Homebrew to install important packages.
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Update repository.
brew update
brew upgrade

# Install tethering tools.
brew install gphoto2
brew install libgphoto2

# Install SqLite & Browser.
brew install sqlite
brew install sqliteodbc
brew install sqlitebrowser

# Install torch into home directory.
brew install libreadline-java

# Install essential libraries.
brew install cmake
brew install swig
brew install pkg-config

# Install image processing libraries.
brew install libjpeg
brew install libtiff
brew install jasper
brew install exiv2
brew install boost-python3

# Install OpenCV.
brew install opencv
brew install libopencv
#brew install python3-opencv

# Install OCR tools.
brew install tesseract
brew install tesseract-lang
brew install libleptonica

# Install barcode reader.
brew install ghostscript
brew install zbar

# Install & Upgrade python3 -m pip.
curl https://bootstrap.pypa.io/get-python3 -m pip.py -o get-python3 -m pip.py
python3 get-python3 -m pip.py
python3 -m pip install --upgrade python3 -m pip

# install pyqt5
python3 -m pip install PyQt5
python3 -m pip install PyQtWebEngine

# Install general libraries.
python3 -m pip install python-dateutil
python3 -m pip install screeninfo
python3 -m pip install numpy
python3 -m pip install scipy
python3 -m pip install parse
python3 -m pip install argparse
python3 -m pip install uuid
python3 -m pip install lxml
python3 -m pip install Cython

# Install Geography libraries.
python3 -m pip install pyqtgraph
python3 -m pip install cartopy
python3 -m pip install geopy
python3 -m pip install geocoder
python3 -m pip install geodaisy

# Install image processing libraries.
python3 -m pip install imutils
python3 -m pip install colorcorrect
python3 -m pip install pyexiv2
python3 -m pip install piexif
python3 -m pip install pillow
python3 -m pip install rawpy
python3 -m pip install imageio
python3 -m pip install imutils
python3 -m pip install colorcorrect
python3 -m pip install exifread

# Install Sound processing libraries.
python3 -m pip install sounddevice
python3 -m pip install soundfile

# Install OpenCV.
python3 -m pip install opencv-python
python3 -m pip install opencv-python-headless

# Install barcode tools.
python3 -m pip install pyqrcode
python3 -m pip install pypng
python3 -m pip install python_barcode
python3 -m pip install pyzbar

python3 -m pip install pytesseract

# Install tethering tools.
python3 -m pip install gphoto2
python3 -m pip install pysony

# Install Web tools.
python3 -m pip install flickrapi


#git clone https://github.com/torch/distro.git ~/torch --recursive
#(cd ~/torch; bash install-deps; ./install.sh)

# Install siggraph.
#git clone https://github.com/satoshiiizuka/siggraph2016_colorization.git ~/siggraph --recursive
#(cd ~/siggraph; ./download_model.sh)
