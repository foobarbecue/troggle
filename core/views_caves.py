from troggle.core.models import Cave, CaveAndEntrance, Survey, Expedition, QM, CaveDescription
import troggle.core.models as models
import troggle.settings as settings
from django.forms.models import formset_factory
from django.core.urlresolvers import reverse
from utils import render_with_context # see views_logbooks for explanation on this.
from django.http import HttpResponseRedirect
from django.conf import settings
import re, urlparse
from django.shortcuts import get_object_or_404

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
    return render_with_context(request,'caveindex.html', {'caves': caves, 'notablecaves':notablecaves})

def cave(request, cave_id='', offical_name=''):
    cave=getCave(cave_id)
    if cave.non_public and not request.user.is_authenticated():
        return render_with_context(request,'nonpublic.html', {'instance': cave})
    else:
        return render_with_context(request,'cave.html', {'cave': cave})
    
def qm(request,cave_id,qm_id,year,grade=None):
    year=int(year)
    try:
        qm=getCave(cave_id).get_QMs().get(number=qm_id,found_by__date__year=year)
        return render_with_context(request,'qm.html',locals())

    except QM.DoesNotExist:
        url=urlparse.urljoin(settings.URL_ROOT, r'/admin/core/qm/add/'+'?'+  r'number=' + qm_id)
        if grade:
            url += r'&grade=' + grade
        return HttpResponseRedirect(url)
    

def ent(request, cave_id, ent_letter):
    cave = Cave.objects.filter(kataster_number = cave_id)[0]
    cave_and_ent = CaveAndEntrance.objects.filter(cave = cave).filter(entrance_letter = ent_letter)[0]
    return render_with_context(request,'entrance.html', {'cave': cave,
                                                'entrance': cave_and_ent.entrance,
                                                'letter': cave_and_ent.entrance_letter,})

def survexblock(request, survexpath):
    survexblock = models.SurvexBlock.objects.get(survexpath=survexpath)
    #ftext = survexblock.filecontents()
    ftext = survexblock.text
    return render_with_context(request,'survexblock.html', {'survexblock':survexblock, 'ftext':ftext, })

def surveyindex(request):
    surveys=Survey.objects.all()
    expeditions=Expedition.objects.order_by("-year")
    return render_with_context(request,'survey.html',locals())

def survey(request,year,wallet_number):
    surveys=Survey.objects.all()
    expeditions=Expedition.objects.order_by("-year")
    current_expedition=Expedition.objects.filter(year=year)[0]
    
    if wallet_number!='':
            current_survey=Survey.objects.filter(expedition=current_expedition,wallet_number=wallet_number)[0]
            notes=current_survey.scannedimage_set.filter(contents='notes')
            planSketches=current_survey.scannedimage_set.filter(contents='plan')
            elevationSketches=current_survey.scannedimage_set.filter(contents='elevation')

    return render_with_context(request,'survey.html', locals())

def cave_description(request, cavedescription_name):
    cave_description = get_object_or_404(CaveDescription, short_name = cavedescription_name)
    return render_with_context(request,'cave_description.html', locals())