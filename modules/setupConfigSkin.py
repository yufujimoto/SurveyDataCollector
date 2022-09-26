#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Import general libraries.
import sys, os, subprocess

# Import general operations.
import modules.general as general

# Import PyQt5 libraries for generating the GUI application.
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

def setText(parent):
    print("## setupConfigSkin::setText(parent)")

    try:
        if parent.language == "ja":
            # General Tab
            print("### General Tab...")
            parent.tab_conf_main.setTabText(parent.tab_conf_main.indexOf(parent.tab_general), "一般")

            parent.gbx_general.setTitle("テーマの設定")
            parent.lbl_thm_lang.setText("言語の設定")
            parent.lbl_thm_skin.setText("色の設定")

            parent.gbx_tool.setTitle("ツールの設定")
            parent.lbl_tool_awb.setText("ホワイトバランス")
            parent.lbl_tool_psp.setText("パンシャープン")

            parent.grp_textedit.setTitle("既定のエディタ")
            parent.lbl_exe_textedit.setText("テキストエディタ：")
            parent.tbx_exe_textedit.setText("gedit")

            parent.grp_net_proxy.setTitle("プロキシ設定")
            parent.rbtn_no_proxy.setText("プロキシを使用しない。")
            parent.rbtn_proxy.setText("HTTP Proxy")

            # Camera Tab
            print("### camera Tab...")
            parent.tab_conf_main.setTabText(parent.tab_conf_main.indexOf(parent.tab_camera), "カメラ接続")
            parent.btn_cam_conn.setText("接続")
            parent.btn_cam_detect.setText("カメラの検出")

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
            print("### tool Tab...")
            parent.grp_ocr.setTitle("Tesseract-OCR:")
            parent.lbl_ocr_psm.setText("テキスト認識モード：")
            parent.cbx_psm.addItem("0:OSD（言語データ:osd.traineddata）のみ。文字方向と書字系の検出。言語判定・文字角度識別。")
            parent.cbx_psm.addItem("1:OSDありで自動ページセグメンテーション。")
            parent.cbx_psm.addItem("2:OSDなしで、OCRと自動ページセグメンテーション。")
            parent.cbx_psm.addItem("3:デフォルト設定。OSDなしで自動判断。")
            parent.cbx_psm.addItem("4:可変サイズのテキストと仮定して認識。")
            parent.cbx_psm.addItem("5:垂直テキストの単一ブロックと仮定。（縦書きの文字認識向け）")
            parent.cbx_psm.addItem("6:テキストの単一ブロックと仮定して認識。デフォルトの「3」よりも認識率が良い。（横書き向け？）")
            parent.cbx_psm.addItem("7:画像を1行の文字列として認識。")
            parent.cbx_psm.addItem("8:1単語として認識。")
            parent.cbx_psm.addItem("9:画像を丸の中の1単語として認識。")
            parent.cbx_psm.addItem("10:画像を1つの文字（一文字）として認識。")
            parent.cbx_psm.addItem("11:文字が散らばっているテキスト。")
            parent.cbx_psm.addItem("12:文字が散らばっているテキスト。OSD（言語データ:osd.traineddata）が必要。")
            parent.cbx_psm.addItem("13:Tesseract特有の処理を回避し、画像を1行のテキストとみなす。")

            parent.grp_ocr_lang.setTitle("認識言語：")
            parent.lbl_ocr_lang_available.setText("利用可能な言語")
            parent.lbl_ocr_lang_use.setText("選択中の言語")

            print("### Other Tab...")
            parent.tab_conf_main.setTabText(parent.tab_conf_main.indexOf(parent.tab_thirdparty), "外部サービス")

            parent.gbx_geospatial.setTitle("地理情報")
            parent.lbl_map_tile.setText("マップタイル")

            parent.gbx_flickr.setTitle("flickrの設定")
            parent.lbl_flc_api.setText("APIキー")
            parent.lbl_flc_sec.setText("Secret")

        elif parent.language == "en":
            # General Tab
            print("### General Tab...")
            parent.tab_conf_main.setTabText(parent.tab_conf_main.indexOf(parent.tab_general), "General")

            parent.gbx_general.setTitle("Theme")
            parent.lbl_thm_lang.setText("Language")
            parent.lbl_thm_skin.setText("Color")

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
            print("### Camera Tab...")
            parent.tab_conf_main.setTabText(parent.tab_conf_main.indexOf(parent.tab_camera), "Camera")
            parent.btn_cam_conn.setText("Connect")
            parent.btn_cam_detect.setText("Detect Cameras")

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
            print("### Tool Tab...")
            parent.tab_conf_main.setTabText(parent.tab_conf_main.indexOf(parent.tab_applications), "Application")
            parent.grp_ocr.setTitle("Tesseract-OCR:")
            parent.lbl_ocr_psm.setText("Page Segmentation Mode:")
            parent.cbx_psm.addItem("0:Orientation and script detection (OSD) only.")
            parent.cbx_psm.addItem("1:Automatic page segmentation with OSD. ")
            parent.cbx_psm.addItem("2:Automatic page segmentation, but no OSD, or OCR. ")
            parent.cbx_psm.addItem("3:Fully automatic page segmentation, but no OSD. (Default) ")
            parent.cbx_psm.addItem("4:Assume a single column of text of variable sizes. ")
            parent.cbx_psm.addItem("5:Assume a single uniform block of vertically aligned text. ")
            parent.cbx_psm.addItem("6:Assume a single uniform block of text. ")
            parent.cbx_psm.addItem("7:Treat the image as a single text line. ")
            parent.cbx_psm.addItem("8:Treat the image as a single word. ")
            parent.cbx_psm.addItem("9:Treat the image as a single word in a circle. ")
            parent.cbx_psm.addItem("10:Treat the image as a single character. ")
            parent.cbx_psm.addItem("11:Sparse text. Find as much text as possible in no particular order. ")
            parent.cbx_psm.addItem("12:Sparse text with OSD. ")
            parent.cbx_psm.addItem("13:Raw line. Treat the image as a single text line,bypassing hacks that are Tesseract specific.")

            parent.grp_ocr_lang.setTitle("Languages:")
            parent.lbl_ocr_lang_available.setText("Available Languages:")
            parent.lbl_ocr_lang_use.setText("Selected Languages:")

            # Geography Tab
            print("### Other Tab...")
            parent.tab_conf_main.setTabText(parent.tab_conf_main.indexOf(parent.tab_thirdparty), "Network")
            parent.gbx_geospatial.setTitle("Geospatial")
            parent.lbl_map_tile.setText("map tile")

            parent.gbx_flickr.setTitle("flickr")
            parent.lbl_flc_api.setText("API Key")
            parent.lbl_flc_sec.setText("Secret")
    except Exception as e:
        print("Error occured in setupConfigSkin::setText(parent)")
        print(str(e))
        error.ErrorMessageCameraDetection(details=str(e), show=True, language=self._language)
        return(None)

def setIcons(parent, icon_path):
    print("## setupConfigSkin::setIcons(parent, icon_path)")

    try:
        # Set the skin and icon.
        icon_size = general.getIconSize()
        qicon_size = QSize(icon_size, icon_size)

        parent.tab_conf_main.setTabIcon(0, general.getIconFromPath(os.path.join(icon_path, 'apps.png')))
        parent.tab_conf_main.setTabIcon(1, general.getIconFromPath(os.path.join(icon_path, 'camera_sync.png')))
        parent.tab_conf_main.setTabIcon(2, general.getIconFromPath(os.path.join(icon_path, 'ocr.png')))
        parent.tab_conf_main.setTabIcon(3, general.getIconFromPath(os.path.join(icon_path, 'plugin.png')))

        parent.btn_ocr_lang_off.setIcon(general.getIconFromPath(os.path.join(icon_path, 'to_left.png')))
        parent.btn_ocr_lang_off.setIconSize(qicon_size)

        parent.btn_ocr_lang_on.setIcon(general.getIconFromPath(os.path.join(icon_path, 'to_right.png')))
        parent.btn_ocr_lang_on.setIconSize(qicon_size)

        parent.btn_cam_conn.setIcon(general.getIconFromPath(os.path.join(icon_path, 'network.png')))
        parent.btn_cam_detect.setIcon(general.getIconFromPath(os.path.join(icon_path, 'camera_sync.png')))

        # Set the skin and icon.
        parent.bbx_conf_res.buttons()[0].setIcon(general.getIconFromPath(os.path.join(icon_path, 'check.png')))
        parent.bbx_conf_res.buttons()[1].setIcon(general.getIconFromPath(os.path.join(icon_path, 'close.png')))

        # Set Check box style
        check_on = "QCheckBox::indicator:unchecked {image: url(" + os.path.join(icon_path,"check_off_s.png") + ");}\n"
        check_off = "QCheckBox::indicator:checked {image: url(" + os.path.join(icon_path,"check_on_s.png") + ");}"
        parent.rbtn_no_proxy.setStyleSheet(check_off + check_on)
        parent.rbtn_proxy.setStyleSheet(check_off + check_on)

    except Exception as e:
        print("Error occured in setupConfigSkin::setIcons(parent, icon_path)")
        print(str(e))
        error.ErrorMessageCameraDetection(details=str(e), show=True, language=self._language)
        return(None)

def setSkin(parent, icon_directory, skin="grey"):
    print("## setupConfigSkin::setSkin(parent, icon_directory, skin='grey')")

    try:
        # Get the proper font size from the display size and set the font size.
        font_size = general.getFontSize()

        # Make the style sheet.
        font_style_size = 'font: regular ' + str(font_size) + 'px;'

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
            setIcons(parent, icon_path)

            # Set the default background and front color.
            back_color = 'background-color: #2C2C2C;'
            border_color = 'border-color: #4C4C4C;'
            border_style = 'border-style: none; border-color: #4C4C4C;'
            font_style_color = 'color: #FFFFFF;'
            font_style = font_style_color + font_style_size

            # Set the default skin for all components.
            parent.frm_conf_btns.setStyleSheet(back_color + font_style + border_color)

            # Set the default skin for tabs.
            back_color_tab = 'QTabBar::tab {background-color: #2C2C2C;}'
            back_color_tab_act = 'QTabBar::tab::selected {background-color: #4C4C4C;}'
            parent.tab_conf_main.setStyleSheet(back_color_tab + back_color_tab_act)

            # Set the default skin for all components.
            parent.setStyleSheet(back_color + font_style + border_style)
            parent.frm_conf_btns.setStyleSheet(back_color + font_style + border_style)
            parent.frm_conf_main.setStyleSheet(back_color + font_style + border_style)

            # Set the default skin for tabs.
            parent.tab_general.setStyleSheet(back_color_tab + back_color_tab_act)
            parent.tab_camera.setStyleSheet(back_color_tab + back_color_tab_act)

            # Set the default skin for text boxes.
            text_border = 'border-style: none; border-width: 0.5px; border-color: #4C4C4C;'
            text_background = "background-color: #6C6C6C;"

            parent.tre_cam.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.lst_lang_available.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.lst_lang_selected.setStyleSheet(font_style_color + font_style_size + text_border + text_background)

            # Set the default skin for groupbox.
            groupbox_border = "QGroupBox {border: 1px solid #4C4C4C;;}"
            parent.gbx_general.setStyleSheet(groupbox_border)
            parent.gbx_tool.setStyleSheet(groupbox_border)
            parent.grp_textedit.setStyleSheet(groupbox_border)
            parent.grp_net_proxy.setStyleSheet(groupbox_border)
            parent.grp_ocr.setStyleSheet(groupbox_border)
            parent.grp_ocr_lang.setStyleSheet(groupbox_border)
            parent.gbx_geospatial.setStyleSheet(groupbox_border)
            parent.gbx_flickr.setStyleSheet(groupbox_border)

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
            setIcons(parent, icon_path)

    except Exception as e:
        print("Error occured in setupConfigSkin::setSkin(parent, icon_directory, skin='grey')")
        print(str(e))
        error.ErrorMessageCameraDetection(details=str(e), show=True, language=self._language)
        return(None)
