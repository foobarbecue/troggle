from django.shortcuts import render_to_response
from troggle.expo.models import Cave, Expedition, Person, LogbookEntry
import troggle.settings as settings
from django import forms
from django.db.models import Q
import re
#import randSent (it's not ready yet)

def stats(request):
    statsDict={}
    statsDict['expoCount'] = int(Expedition.objects.count())
    statsDict['caveCount'] = int(Cave.objects.count())
    statsDict['personCount'] = int(Person.objects.count())
    statsDict['logbookEntryCount'] = int(LogbookEntry.objects.count())
    return render_to_response('statistics.html', statsDict)

#def frontPage(request):
    
#    return render_to_response('index.html', {'randSent':randSent.randomLogbookSentence(),'settings':settings})