from troggle.expo.models import Cave, Expedition, Person, LogbookEntry, PersonExpedition, PersonTrip, Photo
import troggle.settings as settings
from django import forms
from django.db.models import Q
import databaseReset
import re
import randSent
from django.http import HttpResponse

from django.core.urlresolvers import reverse
from troggle.alwaysUseRequestContext import render_response # see views_logbooks for explanation on this.

def showrequest(request):
    return HttpResponse(request.GET)

def stats(request):
    statsDict={}
    statsDict['expoCount'] = int(Expedition.objects.count())
    statsDict['caveCount'] = int(Cave.objects.count())
    statsDict['personCount'] = int(Person.objects.count())
    statsDict['logbookEntryCount'] = int(LogbookEntry.objects.count())
    return render_response(request,'statistics.html', statsDict)

def frontpage(request):
    message = "no test message"  #reverse('personn', kwargs={"name":"hkjhjh"}) 
    if "reloadexpos" in request.GET:
        message = LoadPersonsExpos()
        message = "Reloaded personexpos"
    if "reloadsurvex" in request.POST:
        message = LoadAllSurvexBlocks()
        message = "Reloaded survexblocks"

    #'randSent':randSent.randomLogbookSentence(),
    expeditions =  Expedition.objects.order_by("-year")
    totallogbookentries = LogbookEntry.objects.count()
    return render_response(request,'index.html', {'expeditions':expeditions, 'all':'all', 'totallogbookentries':totallogbookentries, "message":message})
    
def calendar(request,year):
    week=['S','S','M','T','W','T','F']
    if year:
        expedition=Expedition.objects.get(year=year)
        PersonExpeditions=expedition.personexpedition_set.all()
    
    return render_response(request,'calendar.html', locals())

def controlPanel(request):
    message = "no test message"  #reverse('personn', kwargs={"name":"hkjhjh"}) 
    if request.method=='POST':
        for item in request.POST:
            if request.user.is_superuser and item!='item':
                print "running"+ " databaseReset."+item+"()"
                exec "databaseReset."+item+"()"

    return render_response(request,'controlPanel.html', )