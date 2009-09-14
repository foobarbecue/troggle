import sys, os, types, logging, stat
#sys.path.append('C:\\Expo\\expoweb')
#from troggle import *
#os.environ['DJANGO_SETTINGS_MODULE']='troggle.settings'
import settings
from core.models import *
from PIL import Image
#import settings
#import core.models as models
import csv
import re
import datetime
from utils import save_carefully

def get_or_create_placeholder(year):
    """ All surveys must be related to a logbookentry. We don't have a way to
        automatically figure out which survey went with which logbookentry,
        so we create a survey placeholder logbook entry for each year. This
        function always returns such a placeholder, and creates it if it doesn't
        exist yet.
    """
    lookupAttribs={'date__year':int(year),  'title':"placeholder for surveys",}
    nonLookupAttribs={'text':"surveys temporarily attached to this should be re-attached to their actual trips", 'date':datetime.date(int(year),1,1)}
    placeholder_logbook_entry, newly_created = save_carefully(LogbookEntry, lookupAttribs, nonLookupAttribs)
    return placeholder_logbook_entry

# dead
def readSurveysFromCSV():
    try:   # could probably combine these two
        surveytab = open(os.path.join(settings.SURVEY_SCANS, "Surveys.csv"))
    except IOError:
        import cStringIO, urllib  
        surveytab = cStringIO.StringIO(urllib.urlopen(settings.SURVEY_SCANS + "/Surveys.csv").read())
    dialect=csv.Sniffer().sniff(surveytab.read())
    surveytab.seek(0,0)
    surveyreader = csv.reader(surveytab,dialect=dialect)
    headers = surveyreader.next()
    header = dict(zip(headers, range(len(headers)))) #set up a dictionary where the indexes are header names and the values are column numbers

    # test if the expeditions have been added yet
    if Expedition.objects.count()==0:
        print "There are no expeditions in the database. Please run the logbook parser."
        sys.exit()

    
    logging.info("Deleting all scanned images")
    ScannedImage.objects.all().delete()
    
    
    logging.info("Deleting all survey objects")
    Survey.objects.all().delete()
    
    
    logging.info("Beginning to import surveys from "+str(os.path.join(settings.SURVEYS, "Surveys.csv"))+"\n"+"-"*60+"\n")
    
    for survey in surveyreader:
        #I hate this, but some surveys have a letter eg 2000#34a. The next line deals with that.
        walletNumberLetter = re.match(r'(?P<number>\d*)(?P<letter>[a-zA-Z]*)',survey[header['Survey Number']]) 
    #    print walletNumberLetter.groups()
        year=survey[header['Year']]

        
        surveyobj = Survey(
            expedition = Expedition.objects.filter(year=year)[0],
            wallet_number = walletNumberLetter.group('number'),
            logbook_entry = get_or_create_placeholder(year),
            comments = survey[header['Comments']],
            location = survey[header['Location']]
            )
        surveyobj.wallet_letter = walletNumberLetter.group('letter')
        if survey[header['Finished']]=='Yes':
            #try and find the sketch_scan
            pass
        surveyobj.save()

        
        logging.info("added survey " + survey[header['Year']] + "#" + surveyobj.wallet_number + "\r")

# dead
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
    yearPath=os.path.join(settings.SURVEY_SCANS, "years", year.year)
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
                placeholder=get_or_create_placeholder(year=int(year.year))
                survey=Survey.objects.get_or_create(wallet_number=surveyNumber, expedition=year, defaults={'logbook_entry':placeholder})[0]
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
                    print file + " is an interlaced PNG. No can do."
                continue
            scanObj.save()

# dead
def parseSurveys(logfile=None):
    readSurveysFromCSV()                
    for year in Expedition.objects.filter(year__gte=2000):   #expos since 2000, because paths and filenames were nonstandard before then
        parseSurveyScans(year)

# dead
def isInterlacedPNG(filePath): #We need to check for interlaced PNGs because the thumbnail engine can't handle them (uses PIL)
    file=Image.open(filePath)
    print filePath
    if 'interlace' in file.info:
        return file.info['interlace']
    else:
        return False


# handles url or file, so we can refer to a set of scans on another server
def GetListDir(sdir):
    res = [ ]
    if sdir[:7] == "http://":
        assert False, "Not written"
        s = urllib.urlopen(sdir)
    else:
        for f in os.listdir(sdir):
            if f[0] != ".":
                ff = os.path.join(sdir, f)
                res.append((f, ff, os.path.isdir(ff)))
    return res
        
        
        


def LoadListScansFile(survexscansfolder):
    gld = [ ]
    
    # flatten out any directories in these book files
    for (fyf, ffyf, fisdiryf) in GetListDir(survexscansfolder.fpath):
        if fisdiryf:
            gld.extend(GetListDir(ffyf))
        else:
            gld.append((fyf, ffyf, fisdiryf))
    
    for (fyf, ffyf, fisdiryf) in gld:
        assert not fisdiryf, ffyf
        if re.search("\.(?:png|jpg|jpeg)(?i)$", fyf):
            survexscansingle = SurvexScanSingle(ffile=ffyf, name=fyf, survexscansfolder=survexscansfolder)
            survexscansingle.save()

        
# this iterates through the scans directories (either here or on the remote server)
# and builds up the models we can access later
def LoadListScans():
    SurvexScanSingle.objects.all().delete()
    SurvexScansFolder.objects.all().delete()

    # first do the smkhs (large kh survey scans) directory
    survexscansfoldersmkhs = SurvexScansFolder(fpath=os.path.join(settings.SURVEY_SCANS, "smkhs"), walletname="smkhs") 
    if os.path.isdir(survexscansfoldersmkhs.fpath):
        survexscansfoldersmkhs.save()
        LoadListScansFile(survexscansfoldersmkhs)
        
    
    # iterate into the surveyscans directory
    for f, ff, fisdir in GetListDir(os.path.join(settings.SURVEY_SCANS, "surveyscans")):
        if not fisdir:
            continue
        
        # do the year folders
        if re.match("\d\d\d\d$", f):
            for fy, ffy, fisdiry in GetListDir(ff):
                assert fisdiry, ffy
                survexscansfolder = SurvexScansFolder(fpath=ffy, walletname=fy)
                survexscansfolder.save()
                LoadListScansFile(survexscansfolder)
        
        # do the 
        elif f != "thumbs":
            survexscansfolder = SurvexScansFolder(fpath=ff, walletname=f)
            survexscansfolder.save()
            LoadListScansFile(survexscansfolder)
            

def FindTunnelScan(tunnelfile, path):
    scansfolder, scansfile = None, None
    mscansdir = re.search("(\d\d\d\d#\d+\w?|1995-96kh|92-94Surveybookkh|1991surveybook|smkhs)/(.*?(?:png|jpg))$", path)
    if mscansdir:
        scansfolderl = SurvexScansFolder.objects.filter(walletname=mscansdir.group(1))
        if len(scansfolderl):
            assert len(scansfolderl) == 1
            scansfolder = scansfolderl[0]
        if scansfolder:
            scansfilel = scansfolder.survexscansingle_set.filter(name=mscansdir.group(2))
            if len(scansfilel):
                assert len(scansfilel) == 1
                scansfile = scansfilel[0]
            
        if scansfolder:
            tunnelfile.survexscansfolders.add(scansfolder)
        if scansfile:
            tunnelfile.survexscans.add(scansfile)
    
    elif path and not re.search("\.(?:png|jpg)$(?i)", path):
        name = os.path.split(path)[1]
        print "ttt", tunnelfile.tunnelpath, path, name
        rtunnelfilel = TunnelFile.objects.filter(tunnelname=name)
        if len(rtunnelfilel):
            assert len(rtunnelfilel) == 1, ("two paths with name of", path, "need more discrimination coded")
            rtunnelfile = rtunnelfilel[0]
            #print "ttt", tunnelfile.tunnelpath, path, name, rtunnelfile.tunnelpath
            tunnelfile.tunnelcontains.add(rtunnelfile)

    tunnelfile.save()


def SetTunnelfileInfo(tunnelfile):
    ff = os.path.join(settings.TUNNEL_DATA, tunnelfile.tunnelpath)
    tunnelfile.filesize = os.stat(ff)[stat.ST_SIZE]
    fin = open(ff)
    ttext = fin.read()
    fin.close()
    
    mtype = re.search("<(fontcolours|sketch)", ttext)
    assert mtype, ff
    tunnelfile.bfontcolours = (mtype.group(1)=="fontcolours")
    tunnelfile.npaths = len(re.findall("<skpath", ttext))
    tunnelfile.save()
    
    # <tunnelxml tunnelversion="version2009-06-21 Matienzo" tunnelproject="ireby" tunneluser="goatchurch" tunneldate="2009-06-29 23:22:17">
    # <pcarea area_signal="frame" sfscaledown="12.282584" sfrotatedeg="-90.76982" sfxtrans="11.676667377221136" sfytrans="-15.677173422877454" sfsketch="204description/scans/plan(38).png" sfstyle="" nodeconnzsetrelative="0.0">
    for path, style in re.findall('<pcarea area_signal="frame".*?sfsketch="([^"]*)" sfstyle="([^"]*)"', ttext):
        FindTunnelScan(tunnelfile, path)
    
    # should also scan and look for survex blocks that might have been included
    # and also survex titles as well.  
    
    tunnelfile.save()


def LoadTunnelFiles():
    tunneldatadir = settings.TUNNEL_DATA
    TunnelFile.objects.all().delete()
    tunneldirs = [ "" ]
    while tunneldirs:
        tunneldir = tunneldirs.pop()
        for f in os.listdir(os.path.join(tunneldatadir, tunneldir)):
            if f[0] == "." or f[-1] == "~":
                continue
            lf = os.path.join(tunneldir, f)
            ff = os.path.join(tunneldatadir, lf)
            if os.path.isdir(ff):
                tunneldirs.append(lf)
            elif f[-4:] == ".xml":
                tunnelfile = TunnelFile(tunnelpath=lf, tunnelname=os.path.split(f[:-4])[1])
                tunnelfile.save()
                
    for tunnelfile in TunnelFile.objects.all():
        SetTunnelfileInfo(tunnelfile)
    
        


