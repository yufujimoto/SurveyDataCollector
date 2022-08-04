====================================
# New Commands for Python 3 Series
====================================
# Update repository.
add-apt-repository universe

apt update
apt upgrade

# Install & Upgrade pip.
apt install python3-pip
pip install --upgrade pip

#pip install pipes

# Install essential libraries. 
apt install cmake
apt install swig
apt install python3-dev 
apt install build-essential 
apt install pkg-config

# Install general libraries.
apt install python3-dateutil
pip install screeninfo
pip install numpy
pip install scipy
pip install parse
pip install argparse
pip install uuid
pip install lxml
pip install Cython

# Install GUI libraries.
apt install libqt5webkit5-dev
apt install libqt5multimedia5-plugins
apt install python3-pyqt5
apt install python3-pyqt5.qtwebkit
apt install python3-pyqt5.qtmultimedia
apt install pyqt5-dev-tools

# Install Geography libraries.
apt install libgeos-dev
apt install libproj-dev
pip install pyqtgraph
pip install cartopy
pip install geopy
pip install geocoder
pip install geodaisy

# Install image processing libraries.
apt install libjpeg8-dev
apt install libtiff5-dev 
apt install libjasper-dev 
apt install exiv2
apt install libexiv2-dev
apt install libboost-python-dev
pip install py3exiv2
pip install pillow
pip install rawpy
pip install imageio
pip install imutils
pip install colorcorrect
pip install exifread

# Install Sound processing libraries.
pip install sounddevice
pip install soundfile

# Install video processing libraries.
apt install libavcodec-dev 
apt install libavformat-dev
apt install libswscale-dev 
apt install libv4l-dev
apt install libxvidcore-dev 
apt install libx264-dev

# Install OpenCV.
apt install opencv-data 
apt install libopencv-dev 
apt install python3-opencv
pip install opencv-python-headless

# Install tethering tools.
apt install gphoto2
apt install libgphoto2-dev
pip install gphoto2
pip install pysony

# Install external application software.
apt install gimp
apt install audacity

# Install Web tools.
pip install flickrapi

# Install SqLite & Browser.
apt install sqlite
apt install sqlitebrowser























# Install torch into home directory.
apt-get install libreadline-dev 
apt install torch-trepl

git clone https://github.com/torch/distro.git ~/torch --recursive
(cd ~/torch; bash install-deps; ./install.sh)

# Install siggraph.
git clone https://github.com/satoshiiizuka/siggraph2016_colorization.git ~/siggraph --recursive
(cd ~/siggraph; ./download_model.sh)

