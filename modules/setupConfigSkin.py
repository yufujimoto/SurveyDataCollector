#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Import general libraries.
import sys, os, subprocess

# Import PyQt5 libraries for generating the GUI application.
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

def getIconFromPath(file_path):
    print("setupConfigSkin::getIconFromPath(file_path)")
    return(QIcon(QPixmap(file_path)))

def getFontSize():
    print("setupConfigSkin::getFontSize()")
    
    # Get the screen size and setting up font size.
    screen_size = getScreenSize()
    font_size = 10
    
    if int(screen_size[0]) >= 1200:
        font_size = 10
    elif int(screen_size[0]) < 1200:
        font_size = 7
    return(font_size)

def getIconSize():
    print("setupConfigSkin::getIconSize()")
    
    # Get the screen size and setting up font size.
    screen_size = getScreenSize()
    icon_size = 24
    
    if int(screen_size[0]) >= 1200:
        icon_size = 24
    elif int(screen_size[0]) < 1200:
        icon_size = 14

    return(icon_size)

def getScreenSize():
    print("setupConfigSkin::getScreenSize()")
    
    pop = subprocess.Popen('xrandr | grep "\*"',shell=True, stdout=subprocess.PIPE)
    pop.wait()
    
    screen = pop.communicate()[0].decode("UTF-8").split()[0].split("x")
    return(screen)

def getImagePreviewSize():
    print("setupConfigSkin::getImagePreviewSize()")
    screen_size = getScreenSize()

    if int(screen_size[0]) >= 1200:
        return(300, 400)
    elif int(screen_size[0]) < 1200:
        return(200,150)

def setConfigWindowButtonText(parent):
    print("setupConfigSkin::setConfigWindowButtonText(parent)")
    
    if parent.language == "ja":
        # Main menue
        parent.tab_conf_main.setTabText(parent.tab_conf_main.indexOf(parent.tab_general), "一般")
        parent.tab_conf_main.setTabText(parent.tab_conf_main.indexOf(parent.tab_geoinfo), "地理情報")
        parent.tab_conf_main.setTabText(parent.tab_conf_main.indexOf(parent.tab_network), "ネットワーク")
        parent.tab_conf_main.setTabText(parent.tab_conf_main.indexOf(parent.tab_camera), "カメラ接続")
        
        
        parent.gbx_general.setTitle("テーマの設定")
        parent.gbx_tool.setTitle("ツールの設定")
        parent.gbx_geospatial.setTitle("地理情報")
        parent.gbx_flickr.setTitle("flickrの設定")
        
        parent.lbl_lang.setText("言語の設定")
        parent.lbl_skin.setText("色の設定")
        parent.lbl_map_tile.setText("マップタイル")
        parent.lbl_tool_awb.setText("ホワイトバランス")
        parent.lbl_tool_psp.setText("パンシャープン")
        
        parent.btn_cam_conn.setText("接続")
        
    elif parent.language == "en":
        # Main menue
        parent.tab_conf_main.setTabText(parent.tab_conf_main.indexOf(parent.tab_general), "General")
        parent.tab_conf_main.setTabText(parent.tab_conf_main.indexOf(parent.tab_geoinfo), "Geographic Information")
        parent.tab_conf_main.setTabText(parent.tab_conf_main.indexOf(parent.tab_network), "Network Settings")
        parent.tab_conf_main.setTabText(parent.tab_conf_main.indexOf(parent.tab_camera), "Camera Connection")
        
        parent.gbx_general.setTitle("Theme")
        parent.gbx_tool.setTitle("Algorithm")
        parent.gbx_geospatial.setTitle("Geospatial")
        parent.gbx_flickr.setTitle("flickr")
        
        parent.lbl_lang.setText("Language")
        parent.lbl_skin.setText("Color")
        parent.lbl_map_tile.setText("map tile")
        parent.lbl_tool_awb.setText("White Balance")
        parent.lbl_tool_psp.setText("Pansharpen")
        
        parent.btn_cam_conn.setText("Connect")

def setConfigWindowIcons(parent, icon_path):
    print("setupConfigSkin::setConfigWindowIcons(parent, icon_path)")
    icon_size = getIconSize()
    qicon_size = QSize(icon_size, icon_size)
        
    parent.tab_conf_main.setTabIcon(0, getIconFromPath(os.path.join(icon_path, 'apps.png')))
    parent.tab_conf_main.setTabIcon(1, getIconFromPath(os.path.join(icon_path, 'place.png')))
    parent.tab_conf_main.setTabIcon(2, getIconFromPath(os.path.join(icon_path, 'network.png')))
    parent.tab_conf_main.setTabIcon(3, getIconFromPath(os.path.join(icon_path, 'camera_sync.png')))
    
    # Set the skin and icon.
    parent.bbx_conf_res.buttons()[0].setIcon(getIconFromPath(os.path.join(icon_path, 'check.png')))
    parent.bbx_conf_res.buttons()[1].setIcon(getIconFromPath(os.path.join(icon_path, 'close.png')))

def applyConfigWindowSkin(parent, icon_directory, skin="grey"):
    print("setupConfigSkin::applyConfigWindowSkin(parent, icon_directory, skin='grey')")
    
    # Get the proper font size from the display size and set the font size.
    font_size = getFontSize()
    
    # Make the style sheet.
    font_style_size = 'font: regular ' + str(getFontSize()) + 'px;'
    
    # Define the font object for Qt.
    font = QFont()
    font.setPointSize(font_size)
    
    # Apply the font style.
    parent.setFont(font)
    parent.tab_conf_main.setFont(font)
    
    # Setup the skin for the dialog.
    if parent.skin == "grey":
        # Set the icon path.
        icon_path = os.path.join(icon_directory, "white")
        setConfigWindowIcons(parent, icon_path)
        
        # Set the default background and front color.
        back_color = 'background-color: #2C2C2C;'
        font_style_color = 'color: #FFFFFF;'
        font_style = font_style_color + font_style_size
        
        # Set the default skin for all components.
        parent.frm_conf_btns.setStyleSheet(back_color + font_style + 'border-color: #4C4C4C;')
        
        # Set the default skin for tabs.
        back_color_tab = 'QTabBar::tab {background-color: #2C2C2C; }'
        back_color_tab_act = 'QTabBar::tab::selected {background-color: #4C4C4C;}'
        parent.tab_conf_main.setStyleSheet(back_color_tab + back_color_tab_act)
        
        # Set the default skin for all components.
        parent.setStyleSheet(back_color + font_style + 'border-style: none; border-color: #4C4C4C;')
        parent.frm_conf_btns.setStyleSheet(back_color + font_style + 'border-style: none; border-color: #4C4C4C;')
        parent.frm_conf_main.setStyleSheet(back_color + font_style + 'border-style: none; border-color: #4C4C4C;')
        
        # Set the default skin for tabs.
        back_color_tab = 'QTabBar::tab {background-color: #2C2C2C; }'
        back_color_tab_act = 'QTabBar::tab::selected {background-color: #4C4C4C;}'
        parent.tab_general.setStyleSheet(back_color_tab + back_color_tab_act)
        parent.tab_camera.setStyleSheet(back_color_tab + back_color_tab_act)
        
        # Set the default skin for text boxes.
        text_border = 'border-style: none; border-width: 0.5px; border-color: #4C4C4C;'
        text_background = "background-color: #6C6C6C;"
        
        parent.cbx_lang.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.cbx_skin.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.cbx_tool_awb.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.cbx_tool_psp.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        
        parent.txt_flc_api.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.txt_flc_sec.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        
        parent.cbx_map_tile.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.txt_proxy.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        
        parent.cbx_cam_size.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.cbx_cam_iso.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.cbx_cam_wht.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.cbx_cam_exp.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.cbx_cam_fval.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.cbx_cam_qoi.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.cbx_cam_fmod.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.cbx_cam_epg.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.cbx_cam_cpt.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.cbx_cam_met.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        
    elif skin == "white":
        icon_path = os.path.join(icon_path, "black")
        setConfigWindowIcons(parent, icon_path)

    

