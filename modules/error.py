#!/usr/bin/python
# -*- coding: UTF-8 -*-

# self._language = "en"

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
    @property
    def language(self): return self._language
    
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
    @language.setter
    def language(self, value): self._language = value
    
    def __init__(self, language):
        self._language = language
        
        if self._language == "ja": self._title = "エラーが発生しました"
        elif self._language == "en": self._title = "Error!!"
        
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
    def __init__(self, language, details=None, show=True):
        # Initialize the super class.
        ErrorMessage.__init__(self, language)
        
        if self._language == "ja":                
            self._message = "プロジェクトが開かれていません。"
            self._information = "プロジェクトのディレクトリを参照し、指定ください。"
        elif self._language == "en":
            self._message = "Project is not opened."
            self._information = "Please open the project directory."
        self._icon = QMessageBox.Information
        self._details = details
        
        # Execute the query.
        if not show == False: super(ErrorMessageProjectOpen, self).showMessageBox()

class ErrorMessageTreeItemNotSelected(ErrorMessage):
    def __init__(self, language, details=None, show=True):
        # Initialize the super class.
        ErrorMessage.__init__(self, language)
        
        if self._language == "ja":           
            self._message = "オブジェクトが選択されていません。"
            self._information = "オブジェクトツリーパネルからオブジェクトを再選択してください。"
        elif self._language == "en":
            self._message = "Any objects are not selected."
            self._information = "Please reselect a specific object from the objects tree panel."
        self._icon = QMessageBox.Information
        self._details = details
        
        # Execute the query.
        if not show == False: super(ErrorMessageTreeItemNotSelected, self).showMessageBox()

class ErrorMessageCurrentConsolidation(ErrorMessage):
    def __init__(self, language, details=None, show=True):
        # Initialize the super class.
        ErrorMessage.__init__(self, language)
        
        if self._language == "ja":           
            self._message = "現在の統合体が選択されていません。"
            self._information = "オブジェクトツリーパネルから統合体を再選択してください。"
        elif self._language == "en":
            self._message = "The current consolidation is empty."
            self._information = "Please reselect the specific consolidation from the objects tree panel."
        self._icon = QMessageBox.Information
        self._details = details
        
        # Execute the query.
        if not show == False: super(ErrorMessageCurrentConsolidation, self).showMessageBox()

class ErrorMessageCurrentMaterial(ErrorMessage):
    def __init__(self, language, details=None, show=True):
        # Initialize the super class.
        ErrorMessage.__init__(self, language)
        
        if self._language == "ja":           
            self._message = "現在の資料が選択されていません。"
            self._information = "オブジェクトツリーパネルから資料を再選択してください。"
        elif self._language == "en":
            self._message = "The current material is empty."
            self._information = "Please reselect the specific material from the objects tree panel."
        self._icon = QMessageBox.Information
        self._details = details
        
        # Execute the query.
        if not show == False: super(ErrorMessageCurrentMaterial, self).showMessageBox()

class ErrorMessageProjectNotCreated(ErrorMessage):
    def __init__(self, details=None, show=True, language="en"):
        # Initialize the super class.
        ErrorMessage.__init__(self, language)
        
        if self._language == "ja":                
            self._message = "新規プロジェクトを作成できませんでした。"
            self._information = "エラーの詳細を確認してください。"
        elif self._language == "en":
            self._message = "New project has not created."
            self._information = "Please check details about the error."
        
        self._icon = QMessageBox.Critical
        self._details = details
        
        # Execute the query.
        if not show == False: super(ErrorMessageProjectNotCreated, self).showMessageBox()

class ErrorMessageFileExport(ErrorMessage):
    def __init__(self, details=None, show=True, language="en"):
        # Initialize the super class.
        ErrorMessage.__init__(self, language)
        
        if self._language == "ja":                
            self._message = "エクスポートに失敗しました。"
            self._information = "対象オブジェクトあるいは保存場所を確認してください。"
        elif self._language == "en":
            self._message = "The object has not exported."
            self._information = "Please check the permission of the saving path."
            
        self._icon = QMessageBox.Information
        self._details = details
        
        # Execute the query.
        super(ErrorMessageFileExport, self).printErrorMessage()
        if not show == False: super(ErrorMessageFileExport, self).showMessageBox()

class ErrorMessageEditImageFile(ErrorMessage):
    def __init__(self, details=None, show=True, language="en"):
        # Initialize the super class.
        ErrorMessage.__init__(self, language)
        
        if self._language == "ja":                
            self._message = "このファイルは対応した形式ではありません。"
            self._information = "編集可能なファイルを選択してください。"
        elif self._language == "en":
            self._message = "This file is not supported format."
            self._information = "Please select supported file."
        
        self._icon = QMessageBox.Critical
        self._details = details
        
        # Execute the query.
        super(ErrorMessageEditImageFile, self).printErrorMessage()
        if not show == False: super(ErrorMessageEditImageFile, self).showMessageBox()

class ErrorMessageFileLocked(ErrorMessage):
    def __init__(self, details=None, show=True, language="en"):
        # Initialize the super class.
        ErrorMessage.__init__(self, language)
        
        if self._language == "ja":                
            self._message = "ファイルの削除に失敗しました。"
            self._information = "このファイルはロックされているか、すでに削除済みのため削除できません。"
        elif self._language == "en":
            self._message = "Cannot delete."
            self._information = "Selected file is locked or already removed."
        
        self._icon = QMessageBox.Information
        self._details = details
        
        # Execute the query.
        super(ErrorMessageFileLocked, self).printErrorMessage()
        if not show == False: super(ErrorMessageFileLocked, self).showMessageBox()

class ErrorMessageFileNotExist(ErrorMessage):
    def __init__(self, details=None, show=True, language="en"):
        # Initialize the super class.
        ErrorMessage.__init__(self, language)
        
        if self._language == "ja":                
            self._message = "選択されたファイルは存在しません。"
            self._information = "すでに削除された可能性あります。選択したファイルを確認してください。"
        elif self._language == "en":
            self._message = "Selected file does not exist."
            self._information = "Selected file might have been already removed."
        
        self._icon = QMessageBox.Critical
        self._details = details
        
        # Execute the query.
        super(ErrorMessageFileNotExist, self).printErrorMessage()
        if not show == False: super(ErrorMessageFileNotExist, self).showMessageBox()        

class ErrorMessageUnknown(ErrorMessage):
    def __init__(self, details=None, show=True, language="en"):
        # Initialize the super class.
        ErrorMessage.__init__(self, language)
        
        if self._language == "ja":                
            self._message = "不明なエラーです。"
            self._information = "想定外のエラーが発生しました。エラーの詳細を確認してください。"
        elif self._language == "en":
            self._message = "Unknown error."
            self._information = "Unexpected error has occured. Please check the detail."
        
        self._icon = QMessageBox.Critical
        self._details = details
        
        # Execute the query.
        super(ErrorMessageUnknown, self).printErrorMessage()
        if not show == False: super(ErrorMessageUnknown, self).showMessageBox()        
        
class ErrorMessageDbConnection(ErrorMessage):
    def __init__(self, details=None, show=True, language="en"):
        # Initialize the super class.
        ErrorMessage.__init__(self, language)
        
        if self._language == "ja":                
            self._message = "データベースの情報を取得できません。"
            self._information = "エラーの詳細を確認してください。"
        elif self._language == "en":
            self._message = "Cannot retrive the Database information."
            self._information = "Please check the detail."
        
        self._icon = QMessageBox.Critical
        self._details = details
        
        # Execute the query.
        super(ErrorMessageDbConnection, self).printErrorMessage()
        if not show == False: super(ErrorMessageDbConnection, self).showMessageBox()       

class ErrorMessageCameraDetection(ErrorMessage):
    def __init__(self, details=None, show=True, language="en"):
        # Initialize the super class.
        ErrorMessage.__init__(self, language)
        
        
        if self._language == "ja":
            self._title = "カメラの接続エラー"
            self._message = "カメラを認識できません。カメラが接続されていないか、複数のイメージデバイス（スマートフォンも含む）が接続されています。"
            self._information = "カメラの接続状況を確認してください。全ての機器を取り外して再度実行してください。"
        elif self._language == "en":
            self._title = "Camera Detection Error"
            self._message = "Cannot detect the connected cameras."
            self._information = "Please check connected devices. Remove all devices and retry this operation."
            
        self._icon = QMessageBox.Critical
        self._details = details
        
        # Execute the query.
        super(ErrorMessageCameraDetection, self).printErrorMessage()
        if not show == False: super(ErrorMessageCameraDetection, self).showMessageBox()

class ErrorMessageCurrentObject(ErrorMessage):
    def __init__(self, details=None, show=True, language="en"):
        # Initialize the super class.
        ErrorMessage.__init__(self, language)
        
        if self._language == "ja":                
            self._message = "オブジェクトを取得できませんでした。"
            self._information = "ツリー・メニューからオブジェクトを選択してください。"
        elif self._language == "en":
            self._message = "Cannot retrive the selected object."
            self._information = "Please reselect the object from the tree."
            
        self._icon = QMessageBox.Critical
        self._details = details
        
        # Execute the query.
        super(ErrorMessageCurrentObject, self).printErrorMessage()
        if not show == False: super(ErrorMessageCurrentObject, self).showMessageBox()
        
class ErrorMessageImagePreview(ErrorMessage):
    def __init__(self, details=None, show=True, language="en"):
        # Initialize the super class.
        ErrorMessage.__init__(self, language)
        
        if self._language == "ja":                
            self._message = "このファイルはプレビューに対応していません。"
            self._information = "諦めてください。RAW + JPEG で撮影することをお勧めします。"
        elif self._language == "en":
            self._message = "Selected file is not supported for preview."
            self._information = "Curently, only JPEG (and some RAW) files are supported."
            
        self._icon = QMessageBox.Critical
        self._details = details
        
        # Execute the query.
        super(ErrorMessageImagePreview, self).printErrorMessage()
        if not show == False: super(ErrorMessageImagePreview, self).showMessageBox()
        
class ErrorMessagePlaySound(ErrorMessage):
    def __init__(self, details=None, show=True, language="en"):
        # Initialize the super class.
        ErrorMessage.__init__(self, language)
        
        if self._language == "ja":                
            self._message = "選択中のファイルは音声ファイルではありません。"
            self._information = "再生可能な音声ファイルを選択してください。"
        elif self._language == "en":
            self._message = "Selected file is not supported. Please select a supported file format."
            self._information = "Curently, only WAV file is supported."
            
        self._icon = QMessageBox.Critical
        self._details = details
        
        # Execute the query.
        super(ErrorMessagePlaySound, self).printErrorMessage()
        if not show == False: super(ErrorMessagePlaySound, self).showMessageBox()

class ErrorMessageImageProcessing(ErrorMessage):
    def __init__(self, details=None, show=True, language="en"):
        # Initialize the super class.
        ErrorMessage.__init__(self, language)
        
        if self._language == "ja":                
            self._message = "画像処理に失敗しました。"
            self._information = "画像処理に失敗しました。エラーの詳細を確認してください。"
        elif self._language == "en":
            self._message = "Cannot run the image processing function."
            self._information = "Cannot run the image processing function. Please check details."
            
        self._icon = QMessageBox.Critical
        self._details = details
        
        # Execute the query.
        super(ErrorMessageImageProcessing, self).printErrorMessage()
        if not show == False: super(ErrorMessageImageProcessing, self).showMessageBox()