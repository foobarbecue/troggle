from django.db import models
from django.conf import settings
import os


###########################################################
# These will allow browsing and editing of the survex data
###########################################################


# Needs to add: 
#   SurvexFile
#   Equates
#   reloading

#
# Single SurvexBlock 
# 
class SurvexBlock(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    parent = models.ForeignKey('SurvexBlock', blank=True, null=True)
    text = models.TextField()
    
    # non-useful representation of incomplete data
    start_year = models.IntegerField(blank=True, null=True)
    start_month = models.IntegerField(blank=True, null=True)
    start_day = models.IntegerField(blank=True, null=True)
    end_year = models.IntegerField(blank=True, null=True)
    end_month = models.IntegerField(blank=True, null=True)
    end_day = models.IntegerField(blank=True, null=True)
    
    date    = models.DateField(blank=True, null=True)
    survexpath  = models.CharField(max_length=100)
    
    # superfluous
    person  = models.ManyToManyField('Person', through='PersonRole', blank=True, null=True)
   
    # code for where in the survex data files this block sits
    begin_file = models.CharField(max_length=200)
    begin_char = models.IntegerField()
    end_file = models.CharField(max_length=200, blank=True, null=True)
    end_char = models.IntegerField(blank=True, null=True)
    
    class Meta:
        ordering = ('date', 'survexpath')

    def __unicode__(self):
        return self.name and unicode(self.name) or 'no name'
    
    def filewithoutsvx(self):
        return self.begin_file[:-4]
    
    def filecontents(self):
        f = os.path.join(settings.SURVEX_DATA, self.begin_file)
        fin = open(f, "rb")
        res = fin.read().decode("latin1")
        fin.close()
        return res
        
    def GetPersonroles(self):
        res = [ ]
        for personrole in self.personrole_set.order_by('personexpedition'):
            if res and res[-1]['person'] == personrole.personexpedition.person:
                res[-1]['roles'] += ", " + str(personrole.role)
            else:
                res.append({'person':personrole.personexpedition.person, 'expeditionyear':personrole.personexpedition.expedition.year, 'roles':str(personrole.role)})
        return res


#
# Replace this with a choice string in PersonRole
#
class Role(models.Model):
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return unicode(self.name)


#
# member of a SurvexBlock
#
class PersonRole(models.Model):
    survex_block        = models.ForeignKey('SurvexBlock')
    role                = models.ForeignKey('Role')  # to go
    
    ROLE_CHOICES = (
        ('insts','Instruments'),
        ('dog','Other'),
        ('notes','Notes'),
        ('pics','Pictures'),
        ('tape','Tape measure'),
        )
    nrole = models.CharField(choices=ROLE_CHOICES, max_length=200, blank=True, null=True)

    # increasing levels of precision
    person              = models.ForeignKey('Person')
    personexpedition    = models.ForeignKey('PersonExpedition')
    persontrip          = models.ForeignKey('PersonTrip', blank=True, null=True)  
    
    def __unicode__(self):
        return unicode(self.person) + " - " + unicode(self.survex_block) + " - " + unicode(self.role)
        
    
