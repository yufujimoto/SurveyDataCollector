#!/usr/bin/env python2
# -*- encoding:utf-8 -*-

from __future__ import print_function

import flickrapi
import os

class Flickr(object):
    @property
    def api_key(self): return self._api_key
    @property
    def api_secret(self): return self._api_secret
    @property
    def api(self): return self._api
    
    @api_key.setter
    def api_key(self, value): self._api_key = value
    @api_secret.setter
    def api_secret(self, value): self._api_secret = value
    @api.setter
    def api(self, value): self._api = value
    
    def __init__(self, api_key, secret_key):
        self.initApi(api_key, secret_key)
        
    def initApi(self, api_key, secret_key):
        # Initialyze the Frickr API.
        self._api_key = api_key
        self._api_secret = secret_key
        self._api = flickrapi.FlickrAPI(api_key, secret_key)
        
        if not self._api.token_valid():
            # Out of band call back.
            self._api.get_request_token(oauth_callback="oob")
            
            # Veryfying code.
            verifier = str(input("Get verifier code from {} and enter it here.\n: ".format(self._api.auth_url(perms="write"))))
            
            # Get access token and store it as ${HOME}/.flickr/oauth-tokens.sqlite.
            # If you want to remove the cache, call api.token_cache.forget().
            self._api.get_access_token(verifier)

class FlickrPhotoSet(Flickr):
    @property
    def photoset_id(self): return self._photoset_id
    @property
    def title(self): return self._title
    @property
    def description(self): return self._description
    @property
    def primary_photo_id(self): return self._primary_photo_id
    @property
    def photos(self): return self._photos
    
    @photoset_id.setter
    def photoset_id(self, value): self._photoset_id = value
    @title.setter
    def title(self, value): self._title = value
    @description.setter
    def description(self, value): self._description = value
    @primary_photo_id.setter
    def primary_photo_id(self, value): self._primary_photo_id = value
    @photos.setter
    def photos(self,value): self._photos = value
    
    def __init__(self, api_key, secret_key, title, description, primary_photo_id=None, photos=[]):
        # Initialize the super class.
        Flickr.__init__(self, api_key, secret_key)
        
        self._title = title
        self._description = description
        self._primary_photo_id = primary_photo_id
        self._photos = photos
        
    def createPhotoset(self):
        try:
            # Create a photoset with title, description and id of the cover photo.
            request_createPhotoset = self._api.photosets.create(
                title=self._title,
                description=self._description,
                primary_photo_id=self._primary_photo_id
            )
            
            # Get the photoset id.
            self._photoset_id = request_createPhotoset.find("photoset").get("id") 
        except Exception as e:
            print(str(e))
            return None
    
    def addPhotosToPhotoset(self):
        try:
            for photo in self._photos:
                # Add uploaded photo to photosets.
                self._api.photosets.addPhoto(photoset_id=self._photoset_id, photo_id=photo)
        except Exception as e:
            print(str(e))
            return None

class FlickrPhoto(Flickr):
    @property
    def photo_id(self): return self._photo_id
    @property
    def path(self): return self._path
    @property
    def title(self): return self._title
    @property
    def description(self): return self._description
    @property
    def tags(self): return self._tags
    
    @photo_id.setter
    def photo_id(self, value): self._photo_id = value
    @path.setter
    def path(self, value): self._path = value
    @title.setter
    def title(self, value): self._title = value
    @description.setter
    def description(self, value): self._description = value
    @tags.setter
    def tags(self, value): self._tags = value
    
    def __init__(self, api_key, secret_key, photo_id=None, path="", title="", description="", tags=None):
        # Initialize the super class.
        Flickr.__init__(self, api_key, secret_key)
        
        self._photo_id = photo_id
        self._path = path
        self._title = title
        self._description = description
        self._tags = tags
    
    def upload(self):
        try:
             # Upload photo and get the ID.
            request_upload = super(FlickrPhoto,self).api.upload(
                filename=self._path, 
                title=self._title, 
                description=self._description, 
                is_private=True)
            
            # Check the result and exit if not OK.
            if request_upload.get("stat") != "ok":
                print("flickrapi.upload({}) failed.".format(self._path))
                return None
            
            # Get the uploaded photo's ID.
            self._photo_id = request_upload.find("photoid").text
            
            return self._photo_id
        except Exception as e:
            print(str(e))
            return None
    
    def replace(self):
        try:
             # Upload photo and get the ID.
            request_replace = super(FlickrPhoto,self).api.replace(
                photo_id=self._photo_id, 
                filename=self._path)
            
            # Check the result and exit if not OK.
            if request_replace.get("stat") != "ok":
                print("flickrapi.upload({}) failed.".format(self._path))
                return None
            
            return self._photo_id
        except Exception as e:
            print(str(e))
            return None
    
    def getInfo(self):
        try:
            request_getinfo = super(FlickrPhoto,self).api.photos_getInfo(photo_id=self._photo_id)
            photo = request_getinfo.find('photo')
            
            if len(photo) < 1:
                return(None)
            else:
                return photo
        except Exception as e:
            print(str(e))
            return None
