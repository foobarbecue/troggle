# -*- coding: utf-8 -*-
import core.models as models
from django.conf import settings
import csv, time, re, os, logging
from utils import save_carefully
from utils import html_to_wiki

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

def LoadCaveTab():
    cavetab = open(os.path.join(settings.EXPOWEB, "noinfo", "CAVETAB2.CSV"),'rU')
    caveReader = csv.reader(cavetab)
    caveReader.next() # Strip out column headers

    logging.info("Beginning to import caves from "+str(cavetab)+"\n"+"-"*60+"\n")

    for katArea in ['1623', '1626']:
        if not models.Area.objects.filter(short_name = katArea):
            newArea = models.Area(short_name = katArea)
            newArea.save()
            logging.info("Added area "+str(newArea.short_name)+"\n")
    area1626 = models.Area.objects.filter(short_name = '1626')[0]
    area1623 = models.Area.objects.filter(short_name = '1623')[0]
    
    counter=0
    for line in caveReader :
        if line[Area] == 'nonexistent':
            continue
        entranceLetters=[] #Used in caves that have mulitlple entrances, which are not described on seperate lines
        if line[MultipleEntrances] == 'yes' or line[MultipleEntrances]=='': #When true, this line contains an actual cave, otherwise it is an extra entrance.
            args = {}
            defaultArgs = {}
            
            def addToArgs(CSVname, modelName):
                if line[CSVname]:
                    args[modelName] = html_to_wiki(line[CSVname])
                    
            def addToDefaultArgs(CSVname, modelName): #This has to do with the non-destructive import. These arguments will be passed as the "default" dictionary in a get_or_create
                if line[CSVname]:
                    defaultArgs[modelName] = html_to_wiki(line[CSVname])
            
            # The attributes added using "addToArgs" will be used to look up an existing cave. Those added using "addToDefaultArgs" will not.
            addToArgs(KatasterNumber, "kataster_number")
            addToDefaultArgs(KatStatusCode, "kataster_code")
            addToArgs(UnofficialNumber, "unofficial_number")
            addToArgs(Name, "official_name")
            addToDefaultArgs(Comment, "notes")
            addToDefaultArgs(Explorers, "explorers")
            addToDefaultArgs(UndergroundDescription, "underground_description")
            addToDefaultArgs(Equipment, "equipment")
            addToDefaultArgs(KatasterStatus, "kataster_status")
            addToDefaultArgs(References, "references")
            addToDefaultArgs(UndergroundCentreLine, "underground_centre_line")
            addToDefaultArgs(UndergroundDrawnSurvey, "survey")
            addToDefaultArgs(Length, "length")
            addToDefaultArgs(Depth, "depth")
            addToDefaultArgs(Extent, "extent")
            addToDefaultArgs(SurvexFile, "survex_file")
            addToDefaultArgs(Notes, "notes")
            
            #The following adds the legacy_file_path.  This is always in either Autogen file or Link file
            for header in (AutogenFile,LinkFile):
                if line[header]:
                    addToDefaultArgs(header,"description_file")
                    break
                    

            #The following checks if this cave is non-public i.e. we don't have rights to display it online.
            #Noinfo was the name of the old password protected directory, so if it has that then we will
            #set the non_public field of the model instance to true.
            defaultArgs["non_public"]=line[AutogenFile].startswith('noinfo') or line[LinkFile].startswith('noinfo')

            newCave, created=save_carefully(models.Cave, lookupAttribs=args, nonLookupAttribs=defaultArgs)
            logging.info("Added cave "+str(newCave)+"\n")

            #If we created a new cave, add the area to it. This does mean that if a cave's identifying features have not changed, areas will not be updated from csv.
            if created and line[Area]:
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
            elif created:
                newCave.area.add(area1623)

            newCave.save()
            
            logging.info("Added area "+line[Area]+" to cave "+str(newCave)+"\n")

            if created and line[UnofficialName]:
                newUnofficialName = models.OtherCaveName(cave = newCave, name = line[UnofficialName])
                newUnofficialName.save()

                logging.info("Added unofficial name "+str(newUnofficialName)+" to cave "+str(newCave)+"\n")

        if created and line[MultipleEntrances] == '' or \
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
                    args[modelName] = surveyPoint
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

            logging.info("Added entrance "+str(newEntrance)+"\n")
    
            if line[Entrances]:
                entrance_letter = line[Entrances]
            else:
                entrance_letter = ''
    
            newCaveAndEntrance = models.CaveAndEntrance(cave = newCave, entrance = newEntrance, entrance_letter = entrance_letter)
            newCaveAndEntrance.save()
            
            logging.info("Added CaveAndEntrance "+str(newCaveAndEntrance)+"\n")


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
        
        
