from django.db import models
from django.contrib import admin


class Expedition(models.Model):
    year        = models.CharField(max_length=20, unique=True)
    name        = models.CharField(max_length=100)
    start_date  = models.DateField(blank=True,null=True)
    end_date    = models.DateField(blank=True,null=True)

    def __unicode__(self):
        return self.year

    def GetPersonExpedition(self, name):
        person_expeditions = PersonExpedition.objects.filter(expedition=self)
        res = None
        for person_expedition in person_expeditions:
            for possible_name_from in person_expedition.GetPossibleNameForms():
                #print "nnn", possiblenamefrom
                if name == possible_name_from:
                    assert not res, "Ambiguous: " + name
                    res = person_expedition
        return res


class Person(models.Model):
    first_name  = models.CharField(max_length=100)
    last_name   = models.CharField(max_length=100)
    is_vfho     = models.BooleanField()
    mug_shot    = models.CharField(max_length=100, blank=True,null=True)
    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

class PersonExpedition(models.Model):
    expedition  = models.ForeignKey(Expedition)
    person      = models.ForeignKey(Person)
    from_date   = models.DateField(blank=True,null=True)
    to_date     = models.DateField(blank=True,null=True)
    is_guest    = models.BooleanField()  
    nickname    = models.CharField(max_length=100,blank=True,null=True)
    
    def GetPossibleNameForms(self):
        res = [ ]
        if self.person.last_name:
            res.append("%s %s" % (self.person.first_name, self.person.last_name))
            res.append("%s %s" % (self.person.first_name, self.person.last_name[0]))
        res.append(self.person.first_name)
        if self.nickname:
            res.append(self.nickname)
        return res

    def __unicode__(self):
        return "%s: (%s)" % (self.person, self.expedition)


class LogbookEntry(models.Model):
    date    = models.DateField()
    author  = models.ForeignKey(PersonExpedition,blank=True,null=True)  # the person who writes it up doesn't have to have been on the trip
    title   = models.CharField(max_length=200)

        # this will be a foreign key of the place the logbook is describing
    place   = models.CharField(max_length=100,blank=True,null=True)  
    text    = models.TextField()

        # several PersonTrips point in to this object
    
    def __unicode__(self):
        return "%s: (%s)" % (self.date, self.title)

class PersonTrip(models.Model):
    person_expedition = models.ForeignKey(PersonExpedition)
    
        # this will be a foreign key of the place(s) the trip went through
        # possibly a trip has a plurality of triplets pointing into it
    place           = models.CharField(max_length=100)  
    date            = models.DateField()    
    time_underground = models.CharField(max_length=100)
    logbook_entry    = models.ForeignKey(LogbookEntry)
    is_logbook_entry_author = models.BooleanField()

    def __unicode__(self):
        return "%s %s (%s)" % (self.person_expedition, self.place, self.date)





