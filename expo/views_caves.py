from troggle.expo.models import Cave, CaveAndEntrance, Survey, Expedition, QM
import troggle.expo.models as models
import troggle.settings as settings
from django.forms.models import formset_factory
import search
from django.core.urlresolvers import reverse
from troggle.alwaysUseRequestContext import render_response # see views_logbooks for explanation on this.
from django.http import HttpResponseRedirect
from django.conf import settings
import re, urlparse

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

def cave(request, cave_id='', offical_name=''):
    cave=getCave(cave_id)
    if cave.non_public:
        return render_response(request,'nonpublic.html', {'instance': cave})
    else:
        return render_response(request,'cave.html', {'cave': cave})
    
def qm(request,cave_id,qm_id,year,grade=None):
    year=int(year)
    try:
        qm=getCave(cave_id).get_QMs().get(number=qm_id,found_by__date__year=year)
        return render_response(request,'qm.html',locals())

    except QM.DoesNotExist:
        url=urlparse.urljoin(settings.URL_ROOT, r'/admin/expo/qm/add/'+'?'+  r'number=' + qm_id)
        if grade:
            url += r'&grade=' + grade
        return HttpResponseRedirect(url)
    

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

def subcave(request, cave_id, subcave):
    print subcave
    subcaveSeq=re.findall('(?:/)([^/]*)',subcave)
    print subcaveSeq
    cave=models.Cave.objects.get(kataster_number = cave_id)
    subcave=models.Subcave.objects.get(title=subcaveSeq[0], cave=cave)
    if len(subcaveSeq)>1: 
        for subcaveUrlSegment in subcaveSeq[1:]:
            if subcaveUrlSegment:
                subcave=subcave.children.get(title=subcaveUrlSegment)
    print subcave
    return render_response(request,'subcave.html', {'subcave': subcave,'cave':cave})

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
    expeditions=Expedition.objects.order_by("-year")
    return render_response(request,'survey.html',locals())

def survey(request,year,wallet_number):
    surveys=Survey.objects.all()
    expeditions=Expedition.objects.order_by("-year")
    current_expedition=Expedition.objects.filter(year=year)[0]
    
    if wallet_number!='':
            current_survey=Survey.objects.filter(expedition=current_expedition,wallet_number=wallet_number)[0]
            notes=current_survey.scannedimage_set.filter(contents='notes')
            planSketches=current_survey.scannedimage_set.filter(contents='plan')
            elevationSketches=current_survey.scannedimage_set.filter(contents='elevation')
    
    return render_response(request,'survey.html', locals())
