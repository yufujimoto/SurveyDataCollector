#!/usr/bin/python
# coding: UTF-8

import os, sys, subprocess, uuid as unique
from lxml import etree as et
import sqlite3 as sqlite
from sqlite3 import Error

import modules.error as error

class SimpleObject(object):
    def __init__(self, is_new, uuid, dbfile):
        if is_new == True:
            if not uuid == None:
                self._uuid = uuid
            else:
                self._uuid = str(unique.uuid4()) 
        else:
            self._uuid = None
    
    @property
    def id(self): return self._id
    @property
    def uuid(self): return self._uuid
    
    @id.setter
    def id(self, value): self._id = value
    @uuid.setter
    def uuid(self, value): self._uuid = value
    
    def excuteSQL(self, dbfile, sql, values):
        # Convert None objects into "Null" values in DB table.
        db_values = list()
        for value in values:
            if value == None or value == "":
                db_values.append("NULL")
            else:
                db_values.append(value)
                
        # Execute the query.
        try:
            # Establish the connection to the DataBase file.
            conn = sqlite.connect(dbfile)
            
            if conn is not None:
                # Instantiate the cursor for query.
                cur = conn.cursor()
                
                # Execute the query.
                cur.execute(sql, db_values)
                
                # Commit the result of the query.
                conn.commit()
        except Error as e:
            # Create error messages.
            error = {
                'title': "エラーが発生しました",
                'message': "データベースに統合体の情報を挿入できませんでした。",
                'info': "SQLiteのデータベース・ファイルあるいはデータベースの設定を確認してください。",
                'icon': "Critical",
                'detailed': e.args[0]
            }
            print(e.args[0])
            # Returns error messages.
            return(error)
        finally:
            # Finally close the connection.
            conn.close()
    
    def fetchOneSQL(self, dbfile, sql, keys):
        # Establish the connection between DB.
        conn = sqlite.connect(dbfile)
        
        if conn is not None:
            # Instantiate the cursor for query.
            cur = conn.cursor()
            
            # Execute the query.
            cur.execute(sql, keys)
            
            # Fetch one row.
            rows = cur.fetchone()
            entry = list()
            
            # Replace NULL values by blank.
            for row in rows:
                if row == "NULL":
                    entry.append("")
                else:
                    entry.append(row)
            
            # Get attributes from the row.
            return(entry)
        else:
            return(None)
    
    def fetchAllSQL(self, dbfile, sql, keys):
        # Establish the connection between DB.
        conn = sqlite.connect(dbfile)
        
        if conn is not None:
            # Instantiate the cursor for query.
            cur = conn.cursor()
            
            # Execute the query.
            cur.execute(sql, keys)
            
            # Fetch one row.
            rows = cur.fetchall()
            
            entries = list()
            
            # Replace NULL values by blank.
            for row in rows:
                entry = list()
                
                for value in row:
                    if value == "NULL":
                        entry.append("")
                    else:
                        entry.append(value)
                entries.append(entry)
            
            # Get attributes from the row.
            return(entries)
        else:
            return(None)

class Consolidation(SimpleObject):
    @property
    def name(self): return self._name
    @property
    def geographic_annotation(self): return self._geographic_annotation
    @property
    def temporal_annotation(self): return self._temporal_annotation
    @property
    def images(self): return self._images
    @property
    def sounds(self): return self._sounds
    @property
    def texts(self): return self._texts
    @property
    def additionalAttributes(self): return self._additionalAttributes
    @property
    def description(self): return self._description
    
    @name.setter
    def name(self, value): self._name = value
    @geographic_annotation.setter
    def geographic_annotation(self, value): self._geographic_annotation = value
    @temporal_annotation.setter
    def temporal_annotation(self, value): self._temporal_annotation = value
    @images.setter
    def images(self, value): self._images = value
    @sounds.setter
    def sounds(self, value): self._sounds = value
    @texts.setter
    def texts(self, value): self._texts = value
    @additionalAttributes.setter
    def additionalAttributes(self, value): self._additionalAttributes = value
    @description.setter
    def description(self, value): self._description = value
    
    def __init__(self, is_new=True, uuid=None, dbfile=None):
        # Initialize the super class.
        SimpleObject.__init__(self, is_new, uuid, dbfile)
        
        if is_new == True and dbfile == None:
            # Initialize as the new instance.
            self._name = None
            self._geographic_annotation = None
            self._temporal_annotation = None
            self._images = list()
            self._sounds = list()
            self._texts = list()
            self._additionalAttributes = list()
            self._description = None
            self._objectPath = None
        elif is_new == False and uuid != None and dbfile != None:
            # Initialize by the DB instance.
            self._initInstanceByUuid(uuid, dbfile)
        else:
            # Other unexpected case.
            return(None)
    
    # operation
    def _initInstanceByUuid(self, uuid, dbfile):
        print("Consolidation::_initInstanceByUuid(self, uuid, dbfile)")
        
        try:
            # Make the SQL statement.
            sql_select = """SELECT  id,
                                    name,
                                    geographic_annotation,
                                    temporal_annotation,
                                    description
                            FROM consolidation WHERE uuid=?"""
            
            # Fech one from DB.
            entry = super(Consolidation, self).fetchOneSQL(dbfile, sql_select, [uuid])
            
            if not entry == None:
                # Get attributes from the row.
                self._id = entry[0]
                self._uuid = uuid
                self._name = entry[1]
                self._geographic_annotation = entry[2]
                self._temporal_annotation = entry[3]
                self._images = self._getFileList(dbfile, "image")
                self._sounds = self._getFileList(dbfile, "audio")
                self._texts = self._getFileList(dbfile, "text")
                self._additionalAttributes = self._getAdditionalAttributes(dbfile)
                self._description = entry[4]
            else:
                return(None)
        except Exception as e:
            err_info = "Error occus in Consolidation::_initInstanceByUuid(self, uuid, dbfile)"
            print(err_info)
            print(str(e))
            error.ErrorCurrentFeature(information=err_info, details=str(e))
    
    def dbInsert(self, dbfile):
        print("Consolidation::dbInsert(self, dbfile)")
        
        try:
            # Insert a new record into the database
            values = [
                self._uuid,
                self._name,
                self._geographic_annotation,
                self._temporal_annotation,
                self._description
            ]
            
            # Create the SQL query for inserting the new consolidation.
            sql_insert = """INSERT INTO consolidation (
                        uuid, 
                        name, 
                        geographic_annotation, 
                        temporal_annotation, 
                        description
                    ) VALUES (?,?,?,?,?)"""
            
            # Execute the query.
            super(Consolidation, self).excuteSQL(dbfile, sql_insert, values)
            
            # Insert images of the Consolidation.
            if not self._images == None:
                if len(self._images) <= 0:
                    for image in self._images: image.dbInsert(dbfile)
            
            # Insert sounds of the Consolidation.
            if not self._sounds == None:
                if not len(self._sounds) <= 0:
                    for sound in self._sounds: sound.dbInsert(dbfile)
            
            # Insert texts of the Consolidation.
            if not self._texts == None:
                if not len(self._texts) <= 0:
                    for text in self._texts: text.dbInsert(dbfile)
            
            # Insert additional attributes.
            if not self._additionalAttributes == None:
                if not len(self._additionalAttributes) <= 0:
                    for additionalAttribute in self._additionalAttributes:
                        additionalAttribute.dbInsert(dbfile, "consolidation", self._uuid)
        except Exception as e:
            err_info = "Error occus in Consolidation::dbInsert(self, dbfile)"
            print(err_info)
            print(str(e))
            error.ErrorCurrentFeature(information=err_info, details=str(e))
    
    def dbUpdate(self, dbfile):
        print("consolidation::dbUpdate(self, dbfile)")
        
        try:
            # Insert a new record into the database
            values = [
                self._name,
                self._geographic_annotation,
                self._temporal_annotation,
                self._description,
                self._uuid
            ]
            
            # Create the SQL query for updating the new consolidation.
            sql_update = """UPDATE consolidation
                        SET 
                            name = ?, 
                            geographic_annotation = ?, 
                            temporal_annotation = ?, 
                            description = ?
                        WHERE uuid = ?"""
            
            # Execute the query.
            super(Consolidation, self).excuteSQL(dbfile, sql_update, values)
            
            # Update images of the Consolidation.
            if not self._images == None:
                if len(self._images) <= 0:
                    for image in self._images: image.dbUpdate(dbfile)
            
            # Update sounds of the Consolidation.
            if not self._sounds == None:
                if not len(self._sounds) <= 0:
                    for sound in self._sounds: sound.dbUpdate(dbfile)
            
            # Update text of the Consolidation.
            if not self._texts == None:
                if not len(self._texts) <= 0:
                    for text in self._texts: text.dbUpdate(dbfile)
            
            # Update additional attributes.
            if not self._additionalAttributes == None:
                if not len(self._additionalAttributes) <= 0:
                    for additionalAttribute in self._additionalAttributes:
                        additionalAttribute.dbUpdate(dbfile)
        except Exception as e:
            err_info = "Error occus in Consolidation::dbUpdate(self, dbfile)"
            print(err_info)
            print(str(e))
            error.ErrorCurrentFeature(information=err_info, details=str(e))
    
    def dbDrop(self, dbfile):
        print("Consolidation::dbDrop(self, dbfile)")
        
        try:
            # Dropt the exsiting entry from the DB.
            values = [self._uuid]
            
            # Create the SQL query for deleting the existing consolidation.
            sql_delete = """DELETE FROM consolidation WHERE uuid = ?"""
            
            # Execute the query.
            super(Consolidation, self).excuteSQL(dbfile, sql_delete, values)
        except Exception as e:
            err_info = "Error occus in Consolidation::dbDrop(self, dbfile)"
            print(err_info)
            print(str(e))
            error.ErrorCurrentFeature(information=err_info, details=str(e))
    
    def _getFileList(self, dbfile, file_type):
        print("Consolidation::_getFileList(self, dbfile, file_type)")
        
        # Initialyze the return value.
        sop_file_list = list()
        
        try:
            # Get image files related to the consolidation.
            sql_select = """SELECT uuid FROM file WHERE con_id = ? AND mat_id="NULL" AND file_type=? ORDER BY id DESC;"""
            
            # Execute the query.
            sop_files = super(Consolidation, self).fetchAllSQL(dbfile, sql_select, [self._uuid, file_type])
            
            # Exit if there are no entries.
            if sop_files == None or len(sop_files) == 0: return(None)
            
            # Create sop image ojects from the DB table.
            for sop_file in sop_files:
                sop_file_list.append(File(is_new=False, uuid=sop_file[0], dbfile=dbfile))
                
            return(sop_file_list)
        except Exception as e:
            err_info = "Error occus in Consolidation::_getFileList(self, dbfile, file_type)"
            print(err_info)
            print(str(e))
            error.ErrorCurrentFeature(information=err_info, details=str(e))
    
    def _getAdditionalAttributes(self, dbfile):
        print("Consolidation::_getAdditionalAttributes(self, dbfile)")
        
        # Initialyze the return value.
        sop_attr_list = list()
        
        try:
            # Get image files related to the consolidation.
            sql_select = """SELECT uuid FROM additional_attribute WHERE ref_table = 'consolidation' AND ref_uuid=?;"""
            
            # Execute the query.
            sop_attrs = super(Consolidation, self).fetchAllSQL(dbfile, sql_select, [self._uuid])
            
            # Exit if there are no entries.
            if (sop_attrs == None or len(sop_attrs) <= 0): return(sop_attr_list)
            
            # Create sop image ojects from the DB table.
            for sop_attr in sop_attrs:
                sop_attr_list.append(AdditionalAttribute(is_new=False, uuid=sop_attr[0], dbfile=dbfile, ref_table="consolidation", ref_uuid=self._uuid))
            
            return(sop_attr_list)
        except Exception as e:
            err_info = "Error occus in Consolidation::_getAdditionalAttributes(self, dbfile)"
            print(err_info)
            print(str(e))
            error.ErrorCurrentFeature(information=err_info, details=str(e))
        
class Material(SimpleObject):
    def __init__(self, is_new = True, uuid=None, dbfile=None):
        # Initialize the super class.
        SimpleObject.__init__(self, is_new, uuid, dbfile)
        
        if is_new == True and dbfile == None:
            # Initialize as the new instance.
            self._consolidation = None
            self._name = None
            self._estimated_period_beginning = None
            self._estimated_period_peak = None
            self._estimated_period_ending = None
            self._latitude = None
            self._longitude = None
            self._altitude = None
            self._material_number = None
            self._images = list()
            self._sounds = list()
            self._texts = list()
            self._additionalAttributes = list()
            self._description = None
        elif is_new == False and uuid != None and dbfile != None:
            # Initialize by the DB instance.
            self._initInstanceByUuid(uuid, dbfile)
        else:
            # Other unexpected case.
            return(None)
    
    @property
    def consolidation(self): return self._consolidation
    @property
    def name(self): return self._name
    @property
    def estimated_period_beginning(self): return self._estimated_period_beginning
    @property
    def estimated_period_peak(self): return self._estimated_period_peak
    @property
    def estimated_period_ending(self): return self._estimated_period_ending
    @property
    def latitude(self): return self._latitude
    @property
    def longitude(self): return self._longitude
    @property
    def altitude(self): return self._altitude
    @property
    def material_number(self): return self._material_number
    @property
    def images(self): return self._images
    @property
    def sounds(self): return self._sounds
    @property
    def texts(self): return self._texts
    @property
    def additionalAttributes(self): return self._additionalAttributes
    @property
    def description(self): return self._description
    
    @consolidation.setter
    def consolidation(self, value): self._consolidation = value
    @name.setter
    def name(self, value): self._name = value
    @estimated_period_beginning.setter
    def estimated_period_beginning(self, value): self._estimated_period_beginning = value
    @estimated_period_peak.setter
    def estimated_period_peak(self, value): self._estimated_period_peak = value
    @estimated_period_ending.setter
    def estimated_period_ending(self, value): self._estimated_period_ending = value
    @latitude.setter
    def latitude(self, value): self._latitude = value
    @longitude.setter
    def longitude(self, value): self._longitude = value
    @altitude.setter
    def altitude(self, value): self._altitude = value
    @material_number.setter
    def material_number(self, value): self._material_number = value
    @images.setter
    def images(self, value): self._images = value
    @sounds.setter
    def sounds(self, value): self._sounds = value
    @texts.setter
    def texts(self, value): self._texts = value
    @additionalAttributes.setter
    def additionalAttributes(self, value): self._additionalAttributes = value
    @description.setter
    def description(self, value): self._description = value
    
    # operation
    def _initInstanceByUuid(self, uuid, dbfile):
        print("Material::_initInstanceByUuid(self, uuid, dbfile)")
        
        try:
            # Make the SQL statement.
            sql_select = """SELECT  id,
                                    con_id,
                                    name,
                                    material_number,
                                    estimated_period_beginning,
                                    estimated_period_peak,
                                    estimated_period_ending,
                                    latitude,
                                    longitude,
                                    altitude,
                                    material_number,
                                    description
                                FROM material WHERE uuid=?"""
            
            # Fech one from DB.
            entry = super(Material, self).fetchOneSQL(dbfile, sql_select, [uuid])
            
            if not entry == None:
                # Get attributes from the row.
                self._id = entry[0]
                self._uuid = uuid
                self._consolidation = entry[1]
                self._name = entry[2]
                self._material_number = entry[3]
                self._estimated_period_beginning = entry[4]
                self._estimated_period_peak = entry[5]
                self._estimated_period_ending = entry[6]
                self._latitude = entry[7]
                self._longitude = entry[8]
                self._altitude = entry[9]
                self._material_number = entry[10]
                self._images = self._getFileList(dbfile, "image")
                self._sounds = self._getFileList(dbfile, "audio")
                self._texts = self._getFileList(dbfile, "text")
                self._additionalAttributes = self._getAdditionalAttributes(dbfile)
                self._description = entry[11]
            else:
                return(None)
        
        except Exception as e:
            err_info = "Error occus in Material::_initInstanceByUuid(self, uuid, dbfile)"
            print(err_info)
            print(str(e))
            error.ErrorCurrentFeature(information=err_info, details=str(e))
    
    def dbInsert(self, dbfile):
        print("Material::dbInsert(self, dbfile)")
        
        try:
            # Insert a new record into the database
            values = [
                self._uuid,
                self._consolidation,
                self._name,
                self._material_number,
                self._estimated_period_beginning,
                self._estimated_period_peak,
                self._estimated_period_ending,
                self._latitude,
                self._longitude,
                self._altitude,
                self._description
            ]
            
            # Create the SQL query for inserting the new material.
            sql_insert = """INSERT INTO material (
                        uuid,
                        con_id, 
                        name,
                        material_number,
                        estimated_period_beginning,
                        estimated_period_peak,
                        estimated_period_ending,
                        latitude,
                        longitude,
                        altitude,
                        description
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?)"""
            
            # Execute the query.
            super(Material, self).excuteSQL(dbfile, sql_insert, values)
            
            # Insert images of the Material.
            if not self._images == None:
                if len(self._images) <= 0:
                    for image in self._images: image.dbInsert(dbfile)
            
            # Insert sounds of the Material.
            if not self._sounds == None:
                if not len(self._sounds) <= 0:
                    for sound in self._sounds: sound.dbInsert(dbfile)
            
            # Insert texts of the Material.
            if not self._texts == None:
                if not len(self._texts) <= 0:
                    for text in self._texts: text.dbInsert(dbfile)
            
            # Insert additional attributes.
            if not self._additionalAttributes == None:
                if not len(self._additionalAttributes) <= 0:
                    for additionalAttribute in self._additionalAttributes:
                        additionalAttribute.dbInsert(dbfile, "material", self._uuid)
        except Exception as e:
            err_info = "Error occus in Material::dbInsert(self, dbfile)"
            print(err_info)
            print(str(e))
            error.ErrorCurrentFeature(information=err_info, details=str(e))
    
    def dbUpdate(self, dbfile):
        print("Material::dbUpdate(self, dbfile)")
        
        try:
            # Insert a new record into the database
            values = [
                self._name,
                self._material_number,
                self._estimated_period_beginning,
                self._estimated_period_peak,
                self._estimated_period_ending,
                self._latitude,
                self._longitude,
                self._altitude,
                self._description,
                self._uuid
            ]
            
            # Create the SQL query for updating the new material.
            sql_update = """UPDATE material
                        SET
                            name = ?,
                            material_number = ?,
                            estimated_period_beginning = ?,
                            estimated_period_peak = ?,
                            estimated_period_ending = ?,
                            latitude = ?,
                            longitude = ?,
                            altitude = ?,
                            description = ?
                        WHERE uuid = ?"""
            
            # Execute the query.
            super(Material, self).excuteSQL(dbfile, sql_update, values)
            
            if not self._images == None:
                if len(self._images) <= 0:
                    for image in self._images: image.dbUpdate(dbfile)
            
            # Insert sounds of the Material.
            if not self._sounds == None:
                if not len(self._sounds) <= 0:
                    for sound in self._sounds: sound.dbUpdate(dbfile)
            
            # Insert texts of the Material.
            if not self._texts == None:
                if not len(self._texts) <= 0:
                    for text in self._texts: text.dbUpdate(dbfile)
            
            # Insert additional attributes.
            if not self._additionalAttributes == None:
                if not len(self._additionalAttributes) <= 0:
                    for additionalAttribute in self._additionalAttributes:
                        additionalAttribute.dbUpdate(dbfile)
        except Exception as e:
            err_info = "Error occus in Material::dbUpdate(self, dbfile)"
            print(err_info)
            print(str(e))
            error.ErrorCurrentFeature(information=err_info, details=str(e))
    
    def dbDrop(self, dbfile):
        print("Material::dbDrop(self, dbfile)")
        
        try:
            # Dropt the exsiting entry from the DB.
            values = [self._uuid]
            
            # Create the SQL query for deleting the existing materials.
            sql_delete = """DELETE FROM material WHERE uuid = ?"""
            
            # Execute the query.
            super(Material, self).excuteSQL(dbfile, sql_delete, values)
        except Exception as e:
            err_info = "Error occus in Material::dbDrop(self, dbfile)"
            print(err_info)
            print(str(e))
            error.ErrorCurrentFeature(information=err_info, details=str(e))
            
    def _getFileList(self, dbfile, file_type):
        print("Material::_getFileList(self, dbfile, file_type)")
        
        # Initialyze the return value.
        sop_file_list = list()
        
        try:
            sql_select = """SELECT uuid FROM file WHERE con_id = ? AND mat_id=? AND file_type=? ORDER BY id DESC;"""
            
            # Execute the query.
            sop_files = super(Material, self).fetchAllSQL(dbfile, sql_select, [self._consolidation, self._uuid, file_type])
            
            # Create sop image ojects from the DB table.
            for sop_file in sop_files:
                sop_file_list.append(File(is_new=False, uuid=sop_file[0], dbfile=dbfile))
                
            return(sop_file_list)
        except:
            print("Error in instantiating the File object.")
    
    def _getAdditionalAttributes(self, dbfile):
        print("Material::_getAdditionalAttributes(self, dbfile)")
        
        # Initialyze the return value.
        sop_attr_list = list()
        
        try:
            # Get image files related to the consolidation.
            sql_select = """SELECT uuid FROM additional_attribute WHERE ref_table = 'material' AND ref_uuid=? ORDER BY id;"""
            
            # Execute the query.
            sop_attrs = super(Material, self).fetchAllSQL(dbfile, sql_select, [self._uuid])
            
            # Create sop image ojects from the DB table.
            for sop_attr in sop_attrs:
                sop_attr_list.append(AdditionalAttribute(is_new=False, uuid=sop_attr[0], dbfile=dbfile, ref_table="material", ref_uuid=self._uuid))
                
            return(sop_attr_list)
        except Exception as e:
            print(str(e))

class File(SimpleObject):
    def __init__(self, is_new = True, uuid=None, dbfile=None):
        SimpleObject.__init__(self, is_new, uuid, dbfile)
        
        if is_new == True and dbfile == None:
            self._consolidation = None
            self._material = None
            self._filename = None
            self._created_date = None
            self._modified_date = None
            self._file_type = None
            self._alias = None
            self._status = None
            self._public = None
            self._lock = None
            self._source = None
            self._operation = None
            self._operating_application = None
            self._caption = None
            self._description = None
        elif is_new == False and uuid != None and dbfile != None:
            # Initialize by the DB instance.
            self._initInstanceByUuid(uuid, dbfile)
    
    @property
    def material(self): return self._material
    @property
    def consolidation(self): return self._consolidation
    @property
    def filename(self): return self._filename
    @property
    def created_date(self): return self._created_date
    @property
    def modified_date(self): return self._modified_date
    @property
    def file_type(self): return self._file_type
    @property
    def alias(self): return self._alias
    @property
    def status(self): return self._status
    @property
    def public(self): return self._public
    @property
    def lock(self): return self._lock
    @property
    def source(self): return self._source
    @property
    def operation(self): return self._operation
    @property
    def operating_application(self): return self._operating_application
    @property
    def caption(self): return self._caption
    @property
    def description(self): return self._description    
    
    @material.setter
    def material(self, value): self._material = value
    @consolidation.setter
    def consolidation(self, value): self._consolidation = value
    @filename.setter
    def filename(self, value): self._filename = value
    @created_date.setter
    def created_date(self, value): self._created_date = value
    @modified_date.setter
    def modified_date(self, value): self._modified_date = value
    @file_type.setter
    def file_type(self, value): self._file_type = value
    @alias.setter
    def alias(self, value): self._alias = value
    @status.setter
    def status(self, value): self._status = value
    @public.setter
    def public(self, value): self._public = value
    @lock.setter
    def lock(self, value): self._lock = value
    @source.setter
    def source(self, value): self._source = value
    @source.setter
    def source(self, value): self._source = value
    @operation.setter
    def operation(self, value): self._operation = value
    @operating_application.setter
    def operating_application(self, value): self._operating_application = value
    @caption.setter
    def caption(self, value): self._caption = value
    @description.setter
    def description(self, value): self._description = value
    
    # operation
    def _initInstanceByUuid(self, uuid, dbfile):
        # Make the SQL statement.
        sql_select = """SELECT
                            id,
                            con_id, 
                            mat_id,
                            created_date,
                            modified_date,
                            file_name,
                            file_type,
                            make_public,
                            alias_name,
                            status,
                            is_locked,
                            source, 
                            file_operation,
                            operating_application,
                            caption,
                            description
                        FROM file WHERE uuid=?"""
        
        # Fech one from DB.
        entry = super(File, self).fetchOneSQL(dbfile, sql_select, [uuid])
        
        if not entry == None:
            # Get attributes from the row.
            self._id = str(entry[0])
            self._uuid = str(uuid)
            self._consolidation = str(entry[1])
            self._material = str(entry[2])
            self._created_date = str(entry[3])
            self._modified_date = str(entry[4])
            self._filename = str(entry[5])
            self._file_type = str(entry[6])
            self._public = str(entry[7])
            self._alias = str(entry[8])
            self._status = str(entry[9])
            self._lock = str(entry[10])
            self._source = str(entry[11])
            self._operation = str(entry[12])
            self._operating_application = str(entry[13])
            self._caption = str(entry[14])
            self._description = str(entry[15])
        else:
            return(None)
    
    def dbInsert(self, dbfile):
        # Insert a new record into the database
        values = [
            self._uuid,
            self._consolidation,
            self._material,
            self._created_date,
            self._modified_date,
            self._filename,
            self._file_type,
            self._public,
            self._alias,
            self._status,
            self._lock,
            self._source,
            self._operation,
            self._operating_application,
            self._caption,
            self._description
        ]
        
        # Create the SQL query for updating the new consolidation.
        sql_insert = """INSERT INTO file (
                        uuid,
                        con_id, 
                        mat_id,
                        created_date,
                        modified_date,
                        file_name,
                        file_type,
                        make_public,
                        alias_name,
                        status,
                        is_locked,
                        source, 
                        file_operation,
                        operating_application,
                        caption,
                        description
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
                
        # Execute the query.
        super(File, self).excuteSQL(dbfile, sql_insert, values)
    
    def dbUpdate(self, dbfile):
        print("File::dbUpdate()")
        # Insert a new record into the database
        values = [
            self._consolidation,
            self._material,
            self._created_date,
            self._modified_date,
            self._filename,
            self._file_type,
            self._public,
            self._alias,
            self._status,
            self._lock,
            self._source,
            self._operation,
            self._operating_application,
            self._caption,
            self._description,
            self._uuid
        ]
        
        # Create the SQL query for updating the new consolidation.
        sql_update = """UPDATE file
                    SET
                        con_id = ?,
                        mat_id = ?,
                        created_date = ?,
                        modified_date = ?,
                        file_name = ?,
                        file_type = ?,
                        make_public = ?,
                        alias_name = ?,
                        status = ?,
                        is_locked = ?,
                        source = ?,
                        file_operation = ?,
                        operating_application = ?,
                        caption = ?,
                        description = ?
                    WHERE uuid = ?"""
        
        # Execute the query.
        super(File, self).excuteSQL(dbfile, sql_update, values)
    
    def writeAsXml(self):
        try:
            xml_root = et.Element('File')
            xml_root.set("id", self._id)
            xml_root.set("uuid", self._uuid)
            
            xml_consolidation = et.SubElement(xml_root, "consolidation")
            xml_consolidation.set("idref", self._consolidation)
            
            xml_material = et.SubElement(xml_root, "material")
            xml_material.set("idref", self._material)
            
            xml_created = et.SubElement(xml_root, 'created')
            xml_created.text = self._created_date
            
            xml_created = et.SubElement(xml_root, 'modifed')
            xml_created.text = self.modified_date
            
            xml_filename = et.SubElement(xml_root, 'filename')
            xml_filename.text = os.path.basename(self._filename)
            
            xml_filename = et.SubElement(xml_root, 'filetype')
            xml_filename.text = os.path.basename(self._file_type)
            
            xml_alias = et.SubElement(xml_root, 'alias')
            xml_alias.text = os.path.basename(self._alias)
            
            xml_caption = et.SubElement(xml_root, 'caption')
            xml_caption.text = os.path.basename(self._caption)
            
            xml_caption = et.SubElement(xml_root, 'description')
            xml_caption.text = os.path.basename(self._description)
            
            return(et.tostring(xml_root, pretty_print=True, xml_declaration=True))
        except:
            print("Error occured in XML output.")
            return(None)

class AdditionalAttribute(SimpleObject):
    def __init__(self, is_new = True, uuid=None, dbfile=None, ref_table=None, ref_uuid=None):
        # Initialize the super class.
        SimpleObject.__init__(self, is_new, uuid, dbfile)
        
        if is_new == True and dbfile == None:
            # Initialize as the new instance.
            self._key = None
            self._value = None
            self._datatype = None
            self._description = None
        elif is_new == False and uuid != None and dbfile != None and ref_table != None and ref_uuid != None:
            # Initialize by the DB instance.
            self._initInstanceByUuid(ref_table, ref_uuid, dbfile)
        else:
            # Other unexpected case.
            print("Not Instantiated!!")
            return(None)
    
    @property
    def key(self): return self._key
    @property
    def value(self): return self._value
    @property
    def datatype(self): return self._datatype
    @property
    def description(self): return self._description    
    
    @key.setter
    def key(self, value): self._key = value
    @value.setter
    def value(self, value): self._value = value
    @datatype.setter
    def datatype(self, value): self._datatype = value
    @description.setter
    def description(self, value): self._description = value
    
    # operation
    def _initInstanceByUuid(self, ref_table, ref_uuid, dbfile):
        print("AdditionalAttribute::_initInstanceByUuid(self, table, uuid, dbfile)")
        
        # Make the SQL statement.
        sql_select = """SELECT  uuid,
                                id,
                                key,
                                value,
                                datatype,
                                description
                            FROM additional_attribute WHERE ref_table=? AND ref_uuid=?"""
        
        # Fech one from DB.
        entry = super(AdditionalAttribute, self).fetchOneSQL(dbfile, sql_select, [ref_table, ref_uuid])
        
        if not entry == None:
            # Get attributes from the row.
            self._uuid = entry[0]
            self._id = entry[1]
            self._key = entry[2]
            self._value = entry[3]
            self._datatype = entry[4]
            self._description = entry[5]
        else:
            return(None)
    
    def dbInsert(self, dbfile, ref_table, ref_uuid):
        print("AdditionalAttribute::dbInsert(self, dbfile, ref_table, ref_uuid)")
        
        # Insert a new record into the database
        values = [
            self._uuid,
            self._key,
            self._value,
            self._datatype,
            self._description,
            ref_table,
            ref_uuid
        ]
        
        # Create the SQL query for inserting the new consolidation.
        sql_insert = """INSERT INTO additional_attribute (
                    uuid,
                    key, 
                    value,
                    datatype,
                    description,
                    ref_table,
                    ref_uuid
                ) VALUES (?,?,?,?,?,?,?)"""
        
        # Execute the query.
        super(AdditionalAttribute, self).excuteSQL(dbfile, sql_insert, values)
    
    def dbUpdate(self, dbfile):
        print("AdditionalAttribute::dbUpdate(self, dbfile)")
        
        # Insert a new record into the database
        values = [
            self._key,
            self._value,
            self._datatype,
            self._description,
            self._uuid
        ]
        
        # Create the SQL query for updating the new consolidation.
        sql_update = """UPDATE additional_attribute
                    SET
                        key = ?,
                        value = ?,
                        datatype = ?,
                        description = ?
                    WHERE uuid = ?"""
        print(values)
        # Execute the query.
        super(AdditionalAttribute, self).excuteSQL(dbfile, sql_update, values)
    
    def dbDrop(self, dbfile):
        print("AdditionalAttribute::dbDrop(self, dbfile)")
        
        # Dropt the exsiting entry from the DB.
        values = [self._uuid]
        
        # Create the SQL query for deleting the existing consolidation.
        sql_delete = """DELETE FROM additional_attribute WHERE uuid = ?"""
        
        # Execute the query.
        super(AdditionalAttribute, self).excuteSQL(dbfile, sql_delete, values)

def exportAsHtml(dbfile, output, title="Archive"):
    try:
        # Establish the connection between DB.
        conn = sqlite.connect(dbfile)
        
        if conn == None: return(None)
        
        # Open the file stream
        output_html = open(output,"w") 
        
        output_html.write("<!DOCTYPE html>\n<html>\n\t<head>\n\t\t<title>%s</title>\n\t</head>\t<body>\n\t\t<hr />\n" % (title))
    
        # Make the SQL statement.
        sql_sel_con = """SELECT uuid,
                                name,
                                geographic_annotation,
                                temporal_annotation,
                                description
                        FROM consolidation ORDER BY id;"""
        
        # Instantiate the cursor for query.
        cur_sel_con = conn.cursor()
        cur_sel_con.execute(sql_sel_con)
        
        # Fetch one row.
        con_rows = cur_sel_con.fetchall()
        
        # Replace NULL values by blank.
        for con_row in con_rows:
            con_uuid = con_row[0].encode('utf-8')
            con_cnam = con_row[1].encode('utf-8')
            con_gano = con_row[2].encode('utf-8')
            con_tano = con_row[3].encode('utf-8')
            con_desc = con_row[4].encode('utf-8')
            
            output_html.write("\t\t<div id='%s' style='text-align:center;'>\n" % (con_uuid))
            output_html.write("\t\t\t<table width='800' style='margin: auto; border: hidden; text-align: left'>\n\t\t\t\t<col width='200'>\n\t\t\t\t<col width='600'>\n")
            output_html.write("\t\t\t\t<tr><td colspan='2'><h1 style='text-align: center;'>%s</h1></td></tr>\n" % (con_cnam))
            output_html.write("\t\t\t\t<tr><td style='text-align: right; vertical-align: top'>Geographic Annotation :</td><td style='vertical-align: top'>%s</td></tr>\n" % (con_gano))
            output_html.write("\t\t\t\t<tr><td style='text-align: right; vertical-align: top'>Temporal Annotation :</td><td style='vertical-align: top'>%s</td></tr>\n" % (con_tano))
            output_html.write("\t\t\t\t<tr><td style='text-align: right; vertical-align: top' height='50'>Description :</td><td style='vertical-align: top'>%s</td></tr>\n" % (con_desc))
            output_html.write("\t\t\t</table>\n")
            
            sql_sel_con_img = '''SELECT    uuid,
                                            created_date,
                                            modified_date,
                                            file_name,
                                            alias_name,
                                            status,
                                            source,
                                            file_operation,
                                            caption,
                                            description
                                FROM file WHERE con_id = ? AND mat_id="NULL" AND file_type=? ORDER BY id DESC;'''
            
            # Instantiate the cursor for query.
            cur_sel_con_img = conn.cursor()
            cur_sel_con_img.execute(sql_sel_con_img, [con_uuid, "image"])
            
            con_img_rows = cur_sel_con_img.fetchall()
            
            output_html.write("\t\t\t<table width='800' style='margin: auto; border: hidden; text-align: left'>\n")
            output_html.write("\t\t\t\t<col width='200'>\n\t\t\t\t<col width='150'>\n\t\t\t\t<col width='150'>\n\t\t\t\t<col width='150'>\n\t\t\t\t<col width='150'>\n")
            output_html.write("\t\t\t\t<tr><td colspan='4'><h1 style='text-align: center;'>%s</h1></td></tr>\n" % ("Images"))
            for con_img_row in con_img_rows:
                con_img_uuid = con_img_row[0].encode('utf-8')
                con_img_cdat = con_img_row[1].encode('utf-8')
                con_img_mdat = con_img_row[2].encode('utf-8')
                con_img_fnam = con_img_row[3].encode('utf-8')
                con_img_stts = con_img_row[4].encode('utf-8')
                con_img_srce = con_img_row[5].encode('utf-8')
                con_img_fope = con_img_row[6].encode('utf-8')
                con_img_capt = con_img_row[7].encode('utf-8')
                con_img_desc = con_img_row[8].encode('utf-8')
                
                img_ext = os.path.splitext(con_img_fnam)[1]
                
                if img_ext == ".jpeg" or img_ext == ".jpg":
                    output_html.write("\t\t\t\t<tr style='vertical-align: top'>")
                    output_html.write("<td><img src='%s' height='40'/>$s</td><td>%s</td><td>$s</td><td>$s</td>" % (con_img_fnam, con_img_capt, con_img_stts, con_img_srce, con_img_desc))
                    output_html.write("<td>$s</td></tr>\n")
            output_html.write("\t\t\t</table>\n")
            
            # Make the SQL statement.
            sql_sel_mat = """SELECT uuid,
                                    name,
                                    material_number,
                                    estimated_period_beginning,
                                    estimated_period_peak,
                                    estimated_period_ending,
                                    latitude,
                                    longitude,
                                    altitude,
                                    description
                                FROM material WHERE con_id=?"""
            
            # Instantiate the cursor for query.
            cur_sel_mat = conn.cursor()
            cur_sel_mat.execute(sql_sel_mat, [con_row[0]])
            
            # Fetch one row.
            mat_rows = cur_sel_mat.fetchall()
            
            for mat_row in mat_rows:
                output_html.write("\t\t\t<div id='%s' style='text-align:center;'>\n\t\t\t\t\n" % (mat_row[0].encode('utf-8')))
                output_html.write("\t\t\t<table width='800' style='margin: auto; border: hidden; text-align: left'>\n\t\t\t\t<col width='200'>\n\t\t\t\t<col width='600'>\n")
                output_html.write("\t\t\t\t\t<tr><td colspan='2'><h2 style='text-align: center;'>%s</h2></td></tr>\n" % (mat_row[1].encode('utf-8')))
                output_html.write("\t\t\t\t\t<tr><td style='text-align: right; vertical-align: top'>Material Number :</td><td style='vertical-align: top'>%s</td></tr>\n" % (mat_row[2].encode('utf-8')))
                output_html.write("\t\t\t\t\t<tr><td style='text-align: right; vertical-align: top'>Latitude :</td><td style='vertical-align: top'>%s</td></tr>\n" % (mat_row[6].encode('utf-8')))
                output_html.write("\t\t\t\t\t<tr><td style='text-align: right; vertical-align: top'>Longitude :</td><td style='vertical-align: top'>%s</td></tr>\n" % (mat_row[7].encode('utf-8')))
                output_html.write("\t\t\t\t\t<tr><td style='text-align: right; vertical-align: top'>Altitude :</td><td style='vertical-align: top'>%s</td></tr>\n" % (mat_row[8].encode('utf-8')))
                output_html.write("\t\t\t\t\t<tr><td style='text-align: right; vertical-align: top'>Begining :</td><td style='vertical-align: top'>%s</td></tr>\n" % (mat_row[3].encode('utf-8')))
                output_html.write("\t\t\t\t\t<tr><td style='text-align: right; vertical-align: top'>Peak :</td><td style='vertical-align: top'>%s</td></tr>\n" % (mat_row[4].encode('utf-8')))
                output_html.write("\t\t\t\t\t<tr><td style='text-align: right; vertical-align: top'>Ending :</td><td style='vertical-align: top'>%s</td></tr>\n" % (mat_row[5].encode('utf-8')))
                output_html.write("\t\t\t\t\t<tr><td style='text-align: right; vertical-align: top' height='50'>Description :</td><td style='vertical-align: top'>%s</td></tr>\n" % (mat_row[9].encode('utf-8')))
                output_html.write("\t\t\t\t</table>\n\t\t\t</div>\n")
                
            output_html.write("\t\t</div>\n\t\t<hr />\n")
        output_html.write("\t</body>\n</html>")
        
        output_html.close()
    except Exception as e:
        print(e)

def whatisthis(s):
    if isinstance(s, str):
        print "ordinary string"
    elif isinstance(s, unicode):
        print "unicode string"
    else:
        print "not a string"