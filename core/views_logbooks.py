from django.shortcuts import render_to_response
from troggle.core.models import Expedition, Person, PersonExpedition, PersonTrip, LogbookEntry
import troggle.settings as settings
from django.db import models
from troggle.parsers.logbooks import LoadLogbookForExpedition
from troggle.parsers.people import GetPersonExpeditionNameLookup
from troggle.core.forms import PersonForm
from  django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

# Django uses Context, not RequestContext when you call render_to_response. We always want to use RequestContext, so that django adds the context from settings.TEMPLATE_CONTEXT_PROCESSORS. This way we automatically get necessary settings variables passed to each template. So we use a custom method, render_response instead of render_to_response. Hopefully future Django releases will make this unnecessary.
from troggle.alwaysUseRequestContext import render_response

import search
import re

@models.permalink #this allows the nice get_absolute_url syntax we are using

def getNotablePersons():
    notablepersons = []
    for person in Person.objects.all():
            if person.bisnotable():
                notablepersons.append(person)
    return notablepersons		

def personindex(request):
    persons = Person.objects.all()
    # From what I can tell, "persons" seems to be the table rows, while "personss" is the table columns. - AC 16 Feb 09
    personss = [ ]
    ncols = 5
    nc = (len(persons) + ncols - 1) / ncols
    for i in range(ncols):
        personss.append(persons[i * nc: (i + 1) * nc])
    
    notablepersons = []
    for person in Person.objects.all():
            if person.bisnotable():
                notablepersons.append(person)

    return render_response(request,'personindex.html', {'persons': persons, 'personss':personss, 'notablepersons':notablepersons, })

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
    return render_response(request,'expedition.html', {'expedition': expedition, 'expedition_next':expedition_next, 'expedition_prev':expedition_prev, 'logbookentries':logbookentries, 'message':message, })

    def get_absolute_url(self):
        return ('expedition', (expedition.year))

def person(request, first_name='', last_name='', ):
    person = Person.objects.get(first_name = first_name, last_name = last_name)
    
    #This is for removing the reference to the user's profile, in case they set it to the wrong person
    if request.method == 'GET':
        if request.GET.get('clear_profile')=='True':
            person.user=None
            person.save()
            return HttpResponseRedirect(reverse('profiles_select_profile'))
    
    return render_response(request,'person.html', {'person': person, })
    
    def get_absolute_url(self):
        return settings.URL_ROOT + self.first_name + '_' + self.last_name

#def person(request, name):
#    person = Person.objects.get(href=name)
#    

def personexpedition(request, first_name='',  last_name='', year=''):
    person = Person.objects.get(first_name = first_name, last_name = last_name)
    expedition = Expedition.objects.get(year=year)
    personexpedition = person.personexpedition_set.get(expedition=expedition)
    return render_response(request,'personexpedition.html', {'personexpedition': personexpedition, })

def newQMlink(logbookentry):
    biggestQMnumber=0
    if logbookentry.cave:
        for log in logbookentry.cave.logbookentry_set.all():
            try:
                biggestQMnumberInLog = logbookentry.QMs_found.order_by('-number')[0].number
            except IndexError:
                biggestQMnumberInLog = 0
        if biggestQMnumberInLog > biggestQMnumber:
            biggestQMnumber = biggestQMnumberInLog
    else:
        return None



    nextQMnumber=biggestQMnumber+1
    return settings.URL_ROOT + r'/admin/expo/qm/add/?' + r'found_by=' + str(logbookentry.pk) +'&number=' + str(nextQMnumber)

def logbookentry(request, date, slug):
    logbookentry = LogbookEntry.objects.filter(date=date, slug=slug)

    if len(logbookentry)>1:
        return render_response(request, 'object_list.html',{'object_list':logbookentry})
    else:
        logbookentry=logbookentry[0]
        return render_response(request, 'logbookentry.html', {'logbookentry': logbookentry, 'newQMlink':newQMlink(logbookentry)})

def logbookSearch(request, extra):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
    entry_query = search.get_query(query_string, ['text','title',])
    found_entries = LogbookEntry.objects.filter(entry_query)

    return render_response(request,'logbooksearch.html',
                          { 'query_string': query_string, 'found_entries': found_entries, })
                          #context_instance=RequestContext(request))

def personForm(request,pk):
    person=Person.objects.get(pk=pk)
    form=PersonForm(instance=person)
    return render_response(request,'personform.html', {'form':form,})