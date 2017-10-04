#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Import general libraries.
import sys, os, uuid, shutil, time, math, tempfile, logging, pyexiv2

# Import DB libraries
import sqlite3 as sqlite
from sqlite3 import Error

# Import PyQt5 libraries for generating the GUI application.
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QThread, pyqtSignal

def alert(title, message, icon, info, detailed):
    # Create a message box object.
    msg = QMessageBox()
    
    # Set parameters for the message box.
    msg.setIcon(icon)
    msg.setWindowTitle(title)
    msg.setText(message)
    
    # Generate additional information if exists.
    if not info == None:
        msg.setInformativeText(info)
    if not detailed == None:
        msg.setDetailedText(detailed)
    
    # Show the message box.    
    msg.exec_()

def getFilesWithExtensionList(dir_search, ext_list_search, result=None):
    if result == None:
        result = list()
    
    for ext_search in ext_list_search:
        if os.path.exists(dir_search):
            # Get files from the given directory.
            filenames = os.listdir(dir_search)
            
            for filename in filenames:
                # Get the full path of the file.
                full_path = os.path.join(dir_search, filename)
                
                if not os.path.isdir(full_path):
                    # Split file path into file name and file path.
                    basename, extension = os.path.splitext(filename)
                    
                    # Check the file extension.
                    if extension.lower() == ext_search.lower():
                        result.append(filename)
                else:
                    # Search files recursively if the full path is directory.
                    next_search_ext = list()
                    next_search_ext.append(ext_search)
                    
                    getFilesWithExtensionList(full_path, next_search_ext, result)
        else:
            print("No such path: " + str(dir_search))
            return(None)
    return(result)

def createTables(db_file):
    print("connect")
    
    # Define the create table query for consolidation class.
    sql_con = """CREATE TABLE consolidation (
                    id INTEGER PRIMARY KEY,
                    uuid text NOT NULL,
                    name text,
                    geographic_annotation text,
                    temporal_annotation text,
                    description text
                );"""
    
    # Define the create table query for material class.
    sql_mat = """CREATE TABLE material (
                    id integer PRIMARY KEY,
                    uuid text NOT NULL,
                    con_id integer NOT NULL,
                    name text,
                    estimated_period_beginning character varying(255),
                    estimated_period_ending character varying(255),
                    latitude real,
                    longitude real,
                    altitude real,
                    material_number text,
                    descriptions text,
                    FOREIGN KEY (con_id) REFERENCES consolidation (id) ON UPDATE CASCADE ON DELETE CASCADE
                );"""
    
    # Define the create table query for material class.
    sql_fil = """CREATE TABLE file (
                    id integer PRIMARY KEY,
                    uuid text NOT NULL,
                    con_id integer,
                    mat_id integer,
                    filename character varying(255),
                    mime_type character varying(20),
                    alias_name character varying(255),
                    status character varying(255),
                    make_public bool,
                    is_locked bool,
                    source varying(255),
                    file_operation  varying(255),
                    operating_application varying(255),
                    caption character varying(255),
                    descriptions text,
                    FOREIGN KEY (con_id) REFERENCES consolidation (id) ON UPDATE CASCADE ON DELETE CASCADE,
                    FOREIGN KEY (mat_id) REFERENCES material (id) ON UPDATE CASCADE ON DELETE CASCADE
                );"""
    
    # Create tables by using SQL queries.
    try:
        # Connect to the DataBase file for SQLite.
        conn = sqlite.connect(db_file)
        
        # Create tables if if connection successfully established
        if conn is not None:
            # Instantiate the cursor.
            curs = conn.cursor()
            
            # Execute the SQL queries.
            curs.execute(sql_con)
            curs.execute(sql_mat)
            curs.execute(sql_fil)
            
            # Commit the queries.
            conn.commit()
    except Error as e:
        # Create error messages.
        error_title = "エラーが発生しました"
        error_msg = "テーブルは作成されませんでした!!"
        error_info = "SQLiteのデータベース・ファイルあるいはデータベースの設定を確認してください。"
        error_icon = QMessageBox.Critical
        error_detailed = e.args[0]
        
        # Handle error.
        alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
        
        # Returns nothing.
        return(None)
    finally:
        # Finally close the connection.
        conn.close()

def createDirectories(item_dir, isConsolidation):
    try:
        # Define the root path and create the root directory.
        sop_dir_root = item_dir
        os.mkdir(sop_dir_root)
        
        # Define path of directories for each medium.
        sop_dir_txt = os.path.join(sop_dir_root, "Texts")
        sop_dir_img = os.path.join(sop_dir_root, "Images")
        sop_dir_snd = os.path.join(sop_dir_root, "Sounds")
        sop_dir_mov = os.path.join(sop_dir_root, "Movies")
        sop_dir_lnk = os.path.join(sop_dir_root, "Linkages")
        
        # Make directories for each medium.
        os.mkdir(sop_dir_txt)
        os.mkdir(sop_dir_img)
        os.mkdir(sop_dir_snd)
        os.mkdir(sop_dir_mov)
        os.mkdir(sop_dir_lnk)
        
        # Make directories for images.
        os.mkdir(os.path.join(sop_dir_img, "Main"))
        os.mkdir(os.path.join(sop_dir_img, "Raw"))
        os.mkdir(os.path.join(sop_dir_img, "Thumbs"))
        
        # In case consolidation, create a directory for materials.
        if isConsolidation:
            os.mkdir(os.path.join(sop_dir_root, "Materials"))
    except:
        # Create error messages.
        error_title = "エラーが発生しました"
        error_msg = "ディレクトリの作成に失敗しました。"
        error_info = "不明のエラーです。"
        error_icon = QMessageBox.Critical
        error_detailed = None
        
        # Handle error.
        alert(title=error_title, message=error_msg, icon=error_icon, info=error_info, detailed=error_detailed)
        
        return(None)