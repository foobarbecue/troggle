import csv
import settings
from expo.models import QM, LogbookEntry, Cave
from datetime import *
import re

#sorry that the below code is ugly. I'll fix it sometime, really! - AC

QM.objects.all().delete()



def parseSteinbrQMs():
    try:
	steinBr=Cave.objects.get(official_name="Steinbr&uuml;ckenh&ouml;hle")
    except Cave.DoesNotExist:
        print "Steinbruckenhoehle is not in the database. Please run parsers.cavetab first."
	return
	
    
    qmPath = settings.EXPOWEB+r"smkridge/204/qm.csv"
    qmReader = csv.reader(open(qmPath,'r'),dialect="excel-tab")
    qmReader.next() # Skip header row
    for line in qmReader:
        year=int(line[0][1:5])

	#check if placeholder exists for given year, create it if not
	placeholder, hadToCreate = LogbookEntry.objects.get_or_create(date__year=year, text="placeholder for QMs in 204", defaults={"date": date(year, 1, 1),"cave":steinBr})
        if hadToCreate:
            print "204 placeholder logbook entry for " + str(year) + " added to database"
        QMnum=re.match(r".*?-\d*?-X?(?P<numb>\d*)",line[0]).group("numb")
	newQM = QM(found_by=placeholder,number=QMnum,grade=line[1],area=line[2],location_description=line[3],nearest_station_description=line[4],completion_description=line[5],comment=line[6])
        newQM.save()
	print "QM "+str(newQM) + " added to database"

parseSteinbrQMs()