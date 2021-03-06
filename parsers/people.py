#.-*- coding: utf-8 -*-

from django.conf import settings
import core.models as models
import csv, re, datetime, os, shutil
from utils import save_carefully

def saveMugShot(mugShotPath, mugShotFilename, person):
    if mugShotFilename.startswith(r'i/'): #if filename in cell has the directory attached (I think they all do), remove it
        mugShotFilename=mugShotFilename[2:]
    else:
        mugShotFilename=mugShotFilename # just in case one doesn't
    
    dummyObj=models.Photo(file=mugShotFilename)
    
    #Put a copy of the file in the right place. mugShotObj.file.path is determined by the django filesystemstorage specified in models.py
    if not os.path.exists(dummyObj.file.path):
        shutil.copy(mugShotPath, dummyObj.file.path)
    
    mugShotObj, created = save_carefully(
        models.Photo,
        lookupAttribs={'is_mugshot':True, 'file':mugShotFilename},
        nonLookupAttribs={'caption':"Mugshot for "+person.first_name+" "+person.last_name}
        )
    
    if created:
        mugShotObj.contains_person.add(person)
        mugShotObj.save()	

def parseMugShotAndBlurb(personline, header, person):
    """create mugshot Photo instance"""
    mugShotFilename=personline[header["Mugshot"]]
    mugShotPath = os.path.join(settings.EXPOWEB, "folk", mugShotFilename)
    if mugShotPath[-3:]=='jpg': #if person just has an image, add it
        saveMugShot(mugShotPath=mugShotPath, mugShotFilename=mugShotFilename, person=person)
    elif mugShotPath[-3:]=='htm': #if person has an html page, find the image(s) and add it. Also, add the text from the html page to the "blurb" field in his model instance.
        personPageOld=open(mugShotPath,'r').read()
        if not person.blurb:
            person.blurb=re.search('<body>.*<hr',personPageOld,re.DOTALL).group() #this needs to be refined, take care of the HTML and make sure it doesn't match beyond the blurb
            for mugShotFilename in re.findall('i/.*?jpg',personPageOld,re.DOTALL):
                mugShotPath = os.path.join(settings.EXPOWEB, "folk", mugShotFilename)
                saveMugShot(mugShotPath=mugShotPath, mugShotFilename=mugShotFilename, person=person)
    person.save()

def LoadPersonsExpos():
    
    persontab = open(os.path.join(settings.EXPOWEB, "noinfo", "folk.csv"))
    personreader = csv.reader(persontab)
    headers = personreader.next()
    header = dict(zip(headers, range(len(headers))))
    
    # make expeditions
    print "Loading expeditions"
    years = headers[5:]
    
    for year in years:
        lookupAttribs = {'year':year}
        nonLookupAttribs = {'name':"CUCC expo %s" % year}
        
        save_carefully(models.Expedition, lookupAttribs, nonLookupAttribs)

    
    # make persons
    print "Loading personexpeditions"
    #expoers2008 = """Edvin Deadman,Kathryn Hopkins,Djuke Veldhuis,Becka Lawson,Julian Todd,Natalie Uomini,Aaron Curtis,Tony Rooke,Ollie Stevens,Frank Tully,Martin Jahnke,Mark Shinwell,Jess Stirrups,Nial Peters,Serena Povia,Olly Madge,Steve Jones,Pete Harley,Eeva Makiranta,Keith Curtis""".split(",")
    #expomissing = set(expoers2008)

    for personline in personreader:
        name = personline[header["Name"]]
        name = re.sub("<.*?>", "", name)
        mname = re.match("(\w+)(?:\s((?:van |ten )?\w+))?(?:\s\(([^)]*)\))?", name)
        nickname = mname.group(3) or ""
	
        lookupAttribs={'first_name':mname.group(1), 'last_name':(mname.group(2) or "")}
        nonLookupAttribs={'is_vfho':personline[header["VfHO member"]],}
        person, created = save_carefully(models.Person, lookupAttribs, nonLookupAttribs)
	
        parseMugShotAndBlurb(personline=personline, header=header, person=person)
    
        # make person expedition from table
        for year, attended in zip(headers, personline)[5:]:
            expedition = models.Expedition.objects.get(year=year)
            if attended == "1" or attended == "-1":
                lookupAttribs = {'person':person, 'expedition':expedition}
                nonLookupAttribs = {'nickname':nickname, 'is_guest':(personline[header["Guest"]] == "1")}
                save_carefully(models.PersonExpedition, lookupAttribs, nonLookupAttribs)


    # this fills in those people for whom 2008 was their first expo
    #print "Loading personexpeditions 2008"
    #for name in expomissing:
        # firstname, lastname = name.split()
        # is_guest = name in ["Eeva Makiranta", "Keith Curtis"]
        # print "2008:", name
        # persons = list(models.Person.objects.filter(first_name=firstname, last_name=lastname))
        # if not persons:
            # person = models.Person(first_name=firstname, last_name = lastname, is_vfho = False, mug_shot = "")
            # #person.Sethref()
            # person.save()
        # else:
            # person = persons[0]
        # expedition = models.Expedition.objects.get(year="2008")
        # personexpedition = models.PersonExpedition(person=person, expedition=expedition, nickname="", is_guest=is_guest)
        # personexpedition.save()

    #Notability is now a method of person. Makes no sense to store it in the database; it would need to be recalculated every time something changes. - AC 16 Feb 09
    # could rank according to surveying as well
    #print "Setting person notability"
    #for person in models.Person.objects.all():
        #person.notability = 0.0
        #for personexpedition in person.personexpedition_set.all():
            #if not personexpedition.is_guest:
                #person.notability += 1.0 / (2012 - int(personexpedition.expedition.year))
        #person.bisnotable = person.notability > 0.3 # I don't know how to filter by this
        #person.save()
        
        
# used in other referencing parser functions
# expedition name lookup cached for speed (it's a very big list)
Gpersonexpeditionnamelookup = { }
def GetPersonExpeditionNameLookup(expedition):
    global Gpersonexpeditionnamelookup
    res = Gpersonexpeditionnamelookup.get(expedition.name)
    if res:
        return res
    
    res = { }
    duplicates = set()
    
    print "Calculating GetPersonExpeditionNameLookup for", expedition.year
    personexpeditions = models.PersonExpedition.objects.filter(expedition=expedition)
    for personexpedition in personexpeditions:
        possnames = [ ]
        f = personexpedition.person.first_name.lower()
        l = personexpedition.person.last_name.lower()
        if l:
            possnames.append(f + " " + l)
            possnames.append(f + " " + l[0])
            possnames.append(f + l[0])
            possnames.append(f[0] + " " + l)
        possnames.append(f)
        if personexpedition.nickname:
            possnames.append(personexpedition.nickname.lower())
        
        for possname in possnames:
            if possname in res:
                duplicates.add(possname)
            else:
                res[possname] = personexpedition
        
    for possname in duplicates:
        del res[possname]
    
    Gpersonexpeditionnamelookup[expedition.name] = res
    return res

