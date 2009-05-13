from django.shortcuts import render_to_response
from troggle.expo.models import Expedition, Person, PersonExpedition, PersonTrip, LogbookEntry
import troggle.settings as settings
from troggle.parsers.logbooks import LoadLogbookForExpedition
import search
import re

def personindex(request):
    persons = Person.objects.all()
    return render_to_response('personindex.html', {'persons': persons, 'settings': settings})

def expedition(request, expeditionname):
    year = int(expeditionname)
    expedition = Expedition.objects.get(year=year)
    expedition_next = Expedition.objects.filter(year=year+1) and Expedition.objects.get(year=year+1) or None
    expedition_prev = Expedition.objects.filter(year=year-1) and Expedition.objects.get(year=year-1) or None
    message = "No message"
    if "reload" in request.GET:
        message = LoadLogbookForExpedition(expedition)
    
    logbookentries = expedition.logbookentry_set.order_by('date')
    return render_to_response('expedition.html', {'expedition': expedition, 'expedition_next':expedition_next, 'expedition_prev':expedition_prev, 'logbookentries':logbookentries, 'message':message, 'settings': settings})

def person(request, name):
    persons = Person.objects.all()
    for person in persons:
        if person.href() == name:
            break
        person = None
    return render_to_response('person.html', {'person': person, 'settings': settings})

def logbookentry(request, logbookentry_id):
    logbookentry = LogbookEntry.objects.filter(id = logbookentry_id)[0]
    
    
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
