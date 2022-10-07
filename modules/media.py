#!/usr/bin/python
# -*- coding: UTF-8 -*-

# import the necessary packages
import os, sys, subprocess, tempfile, pipes, getopt, uuid
import shutil, time, math, tempfile, logging, pyexiv2, datetime

import objects.features as features
import modules.general as general
import modules.error as error

def checkMediaType(file_path):
    print("media::checkMediaType(file_path)")
    name, ext = os.path.splitext(file_path)

    # Check the extension of the file and append the file name to the list.
    if ext.lower() == ".jpg": return("image")       # JPEG files.
    elif ext.lower() == ".jpeg": return("image")    # JPEG files.
    elif ext.lower() == ".tif": return("image")    # JPEG files.
    elif ext.lower() == ".tiff": return("image")    # JPEG files.
    elif ext.lower() == ".png": return("image")     # JPEG files.
    elif ext.lower() == ".arw": return("raw")       # RAW files.
    elif ext.lower() == ".wave": return("audio")    # Sound files.
    elif ext.lower() == ".wav": return("audio")     # Sound files.
    elif ext.lower() == ".mp3": return("audio")     # Sound files.
    elif ext.lower() == ".mov": return("movie")     # Movie files.
    elif ext.lower() == ".mp4": return("movie")     # Movie files.
    elif ext.lower() == ".txt": return("text")      # Text file
    elif ext.lower() == ".wkt": return("geometry")  # WKT file
    else: return("unknown")

def mediaImporter(sop_object, item_path, in_dir, mat_uuid, con_uuid, dbfile):
    print("media::mediaImporter(sop_object, item_path, in_dir, mat_uuid, con_uuid, dbfile)")

    try:
        # Add a list for new objects if there are no objects.
        if sop_object.images == None: sop_object.images = list()
        if sop_object.sounds == None: sop_object.sounds = list()
        if sop_object.movies == None: sop_object.movies = list()
        if sop_object.texts == None: sop_object.texts = list()
        if sop_object.geometries == None: sop_object.geometries = list()

        # Define the path for saving files.
        img_path = os.path.join(item_path, "Images"); general.createPathIfNotExists(img_path)
        img_path_main = os.path.join(img_path, "Main"); general.createPathIfNotExists(img_path_main)
        img_path_raw = os.path.join(img_path, "Raw"); general.createPathIfNotExists(img_path_raw)
        snd_path = os.path.join(item_path, "Sounds"); general.createPathIfNotExists(snd_path)
        mov_path = os.path.join(item_path, "Movies"); general.createPathIfNotExists(mov_path)
        txt_path = os.path.join(item_path, "Texts"); general.createPathIfNotExists(txt_path)
        geo_path = os.path.join(item_path, "Geometries"); general.createPathIfNotExists(geo_path)

        # Create empty lists for storeing file names.
        img_files = list()
        raw_files = list()
        snd_files = list()
        txt_files = list()
        mov_files = list()
        geo_files = list()
        err_files = list()

        for in_fl in in_dir:
            name, ext = os.path.splitext(in_fl)

            # Check the extension of the file and append the file name to the list.
            if checkMediaType(in_fl) == "image": img_files.append(in_fl)        # Image file
            elif checkMediaType(in_fl) == "raw": raw_files.append(in_fl)        # RAW file
            elif checkMediaType(in_fl) == "audio": snd_files.append(in_fl)      # Audio file
            elif checkMediaType(in_fl) == "movie": mov_files.append(in_fl)      # Movie file
            elif checkMediaType(in_fl) == "text": txt_files.append(in_fl)       # Plane text
            elif checkMediaType(in_fl) == "geometry": geo_files.append(in_fl)   # WKT files
    except Exception as e:
        print("Error occured in importing file settings.")
        print(str(e))
        error.ErrorMessageUnknown(details=str(e), show=True, language="en")
        return(None)

    # Importing JPEG files.
    try:
        # Move main images from the temporal directory to the object's directory.
        if not (len(img_files) == 0 or img_files == None):
            for img_file in img_files:
                # Generate the GUID for the consolidation
                img_uuid = str(uuid.uuid4())

                # Get current time.
                now = datetime.datetime.utcnow().isoformat()

                # Get the extension of the file
                main_name, main_ext = os.path.splitext(img_file)

                # Define the destination file path.
                main_dest = os.path.join(img_path_main, img_uuid + main_ext)

                # Copy the original file.
                shutil.copy(img_file, main_dest)

                # Instantiate the File class.
                sop_img_file = features.File(is_new=True, uuid=img_uuid, dbfile=None)
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
                sop_img_file.operation = "Imported"
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
        error.ErrorMessageUnknown(details=str(e), show=True, language="en")
        return(None)

    # Importing Raw files.
    try:
        if not (len(raw_files) == 0 or raw_files == None):
            for raw_file in raw_files:
                # Generate the GUID for the consolidation
                raw_uuid = str(uuid.uuid4())

                # Get current time.
                now = datetime.datetime.utcnow().isoformat()

                # Get the extension of the file
                raw_name, raw_ext = os.path.splitext(raw_files)

                # Define the destination file path.
                raw_dest = os.path.join(img_path_raw, raw_uuid + raw_ext)

                # Copy the original file.
                shutil.copy(raw_file, raw_dest)

                # Instantiate the File class.
                sop_raw_file = features.File(is_new=True, uuid=raw_uuid, dbfile=None)
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
                sop_raw_file.operation = "Imported"
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
        error.ErrorMessageUnknown(details=str(e), show=True, language="en")
        return(None)

    # Importing Sound files.
    try:
        if not (len(snd_files) == 0 or snd_files == None):
            for snd_file in snd_files:
                # Generate the GUID for the consolidation
                snd_uuid = str(uuid.uuid4())

                # Get current time.
                now = datetime.datetime.utcnow().isoformat()

                # Get the extension of the file
                snd_name, snd_ext = os.path.splitext(snd_file)

                # Define the destination file path.
                snd_dest = os.path.join(snd_path, snd_uuid + snd_ext)

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
                sop_snd_file.operation = "Imported"
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
        error.ErrorMessageUnknown(details=str(e), show=True, language="en")
        return(None)

    # Importing Texts files.
    try:
        if not (len(txt_files) > 0 or txt_files == None):
            for txt_file in txt_files:
                # Generate the GUID for the consolidation
                txt_uuid = str(uuid.uuid4())

                # Get current time.
                now = datetime.datetime.utcnow().isoformat()

                # Get the extension of the file
                txt_name, txt_ext = os.path.splitext(txt_path)

                # Define the destination file path.
                txt_dest = os.path.join(txt_path, txt_uuid + txt_ext)

                # Copy the original file.
                shutil.copy(txt_file, txt_dest)

                # Instantiate the File class.
                sop_txt_file = features.File(is_new=True, uuid=txt_uuid, dbfile=None)
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
                sop_txt_file.operation = "Imported"
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
        error.ErrorMessageUnknown(details=str(e), show=True, language="en")
        return(None)

    # Importing movies files.
    try:
        if not (len(mov_files) == 0 or mov_files == None):
            for mov_file in mov_files:
                # Generate the GUID for the consolidation
                mov_uuid = str(uuid.uuid4())

                # Get current time.
                now = datetime.datetime.utcnow().isoformat()

                # Get the extension of the file
                mov_name, mov_ext = os.path.splitext(mov_file)

                # Define the destination file path.
                mov_dest = os.path.join(mov_path, mov_uuid + mov_ext)

                # Copy the original file.
                shutil.copy(mov_file, mov_dest)

                # Instantiate the File class.
                sop_mov_file = features.File(is_new=True, uuid=mov_uuid, dbfile=None)
                sop_mov_file.material = mat_uuid
                sop_mov_file.consolidation = con_uuid
                sop_mov_file.filename = general.getRelativePath(mov_dest, "Consolidation")
                sop_mov_file.created_date = now
                sop_mov_file.modified_date = now
                sop_mov_file.file_type = "movie"
                sop_mov_file.alias = "Imported"
                sop_mov_file.status = "Original"
                sop_mov_file.lock = False
                sop_mov_file.public = False
                sop_mov_file.source = "Nothing"
                sop_mov_file.operation = "Imported"
                sop_mov_file.operating_application = "Survey Data Collector"
                sop_mov_file.caption = "Original text"
                sop_mov_file.description = ""

                # Insert the new entry into the database.
                sop_mov_file.dbInsert(dbfile)

                # Add the image to the boject.
                sop_object.movies.insert(0, sop_mov_file)
    except Exception as e:
        print("Error occured in movie file import.")
        print(str(e))
        error.ErrorMessageUnknown(details=str(e), show=True, language="en")
        return(None)

    # Importing geoies files.
    try:
        if not (len(geo_files) == 0 or geo_files == None):
            for geo_file in geo_files:
                # Generate the GUID for the consolidation
                geo_uuid = str(uuid.uuid4())

                # Get current time.
                now = datetime.datetime.utcnow().isoformat()

                # Define the destination file path.
                geo_dest = os.path.join(geo_path, geo_uuid +".wkt")

                # Copy the original file.
                shutil.copy(geo_file, geo_dest)

                # Instantiate the File class.
                sop_geo_file = features.File(is_new=True, uuid=geo_uuid, dbfile=None)
                sop_geo_file.material = mat_uuid
                sop_geo_file.consolidation = con_uuid
                sop_geo_file.filename = general.getRelativePath(geo_dest, "Consolidation")
                sop_geo_file.created_date = now
                sop_geo_file.modified_date = now
                sop_geo_file.file_type = "geometry"
                sop_geo_file.alias = "Imported"
                sop_geo_file.status = "Original"
                sop_geo_file.lock = False
                sop_geo_file.public = False
                sop_geo_file.source = "Nothing"
                sop_geo_file.operation = "Imported"
                sop_geo_file.operating_application = "Survey Data Collector"
                sop_geo_file.caption = "Original geometry"
                sop_geo_file.description = ""

                # Insert the new entry into the database.
                sop_geo_file.dbInsert(dbfile)

                # Add the image to the boject.
                sop_object.geoies.insert(0, sop_geo_file)
    except Exception as e:
        print("Error occured in geoie file import.")
        print(str(e))
        error.ErrorMessageUnknown(details=str(e), show=True, language="en")
        return(None)
