#.-*- coding: utf-8 -*-

import settings
import expo.models as models
import csv
import re
import os
import datetime

persontab = open(os.path.join(settings.EXPOWEB, "noinfo", "folk.csv"))
personreader = csv.reader(persontab)
headers = personreader.next()
header = dict(zip(headers, range(len(headers))))


def LoadExpos():
    models.Expedition.objects.all().delete()
    years = headers[5:]
    years.append("2008")
    for year in years:
        y = models.Expedition(year = year, name = "CUCC expo%s" % year)
        y.save()
    print "lll", years 

def LoadPersons():
    models.Person.objects.all().delete()
    models.PersonExpedition.objects.all().delete()
    expoers2008 = """Edvin Deadman,Kathryn Hopkins,Djuke Veldhuis,Becka Lawson,Julian Todd,Natalie Uomini,Aaron Curtis,Tony Rooke,Ollie Stevens,Frank Tully,Martin Jahnke,Mark Shinwell,Jess Stirrups,Nial Peters,Serena Povia,Olly Madge,Steve Jones,Pete Harley,Eeva Makiranta,Keith Curtis""".split(",")
    expomissing = set(expoers2008)

    for person in personreader:
        name = person[header["Name"]]
        name = re.sub("<.*?>", "", name)
        lname = name.split()
        mbrack = re.match("\((.*?)\)", lname[-1])

        if mbrack:
            nickname = mbrack.group(1)
            del lname[-1]
        elif name == "Anthony Day":
            nickname = "Dour"
        else:
            nickname = ""

        if len(lname) == 3:  # van something
            firstname, lastname = lname[0], "%s %s" % (lname[1], lname[2])
        elif len(lname) == 2:
            firstname, lastname = lname[0], lname[1]
        elif len(lname) == 1:
            firstname, lastname = lname[0], ""
        else:
            assert False, lname
        #print firstname, lastname
        #assert lastname == person[header[""]], person

        pObject = models.Person(first_name = firstname,
                                last_name = lastname,
                                is_vfho = person[header["VfHO member"]],
                                mug_shot = person[header["Mugshot"]])
        pObject.save()
        is_guest = person[header["Guest"]] == "1"  # this is really a per-expo catagory; not a permanent state

        for year, attended in zip(headers, person)[5:]:
            yo = models.Expedition.objects.filter(year = year)[0]
            if attended == "1" or attended == "-1":
                pyo = models.PersonExpedition(person = pObject, expedition = yo, nickname=nickname, is_guest=is_guest)
                pyo.save()

        if name in expoers2008:
            print "2008:", name
            expomissing.discard(name)
            yo = models.Expedition.objects.filter(year = "2008")[0]
            pyo = models.PersonExpedition(person = pObject, expedition = yo, is_guest=is_guest)
            pyo.save()


    # this fills in those peopl for whom 2008 was their first expo
    for name in expomissing:
        firstname, lastname = name.split()
        is_guest = name in ["Eeva Makiranta", "Kieth Curtis"]
        pObject = models.Person(first_name = firstname,
                                last_name = lastname,
                                is_vfho = False,
                                mug_shot = "")
        pObject.save()
        yo = models.Expedition.objects.filter(year = "2008")[0]
        pyo = models.PersonExpedition(person = pObject, expedition = yo, nickname="", is_guest=is_guest)
        pyo.save()


#
# the logbook loading section
#
def GetTripPersons(trippeople, expedition):
    res = [ ]
    author = None
    for tripperson in re.split(",|\+|&| and ", trippeople):
        tripperson = tripperson.strip()
        mul = re.match("<u>(.*?)</u>$", tripperson)
        if mul:
            tripperson = mul.group(1).strip()
        if tripperson and tripperson[0] != '*':
            #assert tripperson in personyearmap, "'%s' << %s\n\n %s" % (tripperson, trippeople, personyearmap)
            personyear = expedition.GetPersonExpedition(tripperson)
            #print personyear
            res.append(personyear)
            if mul:
                author = personyear
    if not author:
        author = res[-1]
    return res, author

def Parselogwikitxt(year, expedition, txt):
    trippara = re.findall("===(.*?)===([\s\S]*?)(?====)", txt)
    for triphead, triptext in trippara:
        tripheadp = triphead.split("|")
        assert len(tripheadp) == 3, tripheadp
        tripdate, tripplace, trippeople = tripheadp
        tripsplace = tripplace.split(" - ")
        tripcave = tripsplace[0]

        tul = re.findall("T/?U:?\s*(\d+(?:\.\d*)?|unknown)\s*(hrs|hours)?", triptext)
        if tul:
            #assert len(tul) <= 1, (triphead, triptext)
            #assert tul[0][1] in ["hrs", "hours"], (triphead, triptext)
            triptime = tul[0][0]
        else:
            triptime = ""
            #assert tripcave == "Journey", (triphead, triptext)

        assert re.match("\d\d\d\d-\d\d-\d\d", tripdate), tripdate
        ldate = datetime.date(int(tripdate[:4]), int(tripdate[5:7]), int(tripdate[8:10]))
        print "ppp", trippeople, len(triptext)
        trippersons, author = GetTripPersons(trippeople, expedition)
        #triptext = triptext[:10] # seems to have aproblem with this
        #print "ttt", triptext
        lbo = models.LogbookEntry(date = ldate, place = tripcave, title = tripsplace[-1], text = triptext, author=author)
        lbo.save()

        print "ppp", trippersons
        for tripperson in trippersons:
            pto = models.PersonTrip(personexpedition = tripperson, place=tripcave, date=ldate, timeunderground=triptime, 
                                    logbookentry=lbo, is_logbookentryauthor=(tripperson == author))
            pto.save()

def Parseloghtmltxt(year, expedition, txt):
    tripparas = re.findall("<hr\s*/>([\s\S]*?)(?=<hr)", txt)
    for trippara in tripparas:
        s = re.match('''(?x)\s*(?:<a\s+id="(.*?)"\s*/>)?
                            \s*<div\s+class="tripdate"\s*(?:id="(.*?)")?>(.*?)</div>
                            \s*<div\s+class="trippeople">(.*?)</div>
                            \s*<div\s+class="triptitle">(.*?)</div>
                            ([\s\S]*?)
                            \s*(?:<div\s+class="timeug">(.*?)</div>)?
                            \s*$
                     ''', trippara)
        assert s, trippara

        tripid, tripid1, tripdate, trippeople, triptitle, triptext, timeug = s.groups()
        mdatestandard = re.match("(\d\d\d\d)-(\d\d)-(\d\d)", tripdate)
        mdategoof = re.match("(\d\d?)/(\d)/(\d\d)", tripdate)
        if mdatestandard:
            year, month, day = int(mdatestandard.group(1)), int(mdatestandard.group(2)), int(mdatestandard.group(3))
        elif mdategoof:
            day, month, year = int(mdategoof.group(1)), int(mdategoof.group(2)), int(mdategoof.group(3)) + 2000
        else:
            assert False, tripdate
        ldate = datetime.date(year, month, day)
        print "ttt", tripdate
        #assert tripid[:-1] == "t" + tripdate, (tripid, tripdate)
        trippersons, author = GetTripPersons(trippeople, expedition)
        tripcave = ""
        ltriptext = re.sub("</p>", "", triptext)
        ltriptext = re.sub("\s*?\n\s*", " ", ltriptext)
        ltriptext = re.sub("<p>", "\n\n", ltriptext).strip()
        lbo = models.LogbookEntry(date = ldate, place = tripcave, title = triptitle, text = ltriptext, author=author)
        lbo.save()
        tu = timeug or ""

        print "ppp", trippeople, trippersons
        for tripperson in trippersons:
            pto = models.PersonTrip(personexpedition = tripperson, place=tripcave, date=ldate, timeunderground=tu, 
                                    logbookentry=lbo, is_logbookentryauthor=(tripperson == author))
            pto.save()



def LoadLogbooks():
    models.LogbookEntry.objects.all().delete()
    expowebbase = os.path.join(settings.EXPOWEB, "years")  
    yearlinks = [ 
                    ("2008", "2008/logbook/2008logbook.txt"), 
                    ("2007", "2007/logbook/2007logbook.txt"), 
                    ("2005", "2005/logbook.html"), 
                    ("2004", "2004/logbook.html"), 
#not done                    ("2003", "2003/logbook.html"), 
                ]

    for year, lloc in yearlinks:
        expedition = models.Expedition.objects.filter(year = year)[0]
        fin = open(os.path.join(expowebbase, lloc))
        txt = fin.read()
        fin.close()
        if year >= "2007":
            Parselogwikitxt(year, expedition, txt)
        else:
            Parseloghtmltxt(year, expedition, txt)


# command line run through the loading stages
# you can comment out these in turn to control what gets reloaded
#LoadExpos()
#LoadPersons()
LoadLogbooks()

