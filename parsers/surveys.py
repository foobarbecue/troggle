import sys
import os
import types
#sys.path.append('C:\\Expo\\expoweb')
#from troggle import *
#os.environ['DJANGO_SETTINGS_MODULE']='troggle.settings'
import troggle.settings as settings
from troggle.expo.models import *
from PIL import Image
#import settings
#import expo.models as models
import csv
import re
import datetime

def readSurveysFromCSV(logfile=None):
    try:
        surveytab = open(os.path.join(settings.SURVEYS, "Surveys.csv"))
    except IOError:
        import cStringIO, urllib
        surveytab = cStringIO.StringIO(urllib.urlopen(settings.SURVEYS + "download/Surveys.csv").read())
    dialect=csv.Sniffer().sniff(surveytab.read())
    surveytab.seek(0,0)
    surveyreader = csv.reader(surveytab,dialect=dialect)
    headers = surveyreader.next()
    header = dict(zip(headers, range(len(headers)))) #set up a dictionary where the indexes are header names and the values are column numbers

    # test if the expeditions have been added yet
    if Expedition.objects.count()==0:
        print "There are no expeditions in the database. Please run the logbook parser."
        sys.exit()

    if logfile:
        logfile.write("Deleting all scanned images")
    ScannedImage.objects.all().delete()
    
    if logfile:
        logfile.write("Deleting all survey objects")
    Survey.objects.all().delete()
    
    if logfile:
        logfile.write("Beginning to import surveys from "+str(os.path.join(settings.SURVEYS, "Surveys.csv"))+"\n"+"-"*60+"\n")
    
    for survey in surveyreader:
        walletNumberLetter = re.match(r'(?P<number>\d*)(?P<letter>[a-zA-Z]*)',survey[header['Survey Number']]) #I hate this, but some surveys have a letter eg 2000#34a. This line deals with that.
    #    print walletNumberLetter.groups()

        surveyobj = Survey(
            expedition = Expedition.objects.filter(year=survey[header['Year']])[0],
            wallet_number = walletNumberLetter.group('number'),

            comments = survey[header['Comments']],
            location = survey[header['Location']]
            )
        surveyobj.wallet_letter = walletNumberLetter.group('letter')
        if survey[header['Finished']]=='Yes':
            #try and find the sketch_scan
            pass
        surveyobj.save()

        if logfile:
            logfile.write("added survey " + survey[header['Year']] + "#" + surveyobj.wallet_number + "\r")

def listdir(*directories):
    try:
        return os.listdir(os.path.join(settings.SURVEYS, *directories))
    except:
        import urllib
        url = settings.SURVEYS + reduce(lambda x, y: x + "/" + y, ["listdir"] + list(directories))
        folders = urllib.urlopen(url.replace("#", "%23")).readlines()
        return [folder.rstrip(r"/") for folder in folders]

# add survey scans
def parseSurveyScans(year, logfile=None):
#    yearFileList = listdir(year.year)
    yearPath=os.path.join(settings.SURVEY_SCANS, year.year)
    yearFileList=os.listdir(yearPath)
    print yearFileList
    for surveyFolder in yearFileList:
        try:
            surveyNumber=re.match(r'\d\d\d\d#0*(\d+)',surveyFolder).groups()
#            scanList = listdir(year.year, surveyFolder)
            scanList=os.listdir(os.path.join(yearPath,surveyFolder))
        except AttributeError:
            print surveyFolder + " ignored",
            continue

        for scan in scanList:
            try:
                scanChopped=re.match(r'(?i).*(notes|elev|plan|elevation|extend)(\d*)\.(png|jpg|jpeg)',scan).groups()
                scanType,scanNumber,scanFormat=scanChopped
            except AttributeError:
                print scan + " ignored \r",
                continue
            if scanType == 'elev' or scanType == 'extend':
                scanType = 'elevation'

            if scanNumber=='':
                scanNumber=1

            if type(surveyNumber)==types.TupleType:
                surveyNumber=surveyNumber[0]
            try:
                survey=Survey.objects.get_or_create(wallet_number=surveyNumber, expedition=year)[0]
            except Survey.MultipleObjectsReturned:
                survey=Survey.objects.filter(wallet_number=surveyNumber, expedition=year)[0]
            file=os.path.join(year.year, surveyFolder, scan)
            scanObj = ScannedImage(
                file=file,
                contents=scanType,
                number_in_wallet=scanNumber,
                survey=survey,
                new_since_parsing=False,
                )
            #print "Added scanned image at " + str(scanObj)
            if scanFormat=="png":
                if isInterlacedPNG(os.path.join(settings.SURVEY_SCANS,file)):
                    print file + "is an interlaced PNG. No can do."
                continue
            scanObj.save()

def parseSurveys(logfile=None):
    readSurveysFromCSV()                
    for year in Expedition.objects.filter(year__gte=2000):   #expos since 2000, because paths and filenames were nonstandard before then
        parseSurveyScans(year)

def isInterlacedPNG(filePath): #We need to check for interlaced PNGs because the thumbnail engine can't handle them (uses PIL)
    file=Image.open(filePath)
    return file.info['interlace']
    