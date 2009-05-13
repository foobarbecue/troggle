from django.shortcuts import render_to_response
from troggle.expo.models import Expedition, Person, PersonExpedition, PersonTrip, LogbookEntry
import troggle.settings as settings

def personindex(request):
    persons = Person.objects.all()
    return render_to_response('personindex.html', {'persons': persons, 'settings': settings})

def person(request, person_id):
    person = Person.objects.filter(id = person_id)[0]
    return render_to_response('person.html', {'person': person, 'settings': settings})

def logbookentry(request, logbookentry_id):
    logbookentry = LogbookEntry.objects.filter(id = logbookentry_id)[0]
    return render_to_response('logbookentry.html', {'logbookentry': logbookentry, 'settings': settings})


