#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Import general libraries.
import sys, os, subprocess

# Import PyQt5 libraries for generating the GUI application.
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Import GIS libraries for showing geographic data.
import numpy as np
import pyqtgraph as pg
import cartopy.crs as ccrs

def activate(ui_main):
    # Add a splitter handle between project item tree and selected object.
    spl_main = QSplitter(Qt.Horizontal)
    spl_main.addWidget(ui_main.frm_left)
    spl_main.addWidget(ui_main.frm_right)
    ui_main.frm_main_lay.addWidget(spl_main)
    ui_main.setLayout(ui_main.frm_main_lay)
    
    # Add a splitter handle between the file list tree and preview screen.
    spl_fl = QSplitter(Qt.Horizontal)
    spl_fl.addWidget(ui_main.frm_fil_info_left)
    spl_fl.addWidget(ui_main.frm_fil_info_right)
    ui_main.frm_fil_info_lay.addWidget(spl_fl)
    ui_main.setLayout(ui_main.frm_fil_info_lay)
    
    # giving the plots names allows us to link their axes together
    ui_main.plt_geo = pg.PlotWidget(name='plt_geo') 
    ui_main.plt_geo.setAspectLocked(lock=True, ratio=1)
    ui_main.tab_src_geo_lay.addWidget(ui_main.plt_geo)
    
    # Activate actions on the menu bar.
    ui_main.bar_menu.setNativeMenuBar(False)
    ui_main.act_prj_open.triggered.connect(ui_main.getTheRootDirectory)
    ui_main.act_imp_csv_con.triggered.connect(ui_main.importConsolidationCSV)
    ui_main.act_imp_csv_mat.triggered.connect(ui_main.importMaterialCSV)
    ui_main.act_imp_csv_fil.triggered.connect(ui_main.importFileCSV)
    ui_main.act_exp_html.triggered.connect(ui_main.exportAsHtml)
    ui_main.act_exp_csv_con.triggered.connect(ui_main.exportConsolidationCSV)
    ui_main.act_exp_csv_mat.triggered.connect(ui_main.exportMaterialCSV)
    ui_main.act_exp_xml.triggered.connect(ui_main.exportAsXML)
    ui_main.act_exp_xml.triggered.connect(ui_main.exportAsXML)
    ui_main.act_reg_flickr.triggered.connect(ui_main.regFlickrKey)
    ui_main.act_exp_flickr.triggered.connect(ui_main.uploadToFlickr)
    
    ui_main.tre_prj_item.itemSelectionChanged.connect(ui_main.toggleCurrentTreeObject)    # Handle current selection of consolidations and materials.
    ui_main.tre_fls.itemSelectionChanged.connect(ui_main.toggleCurrentFile)               # Handle current selection of consolidations and materials.
    
    ui_main.tab_control.setCurrentIndex(0) # Initialyze the tab for source tree view and camera setting.
    ui_main.tab_target.setCurrentIndex(0)  # Initialyze the tab for the current object.
    ui_main.tab_src.setCurrentIndex(0)     # Initialyze the tab icons for source media tabs.
    
    ui_main.tab_target.currentChanged.connect(ui_main.toggleCurrentObjectTab)
    
    # Initialyze objects for consolidation
    ui_main.btn_con_add.clicked.connect(ui_main.addConsolidation)         # Activate the adding a consolidation button.
    ui_main.btn_con_update.clicked.connect(ui_main.updateConsolidation)   # Activate the updating the selected consolidation button.
    ui_main.btn_con_del.clicked.connect(ui_main.deleteConsolidation)      # Activate the deleting the selected consolidation button.
    ui_main.btn_con_take.clicked.connect(ui_main.tetheredShooting)        # Activate the taking a image of the consolidation button.
    ui_main.btn_con_imp.clicked.connect(ui_main.importExternalData)       # Activate the importing files of the consolidation button.
    ui_main.btn_con_rec.clicked.connect(ui_main.recordWithPhoto)          # Activate the opening recording dialog button.
    
    # Initialyze objects for materials
    ui_main.btn_mat_add.clicked.connect(ui_main.addMaterial)          # Activate the adding a material button.
    ui_main.btn_mat_update.clicked.connect(ui_main.updateMaterial)    # Activate the updating the selected material button.
    ui_main.btn_mat_del.clicked.connect(ui_main.deleteMaterial)       # Activate the consolidation delete button.
    ui_main.btn_mat_take.clicked.connect(ui_main.tetheredShooting)    # Activate the taking a image of the material button.
    ui_main.btn_mat_imp.clicked.connect(ui_main.importExternalData)   # Activate the importing files of the consolidation button.
    ui_main.btn_mat_rec.clicked.connect(ui_main.recordWithPhoto)      # Activate the opening recording dialog button.
    
    # Activate operation mode selecting button.
    ui_main.grp_con_ope = QButtonGroup()
    ui_main.grp_con_ope.addButton(ui_main.rad_con_new, 0)
    ui_main.grp_con_ope.addButton(ui_main.rad_con_mod, 1)
    ui_main.grp_con_ope.buttonClicked.connect(ui_main.toggleEditModeForConsolidation)
    
    # Activate selecting operation mode button.
    ui_main.grp_mat_ope = QButtonGroup()
    ui_main.grp_mat_ope.addButton(ui_main.rad_mat_new, 0)
    ui_main.grp_mat_ope.addButton(ui_main.rad_mat_mod, 1)
    ui_main.grp_mat_ope.buttonClicked.connect(ui_main.toggleEditModeForMaterial)
    
    # Initialyze the edit consolidation mode as modifying.
    ui_main.rad_con_mod.setChecked(True)
    ui_main.rad_mat_mod.setChecked(True)
    
    # Activate the check boxes for publishing mode.
    ui_main.cbx_fil_pub.setChecked(False)
    ui_main.cbx_fil_pub.clicked.connect(ui_main.updateFile)
    ui_main.cbx_fil_original.clicked.connect(ui_main.toggleShowFileMode)
    ui_main.cbx_fil_deleted.clicked.connect(ui_main.toggleShowFileMode)
    
    # Activate the image processing functions.
    ui_main.btn_open_gimp.clicked.connect(ui_main.openWithGimp)       # Activate the buttons for opening GIMP.
    ui_main.btn_img_cnt.clicked.connect(ui_main.extractContour)       # Activate the image proccessing tool button of cropping.
    ui_main.btn_img_inv.clicked.connect(ui_main.negativeToPositive)   # Activate the image processing tool button for inverting.
    ui_main.btn_img_del.clicked.connect(ui_main.deleteSelectedImage)  # Activate the image processing tool button for deleting.
    ui_main.btn_img_rot_r.clicked.connect(ui_main.rotateImageRight)   # Activate the image processing tool button for rotating clockwise.
    ui_main.btn_img_rot_l.clicked.connect(ui_main.rotateImageLeft)    # Activating the image processing tool button for rotating anti-clockwise.
    ui_main.btn_img_rot_u.clicked.connect(ui_main.rotateImageInvert)  # Activating the image processing tool button for ratating 180 degree.
    ui_main.btn_img_mno.clicked.connect(ui_main.makeMonoImage)        # Activating the image processing tool button for making monochrome image.
    ui_main.btn_img_enh.clicked.connect(ui_main.enhanceImage)         # Activating the image processing tool button for enhancing.
    ui_main.btn_img_sav.clicked.connect(ui_main.saveImageAs)          # Activating the image processing tool button for export the selected image.
    ui_main.btn_img_awb.clicked.connect(ui_main.adjustWhiteBalance)   # Activating the image processing tool button for adjusting image white balance.
    ui_main.btn_img_col.clicked.connect(ui_main.colorlize)            # Activating the image processing tool button for adjusting image white balance.
    
    # Activate the extra functions.
    ui_main.btn_fil_edit.clicked.connect(ui_main.editImageInformation) # Activate the editing the file informatin button.
    ui_main.btn_cam_detect.clicked.connect(ui_main.detectCamera)      # Activate detecting a connected camera button.
    ui_main.btn_snd_play.clicked.connect(ui_main.soundPlay)           # Activate the play button.