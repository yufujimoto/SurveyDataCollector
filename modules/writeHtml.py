#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Import general libraries.
import sys, os

def startHtml(title): 
    html =  '''
                <!DOCTYPE html>\n
                <html lang='en'>\n
                \t<head>\n
                \t\t<meta charset='utf-8'>\n
                \t\t<meta http-equiv='X-UA-Compatible' content='IE=edge'>\n
                \t\t<meta name='viewport' content='width=device-width, initial-scale=1'>\n
                \t\t<title>%s</title>\n
                \t\t<link href='theme/css/bootstrap.min.css' rel='stylesheet'>\n
                \t\t<link href='theme/css/bootstrap-theme.min.css' rel='stylesheet'>\n
                \t\t<link href='theme/theme.css' rel='stylesheet'>\n
                \t</head>\n\n
            ''' %(title)
    return(html)

def setMenuBar(pages):
    begining =  '''
                    \t\t<div class='navbar navbar-default navbar-fixed-top' role='navigation'>\n
                    \t\t\t<div class='container'>\n
                    \t\t\t\t<div class='navbar-header'>\n
                    \t\t\t\t\t<a class='navbar-brand' href='index.html'>Survey Data Collector</a>\n
                    \t\t\t\t</div>\n
                    \t\t\t\t<div class='collapse navbar-collapse'>\n
                    \t\t\t\t\t<ul class='nav navbar-nav' >\n
                '''
    if not pages == None:
        entry = ""
        
        for title, url in pages.iteritems():
            entry = entry + "\t\t\t\t\t\t<li><a href='%s'>%s</a></li>\n" %(url, title)
    else:
        entry = ""
    
    ending =    '''
                    \t\t\t\t\t</ul>\n
                    \t\t\t\t</div>\n
                    \t\t\t</div>\n
                    \t\t</div>\n
                '''
    
    menu = begining + entry + ending
    
    return(menu)

def setConsolidation(consolidation):
    con_uuid = consolidation.uuid.encode('utf-8')
    con_cnam = consolidation.name.encode('utf-8')
    con_gano = consolidation.geographic_annotation.encode('utf-8')
    con_tano = consolidation.temporal_annotation.encode('utf-8')
    con_desc = consolidation.description.encode('utf-8')
    con_imgs = consolidation.images
    
    if con_imgs:
        if not (len(con_imgs) == 0 or con_imgs == None):
            avatar = "images/" + con_imgs[0].uuid + ".jpg"
        else:
            avatar = "images/noimage.jpg"
    else:
        avatar = "images/noimage.jpg"
    
    div_con =   '''
                    \t\t<div id='%s' class='row' style='padding:0px'>\n
                    \t\t\t<div class='col-xs-12' style='padding:0px; background-color: #f8f8f8;'>\n
                    \t\t\t\t<h3>%s</h3>\n
                    \t\t\t</div>\n
                    \t\t\t<div class='row' style='padding:0px'>\n
                    \t\t\t\t<div class='col-xs-3' style='padding:0px'>\n
                    \t\t\t\t\t<div style='padding: 0px; margin: 5px; width:300px; line-height: 250px; text-align: center; background-color: black;'>\n
                    \t\t\t\t\t\t<a href='%s'>\n
                    \t\t\t\t\t\t\t<img height=200 src='%s' alt='img'/>\n
                    \t\t\t\t\t\t</a>\n
                    \t\t\t\t\t</div>\n
                    \t\t\t\t</div>\n
                    \t\t\t\t<div class='col-xs-9' style='padding:0px'>\n
                    \t\t\t\t\t<ul>\n
                    \t\t\t\t\t\t<li><h4>Geographic Annotation: %s</h4></li>\n
                    \t\t\t\t\t\t<li><h4>Temporal Annotation: %s</h4></li>\n
                    \t\t\t\t\t\t<li style='text-align:justify;'><h4>Description：</h4><p>%s</p></li>\n
                    \t\t\t\t\t</ul>\n
                    \t\t\t\t</div>\n
                    \t\t\t</div>\n
                    \t\t</div>\n
                ''' % (con_uuid, con_cnam, avatar.encode('utf-8'), avatar.encode('utf-8'), con_gano, con_tano, con_desc)
    return(div_con)

def startBody():
    body =   '''
                \t<body　role='document'>\n
            '''
    return(body)

def startContents():
    contents =  '''
                    \t\t<div id='container' class='container' style='padding-top: 70px'>
                '''
    return(contents)

def endContents():
    contents =  '''
                    \t\t</div>\n
                '''
    return(contents)

def endBody():
    body = "\t</body>\n"
    return(body)

def endHtml():
    html = "</thml>"
    return(html)

