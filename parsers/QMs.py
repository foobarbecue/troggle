# -*- coding: UTF-8 -*-

import csv
import settings
from expo.models import QM, LogbookEntry, Cave
from datetime import *
from helpers import save_carefully
import re

def deleteQMs():
    QM.objects.all().delete()

def parseCaveQMs(cave,inputFile):
    """Runs through the CSV file at inputFile (which is a relative path from expoweb) and saves each QM as a QM instance."""

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
    elif cave =='kh':
        try:
            kh=Cave.objects.get(official_name="Kaninchenh&ouml;hle")
        except Cave.DoesNotExist:
            print "Steinbruckenhoehle is not in the database. Please run parsers.cavetab first."
        for file in inputFile:
            parse_KH_QMs(kh, inputFile=file) 
        return

    qmPath = settings.EXPOWEB+inputFile
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
                placeholder, hadToCreate = LogbookEntry.objects.get_or_create(date__year=year, title="placeholder for QMs in 204", text="QMs temporarily attached to this should be re-attached to their actual trips", defaults={"date": date(year, 1, 1),"cave":steinBr})
            elif cave=='hauch':
                placeholder, hadToCreate = LogbookEntry.objects.get_or_create(date__year=year, title="placeholder for QMs in 234", text="QMs temporarily attached to this should be re-attached to their actual trips", defaults={"date": date(year, 1, 1),"cave":hauchHl})            
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
            try:
                preexistingQM=QM.objects.get(number=QMnum, found_by__date__year=year)  #if we don't have this one in the DB, save it
                if preexistingQM.new_since_parsing==False:  #if the pre-existing QM has not been modified, overwrite it
                    preexistingQM.delete()
                    newQM.save()
                    print "overwriting " + str(preexistingQM) +"\r",
                
                else:  # otherwise, print that it was ignored
                    print "preserving "+ str(preexistingQM) + ", which was edited in admin \r",
                    
            except QM.DoesNotExist:         #if there is no pre-existing QM, save the new one
                newQM.save() 
                print "QM "+str(newQM) + ' added to database\r',
                
        except KeyError: #check on this one
            continue
#        except IndexError:
#            print "Index error in " + str(line)
#           continue

def parse_KH_QMs(kh, inputFile):
    """import QMs from the 1623-161 (Kaninchenhöhle) html pages
    """
    khQMs=open(settings.EXPOWEB+inputFile,'r')
    khQMs=khQMs.readlines()
    for line in khQMs:
        res=re.search('name=\"[CB](?P<year>\d*)-(?P<cave>\d*)-(?P<number>\d*).*</a> (?P<grade>[ABDCV])<dd>(?P<description>.*)\[(?P<nearest_station>.*)\]',line)
        if res:
            res=res.groupdict()
            year=int(res['year'])
        #check if placeholder exists for given year, create it if not
            placeholder, hadToCreate = LogbookEntry.objects.get_or_create(date__year=year, title="placeholder for QMs in 161", text="QMs temporarily attached to this should be re-attached to their actual trips", defaults={"date": date((year), 1, 1),"cave":kh})
            lookupArgs={
                'found_by':placeholder,
                'number':res['number']
                }
            nonLookupArgs={
                'grade':res['grade'],
                'nearest_station':res['nearest_station'],
                'location_description':res['description']
                }
            
            if 
            
            save_carefully(QM,lookupArgs,nonLookupArgs)
        

parseCaveQMs(cave='kh', inputFile=r"smkridge/161/qmtodo.htm")
parseCaveQMs(cave='stein',inputFile=r"smkridge/204/qm.csv")
parseCaveQMs(cave='hauch',inputFile=r"smkridge/234/qm.csv")

