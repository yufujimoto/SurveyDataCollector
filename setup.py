# -*- coding: utf-8 -*-
from setuptools import setup, Extension
import sys
#sys.path.append('./src')
#sys.path.append('./test')
version = open('VERSION').read().strip()

setup(name='citmas-sdc',
      version=version,
      description="A digital archiving system",
      long_description=open('README').read(),
      classifiers=[],
      keywords=('digital-archive'),
      author='Yu Fujimoto',
      author_email='yu.fujimoto@geo-nara.net',
      license='GPL',
      packages=['citmas-sdc'],
      install_requires=["PyQt5","imutils","parse","argparse","uuid","lxml","pipes","Cython","pyqtgraph","cartopy","scipy","gphoto2","flickrapi","numpy","scipy","pillow","imutils","colorcorrect","rawKit","exifread","pexif","sounddevice","soundfile","pyqtgraph","cartopy"],
      )
