import csv
import settings
from expo.models import QM, LogbookEntry, Cave
from datetime import *
import re

#sorry that the below code is ugly. I'll fix it sometime, really! - AC

QM.objects.all().delete()

def parseCaveQMs(cave,pathToCSV):
    if cave=='stein':
        try:
        	steinBr=Cave.objects.get(official_name="Steinbr&uuml;ckenh&ouml;hle")
        except Cave.DoesNotExist:
            print "Steinbruckenhoehle is not in the database. Please run parsers.cavetab first."
            return
    elif cave=='hauch':
        try:
        	hauchHl=Cave.objects.get(official_name="Hauchh&ouml;hle")
        except Cave.DoesNotExist:
            print "Steinbruckenhoehle is not in the database. Please run parsers.cavetab first."
            return	
    
    qmPath = settings.EXPOWEB+pathToCSV
    qmCSVContents = open(qmPath,'r')
    dialect=csv.Sniffer().sniff(qmCSVContents.read())
    qmCSVContents.seek(0,0)
    qmReader = csv.reader(qmCSVContents,dialect=dialect)
    qmReader.next() # Skip header row
    for line in qmReader:
        try:
            year=int(line[0][1:5])
            #check if placeholder exists for given year, create it if not
            if cave=='stein':
                placeholder, hadToCreate = LogbookEntry.objects.get_or_create(date__year=year, text="placeholder for QMs in 204", defaults={"date": date(year, 1, 1),"cave":steinBr})
            elif cave=='hauch':
                placeholder, hadToCreate = LogbookEntry.objects.get_or_create(date__year=year, text="placeholder for QMs in 234", defaults={"date": date(year, 1, 1),"cave":hauchHl})            
            if hadToCreate:
                print cave+" placeholder logbook entry for " + str(year) + " added to database"
            QMnum=re.match(r".*?-\d*?-X?(?P<numb>\d*)",line[0]).group("numb")
            newQM = QM()
            newQM.found_by=placeholder
            newQM.number=QMnum
            if line[1]=="Dig":
                newQM.grade="D"
            else:
                newQM.grade=line[1]
            newQM.area=line[2]
            newQM.location_description=line[3]
            
            newQM.completion_description=line[4]
            newQM.nearest_station_description=line[5]
            if newQM.completion_description:  # Troggle checks if QMs are completed by checking if they have a ticked_off_by trip. In the table, completion is indicated by the presence of a completion discription.
                newQM.ticked_off_by=placeholder

            newQM.comment=line[6]
            newQM.save()
            print "QM "+str(newQM) + ' added to database\r',
        except KeyError:
            continue
#        except IndexError:
#            print "Index error in " + str(line)
#           continue

parseCaveQMs(cave='stein',pathToCSV=r"smkridge/204/qm.csv")
parseCaveQMs(cave='hauch',pathToCSV=r"smkridge/234/qm.csv")
