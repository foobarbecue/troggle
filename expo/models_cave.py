from django.db import models
import models_logbooks

class Area(models.Model):
    short_name = models.CharField(max_length=100)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True,null=True)
    parent = models.ForeignKey('Area', blank=True, null=True)
    def __unicode__(self):
        if self.parent:
            return unicode(self.parent) + u" - " + unicode(self.short_name)
        else:
            return unicode(self.short_name)
    def kat_area(self):
        if self.short_name in ["1623", "1626"]:
            return self.short_name
        elif self.parent:
            return self.parent.kat_area()

class CaveAndEntrance(models.Model):
    cave = models.ForeignKey('Cave')
    entrance = models.ForeignKey('Entrance')
    entrance_letter = models.CharField(max_length=20,blank=True,null=True)
    def __unicode__(self):
        return unicode(self.cave) + unicode(self.entrance_letter)
        
class Cave(models.Model):
    official_name = models.CharField(max_length=160)
    area = models.ManyToManyField(Area, blank=True, null=True)
    kataster_code = models.CharField(max_length=20,blank=True,null=True)
    kataster_number = models.CharField(max_length=10,blank=True, null=True)
    unofficial_number = models.CharField(max_length=30,blank=True, null=True)
    entrances = models.ManyToManyField('Entrance', through='CaveAndEntrance')
    explorers = models.TextField(blank=True,null=True)
    underground_description = models.TextField(blank=True,null=True)
    equipment = models.TextField(blank=True,null=True)
    references = models.TextField(blank=True,null=True)
    survey = models.TextField(blank=True,null=True)
    kataster_status = models.TextField(blank=True,null=True)
    underground_centre_line = models.TextField(blank=True,null=True)
    notes = models.TextField(blank=True,null=True)
    length = models.CharField(max_length=40,blank=True,null=True)
    depth = models.CharField(max_length=40,blank=True,null=True)
    extent = models.CharField(max_length=40,blank=True,null=True)
    survex_file = models.CharField(max_length=100,blank=True,null=True)
    def __unicode__(self):
        if self.kataster_number:
            if self.kat_area():
                return self.kat_area() + u": " + self.kataster_number
            else:
                return unicode("l") + u": " + self.kataster_number
        else:
            if self.kat_area():
                return self.kat_area() + u": " + self.unofficial_number
            else:
                return self.unofficial_number
    def kat_area(self):
        for a in self.area.all():
            if a.kat_area():
                return a.kat_area()
    def entrances(self):
        return CaveAndEntrance.objects.filter(cave=self)
    def entrancelist(self):
        rs = []
        res = ""
        for e in CaveAndEntrance.objects.filter(cave=self):
            rs.append(e.entrance_letter)
        rs.sort()
        prevR = None
        n = 0
        for r in rs:
            if prevR:
                if chr(ord(prevR) + 1 ) == r:
                    prevR = r
                    n += 1
                else:
                    if n == 0:
                        res += ", " + prevR
                    else:
                        res += "&ndash;" + prevR
            else:
                prevR = r
                n = 0
                res += r
        if n == 0:
            res += ", " + prevR
        else:
            res += "&ndash;" + prevR
        return res


class OtherCaveName(models.Model):
    name = models.CharField(max_length=160)
    cave = models.ForeignKey(Cave)
    def __unicode__(self):
        return unicode(self.name)

class SurveyStation(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return unicode(self.name)

class Entrance(models.Model):
    name = models.CharField(max_length=60, blank=True,null=True)
    entrance_description = models.TextField(blank=True,null=True)
    explorers = models.TextField(blank=True,null=True)
    map_description = models.TextField(blank=True,null=True)
    location_description = models.TextField(blank=True,null=True)
    approach = models.TextField(blank=True,null=True)
    underground_description = models.TextField(blank=True,null=True)
    photo = models.TextField(blank=True,null=True)
    MARKING_CHOICES = (
        ('P', 'Paint'),
        ('P?', 'Paint (?)'),
        ('T', 'Tag'),
        ('T?', 'Tag (?)'),
        ('R', 'Retagged'),
        ('S', 'Spit'),
        ('S?', 'Spit (?)'),
        ('U', 'Unmarked'),
        ('?', 'Unknown'))
    marking = models.CharField(max_length=2, choices=MARKING_CHOICES)
    marking_comment = models.TextField(blank=True,null=True)
    FINDABLE_CHOICES = (
        ('?', 'To be confirmed ...'),
        ('S', 'Surveyed'),
        ('L', 'Lost'),
        ('R', 'Refindable'))
    findability = models.CharField(max_length=1, choices=FINDABLE_CHOICES, blank=True, null=True)
    findability_description = models.TextField(blank=True,null=True)
    alt = models.TextField(blank=True, null=True)
    northing = models.TextField(blank=True, null=True)
    easting = models.TextField(blank=True, null=True)
    tag_station = models.ForeignKey(SurveyStation, blank=True,null=True, related_name="tag_station")
    exact_station = models.ForeignKey(SurveyStation, blank=True,null=True, related_name="exact_station")
    other_station = models.ForeignKey(SurveyStation, blank=True,null=True, related_name="other_station")
    other_description = models.TextField(blank=True,null=True)
    bearings = models.TextField(blank=True,null=True)
    def __unicode__(self):
        a = CaveAndEntrance.objects.filter(entrance = self)
        name = u''
        if self.name:
            name = unicode(self.name) + u' '
        if len(a) == 1:
            return name + unicode(a[0])
        return name + unicode(a)
    def marking_val(self):
        for m in self.MARKING_CHOICES:
            if m[0] == self.marking:
                return m[1]
    def findability_val(self):
        for f in self.FINDABLE_CHOICES:
            if f[0] == self.findability:
                return f[1]

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

class QM(models.Model):
    #based on qm.csv in trunk/expoweb/smkridge/204 which has the fields:
    #"Number","Grade","Area","Description","Page reference","Nearest station","Completion description","Comment"
    found_by = models.ForeignKey(PersonTrip, related_name='QMs_found',)
    ticked_off_by = models.ForeignKey(PersonTrip, related_name='QMs_ticked_off',null=True,blank=True)
    #the cave field is unneeded- go through trips
    #cave = models.ForeignKey(Cave, edit_inline=models.TABULAR, num_in_admin=3)
    number_in_year = models.IntegerField()
    GRADE_CHOICES=(
	('A', 'A: Large obvious lead'),
	('B', 'B: Average lead'),
	('C', 'C: Tight unpromising lead'),
	('D', 'D: Dig'),
	('X', 'X: Unclimbable aven')
    )
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES)
    location_description = models.TextField(blank=True)
    #should be a foreignkey to surveystation
    nearest_station = models.CharField(max_length=400,blank=True)
    completion_description = models.TextField(blank=True)
    comment=models.TextField(blank=True)
    #the below are unneeded- instead use the date fields of the QM's trips
    #dateFound = models.DateField(blank=True)
    #dateKilled = models.DateField(blank=True)
    def __str__(self):
	QMnumber=str(self.found_by.date.year)+"-"+str(self.number_in_year)+self.grade
	return str(QMnumber)


