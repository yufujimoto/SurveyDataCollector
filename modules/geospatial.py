#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Import general libraries.
import sys, os, uuid, shutil, time, math, tempfile, logging, pyexiv2, datetime, gc

def writeHtml(parent, map_zoom = '10', map_center = '[35.54,134.817]'):
    output = os.path.join(parent.map_directory, 'location.html')
    fl_output = open(output,'w')
    
    if parent.map_tile == "OpenStreetMap":
        map_tile = "'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution: 'OpenStreetMap contributors',maxZoom: 19}"    # OpenStreetMap
    elif parent.map_tile == "Google Streets":
        map_tile = "'http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',{maxZoom: 20,subdomains:['mt0','mt1','mt2','mt3']}"         # Google Streets
    elif parent.map_tile == "Google Hybrid":
        map_tile = "'http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}',{maxZoom: 20,subdomains:['mt0','mt1','mt2','mt3']}"       # Google Hybrid
    elif parent.map_tile == "Google Satellite":
        map_tile = "'http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',{maxZoom: 20,subdomains:['mt0','mt1','mt2','mt3']}"         # Google Satellite
    elif parent.map_tile == "Google Terrain":
        map_tile = "'http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',{maxZoom: 20,subdomains:['mt0','mt1','mt2','mt3']}"         # Google Terrain
    elif parent.map_tile == u"地理院タイル":
        map_tile = "'https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png', {attribution: '地理院タイル'}"
    
    htm_head = "<!DOCTYPE html><html><meta charset='UTF-8'><title>location</title>"
    htm_link = "<link rel='stylesheet' href='https://unpkg.com/leaflet@1.2.0/dist/leaflet.css' />"
    htm_src = "<script src='https://unpkg.com/leaflet@1.2.0/dist/leaflet.js'></script>"
    htm_styl = "<style>body {padding: 0; margin: 0} html, body, #map {height: 100%; width: 100%;}</style>"
    htm_body = "<body><div id='map'></div>"
    htm_scrp = "<script>var map = L.map('map');"
    htm_tile = "L.tileLayer(" + map_tile + ").addTo(map);"
    htm_cent = "map.setView(" + map_center + "," + map_zoom + ");"
    htm_end = "</script></body></html>"
    
    htm_write = htm_head + htm_link + htm_src + htm_styl + htm_body + htm_scrp + htm_tile + htm_cent + htm_end
    
    fl_output.write(htm_write)
    fl_output.close()
    
    
    