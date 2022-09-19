#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Import general libraries.
import sys, os, subprocess

# Import general operations.
import modules.general as general
import modules.error as error

# Import image viewer object.
import viewer.imageViewer as viewer

# Import PyQt5 libraries for generating the GUI application.
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

def setText(parent):
    print("## setupIidSkin::setText(parent)")

    try:
        if parent.language == "ja":
            parent.cbx_fil_pub.setText("公開設定")
            parent.cbx_fil_edit.setText("削除可能")
            parent.lab_fil_sta.setText("ステータス")
            parent.lab_fil_ali.setText("別　名 :")
            parent.lab_fil_dt_cr.setText("作成日時 :")
            parent.lab_fil_dt_mod.setText("編集日時 :")
            parent.lab_fil_ope.setText("操　作 :")
            parent.lab_fil_ope_app.setText("操作アプリ :")
            parent.lab_fil_cap.setText("キャプション :")
            parent.lbl_fil_dsc.setText("備　考 :")
            parent.btn_fil_dt_cre_exif.setText("Exifから取得")
            parent.btn_fil_dt_mod_exif.setText("Exifから取得")
            parent.box_fil_ope.buttons()[0].setText("OK")
            parent.box_fil_ope.buttons()[1].setText("キャンセル")

        elif parent.language == "en":
            parent.cbx_fil_pub.setText("Public")
            parent.cbx_fil_edit.setText("Erasable")
            parent.lab_fil_sta.setText("Status")
            parent.lab_fil_ali.setText("Alias :")
            parent.lab_fil_dt_cr.setText("Date of Create :")
            parent.lab_fil_dt_mod.setText("Date of Edit :")
            parent.lab_fil_ope.setText("Operation :")
            parent.lab_fil_ope_app.setText("Application :")
            parent.lab_fil_cap.setText("Caption :")
            parent.lbl_fil_dsc.setText("Description :")
            parent.btn_fil_dt_cre_exif.setText("Get from Exif")
            parent.btn_fil_dt_mod_exif.setText("Get from Exif")
            parent.box_fil_ope.buttons()[0].setText("OK")
            parent.box_fil_ope.buttons()[1].setText("Cancel")
    except Exception as e:
        print("Error occured in setupIidSkin::setText(parent)")
        print(str(e))
        error.ErrorMessageCameraDetection(details=str(e), show=True, language=parent.language)
        return(None)

def setIcons(parent, icon_path):
    print("## setupIidSkin::setIcons(parent, icon_path)")

    try:
        # Change the default icons for dialoc button box.
        parent.box_fil_ope.buttons()[0].setFlat(True)
        parent.box_fil_ope.buttons()[1].setFlat(True)

        # Set the dialog button size.
        dlg_btn_size = QSize(125, 30)
        parent.box_fil_ope.buttons()[0].setMinimumSize(dlg_btn_size)
        parent.box_fil_ope.buttons()[1].setMinimumSize(dlg_btn_size)

        # Set the skin and icon.
        parent.box_fil_ope.buttons()[0].setIcon(general.getIconFromPath(os.path.join(icon_path, 'check.png')))
        parent.box_fil_ope.buttons()[1].setIcon(general.getIconFromPath(os.path.join(icon_path, 'close.png')))

        parent.btn_fil_dt_cre_exif.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'add_photo.png'))))
        parent.btn_fil_dt_mod_exif.setIcon(QIcon(QPixmap(os.path.join(icon_path, 'add_photo.png'))))

        # Set the skin and icon.
        icon_size = general.getIconSize()
        qicon_size = QSize(icon_size, icon_size)

        #parent.tab_conf_main.setTabIcon(0, general.getIconFromPath(os.path.join(icon_path, 'apps.png')))

        # Set Check box style
        check_on = "QCheckBox::indicator:unchecked {image: url(" + os.path.join(icon_path,"check_off_s.png") + ");}\n"
        check_off = "QCheckBox::indicator:checked {image: url(" + os.path.join(icon_path,"check_on_s.png") + ");}"
        parent.cbx_fil_pub.setStyleSheet(check_off + check_on)
        parent.cbx_fil_edit.setStyleSheet(check_off + check_on)

    except Exception as e:
        print("Error occured in setupIidSkin::setIcons(parent, icon_path)")
        print(str(e))
        error.ErrorMessageCameraDetection(details=str(e), show=True, language=parent.language)
        return(None)

def setSkin(parent, icon_directory, skin="grey"):
    print("## setupIidSkin::setSkin(parent, icon_directory, skin='grey')")

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
            parent.setStyleSheet(back_color + font_style + 'border-style: none; border-color: #4C4C4C;')
            parent.frame.setStyleSheet(back_color + font_style + 'border-style: none; border-color: #4C4C4C;')

            # Set the default skin for text boxes.
            text_border = 'border-style: outset; border-width: 0.5px; border-color: #4C4C4C;'
            text_background = "background-color: #6C6C6C;"
            parent.cmb_fil_stts.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_fil_ali.setStyleSheet(font_style_color + font_style_size + text_border + text_background)

            parent.dte_fil_dt_cre.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.dte_fil_dt_mod.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.cmb_fil_eope.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_fil_ope_app.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_fil_dsc.setStyleSheet(font_style_color + font_style_size + text_border + text_background)
            parent.tbx_fil_capt.setStyleSheet(font_style_color + font_style_size + text_border + text_background)

            # Set the default skin for tabs.
            back_color_tab = 'QTabBar::tab {background-color: #2C2C2C; }'
            back_color_tab_act = 'QTabBar::tab::selected {background-color: #4C4C4C;}'
            parent.tab_src.setStyleSheet(back_color_tab + back_color_tab_act)

        elif skin == "white":
            icon_path = os.path.join(icon_path, "black")
            setIcons(parent, icon_path)

    except Exception as e:
        print("Error occured in setupIidSkin::setSkin(parent, icon_directory, skin='grey')")
        print(str(e))
        error.ErrorMessageCameraDetection(details=str(e), show=True, language=parent.language)
        return(None)

def setImageDataView(parent):
    # Add a tab for the image viewer
    tab_img_view = QWidget()
    tab_img_view.setLayoutDirection(Qt.LeftToRight)
    tab_img_view.setObjectName("tab_img_view")

    # Add the layout for image viewer.
    lay_img_view = QVBoxLayout(tab_img_view)
    lay_img_view.setContentsMargins(0, 0, 0, 0)
    lay_img_view.setObjectName("lay_img_view")

    # Create the graphic view item.
    parent.graphicsView = viewer.ImageViewer()
    parent.graphicsView.setObjectName("graphicsView")
    lay_img_view.addWidget(parent.graphicsView)

    # Add a tab for the thumbnail.
    tab_img_exif = QWidget()
    tab_img_exif.setLayoutDirection(Qt.LeftToRight)
    tab_img_exif.setObjectName("tab_img_exif")

    # Add the layout for image viewer.
    lay_img_exif = QVBoxLayout(tab_img_exif)
    lay_img_exif.setContentsMargins(0, 0, 0, 0)
    lay_img_exif.setObjectName("lay_img_exif")

    parent.tre_img_exif = QTreeWidget()
    parent.tre_img_exif.setObjectName("tre_img_exif")
    tre_img_exif_header = QTreeWidgetItem(["Property","Values"])
    parent.tre_img_exif.setHeaderItem(tre_img_exif_header)
    lay_img_exif.addWidget(parent.tre_img_exif)

    # Add the layout to the tab.
    parent.tab_src.addTab(tab_img_view, "Image Viewer")
    parent.tab_src.addTab(tab_img_exif, "Exif Viewer")
