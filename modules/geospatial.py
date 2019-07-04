#!/usr/bin/python
# coding: UTF-8

import os, sys, geocoder
import modules.error as error

class mapObject(object):
    @property
    def map_title(self): return self._map_title
    @property
    def map_tile(self): return self._map_tile
    @property
    def map_functions(self): return self._map_functions
    @property
    def map_markers(self): return self._map_markers
    @property
    def map_lines(self): return self._map_lines
    @property
    def map_polygons(self): return self._map_polygons
    @property
    def map_events(self): return self._map_events
    
    @map_title.setter
    def map_title(self, value): self._map_title = value
    @map_tile.setter
    def map_tile(self, value): self._map_tile = value
    @map_functions.setter
    def map_functions(self, value): self._map_functions = value
    @map_markers.setter
    def map_markers(self, value): self._map_markers = value
    @map_lines.setter
    def map_lines(self, value): self._map_lines = value
    @map_polygons.setter
    def map_polygons(self, value): self._map_polygons = value
    
    def __init__(self, title = None, tile=None, func=None, markers = None, lines = None, polys = None, events = None):
        self._map_title = title
        self._map_source = 'lib/leaflet.js'     #'https://unpkg.com/leaflet@1.5.1/dist/leaflet.js'
        self._map_style = 'lib/leaflet.css'     #'https://unpkg.com/leaflet@1.5.1/dist/leaflet.css'
        self._map_tile = tile
        self._map_functions = func
        self._map_markers = markers
        self._map_lines = lines
        self._map_polygons = polys
        self._map_events = events
    
    def publishMap(self, output, zoom=15):
        print("geospatial::mapTile::publishMap(self, output, zoom=15)")
        
        try:
            saveAs = open(output, 'w')
            
            saveAs.write("<!DOCTYPE html>\n")
            saveAs.write("<html>\n")
            saveAs.write("\t<head>\n")
            saveAs.write("\t\t<title>%s</title>\n" % self._map_title)
            saveAs.write("\t\t<meta charset='utf-8' />\n")
            saveAs.write("\t\t<meta name='viewport' content='width=device-width, initial-scale=1.0'>\n")
            saveAs.write("\t\t<link rel='stylesheet' href='%s' />\n" % self._map_style)
            saveAs.write("\t\t<script src='%s'></script>\n" % self._map_source)
            
            events = self._map_events
            if events != None and len(events) > 0:
                for event in events:
                    saveAs.write("\t\t<script src='%s'></script>\n" % event.script_source)
            
            saveAs.write("\t\t<style>body {padding: 0; margin: 0} html, body, #map {height: 100%; width: 100%;}</style>\n")
            saveAs.write("\t</head>\n")
            saveAs.write("\t<body>\n")
            saveAs.write("\t\t<div id='map'></div>\n")
            
            tileSettings = self._map_tile.createHtmlTileSettings(zoom)
            
            saveAs.write("\t\t<script>\n")
            saveAs.write(tileSettings)
            saveAs.write("\t\t</script>\n")
            
            markers = self._map_markers
            if markers != None and len(markers) > 0:
                for marker in markers:
                    saveAs.write("\t\t<script>\n")
                    saveAs.write("%s\n" % marker.createMarker())
                    saveAs.write("\t\t</script>\n")
                
            lines = self._map_lines
            if lines != None and len(lines) > 0:
                saveAs.write("\t\t<script>\n")
                saveAs.write("\t\t</script>\n")
            
            polys = self._map_polygons
            if polys != None and len(polys) > 0:
                saveAs.write("\t\t<script>\n")
                saveAs.write("\t\t</script>\n")
            
            if events != None and len(events) > 0:
                for event in events:
                    saveAs.write("\t\t<script>\n")
                    saveAs.write("%s\n" % event.createJsMapEvent())
                    saveAs.write("\t\t</script>\n")
            
            saveAs.write("\t</body>\n")
            saveAs.write("</html>\n")
            saveAs.close()
            print("OK")
        except Exception as e:
            print("Error occured in publishMap(self, output, zoom=15)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

class mapTile(object):
    @property
    def tile_name(self): return self._tile_name
    @property
    def tile_style(self): return self._tile_style
    @property
    def tile_src(self): return self._tile_src
    @property
    def tile_center(self): return self._tile_center
    @property
    def tile_attribution(self): return self._tile_attribution
    @property
    def tile_minZoom(self): return self._tile_minZoom
    @property
    def tile_maxZoom(self): return self._tile_maxZoom
    @property
    def tile_subdomains(self): return self._tile_subdomains
    
    @tile_name.setter
    def tile_name(self, value): self._tile_name = value
    @tile_style.setter
    def tile_style(self, value): self._tile_style = value
    @tile_src.setter
    def tile_src(self, value): self._tile_src = value
    @tile_center.setter
    def tile_center(self, value): self._center = value
    @tile_attribution.setter
    def tile_attribution(self, value): self._tile_attribution = value
    @tile_minZoom.setter
    def tile_minZoom(self, value): self._tile_minZoom = value
    @tile_maxZoom.setter
    def tile_maxZoom(self, value): self._tile_maxZoom = value
    @tile_subdomains.setter
    def tile_subdomains(self, value): self._tile_subdomains = value
    
    def __init__(self, name = '', src = '', cntr = [0,0], attr = '', minz = 0, maxz = 18, sub = "'abc'"):
        self._tile_name = name
        self._tile_src = src
        self._tile_center = cntr
        self._tile_attribution = attr
        self._tile_minZoom = minz
        self._tile_maxZoom = maxz
        self._tile_subdomains = sub
    
    def createHtmlTileSettings(self, zoom):
        print("geospatial::mapTile::createHtmlTileSettings(self)")
        
        try:
            # Define the map object and its center.
            lat_center = self._tile_center[0]
            lon_center = self._tile_center[1]
            
            txt_map = "\t\t\tvar map = L.map('map');\n" 
            
            # Set the tile layer with specific attributes.
            src = self._tile_src
            attr = self._tile_attribution
            minz = self._tile_minZoom
            maxz = self._tile_maxZoom
            sub = self._tile_subdomains
            
            txt_lay = '\t\t\tL.tileLayer("%s", {attribution: "%s",minZoom: %s, maxZoom: %s, subdomains: %s}).addTo(map);\n' % (src, attr, minz, maxz, sub)
            txt_set = '\t\t\tmap.setView([%s, %s], %s);\n' % (lat_center, lon_center, zoom)
            
            # Return the value.
            return(txt_map + txt_lay + txt_set)
        except Exception as e:
            print("Error occured in geospatial::mapTile::createHtmlTileSettings(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)

class mapEvent(object):
    @property
    def script_source(self): return self._script_source
    @property
    def script_event(self): return self._script_event
    @property
    def script_function(self): return self._script_function
    
    @script_source.setter
    def script_source(self, value): self._script_source = value
    @script_event.setter
    def script_event(self, value): self._script_event = value
    @script_source.setter
    def script_function(self, value): self._script_function = value
    
    def __init__(self, src = None, event = None, func = None):
        self._script_source = src
        self._script_event = event
        self._script_function = func
    
    def createJsMapEvent(self):
        print("geospatial::mapEvent::createJsMapEvent(self)")
        
        try:
            txt_event = "\t\t\tmap.on('%s', %s);" % (self._script_event, self._script_function)
            return(txt_event)
        except Exception as e:
            print("Error occured in geospatial::mapEvent::createJsMapEvent(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)
    
class mapMarker(object):
    @property
    def geometry(self): return self._geometry
    @property
    def description(self): return self._description
    
    @geometry.setter
    def geometry(self, value): self._geometry = value
    @description.setter
    def description(self, value): self._description = value
    
    def __init__(self, geom = None, desc = None):
        self._geometry = geom
        self._description = desc
    
    def createMarker(self):
        print("geospatial::mapMarker::createMarker(self)")
        
        try:
            txt_marker = "\t\t\tL.marker(%s).addTo(map);" % self._geometry
            return(txt_marker)
        except Exception as e:
            print("Error occured in geospatial::mapMarker::createMarker(self)")
            print(str(e))
            error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
            return(None)


def writeHtml(parent, output, map_zoom = 2, map_center = [32.6759094,129.4209844], markers = None):
    print("geospatial::writeHtml(parent, output, map_zoom = 2, map_center = [32.6759094,129.4209844], markers = None)")
    
    try:
        if parent.map_tile == "OpenStreetMap":      # OpenStreetMap
            src = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attr =  "Map data &copy; <a href='https://www.openstreetmap.org/'>OpenStreetMap</a>contributors, <a href='https://creativecommons.org/licenses/by-sa/2.0/'>CC-BY-SA</a>, Imagery © <a href='https://www.mapbox.com/'>Mapbox</a>"
            minz = 0
            maxz = 19
            sub = "'abc'"
        elif parent.map_tile == "Google Streets":   # Google Streets
            src = "http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}"
            attr =  "Google Streets"
            minz = 0
            maxz = 20
            sub = "['mt0','mt1','mt2','mt3']"
        elif parent.map_tile == "Google Hybrid":    # Google Hybrid
            src = "http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}"
            attr =  "Google Hybrid"
            minz = 0
            maxz = 20
            sub = "['mt0','mt1','mt2','mt3']"
        elif parent.map_tile == "Google Satellite": # Google Satellite
            src = "http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
            attr =  "Google Satellite"
            minz = 0
            maxz = 20
            sub = "['mt0','mt1','mt2','mt3']"
        elif parent.map_tile == "Google Terrain":   # Google Terrain
            src = "http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}"
            attr =  "Google Terrain"
            minz = 0
            maxz = 20
            sub = "['mt0','mt1','mt2','mt3']"
        elif parent.map_tile == u"地理院タイル":
            src = "https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png"
            attr =  u"地理院タイル"
            minz = 0
            maxz = 18
        else:
            src = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attr =  "Map data &copy; <a href='https://www.openstreetmap.org/'>OpenStreetMap</a>contributors, <a href='https://creativecommons.org/licenses/by-sa/2.0/'>CC-BY-SA</a>, Imagery © <a href='https://www.mapbox.com/'>Mapbox</a>"
            minz = 0
            maxz = 19
            sub = "'abc'"
        
        # Generate the click event to get geographic coordinates from the map.
        newEvent = mapEvent(src='lib/copyToClipboard.js', event='click', func='copyCoord')
        
        # Generate the background map tile from the given map server.
        newTile = mapTile(name = '', src = src, cntr = map_center, attr = attr, minz = minz, maxz = maxz, sub = sub)
        
        # Generate the map objects.
        newMap = mapObject(title = 'Get Coordinates from the Map', tile=newTile, markers = markers, events = [newEvent])
        
        # Publish map for leaflet.
        newMap.publishMap(output, zoom = map_zoom)
        
    except Exception as e:
        print("Error occured in main::createMapByLocationName(self)")
        print(str(e))
        error.ErrorMessageUnknown(details=str(e), show=True, language=parent.language)
        return(None)    

def geoCoding(geoname, proxies=None):
    print("geospatial::geoCoding(geoname, proxies=None)")
    
    try:
        if not proxies == None:
            g = geocoder.arcgis(geoname, proxies=proxies)
        else:
            g = geocoder.arcgis(geoname)
        
        return(g.latlng)
    except Exception as e:
        print("Error occured in geospatial::geoCoding(geoname, proxies=None)")
        print(str(e))
        error.ErrorMessageUnknown(details=str(e), show=True, language=self._language)
        return(None)
    
    
    