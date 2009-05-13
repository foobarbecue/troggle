from django.shortcuts import render_to_response
from troggle.expo.models import Cave, Expedition, Person, LogbookEntry
import troggle.settings as settings
from django import forms
from django.db.models import Q

def stats(request):
    statsDict={}
    statsDict['expoCount'] = int(Expedition.objects.count())
    statsDict['caveCount'] = int(Cave.objects.count())
    statsDict['personCount'] = int(Person.objects.count())
    statsDict['logbookEntryCount'] = int(LogbookEntry.objects.count())
    return render_to_response('statistics.html', statsDict)