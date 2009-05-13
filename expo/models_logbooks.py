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
        if name == "Dour":
            name = "Anthony Day"
        personyears = PersonExpedition.objects.filter(expedition=self)
        res = None
        for personyear in personyears:
            if name == "%s %s" % (personyear.person.first_name, personyear.person.last_name):
                assert not res, "Ambiguous:" + name 
                res = personyear
            if name == "%s %s" % (personyear.person.first_name, personyear.person.last_name[0]):
                assert not res, "Ambiguous:" + name 
                res = personyear
            if name == personyear.person.first_name:
                assert not res, "Ambiguous:" + name 
                res = personyear
        return res


class Person(models.Model):
    first_name  = models.CharField(max_length=100)
    last_name   = models.CharField(max_length=100)
    is_guest    = models.BooleanField()
    is_vfho     = models.BooleanField()
    mug_shot    = models.CharField(max_length=100, blank=True,null=True)
    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

class PersonExpedition(models.Model):
    expedition  = models.ForeignKey(Expedition)
    person      = models.ForeignKey(Person)
    from_date   = models.DateField(blank=True,null=True)
    to_date     = models.DateField(blank=True,null=True)
    nickname    = models.CharField(max_length=100,blank=True,null=True)
    def __str__(self):
        return "%s: (%s)" % (self.person, self.expedition)

class LogbookEntry(models.Model):
    date    = models.DateField()
    author  = models.ForeignKey(PersonExpedition,blank=True,null=True) 
    title   = models.CharField(max_length=100)

        # this will be a foreign key
    place   = models.CharField(max_length=100,blank=True,null=True)  
    text    = models.TextField()

    #cavers = models.ManyToManyField(PersonYear)
    #tu = models.CharField(max_length=50)
    def __str__(self):
        return "%s: (%s)" % (self.date, self.title)

class PersonTrip(models.Model):
    personexpedition = models.ForeignKey(PersonExpedition)
    place           = models.CharField(max_length=100)  # this will be a foreign key
    date            = models.DateField()    
    timeunderground = models.CharField(max_length=100)
    logbookentry    = models.ForeignKey(LogbookEntry)

    #is_author    = models.BooleanField()

    def __str__(self):
        return "%s %s (%s)" % (self.personexpedition, self.place, self.date)





