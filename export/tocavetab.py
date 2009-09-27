import core.models as models
from django.conf import settings

import csv, re, os

#format of CAVETAB2.CSV is
headers=['KatasterNumber','KatStatusCode','Entrances','UnofficialNumber','MultipleEntrances','AutogenFile','LinkFile','LinkEntrance','Name','UnofficialName',
 'Comment','Area','Explorers','UndergroundDescription','Equipment','QMList','KatasterStatus','References','UndergroundCentreLine','UndergroundDrawnSurvey',
 'SurvexFile','Length','Depth','Extent','Notes','EntranceName','TagPoint','OtherPoint','DescriptionOfOtherPoint','ExactEntrance','TypeOfFix','GPSpreSA',
 'GPSpostSA','Northing','Easting','Altitude','Bearings','Map','Location','Approach','EntranceDescription','PhotoOfLocation','Marking','MarkingComment',
 'Findability','FindabilityComment']

def cavetabRow(cave):
    #mapping of troggle models to table columns is: (guess this could just be a tuple of tuples rather than a dictionary actually)
    columnsToModelFields={
        'Name':cave.official_name,
        'Area':cave.kat_area(),
        'KatStatusCode':cave.kataster_code,
        'KatasterNumber':cave.kataster_number,
        'UnofficialNumber':cave.unofficial_number,
        #'' : cave.entrances 		This is a multiple foreignkey now, may be tricky to dump back into csv. Work on this.
        'Explorers':cave.explorers,
        'UndergroundDescription':cave.underground_description,
        'Equipment':cave.equipment,
        'References':cave.references,
        'UndergroundDrawnSurvey':cave.survey,
        'KatasterStatus':cave.kataster_status,
        'UndergroundCentreLine':cave.underground_centre_line,
        'Notes':cave.notes,
        'Length':cave.length,
        'Depth':cave.depth,
        'Extent':cave.extent,
        'SurvexFile':cave.survex_file,
        }
        
    caveRow=['' for x in range(len(headers))]
    for column, modelField in columnsToModelFields.items():
        if modelField:
            # Very sorry about the atrocious replace below. I will fix this soon if noone beats me to it. - AC
            caveRow[headers.index(column)]=modelField.replace(u'\xd7','x').replace(u'\u201c','').replace(u'\u2013','').replace(u'\xbd','')
    return caveRow

def writeCaveTab(outfile):
    cavewriter=csv.writer(outfile,lineterminator='\r')
    cavewriter.writerow(headers)
    for cave in models.Cave.objects.all():
        cavewriter.writerow(cavetabRow(cave))


