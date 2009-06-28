from troggle.expo.models import Cave, Expedition, Person, LogbookEntry, PersonExpedition, PersonTrip, Photo
import troggle.settings as settings
from django import forms
from django.template import loader, Context
from django.db.models import Q
import databaseReset
import re
import randSent
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from troggle.alwaysUseRequestContext import render_response # see views_logbooks for explanation on this.
from expo.models import *

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
    logbookentry = LogbookEntry
    cave = Cave
    photo = Photo
    from django.contrib.admin.templatetags import log
    return render_response(request,'frontpage.html', locals())

def todo(request):
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
    jobs_completed=[]
    if request.method=='POST':
        if request.user.is_superuser:
    
            #importlist is mostly here so that things happen in the correct order.
            #http post data seems to come in an unpredictable order, so we do it this way.
            importlist=['reload_db', 'import_people', 'import_cavetab', 'import_logbooks', 'import_surveys', 'import_QMs']
            databaseReset.make_dirs()
            for item in importlist:
                if item in request.POST:
                    print "running"+ " databaseReset."+item+"()"
                    exec "databaseReset."+item+"()"
                    jobs_completed.append(item)
        else:
            if request.user.is_authenticated(): #The user is logged in, but is not a superuser.
                return render_response(request,'controlPanel.html', {'caves':Cave.objects.all(),'error':'You must be a superuser to use that feature.'})
            else:
                return HttpResponseRedirect(reverse('auth_login'))

    return render_response(request,'controlPanel.html', {'caves':Cave.objects.all(),'expeditions':Expedition.objects.all(),'jobs_completed':jobs_completed})

def downloadCavetab(request):
    from export import tocavetab
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=CAVETAB2.CSV'
    tocavetab.writeCaveTab(response)
    return response

def downloadSurveys(request):
    from export import tosurveys
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Surveys.csv'
    tosurveys.writeCaveTab(response)
    return response

def downloadLogbook(request,year=None,extension=None,queryset=None):
    
    if year:
        expedition=Expedition.objects.get(year=year)
        logbook_entries=LogbookEntry.objects.filter(expedition=expedition)
        filename='logbook'+year
    elif queryset:
        logbook_entries=queryset
        filename='logbook'
    else:
        return response(r"Error: Logbook downloader doesn't know what year you want")
    
    if 'year' in request.GET:
        year=request.GET['year']
    if 'extension' in request.GET:
        extension=request.GET['extension']
    
    
    
    if extension =='txt':
        response = HttpResponse(mimetype='text/plain')
        style='2008'
    elif extension == 'html':
        response = HttpResponse(mimetype='text/html')
        style='2005'
        
    template='logbook'+style+'style.'+extension
    response['Content-Disposition'] = 'attachment; filename='+filename+'.'+extension 
    t=loader.get_template(template)
    c=Context({'logbook_entries':logbook_entries})
    response.write(t.render(c))
    return response
    

def downloadQMs(request):
    # Note to self: use get_cave method for the below
    if request.method=='GET':
        try:
            cave=Cave.objects.get(kataster_number=request.GET['cave_id'])
        except Cave.DoesNotExist:
            cave=Cave.objects.get(name=cave_id)

    from export import toqms

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=qm.csv'
    toqms.writeQmTable(response,cave)
    return response
    
def ajax_test(request):
    post_text = request.POST['post_data']
    return HttpResponse("{'response_text': '"+post_text+" recieved.'}", 
                                   mimetype="application/json")
                                   
def eyecandy(request):
    return render_response(request,'eyecandy.html', {})
