#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Import general libraries.
import sys, os, subprocess
from screeninfo import get_monitors

# Import PyQt5 libraries for generating the GUI application.
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import modules.error as error

def getIconFromPath(file_path):
    try:
        return(QIcon(QPixmap(file_path)))
    except Exception as e:
        print("Error occured in getIconFromPath(file_path)")
        print(str(e))
        error.ErrorMessageUnknown(details=str(e), show=True, language="en")
        return(None)
    finally:
        print("# Get Icon from " + file_path +": setMainSkin::getIconFromPath")

def getFontSize():
    # Set the default value.
    font_size = 10

    # Get the screen size and setting up font size.
    try:
        screen_size = getScreenSize()

        if int(screen_size[0]) >= 1200:
            font_size = 10
        elif int(screen_size[0]) < 1200:
            font_size = 7

        return(font_size)
    except Exception as e:
        print("Error occured in getFontSize()")
        print(str(e))
        error.ErrorMessageUnknown(details=str(e), show=True, language="en")
        return(None)
    finally:
        print("# Font size is " + str(font_size) +". setMainSkin::getFontSize")

def getIconSize():
    try:
        # Get the screen size and setting up font size.
        screen_size = getScreenSize()
        icon_size = 24

        if int(screen_size[0]) >= 1200:
            icon_size = 24
        elif int(screen_size[0]) < 1200:
            icon_size = 14

        return(icon_size)
    except Exception as e:
        print("Error occured in getIconSize()")
        print(str(e))
        error.ErrorMessageUnknown(details=str(e), show=True, language="en")
        return(None)
    finally:
        print("# Icon size is " + str(icon_size) +". setMainSkin::getIconSize")

def getScreenSize(select=0):
    try:
        screen = []
        for m in get_monitors():
            screen.append(m)
        return(screen[0].width,screen[0].height)
    except Exception as e:
        print("Error occured in getScreenSize()")
        print(str(e))
        error.ErrorMessageUnknown(details=str(e), show=True, language="en")
        return(None)
    finally:
        print("# Screen size is " + str(screen[0].width) + "x" + str(screen[0].height) + ":setMainSkin::getScreenSize")

def getImagePreviewSize():
    print("setMainSkin::getImagePreviewSize()")

    try:
        screen_size = getScreenSize()
        if int(screen_size[0]) >= 1200:
            return(300, 400)
        elif int(screen_size[0]) < 1200:
            return(200,150)
    except Exception as e:
        print("Error occured in getImagePreviewSize()")
        print(str(e))
        error.ErrorMessageUnknown(details=str(e), show=True, language="en")
        return(None)

def setPlayingIcon(icon_path, btn_play, skin):
    print("setMainSkin::setPlayingIcon(icon_path, btn_play, skin)")

    try:
        icon_size = getIconSize()
        qicon_size = QSize(icon_size, icon_size)

        if skin == "grey":
            # Set the icon path.
            icon_path = os.path.join(icon_path, "white")
        elif skin == "white":
            icon_path = os.path.join(icon_path, "black")

        btn_play.setIcon(getIconFromPath(os.path.join(icon_path, 'playing.png')))
        btn_play.setIconSize(qicon_size)
    except Exception as e:
        print("Error occured in setPlayingIcon(icon_path, btn_stop, skin)")
        print(str(e))
        error.ErrorMessageUnknown(details=str(e), show=True, language="en")
        return(None)

def setStopButtonIcon(icon_path, btn_stop, skin):
    print("setMainSkin::setStopButtonIcon(icon_path, btn_play, skin)")

    try:
        icon_size = getIconSize()
        qicon_size = QSize(icon_size, icon_size)

        if skin == "grey":
            # Set the icon path.
            icon_path = os.path.join(icon_path, "white")
        elif skin == "white":
            icon_path = os.path.join(icon_path, "black")

        btn_stop.setIcon(getIconFromPath(os.path.join(icon_path, 'play.png')))
        btn_stop.setIconSize(qicon_size)
    except Exception as e:
        print("Error occured in setStopButtonIcon(icon_path, btn_stop, skin)")
        print(str(e))
        error.ErrorMessageUnknown(details=str(e), show=True, language="en")
        return(None)

def setPauseButtonIcon(icon_path, btn_pause, skin):
    print("setMainSkin::setPauseButtonIcon(icon_path, btn_pause, skin)")

    try:
        icon_size = getIconSize()
        qicon_size = QSize(icon_size, icon_size)

        if skin == "grey":
            # Set the icon path.
            icon_path = os.path.join(icon_path, "white")
        elif skin == "white":
            icon_path = os.path.join(icon_path, "black")

        btn_pause.setIcon(getIconFromPath(os.path.join(icon_path, 'pause.png')))
        btn_pause.setIconSize(qicon_size)
    except Exception as e:
        print("Error occured in setPauseButtonIcon(icon_path, btn_stop, skin)")
        print(str(e))
        error.ErrorMessageUnknown(details=str(e), show=True, language="en")
        return(None)

def setMainWindowButtonText(parent):
    try:
        if parent.language == "ja":
            # Main menue
            parent.men_prj.setTitle("プロジェクト")
            parent.men_prj_exp.setTitle("Export")
            parent.men_dat.setTitle("データ")
            parent.men_imp.setTitle("インポート")
            parent.men_imp_csv.setTitle("CSV File")
            parent.men_imp_xml.setTitle("XML File")
            parent.men_exp.setTitle("エクスポート")
            parent.men_exp_csv.setTitle("CSV File")
            parent.men_conf.setTitle("設定")
            parent.act_conf.setText("環境設定")
            parent.actionCreate_New_Project.setText("Create New Project")
            parent.actionOpen_Project.setText("Open Project")
            parent.act_prj_open.setText("開く")
            parent.act_prj_open.setShortcut("Ctrl+O")
            parent.act_prj_save.setText("設定の保存")
            parent.act_prj_save.setShortcut("Ctrl+S")
            parent.act_imp_db.setText("データベース")
            parent.act_imp_txt.setText("テキストデータ")
            parent.act_imp_fls.setText("ファイルシステム")
            parent.act_exp_html.setText("HTMLで出力")
            parent.act_imp_csv_con.setText("Consolidation")
            parent.act_imp_csv_mat.setText("Materials")
            parent.actionGML.setText("GML")
            parent.actionSOP.setText("SOP")
            parent.act_imp_gml.setText("GML")
            parent.act_imp_sop.setText("SOP")
            parent.act_exp_csv_con.setText("consolidation")
            parent.act_exp_csv_mat.setText("material")
            parent.act_imp_csv_fil.setText("File")
            parent.lbl_prjDir.setText("プロジェクト : ")
            parent.tre_prj_item.headerItem().setText(0, "UUID")
            parent.tre_prj_item.headerItem().setText(1, "名称")
            parent.tab_target.setTabText(parent.tab_target.indexOf(parent.tab_con), "統合体情報")
            parent.lbl_con_uuid.setText("UUID :")
            parent.btn_con_add.setText("統合体の追加")
            parent.btn_con_update.setText("統合体の更新")
            parent.btn_con_take.setText("撮影する")
            parent.btn_con_imp.setText(" インポートする")
            parent.btn_con_rec.setText("録音する")
            parent.btn_con_txt.setText("テキスト編集")
            parent.btn_con_del.setText("統合体の削除")
            parent.lbl_con_tempral.setText("時間識別子 :")
            parent.lbl_con_description.setText("統合体の備考 :")
            parent.lbl_con_name.setText("統合体の名称 :")
            parent.lbl_con_geoname.setText("地理識別子 :")
            parent.tab_target.setTabText(parent.tab_target.indexOf(parent.tab_mat), "資料情報")
            parent.lbl_mat_uuid.setText("UUID :")
            parent.lbl_mat_number.setText("資料番号 :")
            parent.lbl_mat_name.setText("資料の名称 :")
            parent.lbl_mat_geo_lat.setText("緯度 :")
            parent.lbl_mat_geo_lon.setText("経度 :")
            parent.lbl_mat_geo_alt.setText("標高 :")
            parent.lbl_mat_tmp_bgn.setText("開始時期 :")
            parent.lbl_mat_tmp_mid.setText("中間時期 :")
            parent.lbl_mat_tmp_end.setText("終了時期 :")
            parent.lbl_mat_description.setText("資料の備考 :")
            parent.btn_mat_add.setText("資料の追加")
            parent.btn_mat_update.setText("資料の更新")
            parent.btn_mat_take.setText("撮影する")
            parent.btn_mat_imp.setText(" インポートする")
            parent.btn_mat_rec.setText("録音する")
            parent.btn_mat_txt.setText("テキスト編集")
            parent.btn_mat_del.setText("資料の削除")
            parent.cbx_fil_deleted.setText("削除済みを表示")
            parent.cbx_fil_original.setText("オリジナルを表示")
            parent.tre_fls.headerItem().setText(0, "画像ID")
            parent.tre_fls.headerItem().setText(1, "名前")
            parent.tre_fls.headerItem().setText(2, "データタイプ")
            parent.cbx_fil_pub.setText("公開設定")
            parent.cbx_fil_edit.setText("削除可能")
            parent.tab_src.setTabText(parent.tab_src.indexOf(parent.tab_src_img), "画像")
            parent.tab_img_info.setTabText(parent.tab_img_info.indexOf(parent.tab_img_preview), "プレビュー")
            parent.tab_img_info.setTabText(parent.tab_img_info.indexOf(parent.tab_img_prop), "プロパティ")
            parent.tre_img_prop.headerItem().setText(0, "プロパティ")
            parent.tre_img_prop.headerItem().setText(1, "値")
            parent.tab_src.setTabText(parent.tab_src.indexOf(parent.tab_src_snd), "音声")
            parent.tab_src.setTabText(parent.tab_src.indexOf(parent.tab_src_txt), "テキスト")
            parent.tab_src.setTabText(parent.tab_src.indexOf(parent.tab_src_geo), "空間データ")
            parent.btn_geo_coding.setText("ジオコーディング")
            parent.btn_map_reload.setText("再読込")
        elif parent.language == "en":
            parent.men_prj.setTitle("Project")
            parent.men_prj_exp.setTitle("Export")
            parent.men_dat.setTitle("Data")
            parent.men_imp.setTitle("Import")
            parent.men_imp_csv.setTitle("CSV File")
            parent.men_imp_xml.setTitle("XML File")
            parent.men_exp.setTitle("Export")
            parent.men_exp_csv.setTitle("CSV File")
            parent.men_conf.setTitle("Configuration")
            parent.act_conf.setText("Preference")
            parent.actionCreate_New_Project.setText("Create New Project")
            parent.actionOpen_Project.setText("Open Project")
            parent.act_prj_open.setText("Open")
            parent.act_prj_open.setShortcut("Ctrl+O")
            parent.act_prj_save.setText("Save")
            parent.act_prj_save.setShortcut("Ctrl+S")
            parent.act_imp_db.setText("Database")
            parent.act_imp_txt.setText("Text ile")
            parent.act_imp_fls.setText("File system")
            parent.act_exp_html.setText("Export as HTML")
            parent.act_imp_csv_con.setText("Consolidation")
            parent.act_imp_csv_mat.setText("Materials")
            parent.actionGML.setText("GML")
            parent.actionSOP.setText("SOP")
            parent.act_imp_gml.setText("GML")
            parent.act_imp_sop.setText("SOP")
            parent.act_exp_csv_con.setText("consolidation")
            parent.act_exp_csv_mat.setText("material")
            parent.act_imp_csv_fil.setText("File")
            parent.lbl_prjDir.setText("Project : ")
            parent.tre_prj_item.headerItem().setText(0, "UUID")
            parent.tre_prj_item.headerItem().setText(1, "Name")
            parent.tab_target.setTabText(parent.tab_target.indexOf(parent.tab_con), "Consolidation")
            parent.lbl_con_uuid.setText("UUID :")
            parent.lbl_con_description.setText("Description :")
            parent.lbl_con_name.setText("Name :")
            parent.lbl_con_geoname.setText("Location:")
            parent.lbl_con_tempral.setText("Era/Age:")
            parent.btn_con_add.setText("New Consolidation")
            parent.btn_con_update.setText("Update")
            parent.btn_con_take.setText("Shoot")
            parent.btn_con_imp.setText("Import")
            parent.btn_con_rec.setText("Record")
            parent.btn_con_txt.setText("Text Edit")
            parent.btn_con_del.setText("Delete")
            parent.tab_target.setTabText(parent.tab_target.indexOf(parent.tab_mat), "Material")
            parent.lbl_mat_uuid.setText("UUID :")
            parent.lbl_mat_number.setText("Number :")
            parent.lbl_mat_name.setText("Name :")
            parent.lbl_mat_geo_lat.setText("Latitude :")
            parent.lbl_mat_geo_lon.setText("Longitude :")
            parent.lbl_mat_geo_alt.setText("Altitude :")
            parent.lbl_mat_tmp_bgn.setText("Begin :")
            parent.lbl_mat_tmp_mid.setText("Peak :")
            parent.lbl_mat_tmp_end.setText("End :")
            parent.lbl_mat_description.setText("Description :")
            parent.btn_mat_add.setText("New Material")
            parent.btn_mat_update.setText("Update")
            parent.btn_mat_take.setText("Shoot")
            parent.btn_mat_imp.setText("Import")
            parent.btn_mat_rec.setText("Record")
            parent.btn_mat_txt.setText("Text Edit")
            parent.btn_mat_del.setText("Delete")
            parent.cbx_fil_deleted.setText("Show removed files")
            parent.cbx_fil_original.setText("Show original files")
            parent.tre_fls.headerItem().setText(0, "Image ID")
            parent.tre_fls.headerItem().setText(1, "Name")
            parent.tre_fls.headerItem().setText(2, "Data Type")
            parent.cbx_fil_pub.setText("Make public")
            parent.cbx_fil_edit.setText("Removable")
            parent.tab_src.setTabText(parent.tab_src.indexOf(parent.tab_src_img), "Image")
            parent.tab_src.setTabText(parent.tab_src.indexOf(parent.tab_src_snd), "Sound")
            parent.tab_img_info.setTabText(parent.tab_img_info.indexOf(parent.tab_img_preview), "Preview")
            parent.tab_img_info.setTabText(parent.tab_img_info.indexOf(parent.tab_img_prop), "Property")
            parent.tre_img_prop.headerItem().setText(0, "Property")
            parent.tre_img_prop.headerItem().setText(1, "Value")
            parent.tab_src.setTabText(parent.tab_src.indexOf(parent.tab_src_txt), "Text")
            parent.tab_src.setTabText(parent.tab_src.indexOf(parent.tab_src_geo), "Spatial Data")
            parent.btn_geo_coding.setText("Geocoding")
            parent.btn_map_reload.setText("Reload")
    except Exception as e:
        print("Error occured in setMainWindowButtonText(parent)")
        print(str(e))
        error.ErrorMessageUnknown(details=str(e), show=True, language="en")
        return(None)

def setMainWindowToolTips(parent):
    try:
        if parent.language == "ja":
            parent.btn_open_gimp.setToolTip("選択したファイルをGIMPで開きます。")
            parent.btn_img_cnt.setToolTip("選択したファイルの画像領域を自動で抽出します。")
            parent.btn_img_inv.setToolTip("選択したファイルをネガティブ画像からポジティブ画像に変換します。")
            parent.btn_img_del.setToolTip("選択したファイルを削除します（データベースには残ります）。")
            parent.btn_img_rot_r.setToolTip("選択したファイルを右に回転します。")
            parent.btn_img_rot_l.setToolTip("選択したファイルを左に回転します。")
            parent.btn_img_rot_u.setToolTip("選択したファイルを180度回転します。")
            parent.btn_img_mno.setToolTip("選択したファイルをモノクロ画像に変換します。")
            parent.btn_img_enh.setToolTip("選択したファイルにヒストグラム平滑化処理を加えます")
            parent.btn_img_sav.setToolTip("選択したファイルを指定のファイル名で出力します。")
            parent.btn_img_awb.setToolTip("選択したファイルのホワイトバランスを自動で調整します。")
            parent.btn_img_col.setToolTip("選択したファイルをAIを使って彩色します。")
        if parent.language == "en":
            parent.btn_open_gimp.setToolTip("Open and edit the selected image with GIMP")
            parent.btn_img_cnt.setToolTip("Crop the image automatically.")
            parent.btn_img_inv.setToolTip("Invert the image negative to positive.")
            parent.btn_img_del.setToolTip("Delete the image (Do not delete from the Database file).")
            parent.btn_img_rot_r.setToolTip("Rotate the image right.")
            parent.btn_img_rot_l.setToolTip("Rotate the image left.")
            parent.btn_img_rot_u.setToolTip("Rotaet the image 180 degree.")
            parent.btn_img_mno.setToolTip("Convert the image color to monochrome.")
            parent.btn_img_enh.setToolTip("Normalize the color histogram.")
            parent.btn_img_sav.setToolTip("Export the image to file.")
            parent.btn_img_awb.setToolTip("Adjust white balance automatically.")
            parent.btn_img_col.setToolTip("Make color image from monochrome image by using deep learning.")
    except Exception as e:
        print("Error occured in setMainWindowToolTips(parent)")
        print(str(e))
        error.ErrorMessageUnknown(details=str(e), show=True, language="en")
        return(None)

def setMainWindowIcons(parent, icon_path):
    try:
        icon_size = getIconSize()
        qicon_size = QSize(icon_size, icon_size)

        parent.act_prj_open.setIcon(getIconFromPath(os.path.join(icon_path, 'folder_open.png')))

        parent.tab_target.setTabIcon(0, getIconFromPath(os.path.join(icon_path, 'apps.png')))
        parent.tab_target.setTabIcon(1, getIconFromPath(os.path.join(icon_path, 'insert_photo.png')))

        parent.tab_src.setTabIcon(0, getIconFromPath(os.path.join(icon_path, 'collections.png')))
        parent.tab_src.setTabIcon(1, getIconFromPath(os.path.join(icon_path, 'sounds.png')))
        parent.tab_src.setTabIcon(2, getIconFromPath(os.path.join(icon_path, 'create.png')))
        parent.tab_src.setTabIcon(3, getIconFromPath(os.path.join(icon_path, 'place.png')))

        parent.btn_con_add.setIcon(getIconFromPath(os.path.join(icon_path, 'add_box.png')))
        parent.btn_con_add.setIconSize(qicon_size)

        parent.btn_con_del.setIcon(getIconFromPath(os.path.join(icon_path, 'remove_box.png')))
        parent.btn_con_del.setIconSize(qicon_size)

        parent.btn_con_imp.setIcon(getIconFromPath(os.path.join(icon_path, 'file_download.png')))
        parent.btn_con_imp.setIconSize(qicon_size)

        parent.btn_con_txt.setIcon(getIconFromPath(os.path.join(icon_path, 'file.png')))
        parent.btn_con_txt.setIconSize(qicon_size)

        parent.btn_con_rec.setIcon(getIconFromPath(os.path.join(icon_path, 'voice_recorder.png')))
        parent.btn_con_rec.setIconSize(qicon_size)

        parent.btn_con_take.setIcon(getIconFromPath(os.path.join(icon_path, 'camera.png')))
        parent.btn_con_take.setIconSize(qicon_size)

        parent.btn_con_update.setIcon(getIconFromPath(os.path.join(icon_path, 'check_box.png')))
        parent.btn_con_update.setIconSize(qicon_size)

        parent.btn_mat_add.setIcon(getIconFromPath(os.path.join(icon_path, 'add_circle.png')))
        parent.btn_mat_add.setIconSize(qicon_size)

        parent.btn_mat_del.setIcon(getIconFromPath(os.path.join(icon_path, 'remove_circle.png')))
        parent.btn_mat_del.setIconSize(qicon_size)

        parent.btn_mat_imp.setIcon(getIconFromPath(os.path.join(icon_path, 'file_download.png')))
        parent.btn_mat_imp.setIconSize(qicon_size)

        parent.btn_mat_txt.setIcon(getIconFromPath(os.path.join(icon_path, 'file.png')))
        parent.btn_mat_txt.setIconSize(qicon_size)

        parent.btn_mat_rec.setIcon(getIconFromPath(os.path.join(icon_path, 'voice_recorder.png')))
        parent.btn_mat_rec.setIconSize(qicon_size)

        parent.btn_mat_take.setIcon(getIconFromPath(os.path.join(icon_path, 'camera.png')))
        parent.btn_mat_take.setIconSize(qicon_size)

        parent.btn_mat_update.setIcon(getIconFromPath(os.path.join(icon_path, 'check_circle.png')))
        parent.btn_mat_update.setIconSize(qicon_size)

        parent.btn_open_gimp.setIcon(getIconFromPath(os.path.join(icon_path, 'gimp-icon.png')))
        parent.btn_open_gimp.setIconSize(qicon_size)

        parent.btn_img_cnt.setIcon(getIconFromPath(os.path.join(icon_path, 'crop.png')))
        parent.btn_img_cnt.setIconSize(qicon_size)

        parent.btn_img_inv.setIcon(getIconFromPath(os.path.join(icon_path, 'invert.png')))
        parent.btn_img_inv.setIconSize(qicon_size)

        parent.btn_img_del.setIcon(getIconFromPath(os.path.join(icon_path, 'delete.png')))
        parent.btn_img_del.setIconSize(qicon_size)

        parent.btn_img_rot_r.setIcon(getIconFromPath(os.path.join(icon_path, 'rotate_right.png')))
        parent.btn_img_rot_r.setIconSize(qicon_size)

        parent.btn_img_rot_l.setIcon(getIconFromPath(os.path.join(icon_path, 'rotate_left.png')))
        parent.btn_img_rot_l.setIconSize(qicon_size)

        parent.btn_img_mno.setIcon(getIconFromPath(os.path.join(icon_path, 'monochrome.png')))
        parent.btn_img_mno.setIconSize(qicon_size)

        parent.btn_img_rot_u.setIcon(getIconFromPath(os.path.join(icon_path, 'sync.png')))
        parent.btn_img_rot_u.setIconSize(qicon_size)

        parent.btn_img_enh.setIcon(getIconFromPath(os.path.join(icon_path, 'photo_filter.png')))
        parent.btn_img_enh.setIconSize(qicon_size)

        parent.btn_fil_edit.setIcon(getIconFromPath(os.path.join(icon_path, 'create.png')))
        parent.btn_fil_edit.setIconSize(qicon_size)

        parent.btn_img_sav.setIcon(getIconFromPath(os.path.join(icon_path, 'move_to_inbox.png')))
        parent.btn_img_sav.setIconSize(qicon_size)

        parent.btn_img_awb.setIcon(getIconFromPath(os.path.join(icon_path, 'auto_white_balance.png')))
        parent.btn_img_awb.setIconSize(qicon_size)

        parent.btn_img_col.setIcon(getIconFromPath(os.path.join(icon_path, 'colorlize.png')))
        parent.btn_img_col.setIconSize(qicon_size)

        parent.mlt_btn_play.setIcon(getIconFromPath(os.path.join(icon_path, 'play.png')))
        parent.mlt_btn_play.setIconSize(qicon_size)

        parent.btn_geo_coding.setIcon(getIconFromPath(os.path.join(icon_path, 'location.png')))
        parent.btn_geo_coding.setIconSize(qicon_size)

        parent.btn_map_reload.setIcon(getIconFromPath(os.path.join(icon_path, 'sync.png')))
        parent.btn_map_reload.setIconSize(qicon_size)

        parent.btn_map_search.setIcon(getIconFromPath(os.path.join(icon_path, 'search.png')))
        parent.btn_map_search.setIconSize(qicon_size)
    except Exception as e:
        print("Error occured in setMainWindowIcons(parent, icon_path)")
        print(str(e))
        error.ErrorMessageUnknown(details=str(e), show=True, language="en")
        return(None)

def setDefaultConsolidationText(parent, status, skin="grey"):
    print("skin::setDefaultConsolidationText(parent, status, skin='grey')")

    try:
        font_style_size = "font: regular " + str(getFontSize()) + "px;"
        font_style_color = ""

        if skin == "grey":
            text_border = "border-style: outset; border-width: 0.5px; border-color: #4C4C4C;"
            text_background = "background-color: #6C6C6C;"

            if status == "new":
                font_style_color = "color: rgb(255, 0, 0);"
            elif status == "default":
                font_style_color = "color: #FFFFFF;"
        elif skin == "white":
            text_border = "border-style: outset; border-width: 0.5px; border-color: #4C4C4C;"
            text_background = ""

            if status == "new":
                font_style_color = "color: rgb(255, 0, 0);"
            elif status == "default":
                font_style_color = "color: #1A1A1A;"

        parent.tbx_con_uuid.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.tbx_con_name.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.tbx_con_geoname.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.tbx_con_temporal.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.tbx_con_description.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
    except Exception as e:
        print("Error occured in setDefaultConsolidationText(parent, status, skin='grey')")
        print(str(e))
        error.ErrorMessageUnknown(details=str(e), show=True, language="en")
        return(None)

def setDefaultMaterialText(parent, status, skin="grey"):
    try:
        font_style_size = "font: regular " + str(getFontSize()) + "px;"

        if skin == "grey":
            text_border = "border-style: outset; border-width: 0.5px; border-color: #4C4C4C;"
            text_background = "background-color: #6C6C6C;"

            if status == "new":
                font_style_color = "color: rgb(255, 0, 0);"
            elif status == "default":
                font_style_color = "color: #FFFFFF;"
        elif skin == "white":
            text_border = "border-style: outset; border-width: 0.5px; border-color: #4C4C4C;"
            text_background = ""

            if status == "new":
                font_style_color = "color: rgb(255, 0, 0);"
            elif status == "default":
                font_style_color = "color: #1A1A1A;"

        parent.tbx_mat_uuid.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.tbx_mat_number.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.tbx_mat_name.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.tbx_mat_geo_lat.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.tbx_mat_geo_lon.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.tbx_mat_geo_alt.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.tbx_mat_tmp_bgn.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.tbx_mat_tmp_mid.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.tbx_mat_tmp_end.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
        parent.tbx_mat_description.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
    except Exception as e:
        print("Error occured in setDefaultConsolidationText(parent, status, skin='grey')")
        print(str(e))
        error.ErrorMessageUnknown(details=str(e), show=True, language="en")
        return(None)

def setDefaultFileText(parent, status, skin="grey"):
    try:
        font_style_size = 'font: regular ' + str(getFontSize()) + 'px;'

        if skin == "grey":
            back_color_tree = 'QHeaderView::section {background-color: #2C2C2C;}'

            if status == "original":
                font_style_color = QBrush(QColor("#00FFFF"))
            elif status == "removed":
                font_style_color = QBrush(QColor("#FF0000"))
        elif skin == "white":
            if status == "original":
                font_style_color = QBrush(QColor("#0000FF"))
            elif status == "removed":
                font_style_color = QBrush(QColor("#FF0000"))

        parent.setForeground(0,font_style_color)
        parent.setForeground(1,font_style_color)
        parent.setForeground(2,font_style_color)
    except Exception as e:
        print(str(e))

def applyMainWindowSkin(parent, icon_path="", skin="grey"):
    try:

        # Get the proper font size from the display size and set the font size.
        font_size = getFontSize()

        # Make the style sheet.
        font_style_size = 'font: regular ' + str(getFontSize()) + 'px;'

        # Define the font object for Qt.
        font = QFont()
        font.setPointSize(font_size)

        # Apply the font style.
        parent.setFont(font)
        parent.bar_menu.setFont(font)
        parent.tab_target.setFont(font)
        parent.tab_src.setFont(font)
        parent.tab_img_info.setFont(font)
        parent.frm_fil_info.setFont(font)

        if skin == "grey":
            # Set the icon path.
            icon_path = os.path.join(icon_path, "white")
            setMainWindowIcons(parent, icon_path)

            # Set the default background and front color.
            back_color = 'background-color: #2C2C2C;'
            font_style_color = 'color: #FFFFFF;'
            font_style = font_style_color + font_style_size

            # Set the default skin for tree views.
            back_color_header = 'QHeaderView::section {background-color: #3C3C3C;}'
            parent.tre_prj_item.setStyleSheet(back_color_header)
            parent.tre_fls.setStyleSheet(back_color_header)
            parent.tre_img_prop.setStyleSheet(back_color_header)

            # Set the default skin for all components.
            parent.frm_main.setStyleSheet(back_color + font_style + 'border-color: #4C4C4C;')

            # Set the default skin for tabs.
            back_color_tab = 'QTabBar::tab {background-color: #2C2C2C; }'
            back_color_tab_act = 'QTabBar::tab::selected {background-color: #4C4C4C;}'
            parent.tab_target.setStyleSheet(back_color_tab + back_color_tab_act)
            parent.tab_img_info.setStyleSheet(back_color_tab + back_color_tab_act)
            parent.tab_src.setStyleSheet(back_color_tab + back_color_tab_act)
            parent.tab_target.setStyleSheet(back_color_tab + back_color_tab_act)

            # Set the default skin for text boxes.
            text_border = 'border-style: outset; border-width: 0.5px; border-color: #4C4C4C;'
            text_background = "background-color: #6C6C6C;"
            parent.tbx_con_uuid.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_con_name.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_con_geoname.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_con_temporal.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_con_description.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_mat_uuid.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_mat_number.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_mat_name.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_mat_geo_lat.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_mat_geo_lon.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_mat_geo_alt.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_mat_tmp_bgn.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_mat_tmp_mid.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_mat_tmp_end.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_mat_description.setStyleSheet(font_style_color + font_style_size + text_border + text_background)

            parent.tre_prj_item.headerItem().setForeground(0,QBrush(Qt.gray))
            parent.tre_prj_item.headerItem().setForeground(1,QBrush(Qt.gray))
            parent.tre_fls.headerItem().setForeground(0,QBrush(Qt.gray))
            parent.tre_fls.headerItem().setForeground(1,QBrush(Qt.gray))
            parent.tre_fls.headerItem().setForeground(2,QBrush(Qt.gray))

            # Set Check box style
            check_on = "QCheckBox::indicator:unchecked {image: url(" + os.path.join(icon_path,"check_off_s.png") + ");}\n"
            check_off = "QCheckBox::indicator:checked {image: url(" + os.path.join(icon_path,"check_on_s.png") + ");}"
            parent.cbx_fil_deleted.setStyleSheet(check_off + check_on)
            parent.cbx_fil_original.setStyleSheet(check_off + check_on)
            parent.cbx_fil_pub.setStyleSheet(check_off + check_on)
            parent.cbx_fil_edit.setStyleSheet(check_off + check_on)

        elif skin == "white":
            icon_path = os.path.join(icon_path, "black")
            setMainWindowIcons(parent, icon_path)

            parent.btn_con_add.setFont(font)
            parent.btn_con_del.setFont(font)
            parent.btn_con_imp.setFont(font)
            parent.btn_con_rec.setFont(font)
            parent.btn_con_take.setFont(font)
            parent.btn_con_update.setFont(font)
            parent.btn_mat_add.setFont(font)
            parent.btn_mat_del.setFont(font)
            parent.btn_mat_imp.setFont(font)
            parent.btn_mat_rec.setFont(font)
            parent.btn_mat_take.setFont(font)
            parent.btn_mat_update.setFont(font)
            parent.btn_open_gimp.setFont(font)

            # Set Check box style
            check_on = "QCheckBox::indicator:unchecked {image: url(" + os.path.join(icon_path,"check_off_s.png") + ");}\n"
            check_off = "QCheckBox::indicator:checked {image: url(" + os.path.join(icon_path,"check_on_s.png") + ");}"
            parent.cbx_fil_deleted.setStyleSheet(check_off + check_on)
            parent.cbx_fil_original.setStyleSheet(check_off + check_on)
            parent.cbx_fil_pub.setStyleSheet(check_off + check_on)
            parent.cbx_fil_edit.setStyleSheet(check_off + check_on)
    except Exception as e:
            print("Error occured in applyMainWindowSkin(parent, icon_path="", skin='grey')")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language="en")
            return(None)
