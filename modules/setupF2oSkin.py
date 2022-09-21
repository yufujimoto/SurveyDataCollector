#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Import general libraries.
import sys, os, subprocess

# Import general operations.
import modules.general as general
import modules.error as error

# Import PyQt5 libraries for generating the GUI application.
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

def setText(parent):
    print("## setupF2oSkin::setText(parent)")

    try:
        if parent.language == "ja":
            parent.grp_imp_fld.setTitle("フォルダの選択")
            parent.grp_mat_nam.setTitle("資料名の切り出し")
            parent.grp_con_set.setTitle("統合体の作成")
            parent.lbl_ftyp.setText("ファイル形式：")
            parent.lbl_pos_bgn.setText("開始位置")
            parent.lbl_pos_end.setText("終了位置")
            parent.btn_chk_lbl.setText("資料の確認")
            parent.chk_add_new.setText("新規統合の作成")

        elif parent.language == "en":
            parent.grp_imp_fld.setTitle("Select Folder")
            parent.grp_mat_nam.setTitle("Material Name Extraction")
            parent.grp_con_set.setTitle("Consolidation Setting")
            parent.lbl_ftyp.setText("File Type: ")
            parent.lbl_pos_bgn.setText("Begin: ")
            parent.lbl_pos_end.setText("End: ")
            parent.btn_chk_lbl.setText("Check")
            parent.chk_add_new.setText("Append to new consolidation")

    except Exception as e:
        print("Error occured in setupF2oSkin::setText(parent)")
        print(str(e))
        error.ErrorMessageUnknown(details=str(e), show=True, language=parent.language)
        return(None)

def setIcons(parent, icon_path):
    print("## setupF2oSkin::setIcons(parent, icon_path)")

    try:
        # Set the skin and icon.
        icon_size = general.getIconSize()
        qicon_size = QSize(icon_size, icon_size)

        parent.btn_opn.setIcon(general.getIconFromPath(os.path.join(icon_path, 'folder.png')))
        parent.btn_opn.setIconSize(qicon_size)

        parent.btn_chk_lbl.setIcon(general.getIconFromPath(os.path.join(icon_path, 'check.png')))
        parent.btn_chk_lbl.setIconSize(qicon_size)

        # Set the skin and icon.
        parent.bbx_fto_res.buttons()[0].setIcon(general.getIconFromPath(os.path.join(icon_path, 'check.png')))
        parent.bbx_fto_res.buttons()[1].setIcon(general.getIconFromPath(os.path.join(icon_path, 'close.png')))

        # Set Check box style
        check_on = "QCheckBox::indicator:unchecked {image: url(" + os.path.join(icon_path,"check_off_s.png") + ");}\n"
        check_off = "QCheckBox::indicator:checked {image: url(" + os.path.join(icon_path,"check_on_s.png") + ");}"
        parent.chk_add_new.setStyleSheet(check_off + check_on)

    except Exception as e:
        print("Error occured in setupF2oSkin::setIcons(parent, icon_path)")
        print(str(e))
        error.ErrorMessageUnknown(details=str(e), show=True, language=parent.language)
        return(None)

def setSkin(parent, icon_directory, skin="grey"):
    print("## setupF2oSkin::setSkin(parent, icon_directory, skin='grey')")

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

        # Setup the skin for the dialog.
        if parent.skin == "grey":
            # Set the icon path.
            icon_path = os.path.join(icon_directory, "white")
            setIcons(parent, icon_path)

            # Set the default background and front color.
            back_color = 'background-color: #2C2C2C;'
            font_style_color = 'color: #FFFFFF;'
            font_style = font_style_color + font_style_size

            # Set the default skin for all components.
            parent.setStyleSheet(back_color + font_style )

            parent.tbx_fnam.setStyleSheet('background-color: #6C6C6C;' + font_style + 'border-color: #4C4C4C;')
            parent.tre_con.setStyleSheet('background-color: #6C6C6C;' + font_style + 'border-color: #4C4C4C;')
            parent.spn_pos_bgn.setStyleSheet(font_style + 'border-color: #4C4C4C;')
            parent.spn_pos_end.setStyleSheet(font_style + 'border-color: #4C4C4C;')

            # Set the sample label style.
            back_color = "background-color: #FFFFFF;"
            font_style_color = 'color: #FF0000;'

            parent.lbl_smpl_exmpl.setStyleSheet(font_style_color + back_color)

        elif skin == "white":
            icon_path = os.path.join(icon_path, "black")
            setIcons(parent, icon_path)

    except Exception as e:
        print("Error occured in setupF2oSkin::setSkin(parent, icon_directory, skin='grey')")
        print(str(e))
        error.ErrorMessageUnknown(details=str(e), show=True, language=parent.language)
        return(None)
