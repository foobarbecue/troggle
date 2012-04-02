import core.models as models
from django.conf import settings

import csv, re, os

#This determines the column order
headers={'cavetab2':['KatasterNumber','KatStatusCode','Entrances','UnofficialNumber','MultipleEntrances','AutogenFile','LinkFile','LinkEntrance','Name','UnofficialName',
 'Comment','Area','Explorers','UndergroundDescription','Equipment','QMList','KatasterStatus','References','UndergroundCentreLine','UndergroundDrawnSurvey',
 'SurvexFile','Length','Depth','Extent','Notes','EntranceName','TagPoint','OtherPoint','DescriptionOfOtherPoint','ExactEntrance','TypeOfFix','GPSpreSA',
 'GPSpostSA','Northing','Easting','Altitude','Bearings','Map','Location','Approach','EntranceDescription','PhotoOfLocation','Marking','MarkingComment',
 'Findability','FindabilityComment'],
 'hubeStyle':['Name','Latititude','Longitude','Description','First visit','Latest visit','Est visit frequency','Log count','Photo count','Survey count','Timeseries count']}
 
def cavetabRow(cave, style):
    #mapping of troggle models to table columns is: (guess this could just be a tuple of tuples rather than a dictionary actually)
    columnsToModelFields={
        'hubeStyle':{
            'Name':cave.official_name,
            'Latititude':cave.lat(),
            'Longitude':cave.lon(),
            'Description':cave.underground_description,
            'First visit':cave.firstVisit(),
            'Latest visit':cave.latestVisit(),
            'Est visit frequency':'Not yet implemented',
            'Log count':cave.logbookentry_set.count(),
            'Photo count':cave.photo_set.count(),
            'Survey count':cave.survey_set().count(),
            'Timeseries count':cave.timeseries_set().count()
            },
    
        'cavetab2':{
            'Name':cave.official_name,
            'Area':cave.kat_area,
            'KatStatusCode':cave.kataster_code,
            'KatasterNumber':cave.number,
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
            'SurvexFile':cave.survex_file
            }
        }
        
    caveRow=['' for x in range(len(headers[style]))]
    for column, modelField in columnsToModelFields[style].items():
        if modelField:
            # Very sorry about the atrocious replace below. I will fix this soon if noone beats me to it. - AC
            caveRow[headers[style].index(column)]=unicode(modelField).replace(u'\xd7','x').replace(u'\u201c','').replace(u'\u2013','').replace(u'\xbd','')
    return caveRow

def writeCaveTab(outfile, style='cavetab2'):
    cavewriter=csv.writer(outfile,lineterminator='\r')
    cavewriter.writerow(headers[style])
    for cave in models.Cave.objects.all():
        cavewriter.writerow(cavetabRow(cave, style=style))

    