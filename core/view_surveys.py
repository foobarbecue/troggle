from django.conf import settings
import fileAbstraction
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
import os, stat
import re
from troggle.core.models import SurvexScansFolder, SurvexScanSingle, SurvexBlock, TunnelFile

# inline fileabstraction into here if it's not going to be useful anywhere else 
# keep things simple and ignore exceptions everywhere for now


def getMimeType(extension):
    try:
        return {"txt": "text/plain",
                "html": "text/html",
                }[extension]
    except:
        print "unknown file type"
        return "text/plain"


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


#
# julian's quick hack for something that works
# could signal directories by ending with /, and forward cases where it's missing
#
extmimetypes = {".txt": "text/plain",
             ".html": "text/html",
             ".png": "image/png",
             ".jpg": "image/jpeg",
            }
            
# dead
def jgtfile(request, f):
    fp = os.path.join(settings.SURVEYS, f)
    # could also surf through SURVEX_DATA
    
    # directory listing
    if os.path.isdir(fp):
        listdirfiles = [ ]
        listdirdirs = [ ]
        
        for lf in sorted(os.listdir(fp)):
            hpath = os.path.join(f, lf)  # not absolute path
            if lf[0] == "." or lf[-1] == "~":
                continue
            
            hpath = hpath.replace("\\", "/")  # for windows users
            href = hpath.replace("#", "%23")  # '#' in file name annoyance
            
            flf = os.path.join(fp, lf)
            if os.path.isdir(flf):
                nfiles = len([sf  for sf in os.listdir(flf)  if sf[0] != "."])
                listdirdirs.append((href, hpath + "/", nfiles))
            else:
                listdirfiles.append((href, hpath, os.path.getsize(flf)))
                
        upperdirs = [ ]
        lf = f
        while lf:
            hpath = lf.replace("\\", "/")  # for windows users
            if hpath[-1] != "/":
                hpath += "/"
            href = hpath.replace("#", "%23")
            lf = os.path.split(lf)[0]
            upperdirs.append((href, hpath))
        upperdirs.append(("", "/"))
            
        return render_to_response('listdir.html', {'file':f, 'listdirfiles':listdirfiles, 'listdirdirs':listdirdirs, 'upperdirs':upperdirs, 'settings': settings})
    
    # flat output of file when loaded
    if os.path.isfile(fp):
        ext = os.path.splitext(fp)[1].lower()
        mimetype = extmimetypes.get(ext, "text/plain")
        fin = open(fp)
        ftext = fin.read()
        fin.close()
        return HttpResponse(ftext, mimetype=mimetype)

    return HttpResponse("unknown file::%s::" % f, mimetype = "text/plain")


def UniqueFile(fname):
    while True:
        if not os.path.exists(fname):
            break
        mname = re.match("(.*?)(?:-(\d+))?\.(png|jpg|jpeg)$(?i)", fname)
        if mname:
            fname = "%s-%d.%s" % (mname.group(1), int(mname.group(2) or "0") + 1, mname.group(3))
    return fname


# join it all up and then split them off for the directories that don't exist
# anyway, this mkdir doesn't work
def SaveImageInDir(name, imgdir, project, fdata, bbinary):
    print ("hihihihi", fdata, settings.SURVEYS)
    fimgdir = os.path.join(settings.SURVEYS, imgdir)
    if not os.path.isdir(fimgdir):
        print "*** Making directory", fimgdir
        os.path.mkdir(fimgdir)
    fprojdir = os.path.join(fimgdir, project)
    if not os.path.isdir(fprojdir):
        print "*** Making directory", fprojdir
        os.path.mkdir(fprojdir)
        print "hhh"
        
    fname = os.path.join(fprojdir, name)
    print fname, "fff"
    fname = UniqueFile(fname)
    
    p2, p1 = os.path.split(fname)
    p3, p2 = os.path.split(p2)
    p4, p3 = os.path.split(p3)
    res = os.path.join(p3, p2, p1)
    
    print "saving file", fname
    fout = open(fname, (bbinary and "wb" or "w"))
    fout.write(fdata.read())
    fout.close()
    res = os.path.join(imgdir, name)
    return res.replace("\\", "/")


# do we want to consider saving project/field rather than field/project
def jgtuploadfile(request):
    filesuploaded = [ ]
    project, user, password, tunnelversion = request.POST["tunnelproject"], request.POST["tunneluser"], request.POST["tunnelpassword"], request.POST["tunnelversion"]
    print (project, user, tunnelversion)
    for uploadedfile in request.FILES.values():
        if uploadedfile.field_name in ["tileimage", "backgroundimage"] and \
                        uploadedfile.content_type in ["image/png", "image/jpeg"]:
            fname = user + "_" + re.sub("[\\\\/]", "-", uploadedfile.name) # very escaped \
            print fname
            fileuploaded = SaveImageInDir(fname, uploadedfile.field_name, project, uploadedfile, True)
            filesuploaded.append(settings.URL_ROOT + "/jgtfile/" + fileuploaded)
        if uploadedfile.field_name in ["sketch"] and \
                        uploadedfile.content_type in ["text/plain"]:
            fname = user + "_" + re.sub("[\\\\/]", "-", uploadedfile.name) # very escaped \
            print fname
            fileuploaded = SaveImageInDir(fname, uploadedfile.field_name, project, uploadedfile, False)
            filesuploaded.append(settings.URL_ROOT + "/jgtfile/" + fileuploaded)
    #print "FF", request.FILES
    #print ("FFF", request.FILES.values())
    message = ""
    print "gothere"
    return render_to_response('fileupload.html', {'message':message, 'filesuploaded':filesuploaded, 'settings': settings})

def surveyscansfolder(request, path):
    #print [ s.walletname  for s in SurvexScansFolder.objects.all() ]
    survexscansfolder = SurvexScansFolder.objects.get(walletname=path)
    return render_to_response('survexscansfolder.html', { 'survexscansfolder':survexscansfolder, 'settings': settings })

def surveyscansingle(request, path, file):
    survexscansfolder = SurvexScansFolder.objects.get(walletname=path)
    survexscansingle = SurvexScanSingle.objects.get(survexscansfolder=survexscansfolder, name=file)
    return HttpResponse(content=open(survexscansingle.ffile), mimetype="image/png")
    #return render_to_response('survexscansfolder.html', { 'survexscansfolder':survexscansfolder, 'settings': settings })
    
def surveyscansfolders(request):
    survexscansfolders = SurvexScansFolder.objects.all()
    return render_to_response('survexscansfolders.html', { 'survexscansfolders':survexscansfolders, 'settings': settings })
    
    
def tunneldata(request):
    tunnelfiles = TunnelFile.objects.all()
    return render_to_response('tunnelfiles.html', { 'tunnelfiles':tunnelfiles, 'settings': settings })
    
def tunnelfile(request, path):
    tunnelfile = TunnelFile.objects.get(tunnelpath=path)
    tfile = os.path.join(settings.TUNNEL_DATA, tunnelfile.tunnelpath)
    
    # just output the file
    if not request.POST:
        return HttpResponse(content=open(tfile), mimetype="text/plain")
    
    project, user, password, tunnelversion = request.POST["tunnelproject"], request.POST["tunneluser"], request.POST["tunnelpassword"], request.POST["tunnelversion"]
    print (project, user, tunnelversion)
    for uploadedfile in request.FILES.values():
        if uploadedfile.field_name != "sketch":
            return HttpResponse(content="Error: non-sketch file uploaded", mimetype="text/plain")
        if uploadedfile.content_type != "text/plain":
            return HttpResponse(content="Error: non-plain content type", mimetype="text/plain")
            
        # could use this to add new files
        if os.path.split(path)[1] != uploadedfile.name:  
            return HttpResponse(content="Error: name disagrees", mimetype="text/plain")
        
        orgsize = tunnelfile.filesize   # = os.stat(tfile)[stat.ST_SIZE]
            
        ttext = uploadedfile.read()
        
        # could check that the user and projects agree here
        
        fout = open(tfile, "w")
        fout.write(ttext)
        fout.close()
        
        # redo its settings of 
        tunnelfile.filesize = os.stat(tfile)[stat.ST_SIZE]
        tunnelfile.save()
        
        uploadedfile.close()
        message = "File size %d overwritten with size %d" % (orgsize, tunnelfile.filesize)
        return HttpResponse(content=message, mimetype="text/plain")

    
    

