from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
import re
import os
import datetime
import difflib

from troggle.core.models import Expedition, Person, PersonExpedition, PersonTrip, LogbookEntry, Cave
from troggle.core.models import SurvexBlock, SurvexPersonRole, SurvexFile, SurvexDirectory, SurvexTitle
from parsers.people import GetPersonExpeditionNameLookup

import troggle.settings as settings
import parsers.survex

survextemplatefile = """; Locn: Totes Gebirge, Austria - Loser/Augst-Eck Plateau (kataster group 1623)
; Cave: 

*begin [surveyname]

*export [connecting stations]

*title "area title"
*date 2999.99.99
*team Insts [Caver]
*team Insts [Caver]
*team Notes [Caver]
*instrument [set number]

;ref.: 2009#NN

*calibrate tape +0.0   ; +ve if tape was too short, -ve if too long

*data normal from to tape compass clino
1   2   3.90    298 -20

*data passage station left right up down ignoreall
1   [L]    [R]    [U]   [D]    comment

*end [surveyname]"""        
        
        
def ReplaceTabs(stext):
    res = [ ]
    nsl = 0
    for s in re.split("(\t|\n)", stext):
        if s == "\t":
            res.append(" " * (4 - (nsl % 4)))
            nsl = 0
            continue
        if s == "\n":
            nsl = 0
        else:
            nsl += len(s)
        res.append(s)
    return "".join(res)


class SvxForm(forms.Form):
    dirname = forms.CharField(widget=forms.TextInput(attrs={"readonly":True}))
    filename = forms.CharField(widget=forms.TextInput(attrs={"readonly":True}))
    datetime = forms.DateTimeField(widget=forms.TextInput(attrs={"readonly":True}))
    outputtype = forms.CharField(widget=forms.TextInput(attrs={"readonly":True}))
    code = forms.CharField(widget=forms.Textarea(attrs={"cols":150, "rows":18}))
    
    def GetDiscCode(self):
        fname = settings.SURVEX_DATA + self.data['filename'] + ".svx"
        if not os.path.isfile(fname):
            return survextemplatefile
        fin = open(fname, "rb")
        svxtext = fin.read().decode("latin1")   # unicode(a, "latin1")
        svxtext = ReplaceTabs(svxtext).strip()
        fin.close()
        return svxtext
            
    def DiffCode(self, rcode):
        code = self.GetDiscCode()
        difftext = difflib.unified_diff(code.splitlines(), rcode.splitlines())
        difflist = [ diffline.strip()  for diffline in difftext  if not re.match("\s*$", diffline) ]
        return difflist

    def SaveCode(self, rcode):
        fname = settings.SURVEX_DATA + self.data['filename'] + ".svx"
        if not os.path.isfile(fname):
            # only save if appears valid
            if re.search("\[|\]", rcode):   
                return "Error: clean up all []s from the text"
            mbeginend = re.search("(?s)\*begin\s+(\w+).*?\*end\s+(\w+)", rcode)
            if not mbeginend:
                return "Error: no begin/end block here"
            if mbeginend.group(1) != mbeginend.group(2):
                return "Error: mismatching beginend"
                
        fout = open(fname, "w")
        res = fout.write(rcode.encode("latin1"))
        fout.close()
        return "SAVED"

    def Process(self):
        print "....\n\n\n....Processing\n\n\n"
        cwd = os.getcwd()
        os.chdir(os.path.split(settings.SURVEX_DATA + self.data['filename'])[0])
        os.system(settings.CAVERN + " --log " + settings.SURVEX_DATA + self.data['filename'] + ".svx")
        os.chdir(cwd)
        fin = open(settings.SURVEX_DATA + self.data['filename'] + ".log", "rb")
        log = fin.read()
        fin.close()
        log = re.sub("(?s).*?(Survey contains)", "\\1", log)
        return log


def svx(request, survex_file):
    # get the basic data from the file given in the URL
    dirname = os.path.split(survex_file)[0]
    dirname += "/"
    nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    outputtype = "normal"
    form = SvxForm({'filename':survex_file, 'dirname':dirname, 'datetime':nowtime, 'outputtype':outputtype}) 
    
    # if the form has been returned
    difflist = [ ]
    logmessage = ""
    message = ""

    if request.method == 'POST': # If the form has been submitted...
        rform = SvxForm(request.POST) # 
        if rform.is_valid(): # All validation rules pass (how do we check it against the filename and users?)
            rcode = rform.cleaned_data['code']
            outputtype = rform.cleaned_data['outputtype']
            difflist = form.DiffCode(rcode)
            #print "ssss", rform.data
            
            if "revert" in rform.data:
                pass
            if "process" in rform.data:
                if not difflist:
                    message = "OUTPUT FROM PROCESSING"
                    logmessage = form.Process()
                    print logmessage
                else:
                    message = "SAVE FILE FIRST"
                    form.data['code'] = rcode
            if "save" in rform.data:
                if request.user.is_authenticated():
                    #print "sssavvving"
                    message = form.SaveCode(rcode)
                else:
                    message = "You do not have authority to save this file"
                if message != "SAVED":
                    form.data['code'] = rcode
            if "diff" in rform.data:
                form.data['code'] = rcode
    
    
    #process(survex_file)
    if 'code' not in form.data:    
        form.data['code'] = form.GetDiscCode()
    
    if not difflist:
        difflist.append("none")
    if message:
        difflist.insert(0, message)
    
    #print [ form.data['code'] ]
    svxincludes = re.findall('\*include\s+(\S+)(?i)', form.data['code'] or "")
    
    vmap = {'settings': settings,
            'has_3d': os.path.isfile(settings.SURVEX_DATA + survex_file + ".3d"),
            'title': survex_file,
            'svxincludes': svxincludes,
            'difflist': difflist,
            'logmessage':logmessage,
            'form':form}
    if outputtype == "ajax":
        return render_to_response('svxfiledifflistonly.html', vmap)
    return render_to_response('svxfile.html', vmap)

def svxraw(request, survex_file):
    svx = open(os.path.join(settings.SURVEX_DATA, survex_file+".svx"), "rb")
    return HttpResponse(svx, mimetype="text")


# The cavern running function
def process(survex_file):
    cwd = os.getcwd()
    os.chdir(os.path.split(settings.SURVEX_DATA + survex_file)[0])
    os.system(settings.CAVERN + " --log " + settings.SURVEX_DATA + survex_file + ".svx")
    os.chdir(cwd)


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



def identifycavedircontents(gcavedir):
    name = os.path.split(gcavedir)[1]
    subdirs = [ ]
    subsvx = [ ]
    primesvx = None
    for f in os.listdir(gcavedir):
        if name == "204" and (f in ["skel.svx", "template.svx", "204withents.svx"]):
            pass
        elif name == "136" and (f in ["136-noents.svx"]):
            pass
        elif name == "115" and (f in ["115cufix.svx", "115fix.svx"]):
            pass
        
        elif os.path.isdir(os.path.join(gcavedir, f)):
            if f[0] != ".":
                subdirs.append(f)
        elif f[-4:] == ".svx":
            nf = f[:-4]
            
            if nf.lower() == name.lower() or nf[:3] == "all" or (name, nf) in [("144arge", "144"), ("resurvey2005", "145-2005"), ("cucc", "cu115")]:
                if primesvx:
                    if nf[:3] == "all":
                        assert primesvx[:3] != "all", (name, nf, primesvx, gcavedir, subsvx)
                        primesvx = nf
                    else:
                        assert primesvx[:3] == "all", (name, nf, primesvx, gcavedir, subsvx)
                else:
                    primesvx = nf
            else:
                subsvx.append(nf)
        else:
            assert re.match(".*?(?:.3d|.log|.err|.txt|.tmp|.diff|.e?spec|~)$", f), (gcavedir, f)
    subsvx.sort()
    assert primesvx, (gcavedir, subsvx)
    if primesvx:
        subsvx.insert(0, primesvx)
    return subdirs, subsvx
                
    

# direct local non-database browsing through the svx file repositories
# perhaps should use the database and have a reload button for it
def survexcaveslist(request):
    cavesdir = os.path.join(settings.SURVEX_DATA, "caves")
    cavesdircontents = { }
    
    onefilecaves = [ ]
    multifilecaves = [ ]
    subdircaves = [ ]
    
    # first sort the file list
    fnumlist = [ (-int(re.match("\d*", f).group(0) or "0"), f)  for f in os.listdir(cavesdir) ]
    fnumlist.sort()
    
    # go through the list and identify the contents of each cave directory
    for num, cavedir in fnumlist:
        if cavedir in ["144", "40"]:
            continue
            
        gcavedir = os.path.join(cavesdir, cavedir)
        if os.path.isdir(gcavedir) and cavedir[0] != ".":
            subdirs, subsvx = identifycavedircontents(gcavedir)
            survdirobj = [ ]
            
            for lsubsvx in subsvx:
                survdirobj.append(("caves/"+cavedir+"/"+lsubsvx, lsubsvx))
            
            # caves with subdirectories
            if subdirs:
                subsurvdirs = [ ]
                for subdir in subdirs:
                    dsubdirs, dsubsvx = identifycavedircontents(os.path.join(gcavedir, subdir))
                    assert not dsubdirs
                    lsurvdirobj = [ ]
                    for lsubsvx in dsubsvx:
                        lsurvdirobj.append(("caves/"+cavedir+"/"+subdir+"/"+lsubsvx, lsubsvx))
                    subsurvdirs.append((lsurvdirobj[0], lsurvdirobj[1:]))
                subdircaves.append((cavedir, (survdirobj[0], survdirobj[1:]), subsurvdirs))
            
            # multifile caves
            elif len(survdirobj) > 1:
                multifilecaves.append((survdirobj[0], survdirobj[1:]))
            # single file caves
            else:
                onefilecaves.append(survdirobj[0])
    
    return render_to_response('svxfilecavelist.html', {'settings': settings, "onefilecaves":onefilecaves, "multifilecaves":multifilecaves, "subdircaves":subdircaves })
    

        



# parsing all the survex files of a single cave and showing that it's consistent and can find all the files and people
# doesn't use recursion.  just writes it twice
def survexcavesingle(request, survex_cave):
    breload = False
    cave = Cave.objects.get(kataster_number=survex_cave)
    if breload:
        parsers.survex.ReloadSurvexCave(survex_cave)
    return render_to_response('svxcavesingle.html', {'settings': settings, "cave":cave })

    
    
    
    