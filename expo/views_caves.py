from django.shortcuts import render_to_response
from troggle.expo.models import Cave, CaveAndEntrance
import troggle.settings as settings

def caveindex(request):
    caves = Cave.objects.all()
    return render_to_response('caveindex.html', {'caves': caves, 'settings': settings})

def cave(request, cave_id):
    cave = Cave.objects.filter(kataster_number = cave_id)[0]
    return render_to_response('cave.html', {'cave': cave, 'settings': settings})

def ent(request, cave_id, ent_letter):
    cave = Cave.objects.filter(kataster_number = cave_id)[0]
    cave_and_ent = CaveAndEntrance.objects.filter(cave = cave).filter(entrance_letter = ent_letter)[0]
    return render_to_response('entrance.html', {'cave': cave,
                                                'entrance': cave_and_ent.entrance,
                                                'letter': cave_and_ent.entrance_letter,
                                                'settings': settings})
