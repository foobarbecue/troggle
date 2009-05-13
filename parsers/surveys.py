import sys
import os
import urllib
import types
#sys.path.append('C:\\Expo\\expoweb')
from troggle import *
#os.environ['DJANGO_SETTINGS_MODULE']='troggle.settings'
import troggle.settings as settings
import troggle.expo.models as models
import troggle.expo.fileAbstraction as fileAbstraction

#import settings
#import expo.models as models
import csv
import re
import datetime
import cStringIO

surveytab = fileAbstraction.readFile("Surveys.csv")
dialect=csv.Sniffer().sniff(surveytab)
surveyreader = csv.reader(cStringIO.StringIO(surveytab),dialect=dialect)
print surveyreader
headers = surveyreader.next()
header = dict(zip(headers, range(len(headers)))) #set up a dictionary where the indexes are header names and the values are column numbers
print header

# test if the expeditions have been added yet
if len(models.Expedition.objects.all())==0:
    print "There are no expeditions in the database. Please run the logbook parser."
    sys.exit()
models.ScannedImage.objects.all().delete()
models.Survey.objects.all().delete()
for survey in surveyreader:
    print type(survey), survey
    walletNumberLetter = re.match(r'(?P<number>\d*)(?P<letter>[a-zA-Z]*)',survey[header['Survey Number']]) #I hate this, but some surveys have a letter eg 2000#34a. This line deals with that.
#    print walletNumberLetter.groups()

    surveyobj = models.Survey(
        expedition = models.Expedition.objects.filter(year=survey[header['Year']])[0],
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
    yearDirList = fileAbstraction.dirsAsList(year.year)
    for surveyFolder in yearDirList:
        print surveyFolder
        try:
            surveyNumber=re.match(r'\d\d\d\d#0*(\d+)',surveyFolder).groups()
            scanList=fileAbstraction.filesAsList(year.year, surveyFolder)
            print "BAR: ", year.year, surveyFolder, scanList
        except AttributeError:
            print surveyFolder + " ignored"
            continue

        for scan in scanList:
            try:
                scanChopped=re.match(r'(?i).*(notes|elev|plan|elevation|extend)(\d*)\.(png|jpg|jpeg)',scan).groups()
                print "BAR: ", scanChopped
                scanType,scanNumber,scanFormat=scanChopped
            except AttributeError:
                print "Adding scans: " + scan + " ignored"
                continue
	    if scanType == 'elev' or scanType == 'extend':
		scanType = 'elevation'

            if scanNumber=='':
                scanNumber=1

            if type(surveyNumber)==types.TupleType:
                surveyNumber=surveyNumber[0]
            try:
                survey=models.Survey.objects.get_or_create(wallet_number=surveyNumber, expedition=year)[0]
            except models.Survey.MultipleObjectsReturned:
                survey=models.Survey.objects.filter(wallet_number=surveyNumber, expedition=year)[0]

            scanObj = models.ScannedImage(
                file=os.path.join(year.year, surveyFolder, scan),
                contents=scanType,
                number_in_wallet=scanNumber,
                survey=survey
                )
            print "Added scanned image at " + str(scanObj)
            scanObj.save()
                
for year in models.Expedition.objects.filter(year__gte=2000):   #expos since 2000, because paths and filenames were nonstandard before then
    parseSurveyScans(year)
