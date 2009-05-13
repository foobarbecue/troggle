import fileAbstraction
from django.http import HttpResponse, Http404


def listdir(request, path):
    #try:
        return HttpResponse(fileAbstraction.listdir(path), mimetype = "text/plain")
    #except:
    #    raise Http404

def upload(request, path):
    pass

def download(request, path):
    #try:
        return HttpResponse(fileAbstraction.readFile(path), mimetype=getMimeType(path.split(".")[-1]))
    #except:
    #    raise Http404


def getMimeType(extension):
    try:
        return {"txt": "text/plain",
                "html": "text/html",
                }[extension]
    except:
        print "unknown file type"
        return "text/plain"