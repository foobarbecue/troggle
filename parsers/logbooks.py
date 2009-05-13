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
        elif name == "Duncan Collis":
            nickname = "Dunks"
        elif name == "Mike Richardson":
            nickname = "Mike TA"
        elif name == "Hilary Greaves":
            nickname = "Hils"
        elif name == "Andrew Atkinson":
            nickname = "Andy A"
        elif name == "Wookey":
            nickname = "Wook"
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

            # error
            elif name == "Mike Richardson" and year == "2001":
                print "Mike Richardson(2001) error"
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
    for tripperson in re.split(",|\+|&amp;|&(?!\w+;)| and ", trippeople):
        tripperson = tripperson.strip()
        mul = re.match("<u>(.*?)</u>$(?i)", tripperson)
        if mul:
            tripperson = mul.group(1).strip()
        if tripperson and tripperson[0] != '*':
            #assert tripperson in personyearmap, "'%s' << %s\n\n %s" % (tripperson, trippeople, personyearmap)
            personyear = expedition.GetPersonExpedition(tripperson)
            if not personyear:
                print "NoMatchFor: '%s'" % tripperson    
            res.append(personyear)
            if mul:
                author = personyear
    if not author:
        author = res[-1]
    return res, author

def EnterLogIntoDbase(date, place, title, text, trippeople, expedition, tu):
    trippersons, author = GetTripPersons(trippeople, expedition)
    lbo = models.LogbookEntry(date=date, place=place, title=title, text=text, author=author)
    lbo.save()
    print "ttt", date, place
    for tripperson in trippersons:
        pto = models.PersonTrip(personexpedition = tripperson, place=place, date=date, timeunderground=(tu or ""), 
                                logbookentry=lbo, is_logbookentryauthor=(tripperson == author))
        pto.save()

# 2007, 2008
def Parselogwikitxt(year, expedition, txt):
    trippara = re.findall("===(.*?)===([\s\S]*?)(?====)", txt)
    for triphead, triptext in trippara:
        tripheadp = triphead.split("|")
        assert len(tripheadp) == 3, (tripheadp, triptext)
        tripdate, tripplace, trippeople = tripheadp
        tripsplace = tripplace.split(" - ")
        tripcave = tripsplace[0]

        tul = re.findall("T/?U:?\s*(\d+(?:\.\d*)?|unknown)\s*(hrs|hours)?", triptext)
        if tul:
            #assert len(tul) <= 1, (triphead, triptext)
            #assert tul[0][1] in ["hrs", "hours"], (triphead, triptext)
            tu = tul[0][0]
        else:
            tu = ""
            #assert tripcave == "Journey", (triphead, triptext)

        assert re.match("\d\d\d\d-\d\d-\d\d", tripdate), tripdate
        ldate = datetime.date(int(tripdate[:4]), int(tripdate[5:7]), int(tripdate[8:10]))
        #print "\n", tripcave, "---   ppp", trippeople, len(triptext)
        EnterLogIntoDbase(date = ldate, place = tripcave, title = tripplace, text = triptext, trippeople=trippeople, expedition=expedition, tu=tu)

# 2002, 2004, 2005
def Parseloghtmltxt(year, expedition, txt):
    tripparas = re.findall("<hr\s*/>([\s\S]*?)(?=<hr)", txt)
    for trippara in tripparas:
        s = re.match('''(?x)\s*(?:<a\s+id="(.*?)"\s*/>)?
                            \s*<div\s+class="tripdate"\s*(?:id="(.*?)")?>(.*?)</div>
                            \s*<div\s+class="trippeople">\s*(.*?)</div>
                            \s*<div\s+class="triptitle">\s*(.*?)</div>
                            ([\s\S]*?)
                            \s*(?:<div\s+class="timeug">\s*(.*?)</div>)?
                            \s*$
                     ''', trippara)
        assert s, trippara

        tripid, tripid1, tripdate, trippeople, triptitle, triptext, tu = s.groups()
        mdatestandard = re.match("(\d\d\d\d)-(\d\d)-(\d\d)", tripdate)
        mdategoof = re.match("(\d\d?)/0?(\d)/(?:20)?(\d\d)", tripdate)
        if mdatestandard:
            year, month, day = int(mdatestandard.group(1)), int(mdatestandard.group(2)), int(mdatestandard.group(3))
        elif mdategoof:
            day, month, year = int(mdategoof.group(1)), int(mdategoof.group(2)), int(mdategoof.group(3)) + 2000
        else:
            assert False, tripdate
        ldate = datetime.date(year, month, day)
        #assert tripid[:-1] == "t" + tripdate, (tripid, tripdate)
        trippeople = re.sub("Ol(?!l)", "Olly", trippeople)        
        trippeople = re.sub("Wook(?!e)", "Wookey", trippeople)        
        triptitles = triptitle.split(" - ")
        if len(triptitles) >= 2:
            tripcave = triptitles[0]
        else:
            tripcave = "UNKNOWN"
        #print "\n", tripcave, "---   ppp", trippeople, len(triptext)
        ltriptext = re.sub("</p>", "", triptext)
        ltriptext = re.sub("\s*?\n\s*", " ", ltriptext)
        ltriptext = re.sub("<p>", "\n\n", ltriptext).strip()        EnterLogIntoDbase(date = ldate, place = tripcave, title = triptitle, text = ltriptext, trippeople=trippeople, expedition=expedition, tu=tu)


# main parser for pre-2001.  simpler because the data has been hacked so much to fit it
def Parseloghtml01(year, expedition, txt):
    tripparas = re.findall("<hr[\s/]*>([\s\S]*?)(?=<hr)", txt)
    for trippara in tripparas:
        s = re.match(u"(?s)\s*(?:<p>)?(.*?)</?p>(.*)$(?i)", trippara)
        assert s, trippara[:100]
        tripheader, triptext = s.group(1), s.group(2)
        mtripid = re.search('<a id="(.*?)"', tripheader)
        tripid = mtripid and mtripid.group(1) or ""
        tripheader = re.sub("</?(?:[ab]|span)[^>]*>", "", tripheader)

#        print [tripheader]
#        continue

        tripdate, triptitle, trippeople = tripheader.split("|")
        mdatestandard = re.match("\s*(\d\d\d\d)-(\d\d)-(\d\d)", tripdate)
        ldate = datetime.date(int(mdatestandard.group(1)), int(mdatestandard.group(2)), int(mdatestandard.group(3)))
        mdatestandard = re.match("(\d\d\d\d)-(\d\d)-(\d\d)", tripdate)

        mtu = re.search('<p[^>]*>(T/?U.*)', triptext)
        if mtu:
            tu = mtu.group(1)
            triptext = triptext[:mtu.start(0)] + triptext[mtu.end():]
        else:
            tu = ""

        triptitles = triptitle.split(" - ")
        tripcave = triptitles[0].strip()

        ltriptext = re.sub("</p>", "", triptext)
        ltriptext = re.sub("\s*?\n\s*", " ", ltriptext)
        ltriptext = re.sub("<p>", "\n\n", ltriptext).strip()        ltriptext = re.sub("[^\s0-9a-zA-Z\-.,:;'!]", "NONASCII", ltriptext)

        print ldate, trippeople.strip()
            # could includ the tripid (url link for cross referencing)
        EnterLogIntoDbase(date = ldate, place = tripcave, title = triptitle, text = ltriptext, trippeople=trippeople, expedition=expedition, tu=tu)

def Parseloghtml03(year, expedition, txt):
    tripparas = re.findall("<hr\s*/>([\s\S]*?)(?=<hr)", txt)
    for trippara in tripparas:
        s = re.match(u"(?s)\s*<p>(.*?)</p>(.*)$", trippara)
        assert s, trippara
        tripheader, triptext = s.group(1), s.group(2)
        tripheader = re.sub("&nbsp;", " ", tripheader)
        tripheader = re.sub("\s+", " ", tripheader).strip()
        sheader = tripheader.split(" -- ")
        tu = ""
        if re.match("T/U|Time underwater", sheader[-1]):
            tu = sheader.pop()
        if len(sheader) != 3:
            print sheader
        #    continue
        tripdate, triptitle, trippeople = sheader
        mdategoof = re.match("(\d\d?)/(\d)/(\d\d)", tripdate)
        day, month, year = int(mdategoof.group(1)), int(mdategoof.group(2)), int(mdategoof.group(3)) + 2000
        ldate = datetime.date(year, month, day)        triptitles = triptitle.split(" , ")
        if len(triptitles) >= 2:
            tripcave = triptitles[0]
        else:
            tripcave = "UNKNOWN"
        #print tripcave, "---   ppp", triptitle, trippeople, len(triptext)
        ltriptext = re.sub("</p>", "", triptext)
        ltriptext = re.sub("\s*?\n\s*", " ", ltriptext)
        ltriptext = re.sub("<p>", "\n\n", ltriptext).strip()
        ltriptext = re.sub("[^\s0-9a-zA-Z\-.,:;'!&()\[\]<>?=+*%]", "_NONASCII_", ltriptext)
        EnterLogIntoDbase(date = ldate, place = tripcave, title = triptitle, text = ltriptext, trippeople=trippeople, expedition=expedition, tu=tu)

def LoadLogbooks():
    models.LogbookEntry.objects.all().delete()
    expowebbase = os.path.join(settings.EXPOWEB, "years")  
    yearlinks = [ 
                    ("2008", "2008/logbook/2008logbook.txt", Parselogwikitxt), 
                    ("2007", "2007/logbook/2007logbook.txt", Parselogwikitxt), 
#not done                    ("2006", "2006/logbook/logbook_06.txt"), 
                    ("2005", "2005/logbook.html", Parseloghtmltxt), 
                    ("2004", "2004/logbook.html", Parseloghtmltxt), 
                    ("2003", "2003/logbook.html", Parseloghtml03), 
                    ("2002", "2002/logbook.html", Parseloghtmltxt), 
                    ("2001", "2001/log.htm", Parseloghtml01), 
                    ("2000", "2000/log.htm", Parseloghtml01), 
                    ("1999", "1999/log.htm", Parseloghtml01), 

#                    ("1998", "1998/log.htm", Parseloghtml01), 
#                    ("1997", "1997/log.htm", Parseloghtml01), 
                ]
#    yearlinks = [ ("1997", "1997/log.htm", Parseloghtml01), ] #overwrite

    for year, lloc, parsefunc in yearlinks:
        expedition = models.Expedition.objects.filter(year = year)[0]
        fin = open(os.path.join(expowebbase, lloc))
        txt = fin.read()
        fin.close()
        parsefunc(year, expedition, txt)
        

# command line run through the loading stages
# you can comment out these in turn to control what gets reloaded
#LoadExpos()#LoadPersons()
LoadLogbooks()

