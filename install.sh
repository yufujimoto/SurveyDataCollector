# Update repository.
apt update

# Install essential libraries.
apt install python-pip 
apt install python-dev 
apt install build-essential 
apt install build-essential 
apt install pkg-config

# Install GUI libraries.
apt install python-pyqt5
apt install pyqt5-dev-tools
apt install python-pyexiv2

# Install tethering tools.
apt install gphoto2
apt install libgphoto2-dev

# Install external application software.
apt install gimp
apt install audacity
apt install dcraw

# Install image processing libraries.
apt install libjpeg8-dev
apt install libtiff5-dev 
apt install libjasper-dev 
apt install libavcodec-dev 
pat install libavformat-dev 
apt install libswscale-dev 
apt install libv4l-dev
apt install libxvidcore-dev 
apt install libx264-dev
apt install opencv-data 
apt install libopencv-dev 
apt install python-opencv

# Install SqLite & Browser.
apt install sqlite
apt install sqlitebrowser

# Upgrade pip.
pip2 install --upgrade pip 

pip2 install pillow
pip2 install sounddevice
pip2 install soundfile
pip2 install imutils
pip2 install argparse
pip2 install uuid
pip2 install numpy
pip2 install scipy
pip2 install gphoto2
pip2 install colorcorrect
pip2 install pipes
pip2 install lxml

# Install torch into home directory.
git clone https://github.com/torch/distro.git ~/torch --recursive
(cd ~/torch; bash install-deps; ./install.sh)



