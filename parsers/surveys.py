import sys
import os
import types
sys.path.append('C:\\Expo\\expoweb')
from troggle import *
os.environ['DJANGO_SETTINGS_MODULE']='troggle.settings'
import troggle.settings as settings
import troggle.expo.models as models

#import settings
#import expo.models as models
import csv
import re
import datetime

surveytab = open(os.path.join(settings.SURVEYS, "Surveys.csv"))
dialect=csv.Sniffer().sniff(surveytab.read())
surveytab.seek(0,0)
surveyreader = csv.reader(surveytab,dialect=dialect)
headers = surveyreader.next()
header = dict(zip(headers, range(len(headers)))) #set up a dictionary where the indexes are header names and the values are column numbers

# test if the expeditions have been added yet
if len(models.Expedition.objects.all())==0:
    print "There are no expeditions in the database. Please run the logbook parser."
    sys.exit()
models.ScannedImage.objects.all().delete()
models.Survey.objects.all().delete()
for survey in surveyreader:
    walletNumberLetter = re.match(r'(?P<number>\d*)(?P<letter>[a-zA-Z]*)',survey[header['Survey Number']]) #I hate this, but some surveys have a letter eg 2000#34a. This line deals with that.
#    print walletNumberLetter.groups()
    
    surveyobj = models.Survey(
        expedition_year = models.Expedition.objects.filter(year=survey[header['Year']])[0],
        wallet_number = walletNumberLetter.group('number'),

        comments = survey[header['Comments']],
        location = survey[header['Location']]
        )
    surveyobj.wallet_letter = walletNumberLetter.group('letter')
    if survey[header['Finished']]=='Yes':
        #try and find the sketch_scan
        pass
    surveyobj.save()
    print "added survey " + survey[header['Year']] + "#" + surveyobj.wallet_number
    
# add survey scans
def parseSurveyScans(year):
    yearPath=os.path.join(settings.SURVEYS, year.year)
    yearFileList=os.listdir(yearPath)
    for surveyFolder in yearFileList:
        try:
            surveyNumber=re.match(r'\d\d\d\d#0*(\d+)',surveyFolder).groups()
            scanList=os.listdir(os.path.join(yearPath,surveyFolder))
        except AttributeError:
            print surveyFolder + " ignored"
            continue

        for scan in scanList:
            try:
                scanChopped=re.match(r'([a-zA-Z]*)(\d*)\.(png|jpg|JPG|PNG)',scan).groups()
                scanType,scanNumber,scanFormat=scanChopped
            except AttributeError:
                print scan + " ignored"
                continue
            if scanNumber=='':
                scanNumber=1

            if type(surveyNumber)==types.TupleType:
                surveyNumber=surveyNumber[0]
            try:
                survey=models.Survey.objects.get_or_create(wallet_number=surveyNumber, expedition_year=year)[0]
            except models.Survey.MultipleObjectsReturned:
                survey=models.Survey.objects.filter(wallet_number=surveyNumber, expedition_year=year)[0]
               
            scanObj = models.ScannedImage(
                file=os.path.join(yearPath, surveyFolder, scan),
                contents=scanType,
                number_in_wallet=scanNumber,
                survey=survey
                )
            print "Added scanned image at " + str(scanObj)
            scanObj.save()
                
for year in models.Expedition.objects.filter(year__gte=2000):   #expos since 2000, because paths and filenames were nonstandard before then
    parseSurveyScans(year)
