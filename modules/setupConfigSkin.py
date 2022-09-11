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
    print("Start -> setupConfigSkin::setConfigWindowButtonText(parent)")

    # try:
    if parent.language == "ja":
        # General Tab
        print("## General Tab...")
        parent.tab_conf_main.setTabText(parent.tab_conf_main.indexOf(parent.tab_general), "一般")

        parent.gbx_general.setTitle("テーマの設定")
        parent.lbl_thm_lang.setText("言語の設定")
        parent.lbl_thm_skin.setText("色の設定")

        parent.gbx_tool.setTitle("ツールの設定")
        parent.lbl_tool_awb.setText("ホワイトバランス")
        parent.lbl_tool_psp.setText("パンシャープン")

        parent.grp_textedit.setText("既定のエディタ")
        parent.lbl_exe_textedit.setText("テキストエディタ：")
        parent.tbx_exe_textedit.setText("gedit")

        parent.grp_net_proxy.setText("プロキシ設定")
        parent.rbtn_no_proxy.setText("プロキシを使用しない。")
        parent.rbtn_proxy.setText("HTTP Proxy")

        # Camera Tab
        print("## camera Tab...")
        parent.tab_conf_main.setTabText(parent.tab_conf_main.indexOf(parent.tab_camera), "カメラ接続")
        parent.btn_cam_conn.setText("接続")

        parent.lbl_cur_cam.setText("接続中：")
        parent.lbl_cur_cam_nam.setText("接続されていません")
        parent.lbl_cam_size.setText("画像サイズ")
        parent.lbl_cam_iso.setText("ISO感度")
        parent.lbl_cam_wht.setText("ホワイトバランス")
        parent.lbl_cam_exp.setText("露出補正")
        parent.lbl_cam_fval.setText("F値")
        parent.lbl_cam_qoi.setText("画質")
        parent.lbl_cam_fmod.setText("フォーカスモード")
        parent.lbl_cam_epg.setText("露出プログラム")
        parent.lbl_cam_cpt.setText("撮影モード")
        parent.lbl_cam_met.setText("測光モード")

        # Tool Tab
        print("## tool Tab...")
        parent.grp_ocr.setText("Tesseract OCR")
        parent.lbl_ocr_psm.setText("テキスト認識モード：")

        parent.grp_lang.setText("認識言語：")
        parent.lbl_ocr_lang_available.setText("利用可能な言語")
        parent.lbl_ocr_lang_use.setText("選択中の言語")

        print("## Other Tab...")
        parent.tab_conf_main.setTabText(parent.tab_conf_main.indexOf(parent.tab_thirdparty), "外部サービス")

        parent.gbx_geospatial.setTitle("地理情報")
        parent.lbl_map_tile.setText("マップタイル")

        parent.gbx_flickr.setTitle("flickrの設定")
        parent.lbl_flc_api.setText("APIキー")
        parent.lbl_flc_sec.setText("Secret")

    elif parent.language == "en":
        # General Tab
        print("## General Tab...")
        parent.tab_conf_main.setTabText(parent.tab_conf_main.indexOf(parent.tab_general), "General")

        parent.gbx_general.setTitle("Theme")
        parent.lbl_thm_lang.setText("Language")
        parent.lbl_skin.setText("Color")

        parent.gbx_tool.setTitle("Algorithm")
        parent.lbl_tool_awb.setText("White Balance")
        parent.lbl_tool_psp.setText("Pansharpen")

        parent.grp_textedit.setTitle("Default Editor:")
        parent.lbl_exe_textedit.setText("Text Editor:")
        parent.tbx_exe_textedit.setText("gedit")

        parent.grp_net_proxy.setTitle("Proxy Setting")
        parent.rbtn_no_proxy.setText("No Proxy")
        parent.rbtn_proxy.setText("HTTP Proxy")

        # Camera Tab
        print("## Camera Tab...")
        parent.tab_conf_main.setTabText(parent.tab_conf_main.indexOf(parent.tab_camera), "Camera")
        parent.btn_cam_conn.setText("Connect")

        parent.lbl_cur_cam.setText("Current Camera:")
        parent.lbl_cur_cam_nam.setText("No Camera selected...")
        parent.lbl_cam_size.setText("Image Size:")
        parent.lbl_cam_iso.setText("ISO Speed Rating:")
        parent.lbl_cam_wht.setText("White Balance:")
        parent.lbl_cam_exp.setText("Exposure Compensation:")
        parent.lbl_cam_fval.setText("F-Number:")
        parent.lbl_cam_qoi.setText("Image quality:")
        parent.lbl_cam_fmod.setText("Focus MOde:")
        parent.lbl_cam_epg.setText("Exposure Program:")
        parent.lbl_cam_cpt.setText("Capture Mode:")
        parent.lbl_cam_met.setText("Metering MOde:")

        # Tool Tab
        print("## Tool Tab...")
        parent.tab_conf_main.setTabText(parent.tab_conf_main.indexOf(parent.tab_applications), "Application")
        parent.grp_ocr.setTitle("Tesseract-OCR:")
        parent.lbl_ocr_psm.setText("Page Segmentation Mode:")

        parent.grp_lang.setTitle("Languages:")
        parent.lbl_ocr_lang_available.setText("Available Languages:")
        parent.lbl_ocr_lang_use.setText("Selected Languages:")

        # Geography Tab
        print("## Other Tab...")
        parent.tab_conf_main.setTabText(parent.tab_conf_main.indexOf(parent.tab_thirdparty), "Network")
        parent.gbx_geospatial.setTitle("Geospatial")
        parent.lbl_map_tile.setText("map tile")

        parent.gbx_flickr.setTitle("flickr")
        parent.lbl_flc_api.setText("API Key")
        parent.lbl_flc_sec.setText("Secret")
    # except Exception as e:
    #     print((e.args[0]))

def setConfigWindowIcons(parent, icon_path):
    print("setupConfigSkin::setConfigWindowIcons(parent, icon_path)")
    icon_size = getIconSize()
    qicon_size = QSize(icon_size, icon_size)

    parent.tab_conf_main.setTabIcon(0, getIconFromPath(os.path.join(icon_path, 'apps.png')))
    parent.tab_conf_main.setTabIcon(1, getIconFromPath(os.path.join(icon_path, 'camera_sync.png')))
    parent.tab_conf_main.setTabIcon(2, getIconFromPath(os.path.join(icon_path, 'ocr.png')))
    parent.tab_conf_main.setTabIcon(3, getIconFromPath(os.path.join(icon_path, 'plugin.png')))
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
        border_color = 'border-color: #4C4C4C;'
        border_style = 'border-style: none; border-color: #4C4C4C;'
        font_style_color = 'color: #FFFFFF;'
        font_style = font_style_color + font_style_size

        # Set the default skin for all components.
        parent.frm_conf_btns.setStyleSheet(back_color + font_style + border_color)

        # Set the default skin for tabs.
        back_color_tab = 'QTabBar::tab {background-color: #2C2C2C; }'
        back_color_tab_act = 'QTabBar::tab::selected {background-color: #4C4C4C;}'
        parent.tab_conf_main.setStyleSheet(back_color_tab + back_color_tab_act)

        # Set the default skin for all components.
        parent.setStyleSheet(back_color + font_style + border_style)
        parent.frm_conf_btns.setStyleSheet(back_color + font_style + border_style)
        parent.frm_conf_main.setStyleSheet(back_color + font_style + border_style)

        # Set the default skin for tabs.
        back_color_tab = 'QTabBar::tab {background-color: #2C2C2C; }'
        back_color_tab_act = 'QTabBar::tab::selected {background-color: #4C4C4C;}'
        parent.tab_general.setStyleSheet(back_color_tab + back_color_tab_act)
        parent.tab_camera.setStyleSheet(back_color_tab + back_color_tab_act)

        # Set the default skin for text boxes.
        text_border = 'border-style: none; border-width: 0.5px; border-color: #4C4C4C;'
        text_background = "background-color: #6C6C6C;"

        parent.tre_cam.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.lst_lang_available.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.lst_lang_selected.setStyleSheet(font_style_color + font_style_size + text_border + text_background)

        parent.gbx_general.setStyleSheet(border_color)

        parent.cbx_thm_lang.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.cbx_skin.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.cbx_tool_awb.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.cbx_tool_psp.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.cbx_psm.setStyleSheet(font_style_color + font_style_size + text_border + text_background)

        parent.txt_flc_api.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.txt_flc_sec.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.tbx_exe_textedit.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.tbx_exe_textedit.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.txt_proxy.setStyleSheet(font_style_color + font_style_size + text_border + text_background)

        parent.cbx_map_tile.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
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
