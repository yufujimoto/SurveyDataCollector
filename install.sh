# Update repository.
apt update
apt upgrade

# Upgrade pip.
apt install python-pip
pip2 install --upgrade pip

# Install essential libraries. 
apt install python-dev 
apt install build-essential 
apt install pkg-config

# Install general libraries.
apt install python-dateutil
pip2 install parse
pip2 install argparse
pip2 install uuid
pip2 install lxml
pip2 install pipes

# Install GUI libraries.
apt install python-pyqt5
apt install pyqt5-dev-tools

# Install tethering tools.
apt install gphoto2
apt install libgphoto2-dev
pip2 install gphoto2

# Install external application software.
apt install gimp
apt install audacity

# Install Web tools.
pip2 install flickrapi

# Install image processing libraries.
apt install libjpeg8-dev
apt install libtiff5-dev 
apt install libjasper-dev 
apt install python-pyexiv2
pip2 install numpy
pip2 install scipy
pip2 install pillow
pip2 install imutils
pip2 install colorcorrect
pip2 install rawKit
pip2 install exifread
pip2 install pexif

# Install Sound processing libraries.
apt install python-pyqt5.qtmultimedia
pip2 install sounddevice
pip2 install soundfile

# Install video processing libraries.
apt install libavcodec-dev 
pat install libavformat-dev
apt install libswscale-dev 
apt install libv4l-dev
apt install libxvidcore-dev 
apt install libx264-dev

# Install OpenCV.
apt install opencv-data 
apt install libopencv-dev 
apt install python-opencv

# Install SqLite & Browser.
apt install sqlite
apt install sqlitebrowser

# Install gis tools.
apt install libgeos-dev
apt install libproj-dev
pip2 install pyqtgraph
pip2 install cartopy

# Install torch into home directory.
git clone https://github.com/torch/distro.git ~/torch --recursive
(cd ~/torch; bash install-deps; ./install.sh)

# Install siggraph.
git clone https://github.com/satoshiiizuka/siggraph2016_colorization.git ~/siggraph --recursive
(cd ~/siggraph; ./download_model.sh)

