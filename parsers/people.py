#.-*- coding: utf-8 -*-

import troggle.settings as settings
import troggle.expo.models as models
import csv
import re
import datetime
import os
import shutil

#   Julian: the below code was causing errors and it seems like a duplication of the above. Hope I haven't broken anything by commenting it. -Aaron
#
#        if name in expoers2008:
#            print "2008:", name
#            expomissing.discard(name) # I got an error which I think was caused by this -- python complained that a set changed size during iteration.
#            yo = models.Expedition.objects.filter(year = "2008")[0]
#            pyo = models.PersonExpedition(person = pObject, expedition = yo, is_guest=is_guest)
#            pyo.save()



def saveMugShot(mugShotPath, mugShotFilename, person):
    if mugShotFilename.startswith(r'i/'): #if filename in cell has the directory attached (I think they all do), remove it
        mugShotFilename=mugShotFilename[2:]
    else:
        mugShotFilename=mugShotFilename # just in case one doesn't

    mugShotObj = models.Photo(
        caption="Mugshot for "+person.first_name+" "+person.last_name,
        is_mugshot=True,
        file=mugShotFilename,
        )
    
    shutil.copy(mugShotPath, mugShotObj.file.path) #Put a copy of the file in the right place. mugShotObj.file.path is determined by the django filesystemstorage specified in models.py
    
    mugShotObj.save()
    mugShotObj.contains_person.add(person)
    mugShotObj.save()	

def parseMugShotAndBlurb(personline, header, person):
    #create mugshot Photo instance
    mugShotFilename=personline[header["Mugshot"]]
    mugShotPath = os.path.join(settings.EXPOWEB, "folk", mugShotFilename)
    if mugShotPath[-3:]=='jpg': #if person just has an image, add it
        saveMugShot(mugShotPath=mugShotPath, mugShotFilename=mugShotFilename, person=person)
    elif mugShotPath[-3:]=='htm': #if person has an html page, find the image(s) and add it. Also, add the text from the html page to the "blurb" field in his model instance.
        personPageOld=open(mugShotPath,'r').read()
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
    models.Expedition.objects.all().delete()
    years = headers[5:]
    
    for year in years:
        expedition = models.Expedition(year = year, name = "CUCC expo %s" % year)
        expedition.save()

    
    # make persons
    print "Loading personexpeditions"
    models.Person.objects.all().delete()
    models.PersonExpedition.objects.all().delete()
    expoers2008 = """Edvin Deadman,Kathryn Hopkins,Djuke Veldhuis,Becka Lawson,Julian Todd,Natalie Uomini,Aaron Curtis,Tony Rooke,Ollie Stevens,Frank Tully,Martin Jahnke,Mark Shinwell,Jess Stirrups,Nial Peters,Serena Povia,Olly Madge,Steve Jones,Pete Harley,Eeva Makiranta,Keith Curtis""".split(",")
    expomissing = set(expoers2008)

    for personline in personreader:
        name = personline[header["Name"]]
        name = re.sub("<.*?>", "", name)
        mname = re.match("(\w+)(?:\s((?:van |ten )?\w+))?(?:\s\(([^)]*)\))?", name)
        nickname = mname.group(3) or ""

        person = models.Person(first_name=mname.group(1), last_name=(mname.group(2) or ""))
        person.is_vfho = personline[header["VfHO member"]]
        #person.Sethref()
        #print "NNNN", person.href
        is_guest = (personline[header["Guest"]] == "1")  # this is really a per-expo catagory; not a permanent state
        person.save()
        parseMugShotAndBlurb(personline=personline, header=header, person=person)
    
        # make person expedition from table
        for year, attended in zip(headers, personline)[5:]:
            expedition = models.Expedition.objects.get(year=year)
            if attended == "1" or attended == "-1":
                personexpedition = models.PersonExpedition(person=person, expedition=expedition, nickname=nickname, is_guest=is_guest)
                personexpedition.save()


    # this fills in those people for whom 2008 was their first expo
    print "Loading personexpeditions 2008"
    for name in expomissing:
        firstname, lastname = name.split()
        is_guest = name in ["Eeva Makiranta", "Keith Curtis"]
        print "2008:", name
        persons = list(models.Person.objects.filter(first_name=firstname, last_name=lastname))
        if not persons:
            person = models.Person(first_name=firstname, last_name = lastname, is_vfho = False, mug_shot = "")
            person.Sethref()
            person.save()
        else:
            person = persons[0]
        expedition = models.Expedition.objects.get(year="2008")
        personexpedition = models.PersonExpedition(person=person, expedition=expedition, nickname="", is_guest=is_guest)
        personexpedition.save()

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

