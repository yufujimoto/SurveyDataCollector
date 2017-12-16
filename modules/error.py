#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Import general libraries.
import sys, os, uuid, shutil, time, math, tempfile, logging, pyexiv2, datetime

# Import the library for acquiring file information.
from stat import *

# Import PyQt5 libraries for generating the GUI application.
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QThread, pyqtSignal

class ErrorMessage(object):
    @property
    def title(self): return self._title
    @property
    def message(self): return self._message
    @property
    def information(self): return self._information
    @property
    def icon(self): return self._icon
    @property
    def details(self): return self._details
    
    @title.setter
    def title(self, value): self._title = value
    @message.setter
    def message(self, value): self._message = value
    @information.setter
    def information(self, value): self._information = value
    @icon.setter
    def icon(self, value): self._icon = value
    @details.setter
    def details(self, value): self._details = value
    
    def __init__(self):
        self._title = "エラーが発生しました"
        self._message = None
        self._information = None
        self._icon = None
        self._details = None
    
    def printErrorMessage(self):
        print("Error Occured: %s%s%s" % (self._message, self._information, self._details))
    
    def showMessageBox(self):
        # Create a message box object.
        msg = QMessageBox()
        
        # Generate additional information if exists.
        if not self._icon == None: msg.setIcon(self._icon)
        if not self._title == None: msg.setWindowTitle(self._title)
        if not self._message == None: msg.setText(self._message)
        if not self._information == None: msg.setInformativeText(self._information)
        if not self._details == None: msg.setDetailedText(self._details)
        
        # Show the message box.    
        msg.exec_()

class ErrorMessageProjectOpen(ErrorMessage):
    def __init__(self, details=None, show=True):
        # Initialize the super class.
        ErrorMessage.__init__(self)
        
        self._message = "プロジェクトが開かれていません。"
        self._information = "プロジェクトのディレクトリを参照し、指定ください。"
        self._icon = QMessageBox.Information
        self._details = details
        
        # Execute the query.
        if not show == False: super(ErrorMessageProjectOpen, self).showMessageBox()

class ErrorMessageProjectNotCreated(ErrorMessage):
    def __init__(self, details=None, show=True):
        # Initialize the super class.
        ErrorMessage.__init__(self)
        
        self._message = "新規プロジェクトを作成できませんでした。"
        self._information = "エラーの詳細を確認してください。"
        self._icon = QMessageBox.Critical
        self._details = details
        
        # Execute the query.
        if not show == False: super(ErrorMessageProjectNotCreated, self).showMessageBox()

class ErrorMessageFileExport(ErrorMessage):
    def __init__(self, details=None, show=True):
        # Initialize the super class.
        ErrorMessage.__init__(self)
        
        self._message = "エクスポートに失敗しました。"
        self._information = "対象オブジェクトあるいは保存場所を確認してください。"
        self._icon = QMessageBox.Information
        self._details = details
        
        # Execute the query.
        super(ErrorMessageFileExport, self).printErrorMessage()
        if not show == False: super(ErrorMessageFileExport, self).showMessageBox()

class ErrorMessageEditImageFile(ErrorMessage):
    def __init__(self, details=None, show=True):
        # Initialize the super class.
        ErrorMessage.__init__(self)
        
        self._message = "このファイルは対応した形式ではありません。"
        self._information = "編集可能なファイルを選択してください。"
        self._icon = QMessageBox.Critical
        self._details = details
        
        # Execute the query.
        super(ErrorMessageEditImageFile, self).printErrorMessage()
        if not show == False: super(ErrorMessageEditImageFile, self).showMessageBox()

class ErrorMessageFileLocked(ErrorMessage):
    def __init__(self, details=None, show=True):
        # Initialize the super class.
        ErrorMessage.__init__(self)
        
        self._message = "ファイルの削除に失敗しました。"
        self._information = "このファイルはロックされているか、すでに削除済みのため削除できません。"
        self._icon = QMessageBox.Information
        self._details = details
        
        # Execute the query.
        super(ErrorMessageFileLocked, self).printErrorMessage()
        if not show == False: super(ErrorMessageFileLocked, self).showMessageBox()

class ErrorMessageFileNotExist(ErrorMessage):
    def __init__(self, details=None, show=True):
        # Initialize the super class.
        ErrorMessage.__init__(self)
        
        self._message = "選択されたファイルは存在しません。"
        self._information = "すでに削除された可能性あります。選択したファイルを確認してください。"
        self._icon = QMessageBox.Critical
        self._details = details
        
        # Execute the query.
        super(ErrorMessageFileNotExist, self).printErrorMessage()
        if not show == False: super(ErrorMessageFileNotExist, self).showMessageBox()        

class ErrorMessageUnknown(ErrorMessage):
    def __init__(self, details=None, show=True):
        # Initialize the super class.
        ErrorMessage.__init__(self)
        
        self._message = "不明なエラーです。"
        self._information = "想定外のエラーが発生しました。エラーの詳細を確認してください。"
        self._icon = QMessageBox.Critical
        self._details = details
        
        # Execute the query.
        super(ErrorMessageUnknown, self).printErrorMessage()
        if not show == False: super(ErrorMessageUnknown, self).showMessageBox()        
    
class ErrorMessageDbConnection(ErrorMessage):
    def __init__(self, details=None, show=True):
        # Initialize the super class.
        ErrorMessage.__init__(self)
        
        self._message = "データベースの情報を取得できません。"
        self._information = "エラーの詳細を確認してください。"
        self._icon = QMessageBox.Critical
        self._details = details
        
        # Execute the query.
        super(ErrorMessageDbConnection, self).printErrorMessage()
        if not show == False: super(ErrorMessageDbConnection, self).showMessageBox()       

class ErrorMessageCameraDetection(ErrorMessage):
    def __init__(self, details=None, show=True):
        # Initialize the super class.
        ErrorMessage.__init__(self)
        
        self._message = "カメラを認識できません。"
        self._information = "カメラの接続状況を確認してください。"
        self._icon = QMessageBox.Critical
        self._details = details
        
        # Execute the query.
        super(ErrorMessageCameraDetection, self).printErrorMessage()
        if not show == False: super(ErrorMessageCameraDetection, self).showMessageBox()

class ErrorMessageCurrentObject(ErrorMessage):
    def __init__(self, details=None, show=True):
        # Initialize the super class.
        ErrorMessage.__init__(self)
        
        self._message = "オブジェクトを取得できませんでした。"
        self._information = "ツリー・メニューからオブジェクトを選択してください。"
        self._icon = QMessageBox.Critical
        self._details = details
        
        # Execute the query.
        super(ErrorMessageCurrentObject, self).printErrorMessage()
        if not show == False: super(ErrorMessageCurrentObject, self).showMessageBox()