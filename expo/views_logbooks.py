from django.shortcuts import render_to_response
from troggle.expo.models import Expedition, Person, PersonExpedition, PersonTrip, LogbookEntry
import troggle.settings as settings
import search
import re

def personindex(request):
    persons = Person.objects.all()
    return render_to_response('personindex.html', {'persons': persons, 'settings': settings})

def person(request, person_id, first_name, last_name):
    if first_name == '' or last_name == '':
        person = Person.objects.filter(id = person_id)[0]
    else:
        person = Person.objects.filter(first_name = first_name, last_name = last_name)[0]
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
