import urllib, urlparse, string, os, datetime, logging, re
from django.forms import ModelForm
from django.contrib import admin
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import Min, Max
from django.conf import settings
from decimal import Decimal, getcontext
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from imagekit.models import ImageModel
getcontext().prec=2 #use 2 significant figures for decimal calculations

from models_survex import *

from django.contrib.gis.db import models

def get_related_by_wikilinks(wiki_text):
    found=re.findall(settings.QM_PATTERN,wiki_text)
    res=[]
    for wikilink in found:
        qmdict={'urlroot':'','cave':wikilink[2],'year':wikilink[1],'number':wikilink[3]}
        try:
            qm=QM.objects.get(found_by__cave__kataster_number = qmdict['cave'],
                              found_by__date__year = qmdict['year'],
                              number = qmdict['number'])
            res.append(qm)         
        except QM.DoesNotExist:
            print 'fail on '+str(wikilink)
    
    return render_to_string('object_preview.html',{'object':self})

logging.basicConfig(level=logging.DEBUG,
                           filename=settings.LOGFILE,
                           filemode='w')

#This class is for adding fields and methods which all of our models will have.
class TroggleModel(models.Model):
    new_since_parsing = models.BooleanField(default=False, editable=False)
    non_public = models.BooleanField(default=False)
    
    def object_name(self):
        return self._meta.object_name

    def get_admin_url(self):
        return "/admin/core/" + self.object_name().lower() + "/" + str(self.pk)
    
    def comments(self):
        return render_to_string('comments.html',{'object':self})

    class Meta:
	    abstract = True

class TroggleImageModel(ImageModel, models.Model):
    new_since_parsing = models.BooleanField(default=False, editable=False)
    
    def object_name(self):
        return self._meta.object_name

    def get_admin_url(self):
        return "/admin/core/" + self.object_name().lower() + "/" + str(self.pk)


    class Meta:
	    abstract = True

# 
# single Expedition, usually seen by year
#
class Expedition(TroggleModel):
    year        = models.CharField(max_length=20, unique=True)
    name        = models.CharField(max_length=100)
        
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('-year',)
        get_latest_by = 'year'
    
    def get_absolute_url(self):
        return reverse('expedition', args=[self.year])
    
    # construction function.  should be moved out
    def get_expedition_day(self, date):
        expeditiondays = self.expeditionday_set.filter(date=date)
        if expeditiondays:
            assert len(expeditiondays) == 1
            return expeditiondays[0]
        res = ExpeditionDay(expedition=self, date=date)
        res.save()
        return res
        
    def day_min(self):
        res = self.expeditionday_set.all()
        return res and res[0] or None
    
    def day_max(self):
        res = self.expeditionday_set.all()
        return res and res[len(res) - 1] or None
        
        
# I can't think of a reason why the following model would be necessary. - Aaron 21 Sep 09
#
#class ExpeditionDay(TroggleModel):
#    expedition  = models.ForeignKey("Expedition")
#    date        = models.DateField()

#    class Meta:
#        ordering = ('date',)  

#    def GetPersonTrip(self, personexpedition):
#        personexpeditions = self.persontrip_set.filter(expeditionday=self)
#        return personexpeditions and personexpeditions[0] or None
    
        
#
# single Person, can go on many years
#
class Person(TroggleModel):
    first_name  = models.CharField(max_length=100)
    last_name   = models.CharField(max_length=100, blank=True, null=True)
    affiliation     = models.CharField(max_length=300, blank=True, null=True)
    #mug_shot    = models.CharField(max_length=100, blank=True,null=True)
    blurb = models.TextField(blank=True,null=True)
    
    #the below have been removed and made methods. I'm not sure what the b in bisnotable stands for. - AC 16 Feb
    #notability  = models.FloatField()               # for listing the top 20 people
    #bisnotable  = models.BooleanField()
    user	= models.OneToOneField(User, null=True, blank=True)
    def get_absolute_url(self):
        return reverse('person',kwargs={'first_name':self.first_name,'last_name':self.last_name})

    class Meta:
        verbose_name_plural = "People"
        ordering = ('last_name','first_name')  
    
    def __unicode__(self):
        if self.last_name:
            return "%s %s" % (self.first_name, self.last_name)
        return self.first_name

    def notability(self):
        notability = Decimal(0)
        for personexpedition in self.personexpedition_set.all():
             if not personexpedition.is_guest:
                notability += Decimal(1) / (2012 - int(personexpedition.expedition.year))
        return notability

    def bisnotable(self):
        return self.notability() > Decimal(1)/Decimal(3)
    
    def surveyedleglength(self):
        return sum([personexpedition.surveyedleglength()  for personexpedition in self.personexpedition_set.all()])
    
    def first(self):
        return self.personexpedition_set.order_by('-expedition')[0]
    def last(self):
        return self.personexpedition_set.order_by('expedition')[0]
    
    #def Sethref(self):
        #if self.last_name:
            #self.href = self.first_name.lower() + "_" + self.last_name.lower()
            #self.orderref = self.last_name + " " + self.first_name
        #else:
          #  self.href = self.first_name.lower()
            #self.orderref = self.first_name
        #self.notability = 0.0  # set temporarily
        

#
# Person's attenance to one Expo
#
class PersonExpedition(TroggleModel):
    expedition  = models.ForeignKey(Expedition)
    person      = models.ForeignKey(Person)
    
    
    is_guest    = models.BooleanField(default=False)  
    COMMITTEE_CHOICES = (
        ('leader','Expo leader'),
        ('medical','Expo medical officer'),
        ('treasurer','Expo treasurer'),
        ('sponsorship','Expo sponsorship coordinator'),
        ('research','Expo research coordinator'),
        )
    position = models.CharField(blank=True,null=True,choices=COMMITTEE_CHOICES,max_length=200)
    nickname    = models.CharField(max_length=100,blank=True,null=True)
    
    def GetPersonroles(self):
        res = [ ]
        for personrole in self.personrole_set.order_by('survexblock'):
            if res and res[-1]['survexpath'] == personrole.survexblock.survexpath:
                res[-1]['roles'] += ", " + str(personrole.role)
            else:
                res.append({'date':personrole.survexblock.date, 'survexpath':personrole.survexblock.survexpath, 'roles':str(personrole.role)})
        return res

    class Meta:
        ordering = ('-expedition',)
        #order_with_respect_to = 'expedition'

    def __unicode__(self):
        return "%s: (%s)" % (self.person, self.expedition)
    
    
    #why is the below a function in personexpedition, rather than in person? - AC 14 Feb 09
    def name(self):
        if self.nickname:
            return "%s (%s) %s" % (self.person.first_name, self.nickname, self.person.last_name)
        if self.person.last_name:
            return "%s %s" % (self.person.first_name, self.person.last_name)
        return self.person.first_name

    def get_absolute_url(self):
        return reverse('personexpedition',kwargs={'first_name':self.person.first_name,'last_name':self.person.last_name,'year':self.expedition.year})
	
    def surveyedleglength(self):
        survexblocks = [personrole.survexblock  for personrole in self.personrole_set.all() ]
        return sum([survexblock.totalleglength  for survexblock in set(survexblocks)])
    
    # would prefer to return actual person trips so we could link to first and last ones
    def day_min(self):
        res = self.persontrip_set.aggregate(day_min=Min("expeditionday__date"))
        return res["day_min"]

    def day_max(self):
        res = self.persontrip_set.all().aggregate(day_max=Max("expeditionday__date"))
        return res["day_max"]

#
# Single parsed entry from Logbook
#    
class LogbookEntry(TroggleModel):
    date    = models.DateField()
    
    #below field is unnecessary duplicate; can figure out what expedition it is from any persontrip's personexpedition's expedition.
    expedition  = models.ForeignKey(Expedition,blank=True,null=True)
    
    #author  = models.ForeignKey(PersonExpedition,blank=True,null=True) # the person who writes it up doesn't have to have been on the trip. <- reply to previous from Aaron: if they wrote it up and weren't on the trip, they are actually part of the trip by virtue of writing about it; they just have a time underground of 0.
    title   = models.CharField(max_length=200)
    cave    = models.ForeignKey('Cave',blank=True,null=True)
    place   = models.CharField(max_length=100,blank=True,null=True,help_text="Only use this if you haven't chosen a cave")
    text    = models.TextField()
    slug    = models.SlugField(max_length=50)

    class Meta:
        verbose_name_plural = "Logbook entries"
        ordering = ('-date',)

    def get_absolute_url(self):
        return reverse('logbookentry',kwargs={'date':self.date,'slug':self.slug})

    def __unicode__(self):
        return "%s (%s) at %s" % (self.title, self.date, self.cave or self.place)

    def get_next_by_id(self):
        LogbookEntry.objects.get(id=self.id+1)

    def get_previous_by_id(self):
        LogbookEntry.objects.get(id=self.id-1)

    def new_QM_number(self):
        """Returns  """
        if self.cave:
            nextQMnumber=self.cave.new_QM_number(self.date.year)
        else:
            return none
        return nextQMnumber

    def new_QM_found_link(self):
        """Produces a link to a new QM with the next number filled in and this LogbookEntry set as 'found by' """
        return r'/admin/core/qm/add/?' + r'found_by=' + str(self.pk) +'&number=' + str(self.new_QM_number())

    def DayIndex(self):
        return list(self.expeditionday.logbookentry_set.all()).index(self)
        
    def intro(self):
        if len(self.text) > 80:
            return self.text[0:80] + '...'
        else:
            return self.text
    
    def author(self):
        return PersonTrip.objects.get(logbook_entry=self, is_logbook_entry_author=True).personexpedition.person
#
# Single Person going on a trip, which may or may not be written up (accounts for different T/U for people in same logbook entry)
#
class PersonTrip(TroggleModel):
    personexpedition = models.ForeignKey("PersonExpedition",null=True)
    
    #expeditionday    = models.ForeignKey("ExpeditionDay")
    #date             = models.DateField()    
    time_underground = models.FloatField(help_text="In decimal hours", blank=True, null=True)
    logbook_entry    = models.ForeignKey(LogbookEntry)
    is_logbook_entry_author = models.BooleanField()
    
    
    # sequencing by person (difficult to solve locally) - Julian
    # No, it really isn't difficult at all, see below- Aaron
    #persontrip_next  = models.ForeignKey('PersonTrip', related_name='pnext', blank=True,null=True)
    #persontrip_prev  = models.ForeignKey('PersonTrip', related_name='pprev', blank=True,null=True)
    
    def next_trip_for_person(self):
        self.personexpedition.persontrip_set.order_by('date').filter(date__gte=self.logbook_entry.date,)[0]
    
    def prev_trip_for_person(self):
        self.personexpedition.persontrip_set.order_by('-date').filter(date__lte=self.logbook_entry.date,)[0]
    
    def place(self):
        return self.logbook_entry.cave and self.logbook_entry.cave or self.logbook_entry.place

    def __unicode__(self):
        return "%s (%s)" % (self.personexpedition, self.logbook_entry.date)
    


##########################################
# move following classes into models_cave
##########################################

class Area(TroggleModel):
    name = models.CharField(max_length=200, )
    slug = models.SlugField()
    description = models.TextField(blank=True,null=True)
    parent = models.ForeignKey('Area', blank=True, null=True)
    def __unicode__(self):
        if self.parent:
            return unicode(self.parent) + u" - " + unicode(self.name)
        else:
            return unicode(self.name)
    def kat_area(self):
        if self.short_name in ["1623", "1626"]:
            return self.short_name
        elif self.parent:
            return self.parent.kat_area()

class CaveAndEntrance(TroggleModel):
    cave = models.ForeignKey('Cave')
    entrance = models.ForeignKey('Entrance')
    entrance_letter = models.CharField(max_length=20,blank=True,null=True)
    def __unicode__(self):
        return unicode(self.cave) + ' ' + unicode(self.entrance_letter)

class Cave(TroggleModel):
    # too much here perhaps
    official_name = models.CharField(max_length=160, unique=True)
    slug = models.SlugField(max_length=50)
    area = models.ManyToManyField(Area, blank=True, null=True)
    kataster_code = models.CharField(max_length=20,blank=True,null=True)
    number = models.CharField(max_length=10,blank=True, null=True)
    unofficial_number = models.CharField(max_length=60,blank=True, null=True)
    TYPE_CHOICES = (
        ('tower', 'vertical ice tower without horizontal development'),
        ('cave', 'horizontal ice cave without vertical tower'),
        ('cave_n_tower', 'connected horizontal cave and vertical tower'),
        ('unknown', 'not known, need to check'),
    )
    type = models.CharField(max_length=200, choices=TYPE_CHOICES)
    entrances = models.ManyToManyField('Entrance', through='CaveAndEntrance')
    explorers = models.TextField(blank=True,null=True)
    underground_description = models.TextField(blank=True,null=True)
    equipment = models.TextField(blank=True,null=True)
    references = models.TextField(blank=True,null=True)
    survey = models.TextField(blank=True,null=True)
    kataster_status = models.TextField(blank=True,null=True)
    underground_centre_line = models.TextField(blank=True,null=True)
    notes = models.TextField(blank=True,null=True)
    length = models.CharField(max_length=100,blank=True,null=True)
    depth = models.CharField(max_length=100,blank=True,null=True)
    extent = models.CharField(max_length=100,blank=True,null=True)
    survex_file = models.CharField(max_length=100,blank=True,null=True)
    description_file = models.CharField(max_length=200,blank=True,null=True)
    PROTECTION_CATEGORY_CHOICES= (
        ('A','A: Unrestricted access'),
        ('B','B: Access for scientific purposes only'),
        ('C','C: Biological refuge')
    )
    protection_category = models.CharField(max_length=1,blank=True,null=True,choices=PROTECTION_CATEGORY_CHOICES)

    #href    = models.CharField(max_length=100)


    def get_absolute_url(self):
        if self.unofficial_number:
            href = self.unofficial_number
        else:
            href = self.slug
        #return settings.URL_ROOT + '/cave/' + href + '/'
        return reverse('cave',kwargs={'cave_id':href,})

    def __unicode__(self):
        return self.official_name

    def get_QMs(self):
        return QM.objects.filter(found_by__cave=self)	

    def new_QM_number(self, year=datetime.date.today().year):
            """Given a cave and the current year, returns the next QM number."""
            try:
                res=QM.objects.filter(found_by__date__year=year, found_by__cave=self).order_by('-number')[0]
            except IndexError:
                return 1
            return res.number+1

    def kat_area(self):
        for a in self.area.all():
            if a.kat_area():
                return a.kat_area()
    
    def entrances(self):
        entrances=[]
        for caveandentrance in self.caveandentrance_set.all():
            entrances.append(caveandentrance.entrance)
        return entrances
    
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

    def timeseries_set(self):
        from datalogging.models import Timeseries
        return Timeseries.objects.filter(logbook_entry__cave=self)

    def survey_set(self):
        return Survey.objects.filter(logbook_entry__cave=self)

    class Meta:
        ordering=['-official_name']
        
    def lat(self):
        try:
            return self.entrances()[0].location.y
        except:
            return None

    def lon(self):
        try:
            return self.entrances()[0].location.x
        except:
            return None
    
    def firstVisit(self):
        try:
            return unicode(self.logbookentry_set.order_by('date')[0].date)
        except:
            return None
        
    def latestVisit(self):
        try:
            return unicode(self.logbookentry_set.order_by('-date')[0].date)
        except:
            return None
    

class OtherCaveName(TroggleModel):
    name = models.CharField(max_length=160)
    cave = models.ForeignKey(Cave)
    def __unicode__(self):
        return unicode(self.name)

class SurveyStation(TroggleModel):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return unicode(self.name)

class Entrance(TroggleModel):
    #fields using django.contrib.gis
    location = models.PointField()
    objects = models.GeoManager()
    
    name = models.CharField(max_length=100, blank=True,null=True)
    entrance_description = models.TextField(blank=True,null=True)
    explorers = models.TextField(blank=True,null=True)
    map_description = models.TextField(blank=True,null=True)
    location_description = models.TextField(blank=True,null=True)
    equipment = models.TextField(blank=True,null=True)
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
    tag_station = models.ForeignKey(SurveyStation, blank=True,null=True, related_name="tag_station")
    exact_station = models.ForeignKey(SurveyStation, blank=True,null=True, related_name="exact_station")
    other_station = models.ForeignKey(SurveyStation, blank=True,null=True, related_name="other_station")
    other_description = models.TextField(blank=True,null=True)
    bearings = models.TextField(blank=True,null=True)
    def __unicode__(self):
        CaveNEntrance = CaveAndEntrance.objects.filter(entrance = self)
        name = u''
        if self.name:
            name = unicode(self.name)
        if len(CaveNEntrance) == 1:
            return unicode(CaveNEntrance[0])+' '+name
        return unicode(CaveNEntrance) + ' ' +name

    def kmlPlacemark(self):
        return "<Placemark><name>%s</name>%s</Placemark>\n" % (self.__unicode__(), self.location.kml)

    def coordsUtmZone58C(self):
        return self.location.transform(32758, clone=True)

    def marking_val(self):
        for m in self.MARKING_CHOICES:
            if m[0] == self.marking:
                return m[1]
    
    def findability_val(self):
        for f in self.FINDABLE_CHOICES:
            if f[0] == self.findability:
                return f[1]
                
    def caves(self):
        caves=[]
        for caveandentrance in self.caveandentrance_set.all():
            caves.append(caveandentrance.cave)
        return caves

    def get_absolute_url(self):
        
        #ancestor_titles='/'.join([subcave.title for subcave in self.get_ancestors()])
        #if ancestor_titles:
            #res = '/'.join((self.get_root().cave.get_absolute_url(), ancestor_titles, self.title))
        
        #else:
            #res = '/'.join((self.get_root().cave.get_absolute_url(), self.title))
            
        try:
            return res.caves()[0].get_absolute_url()
        except:
            return None
    
    class Meta:
        ordering=['caveandentrance__cave']

class CaveDescription(TroggleModel):
    short_name = models.CharField(max_length=50, unique = True)
    long_name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True,null=True)
    linked_subcaves = models.ManyToManyField("NewSubCave", blank=True,null=True)
    linked_entrances = models.ManyToManyField("Entrance", blank=True,null=True)
    linked_qms = models.ManyToManyField("QM", blank=True,null=True)

    def __unicode__(self):
        if self.long_name:
            return unicode(self.long_name)
        else:
            return unicode(self.short_name)
    
    def get_absolute_url(self):
        return reverse('cavedescription', args=(self.short_name,))
    
    def save(self):
        """
        Overridden save method which stores wikilinks in text as links in database.
        """
        super(CaveDescription, self).save()
        qm_list=get_related_by_wikilinks(self.description)
        for qm in qm_list:
            self.linked_qms.add(qm)
        super(CaveDescription, self).save()

class NewSubCave(TroggleModel):
    name = models.CharField(max_length=200, unique = True)
    def __unicode__(self):
        return unicode(self.name)

class QM(TroggleModel):
    #based on qm.csv in trunk/expoweb/smkridge/204 which has the fields:
    #"Number","Grade","Area","Description","Page reference","Nearest station","Completion description","Comment"
    found_by = models.ForeignKey(LogbookEntry, related_name='QMs_found',blank=True, null=True )
    ticked_off_by = models.ForeignKey(LogbookEntry, related_name='QMs_ticked_off',null=True,blank=True)
    number = models.IntegerField(help_text="this is the sequential number in the year", )
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
    nearest_station_description = models.CharField(max_length=400,null=True,blank=True)
    nearest_station = models.CharField(max_length=200,blank=True,null=True)
    area = models.CharField(max_length=100,blank=True,null=True)
    completion_description = models.TextField(blank=True,null=True)
    comment=models.TextField(blank=True,null=True)

    def __unicode__(self):
	return u"%s %s" % (self.code(), self.grade)

    def code(self):
	return u"%s-%s-%s" % (unicode(self.found_by.cave)[6:], self.found_by.date.year, self.number)

    def get_absolute_url(self):
        #return settings.URL_ROOT + '/cave/' + self.found_by.cave.kataster_number + '/' + str(self.found_by.date.year) + '-' + '%02d' %self.number
        return reverse('qm',kwargs={'cave_id':self.found_by.cave.kataster_number,'year':self.found_by.date.year,'qm_id':self.number,'grade':self.grade})

    def get_next_by_id(self):
        return QM.objects.get(id=self.id+1)

    def get_previous_by_id(self):
        return QM.objects.get(id=self.id-1)

    def wiki_link(self):
	return u"%s%s%s" % ('[[QM:',self.code(),']]')

photoFileStorage = FileSystemStorage(location=settings.PHOTOS_ROOT, base_url=settings.PHOTOS_URL)
class Photo(TroggleImageModel):    
    file = models.ImageField(storage=photoFileStorage, upload_to='.',null=False)
    caption = models.TextField(blank=True,null=True)
    slug=models.SlugField()    
    contains_logbookentry = models.ForeignKey(LogbookEntry,blank=True,null=True)
    contains_person = models.ManyToManyField(Person,blank=True,null=True)
    is_mugshot = models.BooleanField(default=False)
    contains_cave = models.ForeignKey(Cave,blank=True,null=True, help_text='If you fill this out, do not fill out "location" below.')
    contains_entrance = models.ForeignKey(Entrance, related_name="photo_file",blank=True,null=True,  help_text='If you fill this out, do not fill out "location" below.')
    nearest_survey_point = models.ForeignKey(SurveyStation,blank=True,null=True,  help_text='If you fill this out, do not fill out "location" below.')
    nearest_QM = models.ForeignKey(QM,blank=True,null=True,  help_text='If you fill this out, do not fill out "location" below.')
    taken_by = models.ForeignKey(Person, blank=True, null=True, related_name="photographer")
    location = models.PointField(blank=True,null=True,help_text='Only fill this out if the photo is not linked to a cave, entrance, survey point, or QM. You can use the text field below to manually enter coordinates in the Well-Known Text format.')
    objects = models.GeoManager()
    
    class IKOptions:
        spec_module = 'core.imagekit_specs'
        cache_dir = 'thumbs'
        image_field = 'file'
        
    #content_type = models.ForeignKey(ContentType)
    #object_id = models.PositiveIntegerField()
    #location = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.caption

scansFileStorage = FileSystemStorage(location=settings.SURVEY_SCANS, base_url=settings.SURVEYS_URL)
def get_scan_path(instance, filename):
    year=instance.survey.expedition.year
    if instance.survey.wallet_number:
        print "WN: ", type(instance.survey.wallet_number), instance.survey.wallet_number
        number="%02d" % instance.survey.wallet_number + str(instance.survey.wallet_letter) #using %02d string formatting because convention was 2009#01
        return os.path.join('./',year,year+r'#'+number,instance.contents+str(instance.number_in_wallet)+r'.jpg')
    else:
        return unicode(instance.survey)+'_'+unicode(instance.contents)+'_'+unicode(len(instance.survey.scannedimage_set.all())+1)+r'.jpg'

class ScannedImage(TroggleImageModel): 
    file = models.ImageField(storage=scansFileStorage, upload_to=get_scan_path)
    scanned_by = models.ForeignKey(Person,blank=True, null=True)
    scanned_on = models.DateField(null=True)
    survey = models.ForeignKey('Survey')
    contents = models.CharField(max_length=20,choices=(('notes','notes'),('plan','plan_sketch'),('elevation','elevation_sketch'),('survey','rendered_survey')))
    number_in_wallet = models.IntegerField(blank=True,null=True)

    class IKOptions:
        spec_module = 'core.imagekit_specs'
        cache_dir = 'thumbs'
        image_field = 'file'
    #content_type = models.ForeignKey(ContentType)
    #object_id = models.PositiveIntegerField()
    #location = generic.GenericForeignKey('content_type', 'object_id')

    #This is an ugly hack to deal with the #s in our survey scan paths. The correct thing is to write a custom file storage backend which calls urlencode on the name for making file.url but not file.path.
    def correctURL(self):
	return string.replace(self.file.url,r'#',r'%23')
    
    def __unicode__(self):
        return get_scan_path(self,'')

class Survey(TroggleModel):
    expedition = models.ForeignKey('Expedition') #REDUNDANT (logbook_entry)
    wallet_number = models.IntegerField(blank=True,null=True)
    wallet_letter = models.CharField(max_length=1,blank=True,null=True)
    comments = models.TextField(blank=True,null=True)
    location = models.CharField(max_length=400,blank=True,null=True) #REDUNDANT
    subcave = models.ForeignKey('NewSubCave', blank=True, null=True)
    #notes_scan = models.ForeignKey('ScannedImage',related_name='notes_scan',blank=True, null=True)  	#Replaced by contents field of ScannedImage model
    survex_block  = models.OneToOneField('SurvexBlock',blank=True, null=True)
    logbook_entry = models.ForeignKey('LogbookEntry')
    centreline_printed_on = models.DateField(blank=True, null=True)
    centreline_printed_by = models.ForeignKey('Person',related_name='centreline_printed_by',blank=True,null=True)
    #sketch_scan = models.ForeignKey(ScannedImage,blank=True, null=True) 					#Replaced by contents field of ScannedImage model
    tunnel_file = models.FileField(upload_to='surveyXMLfiles',blank=True, null=True)
    tunnel_main_sketch = models.ForeignKey('Survey',blank=True,null=True)
    integrated_into_main_sketch_on = models.DateField(blank=True,null=True)
    integrated_into_main_sketch_by = models.ForeignKey('Person' ,related_name='integrated_into_main_sketch_by', blank=True,null=True)

    def __unicode__(self):
        if self.wallet_number:
            return self.expedition.year+"#"+"%02d" % int(self.wallet_number)
        else:
            return str(self.logbook_entry.slug)+'_survey from '+str(self.expedition.year)+' '

    def notes(self):
	    return self.scannedimage_set.filter(contents='notes')

    def plans(self):
	    return self.scannedimage_set.filter(contents='plan')

    def elevations(self):
	    return self.scannedimage_set.filter(contents='elevation')
    
    class IKOptions:
        spec_module = 'core.imagekit_specs'
        cache_dir = 'thumbs'
        image_field = 'file'
