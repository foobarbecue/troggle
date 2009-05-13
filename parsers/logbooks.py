#.-*- coding: utf-8 -*-

import troggle.settings as settings
import troggle.expo.models as models

from troggle.parsers.people import GetPersonExpeditionNameLookup
from troggle.parsers.cavetab import GetCaveLookup

from django.template.defaultfilters import slugify

import csv
import re
import datetime
import os

from save_carefully import save_carefully

# 
# When we edit logbook entries, allow a "?" after any piece of data to say we've frigged it and
# it can be checked up later from the hard-copy if necessary; or it's not possible to determin (name, trip place, etc)
#

#
# the logbook loading section
#
def GetTripPersons(trippeople, expedition, logtime_underground):    
    res = [ ]
    author = None
    for tripperson in re.split(",|\+|&amp;|&(?!\w+;)| and ", trippeople):
        tripperson = tripperson.strip()
        mul = re.match("<u>(.*?)</u>$(?i)", tripperson)
        if mul:
            tripperson = mul.group(1).strip()
        if tripperson and tripperson[0] != '*':
            #assert tripperson in personyearmap, "'%s' << %s\n\n %s" % (tripperson, trippeople, personyearmap)
            personyear = GetPersonExpeditionNameLookup(expedition).get(tripperson.lower())
            if not personyear:
                print "NoMatchFor: '%s'" % tripperson    
            res.append((personyear, logtime_underground))
            if mul:
                author = personyear
    if not author:
        author = res[-1][0]
    return res, author

def GetTripCave(place):                     #need to be fuzzier about matching here. Already a very slow function...
#    print "Getting cave for " , place
    try:
        katastNumRes=[]
        katastNumRes=list(models.Cave.objects.filter(kataster_number=int(place)))
    except ValueError:
        pass
    officialNameRes=list(models.Cave.objects.filter(official_name=place))
    tripCaveRes=officialNameRes+katastNumRes

    if len(tripCaveRes)==1:
#        print "Place " , place , "entered as" , tripCaveRes[0]
        return tripCaveRes[0]

    elif models.OtherCaveName.objects.filter(name=place):
        tripCaveRes=models.OtherCaveName.objects.filter(name__icontains=place)[0].cave
#        print "Place " , place , "entered as" , tripCaveRes
        return tripCaveRes

    elif len(tripCaveRes)>1:
        print "Ambiguous place " + str(place) + " entered. Choose from " + str(tripCaveRes)
        correctIndex=input("type list index of correct cave")
        return tripCaveRes[correctIndex]
    else:
        print "No cave found for place " , place
        return


noncaveplaces = [ "Journey", "Loser Plateau" ]
def EnterLogIntoDbase(date, place, title, text, trippeople, expedition, logtime_underground):
    """ saves a logbook entry and related persontrips """
    trippersons, author = GetTripPersons(trippeople, expedition, logtime_underground)
#    tripCave = GetTripCave(place)
    #
    lplace = place.lower()
    if lplace not in noncaveplaces:
        cave=GetCaveLookup().get(lplace)

    #Check for an existing copy of the current entry, and save
    lookupAttribs={'date':date, 'title':title[:50]} 
    nonLookupAttribs={'place':place, 'text':text, 'author':author, 'expedition':expedition, 'cave':cave}
    lbo, created=save_carefully(models.LogbookEntry, lookupAttribs, nonLookupAttribs)

    for tripperson, time_underground in trippersons:
        lookupAttribs={'person_expedition':tripperson, 'date':date}
        nonLookupAttribs={'place':place,'time_underground':time_underground,'logbook_entry':lbo,'is_logbook_entry_author':(tripperson == author)}
        save_carefully(models.PersonTrip, lookupAttribs, nonLookupAttribs)


def ParseDate(tripdate, year):
    mdatestandard = re.match("(\d\d\d\d)-(\d\d)-(\d\d)", tripdate)
    mdategoof = re.match("(\d\d?)/0?(\d)/(20|19)?(\d\d)", tripdate)
    if mdatestandard:
        assert mdatestandard.group(1) == year, (tripdate, year)
        year, month, day = int(mdatestandard.group(1)), int(mdatestandard.group(2)), int(mdatestandard.group(3))
    elif mdategoof:
        assert not mdategoof.group(3) or mdategoof.group(3) == year[:2]
        yadd = int(year[:2]) * 100
        day, month, year = int(mdategoof.group(1)), int(mdategoof.group(2)), int(mdategoof.group(4)) + yadd
    else:
        assert False, tripdate
    return datetime.date(year, month, day)

# 2007, 2008, 2006
def Parselogwikitxt(year, expedition, txt):
    trippara = re.findall("===(.*?)===([\s\S]*?)(?====)", txt)
    for triphead, triptext in trippara:
        tripheadp = triphead.split("|")
        assert len(tripheadp) == 3, (tripheadp, triptext)
        tripdate, tripplace, trippeople = tripheadp
        tripsplace = tripplace.split(" - ")
        tripcave = tripsplace[0].strip()

        tul = re.findall("T/?U:?\s*(\d+(?:\.\d*)?|unknown)\s*(hrs|hours)?", triptext)
        if tul:
            #assert len(tul) <= 1, (triphead, triptext)
            #assert tul[0][1] in ["hrs", "hours"], (triphead, triptext)
            tu = tul[0][0]
        else:
            tu = ""
            #assert tripcave == "Journey", (triphead, triptext)

        ldate = ParseDate(tripdate.strip(), year)
        #print "\n", tripcave, "---   ppp", trippeople, len(triptext)
        EnterLogIntoDbase(date = ldate, place = tripcave, title = tripplace, text = triptext, trippeople=trippeople, expedition=expedition, logtime_underground=0)

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
        ldate = ParseDate(tripdate.strip(), year)
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
        ltriptext = re.sub("<p>", "\n\n", ltriptext).strip()
        EnterLogIntoDbase(date = ldate, place = tripcave, title = triptitle, text = ltriptext, trippeople=trippeople, expedition=expedition, logtime_underground=0)


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

        #print [tripheader]
        #continue

        tripdate, triptitle, trippeople = tripheader.split("|")
        ldate = ParseDate(tripdate.strip(), year)

        mtu = re.search('<p[^>]*>(T/?U.*)', triptext)
        if mtu:
            tu = mtu.group(1)
            triptext = triptext[:mtu.start(0)] + triptext[mtu.end():]
        else:
            tu = ""

        triptitles = triptitle.split(" - ")
        tripcave = triptitles[0].strip()

        ltriptext = triptext
        
        mtail = re.search('(?:<a href="[^"]*">[^<]*</a>|\s|/|-|&amp;|</?p>|\((?:same day|\d+)\))*$', ltriptext)
        if mtail:
            #print mtail.group(0)
            ltriptext = ltriptext[:mtail.start(0)]
        ltriptext = re.sub("</p>", "", ltriptext)
        ltriptext = re.sub("\s*?\n\s*", " ", ltriptext)
        ltriptext = re.sub("<p>|<br>", "\n\n", ltriptext).strip()
        #ltriptext = re.sub("[^\s0-9a-zA-Z\-.,:;'!]", "NONASCII", ltriptext)
        ltriptext = re.sub("</?u>", "_", ltriptext)
        ltriptext = re.sub("</?i>", "''", ltriptext)
        ltriptext = re.sub("</?b>", "'''", ltriptext)
        

        #print ldate, trippeople.strip()
            # could includ the tripid (url link for cross referencing)
        EnterLogIntoDbase(date = ldate, place = tripcave, title = triptitle, text = ltriptext, trippeople=trippeople, expedition=expedition, logtime_underground=0)


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
        ldate = ParseDate(tripdate.strip(), year)
        triptitles = triptitle.split(" , ")
        if len(triptitles) >= 2:
            tripcave = triptitles[0]
        else:
            tripcave = "UNKNOWN"
        #print tripcave, "---   ppp", triptitle, trippeople, len(triptext)
        ltriptext = re.sub("</p>", "", triptext)
        ltriptext = re.sub("\s*?\n\s*", " ", ltriptext)
        ltriptext = re.sub("<p>", "\n\n", ltriptext).strip()
        ltriptext = re.sub("[^\s0-9a-zA-Z\-.,:;'!&()\[\]<>?=+*%]", "_NONASCII_", ltriptext)
        EnterLogIntoDbase(date = ldate, place = tripcave, title = triptitle, text = ltriptext, trippeople=trippeople, expedition=expedition, logtime_underground=0)

yearlinks = [ 
                ("2008", "2008/2008logbook.txt", Parselogwikitxt), 
                #("2007", "2007/2007logbook.txt", Parselogwikitxt), 
                ("2006", "2006/logbook/logbook_06.txt", Parselogwikitxt), 
                ("2005", "2005/logbook.html", Parseloghtmltxt), 
                ("2004", "2004/logbook.html", Parseloghtmltxt), 
                ("2003", "2003/logbook.html", Parseloghtml03), 
                ("2002", "2002/logbook.html", Parseloghtmltxt), 
                ("2001", "2001/log.htm", Parseloghtml01), 
                ("2000", "2000/log.htm", Parseloghtml01), 
                ("1999", "1999/log.htm", Parseloghtml01), 
                ("1998", "1998/log.htm", Parseloghtml01), 
                ("1997", "1997/log.htm", Parseloghtml01), 
                ("1996", "1996/log.htm", Parseloghtml01),
                ("1995", "1995/log.htm", Parseloghtml01), 
                ("1994", "1994/log.htm", Parseloghtml01), 
                ("1993", "1993/log.htm", Parseloghtml01), 		
            ]

def SetDatesFromLogbookEntries(expedition):
    for personexpedition in expedition.personexpedition_set.all():
        persontrips = personexpedition.persontrip_set.order_by('date')
        personexpedition.date_from = min([persontrip.date  for persontrip in persontrips] or [None])
        personexpedition.date_to = max([persontrip.date  for persontrip in persontrips] or [None])
        personexpedition.save()

# The below is all unnecessary, just use the built in get_previous_by_date and get_next_by_date
#        lprevpersontrip = None
#        for persontrip in persontrips:
#            persontrip.persontrip_prev = lprevpersontrip
#            if lprevpersontrip:
#                lprevpersontrip.persontrip_next = persontrip
#                lprevpersontrip.save()
#            persontrip.persontrip_next = None
#            lprevpersontrip = persontrip
#            persontrip.save()
            
    # from trips rather than logbook entries, which may include events outside the expedition
    expedition.date_from = min([personexpedition.date_from  for personexpedition in expedition.personexpedition_set.all()  if personexpedition.date_from] or [None])
    expedition.date_to = max([personexpedition.date_to  for personexpedition in expedition.personexpedition_set.all()  if personexpedition.date_to] or [None])
    expedition.save()

# The below has been replaced with the methods get_next_by_id and get_previous_by_id
#    # order by appearance in the logbook (done by id)
#    lprevlogbookentry = None
#    for logbookentry in expedition.logbookentry_set.order_by('id'):
#        logbookentry.logbookentry_prev = lprevlogbookentry
#        if lprevlogbookentry:
#            lprevlogbookentry.logbookentry_next = logbookentry
#            lprevlogbookentry.save()
#        logbookentry.logbookentry_next = None
#        logbookentry.save()
#        lprevlogbookentry = logbookentry
        
# This combined date / number key is a weird way of doing things. Use the primary key instead. If we are going to use the date for looking up entries, we should set it up to allow multiple results.
    # order by date for setting the references
#    lprevlogbookentry = None
#    for logbookentry in expedition.logbookentry_set.order_by('date'):
#        if lprevlogbookentry and lprevlogbookentry.date == logbookentry.date:
#            mcount = re.search("_(\d+)$", lprevlogbookentry.href)
#            mc = mcount and (int(mcount.group(1)) + 1) or 1
#            logbookentry.href = "%s_%d" % (logbookentry.date, mc)
#        else:
#            logbookentry.href = "%s" % logbookentry.date
#        logbookentry.save()
#        lprevlogbookentry = logbookentry

        
        
def LoadLogbookForExpedition(expedition):
    """ Parses all logbook entries for one expedition """
    
    #We're checking for stuff that's changed in admin before deleting it now.
    #print "deleting logbooks for", expedition
    #expedition.logbookentry_set.all().delete()
    #models.PersonTrip.objects.filter(person_expedition__expedition=expedition).delete()
    
    expowebbase = os.path.join(settings.EXPOWEB, "years")  
    year = str(expedition.year)
    for lyear, lloc, parsefunc in yearlinks:
        if lyear == year:
            break
    fin = open(os.path.join(expowebbase, lloc))
    txt = fin.read()
    fin.close()
    parsefunc(year, expedition, txt)
    SetDatesFromLogbookEntries(expedition)
    return "TOLOAD: " + year + "  " + str(expedition.personexpedition_set.all()[1].logbookentry_set.count()) + "  " + str(models.PersonTrip.objects.filter(person_expedition__expedition=expedition).count())


def LoadLogbooks():
    """ This is the master function for parsing all logbooks into the Troggle database. Requires yearlinks, which is a list of tuples for each expedition with expedition year, logbook path, and parsing function. """
    
    #Deletion has been moved to a seperate function to enable the non-destructive importing
    #models.LogbookEntry.objects.all().delete()
    expowebbase = os.path.join(settings.EXPOWEB, "years")  
    #yearlinks = [ ("2001", "2001/log.htm", Parseloghtml01), ] #overwrite
    #yearlinks = [ ("1996", "1996/log.htm", Parseloghtml01),] # overwrite

    for year, lloc, parsefunc in yearlinks:
        expedition = models.Expedition.objects.filter(year = year)[0]
        fin = open(os.path.join(expowebbase, lloc))
        txt = fin.read()
        fin.close()
        parsefunc(year, expedition, txt)
        SetDatesFromLogbookEntries(expedition)


