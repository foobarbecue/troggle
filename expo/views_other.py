from django.shortcuts import render_to_response
from troggle.expo.models import Cave, Expedition, Person, LogbookEntry, PersonExpedition
import troggle.settings as settings
from django import forms
from django.db.models import Q
import re
import randSent

def stats(request):
    statsDict={}
    statsDict['expoCount'] = int(Expedition.objects.count())
    statsDict['caveCount'] = int(Cave.objects.count())
    statsDict['personCount'] = int(Person.objects.count())
    statsDict['logbookEntryCount'] = int(LogbookEntry.objects.count())
    return render_to_response('statistics.html', statsDict)

def frontPage(request):
    
    return render_to_response('index.html', {'randSent':randSent.randomLogbookSentence(),'settings':settings})
    
def calendar(request,year):
    week=['S','S','M','T','W','T','F']
    if year:
	expedition=Expedition.objects.get(year=year)
	PersonExpeditions=expedition.personexpedition_set.all()
	
	dictToPass=locals()
	dictToPass.update({'settings':settings})
    return render_to_response('calendar.html', dictToPass)
	