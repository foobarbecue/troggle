import core.models as models
from django.conf import settings

import csv
import re
import os

#format of QM tables
headers=['Number','Grade','Area','Description','Page reference','Nearest station','Completion description','Comment']

def qmRow(qm):
    #mapping of troggle models to table columns is: (guess this could just be a tuple of tuples rather than a dictionary actually)
    columnsToModelFields={
        'Number':str(qm.number),
        'Grade':qm.grade,
        'Area':qm.area,
        'Description':qm.location_description,
        #'Page reference':              #not implemented
        'Nearest station':qm.nearest_station_description,
        'Completion description':qm.completion_description,
        'Comment':qm.comment
        }

    qmRow=['' for x in range(len(headers))]
    for column, modelField in columnsToModelFields.items():
        if modelField:
            # Very sorry about the atrocious replace below. I will fix this soon if noone beats me to it. - AC
            qmRow[headers.index(column)]=modelField.replace(u'\xd7','x').replace(u'\u201c','').replace(u'\u2013','').replace(u'\xbd','')
    return qmRow

def writeQmTable(outfile,cave):
    cavewriter=csv.writer(outfile,lineterminator='\r')
    cavewriter.writerow(headers)
    for qm in cave.get_QMs():
        cavewriter.writerow(qmRow(qm))
	