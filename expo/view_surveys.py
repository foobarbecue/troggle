import troggle.settings as settings
from django.http import HttpResponse, Http404
import os

def listdir(request, path):
    try:
        l = []
        print settings.FILES, "t", path, "t"
        root = os.path.join(settings.FILES, path)
        print root
        for p in os.listdir(root):
            if os.path.isdir(os.path.join(root, p)):
                l.append(p + "/")
            elif os.path.isfile(os.path.join(root, p)):
                l.append(p)
            #Ignore non-files and non-directories
        return HttpResponse(str(l), mimetype = "text/plain")
    except:
        try:
            return HttpResponse(urllib.urlopen(settings.FILES + "listdir/" + name), mimetype = "text/plain")
        except:
            raise Http404

def upload(request, path):
    pass

def download(request, path):
    try:
        f = open(os.path.join(settings.FILES, path))
    except:
        try:
            f = urllib.urlopen(settings.FILES + "download/" + path)
        except:
            raise Http404
    return HttpResponse(f.read(), mimetype=getMimeType(path.split(".")[-1]))

def getMimeType(extension):
    try:
        return {"txt": "text/plain",
                "html": "text/html",
                }[extension]
    except:
        print "unknown file type"
        return "text/plain"