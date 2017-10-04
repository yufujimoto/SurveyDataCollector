#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os, sys, uuid

import sqlite3 as sqlite
from sqlite3 import Error

from mimetypes import MimeTypes

# Define the default extensions.
QT_IMG = [".BMP", ".GIF", ".JPG", ".JPEG", ".PNG", ".PBM", ".PGM", ".PPM", ".XBM", ".XPM"]
IMG_EXT = [".JPG", ".TIF", ".JPEG", ".TIFF", ".PNG", ".JP2", ".J2K", ".JPF", ".JPX", ".JPM"]
RAW_EXT = [".RAW", ".ARW"]
SND_EXT = [".WAV"]

def executeSqlQuery(query, value):
    global DATABASE
    
    # Establish the connection to the DataBase file.
    conn = sqlite.connect(DATABASE)
    
    if conn is not None:
        # Instantiate the cursor for query.
        cur = conn.cursor()
        
        # Execute the query.
        cur.execute(query, value)
        
        # Commit the result of the query.
        conn.commit()
    
    conn.close()

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
                        result.append(full_path)
                else:
                    # Search files recursively if the full path is directory.
                    next_search_ext = list()
                    next_search_ext.append(ext_search)
                    
                    getFilesWithExtensionList(full_path, next_search_ext, result)
        else:
            print("No such path.")
            return(None)
    return(result)

def getFileEditInfo(path, key, alias="", status="Unknown",source="Unknown", lock=False, operation="Unknown", caption="",descriptions=""):
    fil_uuid = str(uuid.uuid4())
    con_id = ""
    mat_id = ""
    relative_path = ""
    operating_application = "Custom Python Code"
    
    if lock == True:
        is_lock = "TRUE"
    else:
        is_lock = "FALSE"
    
    mime = MimeTypes()
    mime_type = mime.guess_type(path)
    
    # Extract the directories from the full path.
    dirs = path.split("/")
    
    # Get the indecies of starting and ending point for the relative path.
    start = dirs.index(key)
    end = len(dirs)
    
    # Reconstruct the relative path to the source.
    for i in range(start, end):
        # Get the consolidation uuid.
        if str(dirs[i-1]) == "Consolidation":
            if len(dirs[i]) == 36:
                con_id = dirs[i]
            else:
                print("File Name Error in Consolidation")
                
        # Get the materials uuid.
        if str(dirs[i-1]) == "Materials":
            if len(dirs[i]) == 36:
                mat_id = dirs[i]
            else:
                print("File Name Error in Materials")
        
        # Get the relative path
        relative_path = str(relative_path) + "/" + str(dirs[i])
    
    dct_file = {
            'uuid': str(uuid.uuid4()),
            'con_id': con_id,
            'mat_id': mat_id,
            'filename': relative_path.lstrip("/"),
            'mime_type' : str(mime_type[0]),
            'alias' : alias,
            'status' : status,
            'public' : "FALSE",
            'lock' : is_lock,
            'source' : source,
            'operation' : operation,
            'operating_application' : operating_application,
            'caption' : caption,
            'descriptions' : descriptions
        }
    return(dct_file)

def updateFile_auto(dct_file):
    # Check the null value in each entry.
    for key, value in dct_file.items():
        if value == None or value == "":
            dct_file[key] = "NULL"
    
    # Initialyze the consolidation ID.
    fil_uuid = dct_file['uuid']
    fil_cuid = dct_file['con_id']
    fil_muid = dct_file['mat_id']
    fil_fnam = dct_file['filename']
    fil_mime = dct_file['mime_type']
    fil_alia = dct_file['alias']
    fil_stts = dct_file['status']
    fil_mpub = dct_file['public']
    fil_lock = dct_file['lock']
    fil_srce = dct_file['source']
    fil_oper = dct_file['operation']
    fil_opap = dct_file['operating_application']
    fil_capt = dct_file['caption']
    fil_desc = dct_file['descriptions']
        
    # Update the existing record.
    fil_vals = [fil_uuid, fil_cuid, fil_muid, fil_fnam, fil_mime, fil_alia, fil_stts, fil_mpub, fil_lock,fil_srce, fil_oper, fil_opap, fil_capt, fil_desc]
    
    # Create the SQL query for updating the new consolidation.
    sql_fil_ins = """INSERT INTO file (
                    uuid,
                    con_id, 
                    mat_id,
                    filename,
                    mime_type,
                    alias_name,
                    status,
                    make_public,
                    is_locked,
                    source,
                    file_operation,
                    operating_application,
                    caption, 
                    descriptions
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
    
    # Execute the query.
    executeSqlQuery(sql_fil_ins, fil_vals)

def main(root_dir):
    global DATABASE
    
    DATABASE = os.path.join(os.path.join(root_dir, "Table"), "project.db")
    
    res_img = getFilesWithExtensionList(root_dir, IMG_EXT)
    res_raw = getFilesWithExtensionList(root_dir, RAW_EXT)
    res_snd = getFilesWithExtensionList(root_dir, SND_EXT)
    
    for img in res_img:
        res_dict_img = getFileEditInfo(img, "Consolidation")
        updateFile_auto(res_dict_img)
    
    for raw in res_raw:
        res_dict_raw = getFileEditInfo(raw, "Consolidation", status="Original", lock=True, source="None", operation="Unknown")
        updateFile_auto(res_dict_raw)
    
    for snd in res_snd:
        res_dict_snd = getFileEditInfo(snd, "Consolidation", status="Unknown", lock=True, source="None", operation="Unknown")
        updateFile_auto(res_dict_snd)

if __name__ == '__main__':
    main()
    