from django.shortcuts import render_to_response
from troggle.expo.models import Expedition, Person, PersonExpedition, PersonTrip, LogbookEntry
import troggle.settings as settings

from troggle.parsers.logbooks import LoadLogbookForExpedition
from troggle.parsers.people import GetPersonExpeditionNameLookup
from troggle.expo.forms import PersonForm

import search
import re

def personindex(request):
    persons = Person.objects.all()
    personss = [ ]
    ncols = 5
    nc = (len(persons) + ncols - 1) / ncols
    for i in range(ncols):
        personss.append(persons[i * nc: (i + 1) * nc])
    
    notablepersons = Person.objects.filter(bisnotable=True)
    return render_to_response('personindex.html', {'persons': persons, 'personss':personss, 'notablepersons':notablepersons, 'settings': settings})

def expedition(request, expeditionname):
    year = int(expeditionname)
    expedition = Expedition.objects.get(year=year)
    expedition_next = Expedition.objects.filter(year=year+1) and Expedition.objects.get(year=year+1) or None
    expedition_prev = Expedition.objects.filter(year=year-1) and Expedition.objects.get(year=year-1) or None
    message = "No message"
    if "reload" in request.GET:
        message = LoadLogbookForExpedition(expedition)
    #message = str(GetPersonExpeditionNameLookup(expedition).keys())
    logbookentries = expedition.logbookentry_set.order_by('date')
    return render_to_response('expedition.html', {'expedition': expedition, 'expedition_next':expedition_next, 'expedition_prev':expedition_prev, 'logbookentries':logbookentries, 'message':message, 'settings': settings})

def person(request, name):
    person = Person.objects.get(href=name)
    return render_to_response('person.html', {'person': person, 'settings': settings})

def personexpedition(request, name, expeditionname):
    person = Person.objects.get(href=name)
    year = int(expeditionname)
    expedition = Expedition.objects.get(year=year)
    personexpedition = person.personexpedition_set.get(expedition=expedition)
    return render_to_response('personexpedition.html', {'personexpedition': personexpedition, 'settings': settings})

def logbookentry(request, logbookentry_id):
    logbookentry = LogbookEntry.objects.filter(href = logbookentry_id)[0]
    return render_to_response('logbookentry.html', {'logbookentry': logbookentry, 'settings': settings})

def logbookSearch(request, extra):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
	entry_query = search.get_query(query_string, ['text','title',])
	found_entries = LogbookEntry.objects.filter(entry_query)

    return render_to_response('logbooksearch.html',
                          { 'query_string': query_string, 'found_entries': found_entries, 'settings': settings})
                          #context_instance=RequestContext(request))

def personForm(request,pk):
    person=Person.objects.get(pk=pk)
    form=PersonForm(instance=person)
    return render_to_response('personform.html', {'form':form,'settings':settings})