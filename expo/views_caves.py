from django.shortcuts import render_to_response
from troggle.expo.models import Cave, CaveAndEntrance, Survey, Expedition
import troggle.expo.models as models
import troggle.settings as settings
from troggle.expo.forms import CaveForm
import search

def caveindex(request):
    caves = Cave.objects.all()
    return render_to_response('caveindex.html', {'caves': caves, 'settings': settings})

def cave(request, cave_id):
    #hm, we're only choosing by the number within kataster, needs to be fixed. Caves in 1626 will presumably not work. - AC 7DEC08
    cave = Cave.objects.filter(kataster_number = cave_id)[0]
    return render_to_response('cave.html', {'cave': cave, 'settings': settings})

def ent(request, cave_id, ent_letter):
    cave = Cave.objects.filter(kataster_number = cave_id)[0]
    cave_and_ent = CaveAndEntrance.objects.filter(cave = cave).filter(entrance_letter = ent_letter)[0]
    return render_to_response('entrance.html', {'cave': cave,
                                                'entrance': cave_and_ent.entrance,
                                                'letter': cave_and_ent.entrance_letter,
                                                'settings': settings})
def survexblock(request, survexpath):
    survexblock = models.SurvexBlock.objects.get(survexpath=survexpath)
    #ftext = survexblock.filecontents()
    ftext = survexblock.text
    return render_to_response('survexblock.html', {'survexblock':survexblock, 'ftext':ftext, 'settings':settings })

def caveArea(request, name):
    cavearea = models.CaveArea.objects.get(name = name)
    cave = cavearea.cave
    return render_to_response('cavearea.html', {'cavearea': cavearea, 'cave': cave, 'settings':settings })

def caveSearch(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
	entry_query = search.get_query(query_string, ['underground_description','official_name',])
	found_entries = Cave.objects.filter(entry_query)

    return render_to_response('cavesearch.html',
                          { 'query_string': query_string, 'found_entries': found_entries, 'settings': settings})
                          #context_instance=RequestContext(request))

def surveyindex(request):
    surveys=Survey.objects.all()
    expeditions=Expedition.objects.all()
    dictToPass=locals()
    dictToPass.update({'settings':settings})
    return render_to_response('survey.html',dictToPass)

def survey(request,year,wallet_number):
    surveys=Survey.objects.all()
    expeditions=Expedition.objects.all()
    current_expedition=Expedition.objects.filter(year=year)[0]
    
    if wallet_number!='':
	    current_survey=Survey.objects.filter(expedition=current_expedition,wallet_number=wallet_number)[0]
	    notes=current_survey.scannedimage_set.filter(contents='notes')
	    planSketches=current_survey.scannedimage_set.filter(contents='plan')
	    elevationSketches=current_survey.scannedimage_set.filter(contents='elevation')
	    
    dictToPass=locals()
    dictToPass.update({'settings':settings})
    
    return render_to_response('survey.html',dictToPass)
    
