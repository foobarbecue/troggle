from django.db import models
from django.conf import settings
import os
import urlparse
import re
from django.core.urlresolvers import reverse


###########################################################
# These will allow browsing and editing of the survex data
###########################################################
# Needs to add: 
#   Equates
#   reloading

class SurvexDirectory(models.Model):
    path = models.CharField(max_length=200)
    cave = models.ForeignKey('Cave', blank=True, null=True)
    primarysurvexfile = models.ForeignKey('SurvexFile', related_name='primarysurvexfile', blank=True, null=True)
    # could also include files in directory but not referenced
    
    class Meta:
        ordering = ('id',)
    
class SurvexFile(models.Model):
    path = models.CharField(max_length=200)
    survexdirectory = models.ForeignKey("SurvexDirectory", blank=True, null=True)
    cave = models.ForeignKey('Cave', blank=True, null=True)
    
    class Meta:
        ordering = ('id',)
    
    def exists(self):
        fname = os.path.join(settings.SURVEX_DATA, self.path + ".svx")
        return os.path.isfile(fname)
    
    def OpenFile(self):
        fname = os.path.join(settings.SURVEX_DATA, self.path + ".svx")
        return open(fname)
    
    def SetDirectory(self):
        dirpath = os.path.split(self.path)[0]
        survexdirectorylist = SurvexDirectory.objects.filter(cave=self.cave, path=dirpath)
        if survexdirectorylist:
            self.survexdirectory = survexdirectorylist[0]
        else:
            survexdirectory = SurvexDirectory(path=dirpath, cave=self.cave, primarysurvexfile=self)
            survexdirectory.save()
            self.survexdirectory = survexdirectory
        self.save()

class SurvexEquate(models.Model):
    cave        = models.ForeignKey('Cave', blank=True, null=True)

class SurvexStation(models.Model):
    name        = models.CharField(max_length=20)   
    block       = models.ForeignKey('SurvexBlock')
    equate      = models.ForeignKey('SurvexEquate', blank=True, null=True)

class SurvexLeg(models.Model):
    block       = models.ForeignKey('SurvexBlock')
    #title = models.ForeignKey('SurvexTitle')
    stationfrom = models.ForeignKey('SurvexStation', related_name='stationfrom')
    stationto   = models.ForeignKey('SurvexStation', related_name='stationto')
    tape        = models.FloatField()
    compass     = models.FloatField()
    clino       = models.FloatField()


#
# Single SurvexBlock 
# 
class SurvexBlock(models.Model):
    name       = models.CharField(max_length=100)
    parent     = models.ForeignKey('SurvexBlock', blank=True, null=True)
    text       = models.TextField()
    cave       = models.ForeignKey('Cave', blank=True, null=True)
    
    date       = models.DateField(blank=True, null=True)
    #expeditionday = models.ForeignKey("ExpeditionDay", null=True)
    expedition = models.ForeignKey('Expedition', blank=True, null=True)
        
    survexfile = models.ForeignKey("SurvexFile", blank=True, null=True)
    begin_char = models.IntegerField()  # code for where in the survex data files this block sits
    survexpath = models.CharField(max_length=200)   # the path for the survex stations
    
    survexscansfolder = models.ForeignKey("SurvexScansFolder", null=True)  
    #refscandir = models.CharField(max_length=100)
    
    totalleglength = models.FloatField()
    
    class Meta:
        ordering = ('id',)

    def __unicode__(self):
        return self.name and unicode(self.name) or 'no name'
    
    def GetPersonroles(self):
        res = [ ]
        for personrole in self.personrole_set.order_by('personexpedition'):
            if res and res[-1]['person'] == personrole.personexpedition.person:
                res[-1]['roles'] += ", " + str(personrole.role)
            else:
                res.append({'person':personrole.personexpedition.person, 'expeditionyear':personrole.personexpedition.expedition.year, 'roles':str(personrole.role)})
        return res

    def MakeSurvexStation(self, name):
        ssl = self.survexstation_set.filter(name=name)
        if ssl:
            assert len(ssl) == 1
            return ssl[0]
        ss = SurvexStation(name=name, block=self)
        ss.save()
        return ss
    
    def DayIndex(self):
        return list(self.expeditionday.survexblock_set.all()).index(self)
    

class SurvexTitle(models.Model):
    survexblock = models.ForeignKey('SurvexBlock')
    title       = models.CharField(max_length=200)
    cave        = models.ForeignKey('Cave', blank=True, null=True)

#
# member of a SurvexBlock
#
ROLE_CHOICES = (
        ('insts','Instruments'),
        ('dog','Other'),
        ('notes','Notes'),
        ('pics','Pictures'),
        ('tape','Tape measure'),
        ('useless','Useless'),
        ('helper','Helper'),
        ('disto','Disto'),
        ('consultant','Consultant'),
        )

class SurvexPersonRole(models.Model):
    survexblock         = models.ForeignKey('SurvexBlock')
    nrole               = models.CharField(choices=ROLE_CHOICES, max_length=200, blank=True, null=True)
        # increasing levels of precision
    personname          = models.CharField(max_length=100)
    person              = models.ForeignKey('Person', blank=True, null=True)
    personexpedition    = models.ForeignKey('PersonExpedition', blank=True, null=True)
    persontrip          = models.ForeignKey('PersonTrip', blank=True, null=True)  
    #expeditionday       = models.ForeignKey("ExpeditionDay", null=True)
    
    def __unicode__(self):
        return unicode(self.person) + " - " + unicode(self.survexblock) + " - " + unicode(self.nrole)
        
    
class SurvexScansFolder(models.Model):
    fpath               = models.CharField(max_length=200)
    walletname          = models.CharField(max_length=200)
    
    class Meta:
        ordering = ('walletname',)
    
    def get_absolute_url(self):
        return urlparse.urljoin(settings.URL_ROOT, reverse('surveyscansfolder', kwargs={"path":re.sub("#", "%23", self.walletname)}))
    
class SurvexScanSingle(models.Model):
    ffile               = models.CharField(max_length=200)
    name                = models.CharField(max_length=200)
    survexscansfolder   = models.ForeignKey("SurvexScansFolder", null=True)
    
    class Meta:
        ordering = ('name',)
    
    def get_absolute_url(self):
        return urlparse.urljoin(settings.URL_ROOT, reverse('surveyscansingle', kwargs={"path":re.sub("#", "%23", self.survexscansfolder.walletname), "file":self.name}))
    
        
class TunnelFile(models.Model):
    tunnelpath          = models.CharField(max_length=200)
    tunnelname          = models.CharField(max_length=200)
    bfontcolours        = models.BooleanField()
    survexscansfolders  = models.ManyToManyField("SurvexScansFolder")
    survexscans         = models.ManyToManyField("SurvexScanSingle")
    survexblocks        = models.ManyToManyField("SurvexBlock")
    tunnelcontains      = models.ManyToManyField("TunnelFile")  # case when its a frame type
    filesize            = models.IntegerField(default=0)
    npaths              = models.IntegerField(default=0)
    survextitles        = models.ManyToManyField("SurvexTitle")
    
    
    class Meta:
        ordering = ('tunnelpath',)
    