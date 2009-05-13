# -*- coding: utf-8 -*-
import sys
sys.path.append("/home/mjg/expoweb/troggle")
import expo.models as models
import settings as settings
import csv
import time

import re
import os

##format of CAVETAB2.CSV is
KatasterNumber = 0
KatStatusCode = 1
Entrances = 2
UnofficialNumber = 3
MultipleEntrances = 4
AutogenFile = 5
LinkFile = 6
LinkEntrance = 7
Name = 8
UnofficialName = 9
Comment = 10
Area = 11
Explorers = 12
UndergroundDescription = 13
Equipment = 14
QMList = 15
KatasterStatus = 16
References = 17
UndergroundCentreLine = 18
UndergroundDrawnSurvey = 19
SurvexFile = 20
Length = 21
Depth = 22
Extent = 23
Notes = 24
EntranceName = 25
TagPoint = 26
OtherPoint = 27
DescriptionOfOtherPoint = 28
ExactEntrance = 29
TypeOfFix = 30
GPSpreSA = 31
GPSpostSA = 32
Northing = 33
Easting = 34
Altitude = 35
Bearings = 36
Map = 37
Location = 38
Approach = 39
EntranceDescription = 40
PhotoOfLocation = 41
Marking = 42
MarkingComment = 43
Findability = 44
FindabilityComment = 45


def html_to_wiki(text):
    if type(text) != str:
        return text
    text = unicode(text, "utf-8")
    #Characters
    #text = re.sub("&uuml;", u"\xfc", text)
    #text = re.sub("&ouml;", u"\xf6", text)
    #text = re.sub("&auml;", u"\xe4", text)
    #text = re.sub("&deg;", u"\xb0", text)
    #text = re.sub("&copy;", u"\xa9", text)
    #text = re.sub("&amp;", u"\x26", text)
    #text = re.sub("&szlig;", u"\xdf", text)
    #text = re.sub("&szlig;", u"\xdf", text)
    #text = re.sub("&lt;", u"<", text)
    #text = re.sub("&gt;", u">", text)
    #text = re.sub("&egrave;", u"\xe8", text)
    #text = re.sub("&eacute;", u"\xe9", text)
    #text = re.sub("&quote;", u'"', text)
    #text = re.sub("&quot;", u'"', text)
    #text = re.sub("&Ouml;", u'\xd6', text)
    #text = re.sub("&times;", u'"', text)

    #text = re.sub("&(.*);", "/1", text)
    #if s:
    #    print s.groups()
    #Lists
    text = re.sub("</p>", r"", text)
    text = re.sub("<p>$", r"", text)
    text = re.sub("<p>", r"\n\n", text)
    out = ""
    lists = ""
    while text:
        mstar = re.match("^(.*?)<ul>\s*<li[^>]*>(.*?)</li>(.*)$", text, re.DOTALL)
        munstar = re.match("^(\s*)</ul>(.*)$", text, re.DOTALL)
        mhash = re.match("^(.*?)<ol>\s*<li[^>]*>(.*?)</li>(.*)$", text, re.DOTALL)
        munhash = re.match("^(\s*)</ol>(.*)$", text, re.DOTALL)
        mitem = re.match("^(\s*)<li[^>]*>(.*?)</li>(.*)$", text, re.DOTALL)
        ms = [len(m.groups()[0]) for m in [mstar, munstar, mhash, munhash, mitem] if m]
        def min_(i, l):
            try:
                v = i.groups()[0]
                l.remove(len(v))
                return len(v) < min(l, 1000000000)
            except:
                return False
        if min_(mstar, ms):
            lists += "*"
            pre, val, post = mstar.groups()
            out += pre + "\n" + lists + " " + val
            text = post
        elif min_(mhash, ms):
            lists += "#"
            pre, val, post = mhash.groups()
            out += pre + "\n" + lists + " " + val
            text = post
        elif min_(mitem, ms):
            pre, val, post = mitem.groups()
            out += "\n" + lists + " " + val
            text = post
        elif min_(munstar, ms):
            lists = lists[:-1]
            text = munstar.groups()[1]
        elif min_(munhash, ms):
            lists.pop()
            text = munhash.groups()[1]
        else:
            out += text
            text = ""
    text2 = out
    while text2:
        mtag = re.match("^(.*?)<(.*?)>(.*)$", text, re.DOTALL)
        if mtag:
            text2 = mtag.groups()[2]
            print mtag.groups()[1]
        else:
            text2 = ""
    return out

def LoadCaveTab():
    cavetab = open(os.path.join(settings.EXPOWEB, "noinfo", "CAVETAB2.CSV"))
    caveReader = csv.reader(cavetab)
    caveReader.next() # Strip out column headers
    
    for katArea in ['1623', '1626']:
        if not models.Area.objects.filter(short_name = katArea):
            newArea = models.Area(short_name = katArea)
            newArea.save()
    area1626 = models.Area.objects.filter(short_name = '1626')[0]
    area1623 = models.Area.objects.filter(short_name = '1623')[0]
    
    counter=0
    for line in caveReader :
        if line[Area] == 'nonexistent':
            continue
        entranceLetters=[] #Used in caves that have mulitlple entrances, which are not described on seperate lines
        if line[MultipleEntrances] == 'yes' or line[MultipleEntrances]=='':
            args = {}
            def addToArgs(CSVname, modelName):
                if line[CSVname]:
                    args[modelName] = html_to_wiki(line[CSVname])
            addToArgs(KatasterNumber, "kataster_number")
            addToArgs(KatStatusCode, "kataster_code")
            addToArgs(UnofficialNumber, "unofficial_number")
            addToArgs(Name, "official_name")
            addToArgs(Comment, "notes")
            addToArgs(Explorers, "explorers")
            addToArgs(UndergroundDescription, "underground_description")
            addToArgs(Equipment, "equipment")
            addToArgs(KatasterStatus, "kataster_status")
            addToArgs(References, "references")
            addToArgs(UndergroundCentreLine, "underground_centre_line")
            addToArgs(UndergroundDrawnSurvey, "survey")
            addToArgs(Length, "length")
            addToArgs(Depth, "depth")
            addToArgs(Extent, "extent")
            addToArgs(SurvexFile, "survex_file")
            addToArgs(Notes, "notes")

            newCave = models.Cave(**args)
            newCave.Sethref()
            newCave.save()
    
            if line[Area]:
                if line[Area] ==  "1626":
                    newCave.area.add(area1626)
                else:
                    area = models.Area.objects.filter(short_name = line[Area])
                    if area:
                        newArea = area[0]
                    else:
                        newArea = models.Area(short_name = line[Area], parent = area1623)
                        newArea.save()
                    newCave.area.add(newArea)
            else:
                newCave.area.add(area1623)
    
            newCave.save()

        if line[UnofficialName]:
            newUnofficialName = models.OtherCaveName(cave = newCave, name = line[UnofficialName])
            newUnofficialName.save()
    
        if line[MultipleEntrances] == '' or \
            line[MultipleEntrances] == 'entrance' or \
            line[MultipleEntrances] == 'last entrance':
            args = {}
            def addToArgs(CSVname, modelName):
                if line[CSVname]:
                    args[modelName] = html_to_wiki(line[CSVname])
            def addToArgsViaDict(CSVname, modelName, dictionary):
                if line[CSVname]:
                    args[modelName] = dictionary[html_to_wiki(line[CSVname])]
            addToArgs(EntranceName, 'name')
            addToArgs(Explorers, 'explorers')
            addToArgs(Map, 'map_description')
            addToArgs(Location, 'location_description')
            addToArgs(Approach, 'approach')
            addToArgs(EntranceDescription, 'entrance_description')
            addToArgs(UndergroundDescription, 'underground_description')
            addToArgs(PhotoOfLocation, 'photo')
            addToArgsViaDict(Marking, 'marking', {"Paint": "P",
                                                "Paint (?)": "P?",
                                                "Tag": "T",
                                                "Tag (?)": "T?",
                                                "Retagged": "R",
                                                "Retag": "R",
                                                "Spit": "S",
                                                "Spit (?)": "S?",
                                                "Unmarked": "U",
                                                "": "?",
                                                })
            addToArgs(MarkingComment, 'marking_comment')
            addToArgsViaDict(Findability, 'findability', {"Surveyed": "S",
                                                        "Lost": "L",
                                                        "Refindable": "R",
                                                        "": "?",
                                                        "?": "?",
                                                        })
            addToArgs(FindabilityComment, 'findability_description')
            addToArgs(Easting, 'easting')
            addToArgs(Northing, 'northing')
            addToArgs(Altitude, 'alt')
            addToArgs(DescriptionOfOtherPoint, 'other_description')
            def addToArgsSurveyStation(CSVname, modelName):
                if line[CSVname]:
                    surveyPoint = models.SurveyStation(name = line[CSVname])
                    surveyPoint.save()
                    args[modelName] = html_to_wiki(surveyPoint)
            addToArgsSurveyStation(TagPoint, 'tag_station')
            addToArgsSurveyStation(ExactEntrance, 'exact_station')
            addToArgsSurveyStation(OtherPoint, 'other_station')
            addToArgs(OtherPoint, 'other_description')
            if line[GPSpreSA]:
                addToArgsSurveyStation(GPSpreSA, 'other_station')
                args['other_description'] = 'pre selective availability GPS'
            if line[GPSpostSA]:
                addToArgsSurveyStation(GPSpostSA, 'other_station')
                args['other_description'] = 'post selective availability GPS'
            addToArgs(Bearings, 'bearings')
            newEntrance = models.Entrance(**args)
            newEntrance.save()
    
            if line[Entrances]:
                entrance_letter = line[Entrances]
            else:
                entrance_letter = ''
    
            newCaveAndEntrance = models.CaveAndEntrance(cave = newCave, entrance = newEntrance, entrance_letter = entrance_letter)
            newCaveAndEntrance.save()


# lookup function modelled on GetPersonExpeditionNameLookup
Gcavelookup = None
def GetCaveLookup():
    global Gcavelookup
    if Gcavelookup:
        return Gcavelookup
    Gcavelookup = {"NONEPLACEHOLDER":None}
    for cave in models.Cave.objects.all():
        Gcavelookup[cave.official_name.lower()] = cave
        if cave.kataster_number:
            Gcavelookup[cave.kataster_number] = cave
        if cave.unofficial_number:
            Gcavelookup[cave.unofficial_number] = cave
    
    Gcavelookup["tunnocks"] = Gcavelookup["258"]
    Gcavelookup["hauchhole"] = Gcavelookup["234"]
    return Gcavelookup
        
        
