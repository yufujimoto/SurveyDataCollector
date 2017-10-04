#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os, sys, uuid as unique
import sqlite3 as sqlite
from sqlite3 import Error

class SimpleObject(object):
    def __init__(self, is_new, uuid, dbfile):
        if is_new == True and uuid == None and dbfile == None:
            self._id = None
            if is_new == True:
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

class Consolidation(SimpleObject):
    def __init__(self, is_new=True, uuid=None, dbfile=None):
        # Initialize the super class.
        SimpleObject.__init__(self, is_new, uuid, dbfile)
        
        if is_new == True and uuid == None and dbfile == None:
            # Initialize as the new instance.
            self._name = None
            self._geographic_annotation = None
            self._temporal_annotation = None
            self._description = None
        elif is_new == False and uuid != None and dbfile != None:
            # Initialize by the DB instance.
            self._initInstanceByUuid(uuid, dbfile)
        else:
            # Other unexpected case.
            return(None)
    
    @property
    def name(self): return self._name
    @property
    def geographic_annotation(self): return self._geographic_annotation
    @property
    def temporal_annotation(self): return self._temporal_annotation
    @property
    def description(self): return self._description    
    
    @name.setter
    def name(self, value): self._name = value
    @geographic_annotation.setter
    def geographic_annotation(self, value): self._geographic_annotation = value
    @temporal_annotation.setter
    def temporal_annotation(self, value): self._temporal_annotation = value
    @description.setter
    def description(self, value): self._description = value
    
    # operation
    def _initInstanceByUuid(self, uuid, dbfile):
        # Make the SQL statement.
        sql_select = """SELECT  id,
                                name,
                                geographic_annotation,
                                temporal_annotation,
                                description
                        FROM consolidation WHERE uuid=?"""
        
        # Establish the connection between DB.
        conn = sqlite.connect(dbfile)
        
        if conn is not None:
            # Instantiate the cursor for query.
            cur = conn.cursor()
            
            # Execute the query.
            cur.execute(sql_select, [uuid])
            
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
            self._id = str(entry[0])
            self._uuid = str(uuid)
            self._name = str(entry[1])
            self._geographic_annotation = str(entry[2])
            self._temporal_annotation = str(entry[3])
            self._description = str(entry[4])
        else:
            return(None)
    
    def dbInsert(self, dbfile):
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
    
    def dbUpdate(self, dbfile):
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
    
    def dbDrop(self, dbfile):
        # Dropt the exsiting entry from the DB.
        values = [self._uuid]
        
        # Create the SQL query for deleting the existing consolidation.
        sql_delete = """DELETE FROM consolidation WHERE uuid = ?"""
        
        # Execute the query.
        super(Consolidation, self).excuteSQL(dbfile, sql_delete, values)

class Material(SimpleObject):
    def __init__(self, is_new = True, uuid=None, dbfile=None):
        # Initialize the super class.
        SimpleObject.__init__(self, is_new, uuid, dbfile)
        
        if is_new == True and uuid == None and dbfile == None:
            # Initialize as the new instance.
            self._consolidation = None
            self._name = None
            self._estimated_period_beginning = None
            self._estimated_period_ending = None
            self._latitude = None
            self._longitude = None
            self._altitude = None
            self._material_number = None
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
    def description(self): return self._description    
    
    @consolidation.setter
    def consolidation(self, value): self._consolidation = value
    @name.setter
    def name(self, value): self._name = value
    @estimated_period_beginning.setter
    def estimated_period_beginning(self, value): self._estimated_period_beginning = value
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
    @description.setter
    def description(self, value): self._description = value
    
    # operation
    def _initInstanceByUuid(self, uuid, dbfile):
        # Make the SQL statement.
        sql_select = """SELECT  id,
                                con_id,
                                name,
                                estimated_period_beginning,
                                estimated_period_ending,
                                latitude,
                                longitude,
                                altitude,
                                material_number,
                                descriptions
                            FROM material WHERE uuid=?"""
        
        # Establish the connection between DB.
        conn = sqlite.connect(dbfile)
        
        if conn is not None:
            # Instantiate the cursor for query.
            cur = conn.cursor()
            
            # Execute the query.
            cur.execute(sql_select, [uuid])
            
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
            self._id = str(entry[0])
            self._uuid = str(uuid)
            self._consolidation = str(entry[1])
            self._name = str(entry[2])
            self._estimated_period_beginning = str(entry[3])
            self._estimated_period_ending = str(entry[4])
            self._latitude = str(entry[5])
            self._longitude = str(entry[6])
            self._altitude = str(entry[7])
            self._material_number = str(entry[8])
            self._description = str(entry[9])
        else:
            return(None)
    
    def dbInsert(self, dbfile):
        # Insert a new record into the database
        values = [
            self._uuid,
            self._consolidation,
            self._name,
            self._estimated_period_beginning,
            self._estimated_period_ending,
            self._latitude,
            self._longitude,
            self._altitude,
            self._description
        ]
        
        # Create the SQL query for inserting the new consolidation.
        sql_insert = """INSERT INTO material (
                    uuid,
                    con_id, 
                    name,
                    estimated_period_beginning,
                    estimated_period_ending,
                    latitude,
                    longitude,
                    altitude,
                    descriptions
                ) VALUES (?,?,?,?,?,?,?,?,?)"""
        
        # Execute the query.
        super(Material, self).excuteSQL(dbfile, sql_insert, values)
    
    def dbUpdate(self, dbfile):
        # Insert a new record into the database
        values = [
            self._name,
            self._estimated_period_beginning,
            self._estimated_period_ending,
            self._latitude,
            self._longitude,
            self._altitude,
            self._description,
            self._uuid
        ]
        
        # Create the SQL query for updating the new consolidation.
        sql_update = """UPDATE material
                    SET
                        name = ?,
                        estimated_period_beginning = ?,
                        estimated_period_ending = ?,
                        latitude = ?,
                        longitude = ?,
                        altitude = ?,
                        descriptions = ?
                    WHERE uuid = ?"""
        
        # Execute the query.
        super(Material, self).excuteSQL(dbfile, sql_update, values)
    
    def dbDrop(self, dbfile):
        # Dropt the exsiting entry from the DB.
        values = [self._uuid]
        
        # Create the SQL query for deleting the existing consolidation.
        sql_delete = """DELETE FROM material WHERE uuid = ?"""
        
        # Execute the query.
        super(Material, self).excuteSQL(dbfile, sql_delete, values)

class File(SimpleObject):
    def __init__(self, is_new = True, uuid=None, dbfile=None):
        SimpleObject.__init__(self, is_new, uuid, dbfile)
        
        if is_new == True and uuid == None and dbfile == None:
            self._consolidation = None
            self._material = None
            self._filename = None
            self._last_edit = None
            self._mime_type = None
            self._alias = None
            self._status = None
            self._public = None
            self._lock = None
            self._source = None
            self._operation = None
            self._operating_application = None
            self._caption = None
            self._description = None 
    
    @property
    def material(self): return self._material
    @property
    def consolidation(self): return self._consolidation
    @property
    def filename(self): return self._filename
    @property
    def last_edit(self): return self._last_edit
    @property
    def mime_type(self): return self._mime_type
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
    @last_edit.setter
    def last_edit(self, value): self._last_edit = value
    @mime_type.setter
    def mime_type(self, value): self._mime_type = value
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
    def dbInsert(self, dbfile):
        # Insert a new record into the database
        values = [
            self._uuid,
            self._consolidation,
            self._material,
            self._filename,
            self._mime_type,
            self._alias,
            self._status,
            self._public,
            self._lock,
            self._source,
            self._operation,
            self._operating_application,
            self._caption,
            self._description
        ]
        
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
        super(Material, self).excuteSQL(dbfile, sql_insert, values)