#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Import general libraries.
import sys, os, time, pyexiv2, shutil
import sqlite3 as sqlite
import xml.etree.cElementTree as ET

from mimetypes import MimeTypes

# Import custom modules
import modules.error as error

# Import PyQt5 libraries for generating the GUI application.
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QThread, pyqtSignal

# Labels for Consolidation and Material
LAB_CON_JA = u"統合体"
LAB_MAT_JA = u"資料"
LAB_CON_EN = u"Consolidation"
LAB_MAT_EN = u"Material"

def initAll(parent):
    print("general::initAll(parent)")
    
    try:
        # Define paths
        parent.root_directory = None
        parent.table_directory = None
        parent.consolidation_directory = None
        parent.database = None
        
        # Define the default extensions.
        parent.qt_image = [".BMP", ".GIF", ".JPG", ".JPEG", ".PNG", ".PBM", ".PGM", ".PPM", ".XBM", ".XPM"]
        parent.image_extensions = [".JPG", ".TIF", ".JPEG", ".TIFF", ".PNG", ".JP2", ".J2K", ".JPF", ".JPX", ".JPM"]
        parent.raw_image_extensions = [".RAW", ".ARW"]
        parent.sound_extensions = [".WAV"]
        
        # Difine the current objects
        parent.current_consolidation = None
        parent.current_material = None
        parent.current_file = None
        parent.current_camera = None
        
        # Initialize the flickr API keys.
        parent.flickr_apikey = None
        parent.flickr_secret = None
        
        # Initialize the map tile source.
        # Set the default settings.
        parent.language = "en"
        parent.skin = "grey"
        parent.map_tile = "OpenStreetMap"
        parent.proxy = "No Proxy"
        
        # Set default algorithms.
        parent.awb_algo = "retinex_adjusted"
        parent.psp_algo = "ihsConvert"
        
        # Initialyze the temporal directory.
        if not os.path.exists(parent.temporal_directory):
            # Create the temporal directory if not exists.
            os.mkdir(parent.temporal_directory)
        else:
            # Delete the existing temporal directory before create.
            shutil.rmtree(parent.temporal_directory)
            os.mkdir(parent.temporal_directory)
    except Exception as e:
        print("Error occured in main::initAll(parent)")
        print(str(e))
        error.ErrorMessageUnknown(details=str(e), show=True, language="en")
        return(None)
    
def initConfig(parent):
    print("main::initConfig(parent)")
    
    try:
        # Create the root node.
        root = ET.Element("config")
        
        # Create the theme node.
        theme = ET.SubElement(root, "theme")
        
        ET.SubElement(theme, "language").text = parent.language
        ET.SubElement(theme, "skin").text = parent.skin
        
        # Create the project node.
        project = ET.SubElement(root, "project")
        ET.SubElement(project, "root").text = ""
        
        # Create the tool node
        tools = ET.SubElement(root, "tools")
        
        ET.SubElement(tools, "awb").text = parent.awb_algo
        ET.SubElement(tools, "psp").text = parent.psp_algo
        
        # Create the tool node
        geoInfo = ET.SubElement(root, "geoinfo")
        ET.SubElement(geoInfo, "maptile").text = parent.map_tile
        
        # Create the network node.
        network = ET.SubElement(root, "network")
        ET.SubElement(network, "proxy").text = parent.proxy
        
        # Write the 
        tree = ET.ElementTree(root)
        tree.write(parent.config_file)
    except Exception as e:
        print("Error occured in main::initConfig(self)")
        print(str(e))
        error.ErrorMessageUnknown(details=str(e), show=True, language="en")
        return(None)

def loadConfig(parent, file_config):
    print("general::loadConfig(parent)")
    
    try:
        xml_config = ET.parse(file_config).getroot()
        
        for xml_child in xml_config:
            if xml_child.tag == "theme":
                parent.language = xml_child.find("language").text
                parent.skin = xml_child.find("skin").text
            elif xml_child.tag == "tools":
                parent.awb_algo = xml_child.find("awb").text
                parent.psp_algo = xml_child.find("psp").text
            elif xml_child.tag == "geoinfo":
                parent.map_tile = xml_child.find("maptile").text
            elif xml_child.tag == "network":
                parent.proxy = xml_child.find("proxy").text
            elif xml_child.tag == "project":
                if not xml_child.find("root").text == "":
                    xml_root = xml_child.find("root").text
                    
                    if xml_root and os.path.exists(xml_root):
                        parent.root_directory = xml_child.find("root").text
                        
                        # Some essential directories are created under the root directory if they are not existed.
                        parent.table_directory = os.path.join(parent.root_directory, "Table")
                        parent.consolidation_directory = os.path.join(parent.root_directory, "Consolidation")
                        
                        # Define the DB file.
                        parent.database = os.path.join(parent.table_directory, "project.db")
        
        # Check directories and files.
        if not os.path.exists(parent.root_directory): return(None)
        if not os.path.exists(parent.table_directory): return(None)
        if not os.path.exists(parent.consolidation_directory): return(None)
        if not os.path.exists(parent.database): return(None)
        
        # Return True
        return(True)
    except Exception as e:
        print("Error occured in main::loadConfig(self)")
        print(str(e))
        error.ErrorMessageUnknown(details=str(e), show=True, language="en")
        return(None)

def changeConfig(parent):
    print("main::changeConfig(self)")
    
    try:
        # Get the root node of the configuration file.
        xml_config = ET.parse(parent.config_file).getroot()
        
        # Replace current settings by new values.
        for xml_child in xml_config:
            # Configurations for User Interface.
            if xml_child.tag == "theme":
                xml_child.find("language").text = parent.language   # Language settings.
                xml_child.find("skin").text = parent.skin           # Skin settings.
            if xml_child.tag == "project":
                xml_child.find("root").text = parent.root_directory # Current project.
            if xml_child.tag == "tools":
                xml_child.find("awb").text = parent.awb_algo        # Auto white balance algorithm.
                xml_child.find("psp").text = parent.psp_algo        # Pansharpen algorithm
            if xml_child.tag == "geoinfo":
                xml_child.find("maptile").text = parent.map_tile    # Source for the map tile
            if xml_child.tag == "network":
                xml_child.find("proxy").text = parent.proxy         # Proxy setting
        
        # Create a new tree object by new entries.
        tree = ET.ElementTree(xml_config)
        
        # Save the new configuration.
        tree.write(parent.config_file)
    except Exception as e:
        print("Error occured in main::changeConfig(self)")
        print(str(e))
        error.ErrorMessageUnknown(details=str(e), show=True, language=parent.language)
        return(None)

def pyDateTimeToQDateTime(value):
    print("general::pyDateTimeToqDateTime(value)")
    try:
        qDateTime = QDateTime(
            value.year,
            value.month,
            value.day,
            value.hour,
            value.minute,
            value.second
        )
        return (qDateTime)
    except Exception as e:
        print(str(e) + ":" + str(value))
        
def pyDateToQDate(value):
    print("general::pyDateTimeToqDateTime(value)")
    try:
        qDate = QDate(
            value.year,
            value.month,
            value.day,
        )
        return (qDate)
    except Exception as e:
        print(str(e) + ":" + str(value))

def askNewProject(parent):
    try:
        if parent.language == "ja":
            title = "データベース・ファイルが見つかりません。"
            message = "新規プロジェクトを作成しますか？"
        elif parent.language == "en":
            title = "Database file is not found."
            message = "Would you like to create the new Database file？"
        
        # Confirm whether create a directory for consolidations.
        reply = QMessageBox.question(
                parent, 
                title, 
                message, 
                QMessageBox.Yes, 
                QMessageBox.No
            )
        
        # Create the directory of consolidation
        if reply == QMessageBox.Yes:
            # Create the consolidation directory and the table directory.
            os.mkdir(parent.consolidation_directory)
            os.mkdir(parent.table_directory)
            
            # Create new tables which defined by Simple Object Profile(SOP).
            createTables(parent.database)
            
            # Returns True. 
            return(True)    
        else:
            raise
    except Exception as e:
        error.ErrorMessageProjectNotCreated(details=str(e), language=parent.language)
        return(None)

def askDeleteConsolidation(parent):
    con_uuid = parent.current_consolidation.uuid
    
    if parent.language == "ja":
        title = LAB_CON_JA + u"の削除"
        message = LAB_CON_JA + u"が内包する全てのデータが削除されます。本当に削除しますか？"
    elif parent.language == "en":
        title = u"Delete the " + LAB_CON_EN + "."
        message = u"Every kinds of datasets included in the " + LAB_CON_EN + u" will be removed. Would you like to delete the " + LAB_CON_EN + u" ?"
    
    reply = QMessageBox.question(
        parent, 
        title, 
        message, 
        QMessageBox.Yes, 
        QMessageBox.No
    )
    
    return(reply)

def askNewMaterial(parent):
    try:
        con_uuid = parent.current_consolidation.uuid
        
        if parent.language == "ja":
            title = LAB_MAT_JA + u"を内包する" + LAB_CON_JA + u"が指定されていません。"
            message = u"現在の" + LAB_CON_JA + u"（" + con_uuid.decode("utf-8") + u"）に新規の" + LAB_MAT_JA + u"を追加しますか？"
        elif parent.language == "en":
            title = LAB_CON_EN + u" including the " + LAB_MAT_EN + u" is not selected."
            message = u"Would you like to add a " + LAB_MAT_JA + u" to the current " + LAB_CON_EN + u" （" + con_uuid.decode("utf-8") + u"?"
            
        reply = QMessageBox.question(
            parent, 
            title, 
            message, 
            QMessageBox.Yes, 
            QMessageBox.No
        )
        
        return(reply)
    except Exception as e:
        print(str(e))

def askDeleteMaterial(parent):
    mat_uuid = parent.current_material.uuid
    
    if parent.language == "ja":
        title = LAB_MAT_JA + u"の削除"
        message = LAB_MAT_JA + u"が内包する全てのデータが削除されます。本当に削除しますか？"
    elif parent.language == "en":
        title = u"Delete the " + LAB_MAT_EN + "."
        message = u"Every kinds of datasets included in the " + LAB_MAT_EN + u" will be removed. Would you like to delete the " + LAB_MAT_JA + u" ?"
        
    reply = QMessageBox.question(
        parent, 
        title, 
        message, 
        QMessageBox.Yes, 
        QMessageBox.No
    )
    
    return(reply)

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

def executeSql(dbfile, sql):
    print("general::executeSql(dbfile, sql)")
    
    # Create tables by using SQL queries.
    try:
        # Connect to the DataBase file for SQLite.
        conn = sqlite.connect(dbfile)
        
        # Create tables if if connection successfully established
        if conn is not None:
            # Instantiate the cursor.
            curs = conn.cursor()
            
            # Execute the SQL queries.
            curs.execute(sql)
            
            # Commit the queries.
            conn.commit()
            
            # Retrun as True.
            return(True)
    except Error as e:
        print("Cannot execute the SQL: general::executeSql(dbfile, sql)")
        print(str(e))
        
        # Exit with 0.
        return(None)
    finally:
        # Finally close the connection.
        conn.close()

def getFilesWithExtensionList(dir_search, ext_list_search, result=None):
    print("general::getFilesWithExtensionList(dir_search, ext_list_search, result=None)")
    
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

def createTables(dbfile):
    print("general::createTables(dbfile)")
    
    try:
        # Define the create table query for consolidation class.
        createTableConsolidation(dbfile)
        
        # Define the create table query for material class.
        createTableMaterial(dbfile)
        
        # Define the create table query for file class.
        createTableFile(dbfile)
        
        # Define the create table query for additional attribute class.
        createTableAdditionalAttribute(dbfile)
    except Exception as e:
        print("Error occured in general::createTables(dbfile)")
        print(str(e))
        
        # Return Nothing..
        return(None)

def createTableConsolidation(dbfile):
    print("general::createTableConsolidation(dbfile)")
    
    try:
        # Define the create table query for consolidation class.
        sql_create = """CREATE TABLE consolidation (
                        id INTEGER PRIMARY KEY,
                        uuid text NOT NULL,
                        name text,
                        geographic_annotation text,
                        temporal_annotation text,
                        description text,
                        flickr_photosetid
                    );"""
        # Execute SQL create.
        executeSql(dbfile, sql_create)
    except Exception as e:
        print("Error occured in general::createTableConsolidation(dbfile)")
        print(str(e))
        
        # Return Nothing
        return(None)

def createTableMaterial(dbfile):
    print("general::createTableMaterial(dbfile)")
    
    try:
        # Define the create table query for material class.
        sql_create = """CREATE TABLE material (
                        id integer PRIMARY KEY,
                        uuid text NOT NULL,
                        con_id text NOT NULL,
                        name text,
                        material_number text,
                        estimated_period_beginning character varying(255),
                        estimated_period_peak character varying(255),
                        estimated_period_ending character varying(255),
                        latitude real,
                        longitude real,
                        altitude real,
                        description text,
                        FOREIGN KEY (con_id) REFERENCES consolidation (uuid) ON UPDATE CASCADE ON DELETE CASCADE
                    );"""
        
        # Execute SQL create.
        executeSql(dbfile, sql_create)
    except Exception as e:
        print("Error occured in general::createTableMaterial(dbfile)")
        print(str(e))
        
        # Retrun nothing.
        return(None)

def createTableFile(dbfile):
    print("general::createTableFile(dbfile)")
    
    try:
        # Define the create table query for file class.
        sql_create = """CREATE TABLE file (
                        id integer PRIMARY KEY,
                        uuid text NOT NULL,
                        con_id text,
                        mat_id text,
                        created_date datetime,
                        modified_date datetime,
                        file_name character varying(255),
                        file_type character varying(20),
                        alias_name character varying(255),
                        status character varying(255),
                        make_public bool,
                        is_locked bool,
                        source varying(255),
                        file_operation  varying(255),
                        operating_application varying(255),
                        caption character varying(255),
                        description text,
                        flickr_photoid text,
                        FOREIGN KEY (con_id) REFERENCES consolidation (uuid) ON UPDATE CASCADE ON DELETE CASCADE,
                        FOREIGN KEY (mat_id) REFERENCES material (uuid) ON UPDATE CASCADE ON DELETE CASCADE
                    );"""
        
        # Execute SQL create.
        executeSql(dbfile, sql_create)
    except Exception as e:
        print("Error occured in general::createTables(dbfile)")
        print(str(e))
        
        # Return Nothing.
        return(None)

def createTableAdditionalAttribute(dbfile):
    print("general::createTableAdditionalAttribute(dbfile)")
    
    try:
        # Define the create table query for file class.
        sql_create = """CREATE TABLE additional_attribute (
                        id integer PRIMARY KEY,
                        uuid text NOT NULL,
                        ref_table text,
                        ref_uuid text,
                        key text,
                        value text,
                        datatype text,
                        description text
                    );"""
        
        # Execute SQL create.
        executeSql(dbfile, sql_create)
    except Exception as e:
        print("Error occured in general::createTables(dbfile)")
        print(str(e))
        
        # Return Nothing.
        return(None)

def checkTableExist(dbfile, table_name):
    print("general::checkTableExist(dbfile, table_name)")
    
    try:
        sql_check = """SELECT name FROM sqlite_master WHERE type='table' AND name=?;"""
        
        # Establish the connection between DB.
        conn = sqlite.connect(dbfile)
        
        if conn is not None:
            # Instantiate the cursor for query.
            cur = conn.cursor()
            
            # Execute the query.
            cur.execute(sql_check, [table_name])
            
            # Fetch one row.
            rows = cur.fetchone()
            
            if not rows == None:
                return(True)
            else:
                return(False)
    except Exception as e:
        print("Error occured in general::checkTableExist(dbfile, table_name)")
        print(str(e))
        
        # Return nothing.
        return(None)

def checkConsolidationTableFields(dbfile):
    print("general::checkConsolidationTableFields(dbfile)")
    
    try:
        # Create a list for fields checking.
        con_fields = [
                        ("uuid", "text"),
                        ("name", "text"),
                        ("geographic_annotation", "text"),
                        ("temporal_annotation", "text"),
                        ("description", "text"),
                        ("flickr_photosetid", "text")
                    ]
        # Check fields.
        checkFieldsExists(dbfile, "consolidation", con_fields)
    except Exception as e:
        print("Error occured in general::checkConsolidationTableFields(dbfile)")
        print(str(e))
        
        # Return nothing.
        return(None)

def checkMaterialTableFields(dbfile):
    print("general::checkMaterialTableFields(dbfile)")
    
    try:
        mat_fields= [
                        ("con_id", "text"),
                        ("name", "text"),
                        ("material_number", "text"),
                        ("estimated_period_beginning", "character varying(255)"),
                        ("estimated_period_peak", "character varying(255)"),
                        ("estimated_period_ending", "character varying(255)"),
                        ("latitude", "real"),
                        ("longitude", "real"),
                        ("altitude", "real"),
                        ("material_number", "text"),
                        ("description", "text")
                    ]
        # Check fields.
        checkFieldsExists(dbfile, "material", mat_fields)
    except Exception as e:
        print("Error occured in general::checkMaterialTableFields(dbfile)")
        print(str(e))
        
        # Return nothing.
        return(None)

def checkFileTableFields(dbfile):
    print("general::checkFileTableFields(dbfile)")
    
    try:
        fil_fields = [
                        ("uuid", "text"),
                        ("con_id", "text"),
                        ("mat_id", "text"),
                        ("created_date", "datetime"),
                        ("modified_date", "datetime"),
                        ("file_name", "character varying(255)"),
                        ("file_type", "character varying(20)"),
                        ("make_public", "bool"),
                        ("alias_name", "character varying(255)"),
                        ("status", "character varying(255)"),
                        ("is_locked", "bool"),
                        ("source", "character varying(255)"),
                        ("file_operation", "character varying(255)"),
                        ("operating_application", "character varying(255)"),
                        ("caption", "character varying(255)"),
                        ("description", "text"),
                        ("flickr_photoid", "text")
                    ]
        # Check fields.
        checkFieldsExists(dbfile, "file", fil_fields)
    except Exception as e:
        print("Error occured in general::checkFileTableFields(dbfile)")
        print(str(e))
        
        # Return nothing.
        return(None)
    
def checkAdditionalAttributeTableFields(dbfile):
    print("general::checkAdditionalAttributeTableFields(dbfile)")
    
    try:
        add_fields = [
                        ("uuid", "text"),
                        ("ref_table", "text"),
                        ("mat_id", "text"),
                        ("ref_uuid", "text"),
                        ("key", "text"),
                        ("value", "text"),
                        ("datatype", "text"),
                        ("description", "text")
                    ]
        # Check fields.
        checkFieldsExists(dbfile, "additional_attribute", add_fields)
    except Exception as e:
        print("Error occured in general::checkAdditionalAttributeTableFields(dbfile)")
        print(str(e))
        
        # Return nothing.
        return(None)
    
def checkFieldsExists(dbfile, table_name, fields):
    print("general::checkFieldsExists(dbfile, table_name, fields)")
    
     # Create tables by using SQL queries.
    sql_check = "PRAGMA table_info('" + table_name + "')"
    
    try:
        # Connect to the DataBase file for SQLite.
        conn = sqlite.connect(dbfile)
        
        # Create tables if if connection successfully established
        if conn is not None:
            # Instantiate the cursor.
            cur = conn.cursor()
            
            # Execute the SQL queries.
            cur.execute(sql_check)
            
            # Fetch one row.
            rows = cur.fetchall()
            
            for field in fields:
                isExist = False
                
                for row in rows:
                    if field[0] == row[1]: isExist = True
                    
                if isExist == False:
                    print("Add a column of " + field[0])
                    sql_alt = "ALTER TABLE '" + table_name + "' ADD '" +  field[0] + "' " + field[1]
                    cur_alt = conn.cursor()
                    cur.execute(sql_alt)
            # Commit the result of the query.
            conn.commit()
    except Error as e:
        print("Error occured in general::checkFieldsExists(dbfile, table_name, fields)")
        print(str(e))
        
        # Returns nothing.
        return(None)
    finally:
        # Finally close the connection.
        conn.close()

def createDirectories(item_path, isConsolidation):
    print("general::createDirectories(item_path, isConsolidation)")
    
    try:
        # Define the root path and create the root directory.
        sop_dir_root = item_path
        os.mkdir(sop_dir_root)
        
        # Define path of directories for each medium.
        sop_dir_txt = os.path.join(sop_dir_root, "Texts")
        sop_dir_img = os.path.join(sop_dir_root, "Images")
        sop_dir_snd = os.path.join(sop_dir_root, "Sounds")
        sop_dir_mov = os.path.join(sop_dir_root, "Movies")
        sop_dir_geo = os.path.join(sop_dir_root, "Geometries")
        sop_dir_lnk = os.path.join(sop_dir_root, "Linkages")
        
        # Make directories for each medium.
        os.mkdir(sop_dir_txt)
        os.mkdir(sop_dir_img)
        os.mkdir(sop_dir_snd)
        os.mkdir(sop_dir_mov)
        os.mkdir(sop_dir_geo)
        os.mkdir(sop_dir_lnk)
        
        # Make directories for images.
        os.mkdir(os.path.join(sop_dir_img, "Main"))
        os.mkdir(os.path.join(sop_dir_img, "Raw"))
        os.mkdir(os.path.join(sop_dir_img, "Thumbs"))
        
        open(os.path.join(sop_dir_geo, "markers.txt", "w")).close()
        open(os.path.join(sop_dir_geo, "lines.txt", "w")).close()
        open(os.path.join(sop_dir_geo, "polygons.txt", "w")).close()
        
        # In case consolidation, create a directory for materials.
        if isConsolidation:
            os.mkdir(os.path.join(sop_dir_root, "Materials"))
    except Exception as e:
        print("Error occured in general::checkAdditionalAttributeTableFields(dbfile)")
        print(str(e))
        
        return(None)

def getRelativePath(path, root):
    print("general::getRelativePath(path, root)")
    
    try:
        # Initialyze the variable for storing relative path.
        relative_path = ""
        
        # Extract the directories from the full path.
        dirs = path.split("/")
        
        # Get the indecies of starting and ending point for the relative path.
        start = dirs.index(root)
        end = len(dirs)
        
        # Reconstruct the relative path to the source.
        for i in range(start, end):        
            # Get the relative path
            relative_path = os.path.join(str(relative_path), str(dirs[i]))
        
        return(relative_path)
    except Exception as e:
        print("Erro!! Cannot get relative path.")
        print(str(e))
        
        return(None)

def getMimeType(path):
    print("general::getMimeType(path)")
    
    try:
        mime = MimeTypes()
        mime_type = mime.guess_type(path)
        
        return(mime_type)
    except Exception as e:
        print("Error occured in general::getMimeType(path)")
        print(str(e))
        
        return(None)

def copyExif(org_file, dst_file):
    print("general::copyExif(org_file, dst_file)")
    
    try:
        # Get the exif information for the original image.
        meta_org = pyexiv2.ImageMetadata(org_file)
        meta_org.read()
        meta_org.modified = True
        
        # Get the exif information for the cropped image.
        meta_dst = pyexiv2.metadata.ImageMetadata(dst_file)
        meta_dst.read()
        
        # Copy the original exif information to the cropped image.
        meta_org.copy(meta_dst)
        meta_dst.write()
    except Exception as e:
        print("Error occured in general::copyExif(org_file, dst_file)")
        print(str(e))
        
        return(None)
