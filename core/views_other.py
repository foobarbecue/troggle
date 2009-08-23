from troggle.core.models import Cave, Expedition, Person, LogbookEntry, PersonExpedition, PersonTrip, DPhoto, QM
from django.conf import settings
from django import forms
from django.template import loader, Context
from django.db.models import Q
import databaseReset
import re
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from utils import render_with_context
from core.models import *

def showrequest(request):
    return HttpResponse(request.GET)

def stats(request):
    statsDict={}
    statsDict['expoCount'] = int(Expedition.objects.count())
    statsDict['caveCount'] = int(Cave.objects.count())
    statsDict['personCount'] = int(Person.objects.count())
    statsDict['logbookEntryCount'] = int(LogbookEntry.objects.count())
    return render_with_context(request,'statistics.html', statsDict)

def frontpage(request):
    if request.user.is_authenticated():
        return render_with_context(request,'tasks.html')

    expeditions =  Expedition.objects.order_by("-year")
    logbookentry = LogbookEntry
    cave = Cave
    photo = DPhoto
    from django.contrib.admin.templatetags import log
    return render_with_context(request,'frontpage.html', locals())

def todo(request):
    message = "no test message"  #reverse('personn', kwargs={"name":"hkjhjh"}) 
    if "reloadexpos" in request.GET:
        message = LoadPersonsExpos()
        message = "Reloaded personexpos"
    if "reloadsurvex" in request.POST:
        message = LoadAllSurvexBlocks()
        message = "Reloaded survexblocks"

    expeditions =  Expedition.objects.order_by("-year")
    totallogbookentries = LogbookEntry.objects.count()
    return render_with_context(request,'index.html', {'expeditions':expeditions, 'all':'all', 'totallogbookentries':totallogbookentries, "message":message})

def calendar(request, year):
    week=['S','S','M','T','W','T','F']
    expedition = Expedition.objects.get(year=year)
    personexpeditions = expedition.personexpedition_set.all()
    
    listdays = [ ]   # the columns of the table
    date = expedition.date_from
    while date <= expedition.date_to:
        listdays.append(date)
        date += datetime.timedelta(days=1)
                
    personexpeditiondays = [ ]
    for personexpedition in personexpeditions:
        pelistdays = [ (personexpedition.date_from and (personexpedition.date_from <= date < personexpedition.date_to))  for date in listdays ]
        personexpeditiondays.append([personexpedition, pelistdays])
        
    return render_with_context(request,'calendar.html', {"expedition":expedition, "listdays":listdays, "personexpeditiondays":personexpeditiondays})

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
                return render_with_context(request,'controlPanel.html', {'caves':Cave.objects.all(),'error':'You must be a superuser to use that feature.'})
            else:
                return HttpResponseRedirect(reverse('auth_login'))

    return render_with_context(request,'controlPanel.html', {'caves':Cave.objects.all(),'expeditions':Expedition.objects.all(),'jobs_completed':jobs_completed})

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
    return 

def ajax_QM_number(request):
    if request.method=='POST':
        cave=Cave.objects.get(id=request.POST['cave'])
        print cave
        exp=Expedition.objects.get(pk=request.POST['year'])
        print exp
        res=cave.new_QM_number(exp.year)

    return HttpResponse(res)

def logbook_entry_suggestions(request):
    """
    Generates a html box with suggestions about what to do with QMs
    in logbook entry text.
    """
    unwiki_QM_pattern=r"(?P<whole>(?P<explorer_code>[ABC]?)(?P<cave>\d*)-?(?P<year>\d\d\d?\d?)-(?P<number>\d\d)(?P<grade>[ABCDXV]?))"
    unwiki_QM_pattern=re.compile(unwiki_QM_pattern)
    #wikilink_QM_pattern=settings.QM_PATTERN
    
    slug=request.POST['slug']
    date=request.POST['date']
    lbo=LogbookEntry.objects.get(slug=slug, date=date)
    
    #unwiki_QMs=re.findall(unwiki_QM_pattern,lbo.text)
    unwiki_QMs=[m.groupdict() for m in unwiki_QM_pattern.finditer(lbo.text)]
    
    print unwiki_QMs
    for qm in unwiki_QMs:
        #try:
            if len(qm['year'])==2:
                if int(qm['year'])<50:
                    qm['year']='20'+qm['year']
                else:
                    qm['year']='19'+qm['year']

            if lbo.date.year!=int(qm['year']):
                try:
                    lbo=LogbookEntry.objects.get(date__year=qm['year'],title__icontains="placeholder for QMs in")
                except:
                    print "failed to get placeholder for year "+str(qm['year'])
            
            temp_QM=QM(found_by=lbo,number=qm['number'],grade=qm['grade'])
            temp_QM.grade=qm['grade']
            qm['wikilink']=temp_QM.wiki_link()
        #except:
            #print 'failed'

    print unwiki_QMs
    
    
    #wikilink_QMs=re.findall(wikilink_QM_pattern,lbo.text)
    attached_QMs=lbo.QMs_found.all()
    unmentioned_attached_QMs=''#not implemented, fill this in by subtracting wiklink_QMs from attached_QMs
    
    #Find unattached_QMs. We only look at the QMs with a proper wiki link.
    #for qm in wikilink_QMs:
        #Try to look up the QM. 
        
    print 'got 208'
    any_suggestions=True
    print 'got 210'
    return render_with_context(request,'suggestions.html',
        {
        'unwiki_QMs':unwiki_QMs,
        'any_suggestions':any_suggestions
        })