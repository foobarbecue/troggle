from django.db import models


class SurvexBlock(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    parent = models.ForeignKey('SurvexBlock', blank=True, null=True)
    text = models.TextField()
    start_year = models.IntegerField(blank=True, null=True)
    start_month = models.IntegerField(blank=True, null=True)
    start_day = models.IntegerField(blank=True, null=True)
    end_year = models.IntegerField(blank=True, null=True)
    end_month = models.IntegerField(blank=True, null=True)
    end_day = models.IntegerField(blank=True, null=True)
    person = models.ManyToManyField('Person', through='PersonRole', blank=True, null=True)
    begin_file = models.CharField(max_length=200)
    begin_char = models.IntegerField()
    end_file = models.CharField(max_length=200, blank=True, null=True)
    end_char = models.IntegerField(blank=True, null=True)
    def __unicode__(self):
        return unicode(self.name)

class PersonRole(models.Model):
    person = models.ForeignKey('Person')
    survex_block = models.ForeignKey('SurvexBlock')
    role = models.ForeignKey('Role')
    def __unicode__(self):
        return unicode(self.person) + " - " + unicode(self.survex_block) + " - " + unicode(self.role)
        
class Role(models.Model):
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return unicode(self.name)