from troggle.expo.models import Cave, CaveAndEntrance, Survey, Expedition
import troggle.expo.models as models
import troggle.settings as settings
from troggle.expo.forms import CaveForm
import search
from troggle.alwaysUseRequestContext import render_response # see views_logbooks for explanation on this.

def getCave(cave_id):
    """Returns a cave object when given a cave name or number. It is used by views including cavehref, ent, and qm."""
    try:
        cave = Cave.objects.get(kataster_number=cave_id)
    except Cave.DoesNotExist:
        cave = Cave.objects.get(unofficial_number=cave_id)
    return cave

def caveindex(request):
    caves = Cave.objects.all()
    notablecavehrefs = [ "161", "204", "258", "76" ]  # could detect notability by trips and notability of people who have been down them
    notablecaves = [Cave.objects.get(kataster_number=kataster_number)  for kataster_number in notablecavehrefs ]
    return render_response(request,'caveindex.html', {'caves': caves, 'notablecaves':notablecaves})

def cavehref(request, cave_id='', offical_name=''):
    return render_response(request,'cave.html', {'cave': getCave(cave_id),})

def qm(request,cave_id,qm_id,year):
    year=int(year)
    qm=getCave(cave_id).get_QMs().get(number=qm_id,found_by__date__year=year)
    return render_response(request,'qm.html',{'qm':qm,})

def ent(request, cave_id, ent_letter):
    cave = Cave.objects.filter(kataster_number = cave_id)[0]
    cave_and_ent = CaveAndEntrance.objects.filter(cave = cave).filter(entrance_letter = ent_letter)[0]
    return render_response(request,'entrance.html', {'cave': cave,
                                                'entrance': cave_and_ent.entrance,
                                                'letter': cave_and_ent.entrance_letter,})

def survexblock(request, survexpath):
    survexblock = models.SurvexBlock.objects.get(survexpath=survexpath)
    #ftext = survexblock.filecontents()
    ftext = survexblock.text
    return render_response(request,'survexblock.html', {'survexblock':survexblock, 'ftext':ftext, })

def caveArea(request, name):
    cavearea = models.CaveArea.objects.get(name = name)
    cave = cavearea.cave
    return render_response(request,'cavearea.html', {'cavearea': cavearea, 'cave': cave,})

def caveSearch(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = search.get_query(query_string, ['underground_description','official_name',])
        found_entries = Cave.objects.filter(entry_query)

    return render_response(request,'cavesearch.html',
                          { 'query_string': query_string, 'found_entries': found_entries,})

def surveyindex(request):
    surveys=Survey.objects.all()
    expeditions=Expedition.objects.all()
    return render_response(request,'survey.html',locals())

def survey(request,year,wallet_number):
    surveys=Survey.objects.all()
    expeditions=Expedition.objects.all()
    current_expedition=Expedition.objects.filter(year=year)[0]
    
    if wallet_number!='':
	    current_survey=Survey.objects.filter(expedition=current_expedition,wallet_number=wallet_number)[0]
	    notes=current_survey.scannedimage_set.filter(contents='notes')
	    planSketches=current_survey.scannedimage_set.filter(contents='plan')
	    elevationSketches=current_survey.scannedimage_set.filter(contents='elevation')
    
    return render_response(request,'survey.html', locals())
    
