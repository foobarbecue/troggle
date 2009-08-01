import troggle.settings as settings
import troggle.core.models as models

from troggle.parsers.people import GetPersonExpeditionNameLookup
import re
import os


def RecursiveLoad(survexblock, survexfile, fin, textlines):
    iblankbegins = 0
    text = [ ]
    teammembers = [ ]
    while True:
        svxline = fin.readline().decode("latin1")
        if not svxline:
            return
        textlines.append(svxline)
        mstar = re.match('\s*\*(\w+)\s+(.*?)\s*(?:;.*)?$', svxline)
        
        #;ref.: 2008#18
        mref = re.match('.*?ref.*?(\d+#\d+)', svxline)
        if mref:
            survexblock.refscandir = mref.group(1)
            survexblock.save()
             
        if mstar:
            cmd, line = mstar.groups()
            
            if re.match("include$(?i)", cmd):
                includepath = os.path.join(os.path.split(survexfile.path)[0], re.sub("\.svx$", "", line))
                includesurvexfile = models.SurvexFile(path=includepath, cave=survexfile.cave)
                includesurvexfile.save()
                includesurvexfile.SetDirectory()
                if includesurvexfile.exists():
                    fininclude = includesurvexfile.OpenFile()
                    RecursiveLoad(survexblock, includesurvexfile, fininclude, textlines)
            
            elif re.match("begin$(?i)", cmd):
                if line: 
                    name = line.lower()
                    survexblockdown = models.SurvexBlock(name=name, begin_char=fin.tell(), parent=survexblock, survexpath=survexblock.survexpath+"."+name, cave=survexblock.cave, survexfile=survexfile)
                    survexblockdown.save()
                    textlinesdown = [ ]
                    RecursiveLoad(survexblockdown, survexfile, fin, textlinesdown)
                else:
                    iblankbegins += 1
            
            elif re.match("end$(?i)", cmd):
                if iblankbegins:
                    iblankbegins -= 1
                else:
                    survexblock.text = "".join(textlines)
                    survexblock.save()
                    return
            
            elif re.match("date$(?i)", cmd):
                if len(line) == 10:
                    survexblock.date = re.sub("\.", "-", line)
                    expeditions = models.Expedition.objects.filter(year=line[:4])
                    if expeditions:
                        survexblock.expedition = expeditions[0]
            
            elif re.match("team$(?i)", cmd):
                mteammember = re.match("(Insts|Notes|Tape|Dog|Useless|Pics|Helper|Disto|Consultant)\s+(.*)$(?i)", line)
                if mteammember:
                    for tm in re.split(" and | / |, | & | \+ |^both$|^none$(?i)", mteammember.group(2)):
                        if tm:
                            personexpedition = survexblock.expedition and GetPersonExpeditionNameLookup(survexblock.expedition).get(tm.lower())
                            if (personexpedition, tm) not in teammembers:
                                teammembers.append((personexpedition, tm))
                                personrole = models.PersonRole(survex_block=survexblock, nrole=mteammember.group(1).lower(), personexpedition=personexpedition, personname=tm)
                                personrole.save()
                                
            elif cmd == "title":
                survextitle = models.SurvexTitle(survexblock=survexblock, title=line.strip('"'), cave=survexblock.cave)
                survextitle.save()
                
            else:
                assert cmd.lower() in [ "sd", "equate", "include", "units", "entrance", "fix", "data", "flags", "title", "export", "instrument", "calibrate", ], (cmd, line, survexblock)
        

def ReloadSurvexCave(survex_cave):
    cave = models.Cave.objects.get(kataster_number=survex_cave)
    cave.survexblock_set.all().delete()
    cave.survexfile_set.all().delete()
    cave.survexdirectory_set.all().delete()
    
    survexfile = models.SurvexFile(path="caves/" + survex_cave + "/" + survex_cave, cave=cave)
    survexfile.save()
    survexfile.SetDirectory()
    
    survexblockroot = models.SurvexBlock(name="root", survexpath="caves", begin_char=0, cave=cave, survexfile=survexfile)
    survexblockroot.save()
    fin = survexfile.OpenFile()
    textlines = [ ]
    RecursiveLoad(survexblockroot, survexfile, fin, textlines)
    survexblockroot.text = "".join(textlines)
    survexblockroot.save()

def LoadAllSurvexBlocks():
    caves = models.Cave.objects.all()
    for cave in caves:
        if cave.kataster_number and os.path.isdir(os.path.join(settings.SURVEX_DATA, "caves", cave.kataster_number)):
            if cave.kataster_number not in ['40']:
                print "loading", cave
                ReloadSurvexCave(cave.kataster_number)
    

