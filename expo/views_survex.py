from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
import re
import os

import troggle.settings as settings

def index(request, survex_file):
    process(survex_file)
    f = open(settings.SURVEX_DATA + survex_file + ".svx", "rb")
    a = f.read()
    return render_to_response('svxfile.html', {'settings': settings,
                                               'has_3d': os.path.isfile(settings.SURVEX_DATA + survex_file + ".3d"),
                                               'title': survex_file,
                                               'text': unicode(a, "latin1")})

def svx(request, survex_file):
    svx = open(settings.SURVEX_DATA + survex_file + ".svx", "rb")
    return HttpResponse(svx, mimetype="text")

def threed(request, survex_file):
    process(survex_file)
    try:
        threed = open(settings.SURVEX_DATA + survex_file + ".3d", "rb")
        return HttpResponse(threed, mimetype="model/3d")
    except:
        log = open(settings.SURVEX_DATA + survex_file + ".log", "rb")
        return HttpResponse(log, mimetype="text")

def log(request, survex_file):
    process(survex_file)
    log = open(settings.SURVEX_DATA + survex_file + ".log", "rb")
    return HttpResponse(log, mimetype="text")

def err(request, survex_file):
    process(survex_file)
    err = open(settings.SURVEX_DATA + survex_file + ".err", "rb")
    return HttpResponse(err, mimetype="text")

def process(survex_file):
    cwd = os.getcwd()
    os.chdir(os.path.split(settings.SURVEX_DATA + survex_file)[0])
    os.system(settings.CAVERN + " --log " +settings.SURVEX_DATA + survex_file + ".svx")
    os.chdir(cwd)
