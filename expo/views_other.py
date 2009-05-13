from django.shortcuts import render_to_response
from troggle.expo.models import Cave, Expedition, Person, LogbookEntry, PersonExpedition
import troggle.settings as settings
from django import forms
from django.db.models import Q
from troggle.parsers.people import LoadPersonsExpos
import re
from troggle.parsers.survex import LoadAllSurvexBlocks
import randSent

from django.core.urlresolvers import reverse

def stats(request):
    statsDict={}
    statsDict['expoCount'] = int(Expedition.objects.count())
    statsDict['caveCount'] = int(Cave.objects.count())
    statsDict['personCount'] = int(Person.objects.count())
    statsDict['logbookEntryCount'] = int(LogbookEntry.objects.count())
    return render_to_response('statistics.html', statsDict)

def frontPage(request):
    message = "no test message"  #reverse('personn', kwargs={"name":"hkjhjh"}) 
    if "reloadexpos" in request.GET:
        message = LoadPersonsExpos()
        message = "Reloaded personexpos"
    if "reloadsurvex" in request.GET:
        message = LoadAllSurvexBlocks()
        message = "Reloaded survexblocks"

    #'randSent':randSent.randomLogbookSentence(),
    expeditions =  Expedition.objects.all()
    return render_to_response('index.html', {'expeditions':expeditions, 'settings':settings, "message":message})
    
def calendar(request,year):
    week=['S','S','M','T','W','T','F']
    if year:
	expedition=Expedition.objects.get(year=year)
	PersonExpeditions=expedition.personexpedition_set.all()
	
	dictToPass=locals()
	dictToPass.update({'settings':settings})
    return render_to_response('calendar.html', dictToPass)
