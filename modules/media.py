#!/usr/bin/python
# -*- coding: UTF-8 -*-

# import the necessary packages
import os, sys, subprocess, tempfile, pipes, getopt, uuid
import shutil, time, math, tempfile, logging, pyexiv2, datetime
import modules.features as features
import modules.general as general

def mediaImporter(sop_object, item_path, in_dir, mat_uuid, con_uuid, dbfile):
    print("media::mediaImporter(sop_object, item_path, in_dir, mat_uuid, con_uuid, dbfile)")
    
    try:
        # Add a list for new objects if there are no objects.
        if sop_object.images == None: sop_object.images = list()
        if sop_object.sounds == None: sop_object.sounds = list()
        if sop_object.texts == None: sop_object.texts = list()
        
        # Define the path for saving files.
        img_path = os.path.join(item_path, "Images")
        img_path_main = os.path.join(img_path, "Main")
        img_path_raw = os.path.join(img_path, "Raw")
        snd_path = os.path.join(item_path, "Sounds")
        txt_path = os.path.join(item_path, "Texts")
        mov_path = os.path.join(item_path, "Movies")
        
        # Create empty lists for storeing file names.
        img_files = list()
        raw_files = list()
        snd_files = list()
        txt_files = list()
        mov_files = list()
        err_files = list()
        
        for in_fl in in_dir:
            name, ext = os.path.splitext(in_fl)
            
            # Check the extension of the file and append the file name to the list.
            if (ext.lower() == ".jpg" or ext.lower() == ".jpeg"): img_files.append(in_fl)   # JPEG files.
            if ext.lower() == ".arw": raw_files.append(in_fl)                               # RAW files (SONY).
            if (ext.lower() == ".wav" or ext.lower() == ".wave"): snd_files.append(in_fl)   # Sound files.
            if ext.lower() == ".txt": txt_files.append(in_fl)                               # Plane text.
    except Exception as e:
        print("Error occured in importing file settings.")
        print(str(e))
    
    # Importing JPEG files.
    try:
        # Move main images from the temporal directory to the object's directory.
        if len(img_files) > 0:
            for img_file in img_files:
                # Generate the GUID for the consolidation
                img_uuid = str(uuid.uuid4())
                
                # Get current time.
                now = datetime.datetime.utcnow().isoformat()
                
                # Define the destination file path.
                main_dest = os.path.join(img_path_main, img_uuid+".jpg")
                
                # Copy the original file.
                shutil.copy(img_file, main_dest)
                
                # Instantiate the File class.
                sop_img_file = features.File(is_new=True, uuid=None, dbfile=None)
                sop_img_file.material = mat_uuid
                sop_img_file.consolidation = con_uuid
                sop_img_file.filename = general.getRelativePath(main_dest, "Consolidation")
                sop_img_file.created_date = now
                sop_img_file.modified_date = now
                sop_img_file.file_type = "image"
                sop_img_file.alias = "Imported"
                sop_img_file.status = "Original"
                sop_img_file.lock = False
                sop_img_file.public = False
                sop_img_file.source = "Nothing"
                sop_img_file.operation = "Importing"
                sop_img_file.operating_application = "Survey Data Collector"
                sop_img_file.caption = "Imported image"
                sop_img_file.description = ""
                
                # Execute the SQL script.
                sop_img_file.dbInsert(dbfile)
                
                # Add the image to the boject.
                sop_object.images.insert(0, sop_img_file)
    except Exception as e:
        print("Error occured in image file import.")
        print(str(e))
    
    # Importing Raw files.
    try:
        if len(raw_files) > 0:
            for raw_file in raw_files:
                # Get original file name and its extention.
                name, ext = os.path.splitext(raw_file)
                
                # Generate the GUID for the consolidation
                raw_uuid = str(uuid.uuid4())
                
                # Get current time.
                now = datetime.datetime.utcnow().isoformat()
                
                # Define the destination file path.
                raw_dest = os.path.join(img_path_raw, raw_uuid + ext)
                
                # Copy the original file.
                shutil.copy(raw_file, raw_dest)
                
                # Instantiate the File class.
                sop_raw_file = features.File(is_new=True, uuid=None, dbfile=None)
                sop_raw_file.material = mat_uuid
                sop_raw_file.consolidation = con_uuid
                sop_raw_file.filename = general.getRelativePath(main_dest, "Consolidation")
                sop_raw_file.created_date = now
                sop_raw_file.modified_date = now
                sop_raw_file.file_type = "image"
                sop_raw_file.alias = "Imported"
                sop_raw_file.status = "Original(RAW)"
                sop_raw_file.lock = False
                sop_raw_file.public = False
                sop_raw_file.source = "Nothing"
                sop_raw_file.operation = "Importing"
                sop_raw_file.operating_application = "Survey Data Collector"
                sop_raw_file.caption = "Imported image"
                sop_raw_file.description = ""
                
                # Execute the SQL script.
                sop_raw_file.dbInsert(dbfile)
                
                # Add the image to the boject.
                sop_object.images.insert(0, sop_raw_file)
    except Exception as e:
        print("Error occured in raw file import.")
        print(str(e))
    
    # Importing Sound files.
    try:
        if len(snd_files) > 0:
            for snd_file in snd_files:
                # Generate the GUID for the consolidation
                snd_uuid = str(uuid.uuid4())
                
                # Get current time.
                now = datetime.datetime.utcnow().isoformat()
                
                # Define the destination file path.
                snd_dest = os.path.join(snd_path, snd_uuid+".wav")
                
                # Copy the original file.
                shutil.copy(snd_file, snd_dest)
                
                # Instantiate the File class.
                sop_snd_file = features.File(is_new=True, uuid=None, dbfile=None)
                sop_snd_file.material = mat_uuid
                sop_snd_file.consolidation = con_uuid
                sop_snd_file.filename = general.getRelativePath(snd_dest, "Consolidation")
                sop_snd_file.created_date = now
                sop_snd_file.modified_date = now
                sop_snd_file.file_type = "audio"
                sop_snd_file.alias = "Imported"
                sop_snd_file.status = "Original"
                sop_snd_file.lock = False
                sop_snd_file.public = False
                sop_snd_file.source = "Nothing"
                sop_snd_file.operation = "Importing"
                sop_snd_file.operating_application = "Survey Data Collector"
                sop_snd_file.caption = "Original audio"
                sop_snd_file.description = ""
                
                # Insert the new entry into the database.
                sop_snd_file.dbInsert(dbfile)
                
                # Add the image to the boject.
                sop_object.sounds.insert(0, sop_snd_file)
    except Exception as e:
        print("Error occured in sound file import.")
        print(str(e))
    
    # Importing Texts files.
    try:
        if len(txt_files) > 0:
            for txt_file in txt_files:
                # Generate the GUID for the consolidation
                txt_uuid = str(uuid.uuid4())
                
                # Get current time.
                now = datetime.datetime.utcnow().isoformat()
                
                # Define the destination file path.
                txt_dest = os.path.join(txt_path, txt_uuid +".txt")
                
                # Copy the original file.
                shutil.copy(txt_file, txt_dest)
                
                # Instantiate the File class.
                sop_txt_file = features.File(is_new=True, uuid=None, dbfile=None)
                sop_txt_file.material = mat_uuid
                sop_txt_file.consolidation = con_uuid
                sop_txt_file.filename = general.getRelativePath(txt_dest, "Consolidation")
                sop_txt_file.created_date = now
                sop_txt_file.modified_date = now
                sop_txt_file.file_type = "text"
                sop_txt_file.alias = "Imported"
                sop_txt_file.status = "Original"
                sop_txt_file.lock = False
                sop_txt_file.public = False
                sop_txt_file.source = "Nothing"
                sop_txt_file.operation = "Importing"
                sop_txt_file.operating_application = "Survey Data Collector"
                sop_txt_file.caption = "Original text"
                sop_txt_file.description = ""
                
                # Insert the new entry into the database.
                sop_txt_file.dbInsert(dbfile)
                
                # Add the image to the boject.
                sop_object.texts.insert(0, sop_txt_file)
    except Exception as e:
        print("Error occured in text file import.")
        print(str(e))

