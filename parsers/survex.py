import troggle.settings as settings
import troggle.core.models as models

from troggle.parsers.people import GetPersonExpeditionNameLookup
import re
import os



def LoadSurvexLineLeg(survexblock, stardata, sline, comment):
    ls = sline.lower().split()
    ssfrom = survexblock.MakeSurvexStation(ls[stardata["from"]])
    ssto = survexblock.MakeSurvexStation(ls[stardata["to"]])
    
    survexleg = models.SurvexLeg(block=survexblock, stationfrom=ssfrom, stationto=ssto)
    if stardata["type"] == "normal":
        survexleg.tape = float(ls[stardata["tape"]])
        lclino = ls[stardata["clino"]]
        lcompass = ls[stardata["compass"]]
        if lclino == "up":
            survexleg.compass = 0.0
            survexleg.clino = 90.0
        elif lclino == "down":
            survexleg.compass = 0.0
            survexleg.clino = -90.0
        elif lclino == "-" or lclino == "level":
            survexleg.compass = float(lcompass)
            survexleg.clino = -90.0
        else:
            assert re.match("[\d\-+.]+$", lcompass), ls
            assert re.match("[\d\-+.]+$", lclino) and lclino != "-", ls
            survexleg.compass = float(lcompass)
            survexleg.clino = float(lclino)
        
        # only save proper legs
        survexleg.save()
    
    itape = stardata.get("tape")
    if itape:
        survexblock.totalleglength += float(ls[itape])
        survexblock.save()
        
def LoadSurvexEquate(survexblock, sline):
    pass

def LoadSurvexLinePassage(survexblock, stardata, sline, comment):
    pass
    

stardatadefault = { "type":"normal", "t":"leg", "from":0, "to":1, "tape":2, "compass":3, "clino":4 }
stardataparamconvert = { "length":"tape", "bearing":"compass", "gradient":"clino" }

def RecursiveLoad(survexblock, survexfile, fin, textlines):
    iblankbegins = 0
    text = [ ]
    stardata = stardatadefault
    teammembers = [ ]
    
    while True:
        svxline = fin.readline().decode("latin1")
        if not svxline:
            return
        textlines.append(svxline)
        
        # break the line at the comment
        sline, comment = re.match("([^;]*?)\s*(?:;\s*(.*))?\n?$", svxline.strip()).groups()
        
        # detect ref line pointing to the scans directory
        mref = comment and re.match('.*?ref.*?(\d+)\s*#\s*(\d+)', comment)
        if mref:
            refscan = "%s#%s" % (mref.group(1), mref.group(2))
            print refscan
            survexscansfolders = models.SurvexScansFolder.objects.filter(walletname=refscan)
            if survexscansfolders:
                survexblock.survexscansfolder = survexscansfolders[0]
                #survexblock.refscandir = "%s/%s%%23%s" % (mref.group(1), mref.group(1), mref.group(2))
                survexblock.save()   
            continue
        
        if not sline:
            continue
        
        # detect the star command
        mstar = re.match('\s*\*(\w+)\s*(.*?)\s*(?:;.*)?$', sline)
        if not mstar:
            if "from" in stardata:
                LoadSurvexLineLeg(survexblock, stardata, sline, comment)
            elif stardata["type"] == "passage":
                LoadSurvexLinePassage(survexblock, stardata, sline, comment)
            continue
        
        # detect the star command
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
                survexblockdown = models.SurvexBlock(name=name, begin_char=fin.tell(), parent=survexblock, survexpath=survexblock.survexpath+"."+name, cave=survexblock.cave, survexfile=survexfile, totalleglength=0.0)
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
                    assert len(expeditions) == 1
                    survexblock.expedition = expeditions[0]
                    survexblock.expeditiondate = survexblock.expedition.get_expedition_day(survexblock.date)
        elif re.match("team$(?i)", cmd):
            mteammember = re.match("(Insts|Notes|Tape|Dog|Useless|Pics|Helper|Disto|Consultant)\s+(.*)$(?i)", line)
            if mteammember:
                for tm in re.split(" and | / |, | & | \+ |^both$|^none$(?i)", mteammember.group(2)):
                    if tm:
                        personexpedition = survexblock.expedition and GetPersonExpeditionNameLookup(survexblock.expedition).get(tm.lower())
                        if (personexpedition, tm) not in teammembers:
                            teammembers.append((personexpedition, tm))
                            personrole = models.SurvexPersonRole(survexblock=survexblock, nrole=mteammember.group(1).lower(), personexpedition=personexpedition, personname=tm)
                            if personexpedition:
                                personrole.person=personexpedition.person
                            personrole.save()
                            
        elif cmd == "title":
            survextitle = models.SurvexTitle(survexblock=survexblock, title=line.strip('"'), cave=survexblock.cave)
            survextitle.save()
            
        elif cmd == "data":
            ls = line.lower().split()
            stardata = { "type":ls[0] }
            for i in range(0, len(ls)):
                stardata[stardataparamconvert.get(ls[i], ls[i])] = i - 1
            if ls[0] in ["normal", "cartesian", "nosurvey"]:
                assert "from" in stardata, line
                assert "to" in stardata, line
            elif ls[0] == "default":
                stardata = stardatadefault
            else:
                assert ls[0] == "passage", line
        
        elif cmd == "equate":
            LoadSurvexEquate(survexblock, sline)
        
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
    
    survexblockroot = models.SurvexBlock(name="root", survexpath="caves", begin_char=0, cave=cave, survexfile=survexfile, totalleglength=0.0)
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
    

