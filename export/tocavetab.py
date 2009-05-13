import troggle.expo.models as models
from django.conf import settings

import csv
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

##format of CAVETAB2.CSV is
headers=['KatasterNumber','KatStatusCode','Entrances','UnofficialNumber','MultipleEntrances','AutogenFile','LinkFile','LinkEntrance','Name','UnofficialName',
 'Comment','Area','Explorers','UndergroundDescription','Equipment','QMList','KatasterStatus','References','UndergroundCentreLine','UndergroundDrawnSurvey',
 'SurvexFile','Length','Depth','Extent','Notes','EntranceName','TagPoint','OtherPoint','DescriptionOfOtherPoint','ExactEntrance','TypeOfFix','GPSpreSA',
 'GPSpostSA','Northing','Easting','Altitude','Bearings','Map','Location','Approach','EntranceDescription','PhotoOfLocation','Marking','MarkingComment',
 'Findability','FindabilityComment']
headersDict={}
x=0
for column in headers:
    headersDict[x]=column
    x+=1
print headersDict

def writeCaveTab(path):
    outfile=file(path,'w')
    cavewriter=csv.writer(outfile)
    cavewriter.writerows
    for cave in Cave.objects.all():
        caverow[KatasterNumber]=cave.kataster_number
        caverow[KatStatusCode]=cave.katasternumber

def addCell(caverow, attribute):
    caverow[attribute]=cave.attribute
        
