from django.db import models
from django.contrib import admin


class Expedition(models.Model):
    year        = models.CharField(max_length=20, unique=True)
    name        = models.CharField(max_length=100)
    start_date  = models.DateField(blank=True,null=True)
    end_date    = models.DateField(blank=True,null=True)

    def __str__(self):
        return self.year

    def GetPersonExpedition(self, name):
        personexpeditions = PersonExpedition.objects.filter(expedition=self)
        res = None
        for personexpedition in personexpeditions:
            for possiblenameform in personexpedition.GetPossibleNameForms():
                if name == possiblenameform:
                    assert not res, "Ambiguous: " + name
                    res = personexpedition
        return res


class Person(models.Model):
    first_name  = models.CharField(max_length=100)
    last_name   = models.CharField(max_length=100)
    is_vfho     = models.BooleanField()
    mug_shot    = models.CharField(max_length=100, blank=True,null=True)
    def __str__(self):
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

    def __str__(self):
        return "%s: (%s)" % (self.person, self.expedition)


class LogbookEntry(models.Model):
    date    = models.DateField()
    author  = models.ForeignKey(PersonExpedition,blank=True,null=True)  # the person who writes it up doesn't have to have been on the trip
    title   = models.CharField(max_length=100)

        # this will be a foreign key of the place the logbook is describing
    place   = models.CharField(max_length=100,blank=True,null=True)  
    text    = models.TextField()

        # several PersonTrips point in to this object
    
    def __str__(self):
        return "%s: (%s)" % (self.date, self.title)

class PersonTrip(models.Model):
    personexpedition = models.ForeignKey(PersonExpedition)
    
        # this will be a foreign key of the place(s) the trip went through
        # possibly a trip has a plurality of triplets pointing into it
    place           = models.CharField(max_length=100)  
    date            = models.DateField()    
    timeunderground = models.CharField(max_length=100)
    logbookentry    = models.ForeignKey(LogbookEntry)
    is_logbookentryauthor = models.BooleanField()

    def __str__(self):
        return "%s %s (%s)" % (self.personexpedition, self.place, self.date)





