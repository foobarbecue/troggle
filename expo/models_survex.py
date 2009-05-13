from django.db import models
import troggle.settings as settings
import os

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
    
    def __unicode__(self):
        return unicode(self.name)
    
    def filecontents(self):
        f = os.path.join(settings.SURVEX_DATA, self.begin_file)
        fin = open(f, "rb")
        res = fin.read().decode("latin1")
        fin.close()
        return res
        


class PersonRole(models.Model):
    personexpedition = models.ForeignKey('PersonExpedition')
    person = models.ForeignKey('Person')
    survex_block = models.ForeignKey('SurvexBlock')
    role = models.ForeignKey('Role')
    def __unicode__(self):
        return unicode(self.person) + " - " + unicode(self.survex_block) + " - " + unicode(self.role)
        
class Role(models.Model):
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return unicode(self.name)
    
