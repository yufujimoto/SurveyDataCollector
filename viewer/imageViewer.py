#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Import PyQt5 libraries for generating the GUI application.
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QThread, pyqtSignal

class ImageViewScene(QGraphicsScene):
    def __init__( self, *argv, **keywords ):
        super( ImageViewScene, self ).__init__( *argv, **keywords )
        
        self.__zoom          = 1.0
        self.__image_item    = None
        self.__currentPos    = None
        self.__pressedButton = None
    
    def setFile(self, img_path):
        print("ImageViewScene::setFile(self, img_path)")
        
        try:
            # Get the image as QPixmap object.
            pixmap = QPixmap(img_path)
            
            # Refresh the image object if exists.
            if self.__image_item: self.removeItem(self.__image_item)
            
            # Set the item as movable.
            item = QGraphicsPixmapItem(pixmap)
            item.setFlags(QGraphicsItem.ItemIsMovable)
            
            # Add the QPixmap object to the scene.
            self.addItem(item)
            self.__image_item = item
            
            # Fit the image.
            self.fitImage()
        except Exception as e:
            print("Error in ImageViewScene::setFile(self, img_path)")
            print(str(e))
    
    def imageItem(self):
        print("ImageViewScene::imageItem(self)")
        
        try:
            return self.__image_item
        except Exception as e:
            print("Error in ImageViewScene::imageItem(self)")
            print(str(e))
            return(None)
    
    def fitImage(self):
        print("ImageViewScene::fitImage(self)")
        
        # Exit if the image is not loaded.
        if not self.imageItem(): return(None)
        
        try:
            # Get the rectangle of the image and the scene.
            rect_image = self.imageItem().boundingRect()
            rect_scene = self.sceneRect()
            
            # Get the aspect ratio of image and scene.
            aspect_ratio = 100
            aspect_ratio_image  = rect_image.width() / rect_image.height()
            aspect_ratio_scene = rect_scene.width() / rect_scene.height()
            
            # Define the aspect ratio of the image object to display.
            if aspect_ratio_image >= aspect_ratio_scene:
                aspect_ratio = rect_scene.width() / rect_image.width()
            else:
                aspect_ratio = rect_scene.height() / rect_image.height()
            
            # Create the transform object.
            transform = QTransform()
            
            # Apply the aspect ratio.
            transform.scale(aspect_ratio, aspect_ratio)
            
            # Transform the image object.
            self.imageItem().setTransform(transform)
        except Exception as e:
            print("Error in ImageViewScene::fitImage(self)")
            print(str(e))
    
    def mousePressEvent(self, event):
        print("ImageViewScene::mousePressEvent(self, event)")
        
        try:
            # Get current position and pressed button.
            self.__currentPos = event.scenePos()
            self.__pressedButton = event.button()
            
            # Set the cursor icon as closed hand shape.
            cursorShape = Qt.ClosedHandCursor
            
            # Apply the cursor.
            qApp.setOverrideCursor(QCursor(cursorShape))
        except Exception as e:
            print("Error in ImageViewScene::mousePressEvent(self, event)")
            print(str(e))
    
    def wheelEvent(self, event):
        print("ImageViewScene::wheelEvent(self, event)")
        
        # Exit if the image is not loaded.
        if not self.imageItem(): return(None)
        
        try:
            # Get the current secne position.
            scene_pos = event.scenePos()
            
            # Set the zoom factor from mouse wheel.
            self.__zoom = 1.0 + float(event.delta())/1000
            
            # Create the transform object.
            transform = self.imageItem().transform()
            
            # Set the zoom factor.
            transform.scale(self.__zoom, self.__zoom)
            
            # Apply zooming to the image object.
            self.imageItem().setTransform( transform )
        except Exception as e:
            print("Error in ImageViewScene::mousePressEvent(self, event)")
            print(str(e))
        
    def mouseMoveEvent(self, event):
        print("ImageViewScene::mouseMoveEvent(self, event)")
        
        # Exit if the current position is not acquired.
        if not self.__currentPos: return(None)
        
        # Exit if the image is not loaded.
        if not self.imageItem(): return(None)
        
        try:
            # Get the current position.
            scene_pos = event.scenePos()
            
            # Get the new position current position and moved position.
            new_scne_pos = scene_pos - self.__currentPos
            self.__currentPos = scene_pos
                    
            # Create the transform object.
            transform = self.imageItem().transform()
            
            # Set the new scene position.
            transform *= QTransform().translate(new_scne_pos.x(), new_scne_pos.y())
            
            # Apply the new scene position.
            self.imageItem().setTransform(transform)
        except Exception as e:
            print("Error in ImageViewScene::mouseMoveEvent(self, event)")
            print(str(e))
    
    def mouseReleaseEvent(self, event):
        print("ImageViewScene::mouseReleaseEvent(self, event)")
        
        try:
            self.__currentPos    = None
            self.__pressedButton = None
            qApp.restoreOverrideCursor()
            super( ImageViewScene, self ).mouseReleaseEvent( event )
        except Exception as e:
            print("Error in ImageViewScene::mouseReleaseEvent(self, event)")
            print(str(e))

class ImageViewer(QGraphicsView):
    def __init__( self ):
        super( ImageViewer, self ).__init__( )
  
        # Set up the graphic viewer.
        self.setCacheMode( QGraphicsView.CacheBackground )
        self.setRenderHints( QPainter.Antialiasing | QPainter.SmoothPixmapTransform | QPainter.TextAntialiasing)
        
        # Create the custom scene object.
        scene = ImageViewScene(self)
        scene.setSceneRect(QRectF(self.rect()))
        
        self.setScene(scene)
  
    def setFile(self, img_path):
        print("ImageViewer::setFile(self, img_path):")
        
        try:
            # Set the file and initialyze the scene.
            self.scene().setSceneRect(QRectF(self.rect()))
            self.scene().setFile(img_path)
        except Exception as e:
            print("Error in ImageViewer::setFile(self, img_path)")
            print(str(e))
        
    def resizeEvent( self, event ):
        print("ImageViewer::setFile(self, img_path):")
        
        try:
            # Update the rectangle if the view had resized.
            super( ImageViewer, self ).resizeEvent( event )
            self.scene().setSceneRect(QRectF(self.rect()))
        except Exception as e:
            print("Error in ImageViewer::setFile(self, img_path)")
            print(str(e))