'''
This module is the part of troggle that parses descriptions of cave parts (subcaves) from the legacy html files and saves them in the troggle database as instances of the model Subcave. Unfortunately, this parser can not be very flexible because the legacy format is poorly structured.
'''

import sys, os

import os, re, logging
from django.conf import settings
from core.models import Subcave, Cave
from utils import save_carefully

def getLinksInCaveDescription(cave):
    '''
    Returns all HTML <a href> tags from a given cave as a list of tuples
    in the format ('filename.html','Description')
    '''
    pattern='<a href=\"(.*?)\">(.*?)</a>'
    if cave.underground_description:
        return re.findall(pattern,cave.underground_description)
    else:
        return []

def importSubcaves(cave):
    for link in getLinksInCaveDescription(cave):
        try:
            subcaveFilePath=os.path.join(
                settings.EXPOWEB,
                os.path.dirname(cave.description_file),
                link[0])
            subcaveFile=open(subcaveFilePath,'r')
            description=subcaveFile.read().decode('iso-8859-1').encode('utf-8')
            
            lookupAttribs={'title':link[1], 'cave':cave}
            nonLookupAttribs={'description':description}
            newSubcave=save_carefully(Subcave,lookupAttribs=lookupAttribs,nonLookupAttribs=nonLookupAttribs)

            logging.info("Added " + unicode(newSubcave) + " to " + unicode(cave))            
        except IOError:
            logging.info("Subcave import couldn't open "+subcaveFilePath)
    
def importAllSubcaves():
    for cave in Cave.objects.all():
        importSubcaves(cave)
