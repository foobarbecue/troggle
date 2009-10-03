from django.conf.urls.defaults import *
from django.conf import settings

from core.views import *  # flat import
from core.views_other import *
from core.views_caves import *
from core.views_survex import *
from core.models import *
from django.views.generic.create_update import create_object
from django.contrib import admin
from django.views.generic.list_detail import object_list
from django.views.generic.simple import direct_to_template
from django.contrib import databrowse
import datalogging.models

admin.autodiscover()


# type url probably means it's used.

urlpatterns = patterns('',
    
    url(r'^$',              views_other.frontpage,      name="frontpage"),
    url(r'^todo/$',              views_other.todo,      name="todo"),
    (r'^about/$',             direct_to_template, {'template': 'about.html'}),

    url(r'^caves/$',     views_caves.caveindex,      name="caves"),
    url(r'^people/?$',   views_logbooks.personindex, name="personindex"),

    url(r'^newqmnumber/?$',              views_other.ajax_QM_number,  ),
    url(r'^lbo_suggestions/?$',              logbook_entry_suggestions),    
    #(r'^person/(?P<person_id>\d*)/?$', views_logbooks.person),
    url(r'^person/(?P<first_name>[A-Z]*[a-z\-\']*)[^a-zA-Z]*(?P<last_name>[a-z\-\']*[^a-zA-Z]*[A-Z]*[a-z\-]*)/?', views_logbooks.person, name="person"),
    #url(r'^person/(\w+_\w+)$',       views_logbooks.person,      name="person"),
    
    url(r'^expedition/(\d+)$',  views_logbooks.expedition,  name="expedition"),
    url(r'^expeditions/?$',  object_list,  {'queryset':Expedition.objects.all(),'template_name':'object_list.html'},name="expeditions"),
    url(r'^personexpedition/(?P<first_name>[A-Z]*[a-z]*)[^a-zA-Z]*(?P<last_name>[A-Z]*[a-z]*)/(?P<year>\d+)/?$', views_logbooks.personexpedition, name="personexpedition"),
    url(r'^logbookentry/(?P<date>.*)/(?P<slug>.*)/?$', views_logbooks.logbookentry,name="logbookentry"),

    url(r'^cave/(?P<cave_id>[^/]+)/?$', views_caves.cave, name="cave"),
    url(r'^cavedescription/(?P<cavedescription_name>[^/]+)/?$', views_caves.cave_description, name="cavedescription"),
    url(r'^cavedescription/?$', object_list, {'queryset':CaveDescription.objects.all(),'template_name':'object_list.html'}, name="cavedescriptions"),
    #url(r'^cavehref/(.+)$',     views_caves.cave,       name="cave"),url(r'cave'),

    url(r'^jgtfile/(.*)$',      view_surveys.jgtfile,       name="jgtfile"),
    url(r'^jgtuploadfile$',     view_surveys.jgtuploadfile, name="jgtuploadfile"),

    url(r'^cave/(?P<cave_id>[^/]+)/?(?P<ent_letter>[^/])$', ent),
    #(r'^cave/(?P<cave_id>[^/]+)/edit/$', edit_cave),
    #(r'^cavesearch', caveSearch),

    
    url(r'^cave/(?P<cave_id>[^/]+)/(?P<year>\d\d\d\d)-(?P<qm_id>\d*)(?P<grade>[ABCDX]?)?$', views_caves.qm, name="qm"),
    
    
    url(r'^logbooksearch/(.*)/?$', views_logbooks.logbookSearch),

        
    url(r'^statistics/?$', views_other.stats, name="stats"),
    
    url(r'^survey/?$', surveyindex, name="survey"),
    url(r'^survey/(?P<year>\d\d\d\d)\#(?P<wallet_number>\d*)$', survey, name="survey"),

    url(r'^controlpanel/?$', views_other.controlPanel, name="controlpanel"),
    url(r'^CAVETAB2\.CSV/?$', views_other.downloadCavetab, name="downloadcavetab"),    
    url(r'^Surveys\.csv/?$', views_other.downloadSurveys, name="downloadsurveys"),
    url(r'^logbook(?P<year>\d\d\d\d)\.(?P<extension>.*)/?$',views_other.downloadLogbook),
    url(r'^logbook/?$',views_other.downloadLogbook, name="downloadlogbook"),
    url(r'^cave/(?P<cave_id>[^/]+)/qm\.csv/?$', views_other.downloadQMs, name="downloadqms"),        
    (r'^downloadqms$', views_other.downloadQMs),
   
    url(r'^eyecandy$', views_other.eyecandy),

    (r'^admin/doc/?', include('django.contrib.admindocs.urls')),
    url(r'^admin/(.*)', admin.site.root, name="admin"),
    
    (r'^databrowse/(.*)', databrowse.site.root),

    
    # don't know why this needs troggle/ in here.  nice to get it out
    url(r'^troggle/media-admin/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ADMIN_DIR, 'show_indexes':True}),


    (r'^accounts/', include('registration.urls')),
    (r'^profiles/', include('profiles.urls')),

        
#   (r'^personform/(.*)$', personForm),

    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
                
        
    url(r'^survexblock/(.+)$',                     views_caves.survexblock, name="survexblock"),
    url(r'^survexfile/(?P<survex_file>.*?)\.svx$', views_survex.svx,        name="svx"),
    url(r'^survexfile/(?P<survex_file>.*?)\.3d$',  views_survex.threed,     name="threed"),
    url(r'^survexfile/(?P<survex_file>.*?)\.log$', views_survex.svxraw),
    url(r'^survexfile/(?P<survex_file>.*?)\.err$', views_survex.err),
    
            
    url(r'^survexfile/caves/$',                     views_survex.survexcaveslist,  name="survexcaveslist"),
    url(r'^survexfile/caves/(?P<survex_cave>.*)$',  views_survex.survexcavesingle, name="survexcavessingle"),
    url(r'^survexfileraw/(?P<survex_file>.*?)\.svx$', views_survex.svxraw,         name="svxraw"),
            
                
    (r'^survey_files/listdir/(?P<path>.*)$',       view_surveys.listdir),
    (r'^survey_files/download/(?P<path>.*)$',      view_surveys.download),
    #(r'^survey_files/upload/(?P<path>.*)$', view_surveys.upload),

    
            
    (r'^survey_scans/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.SURVEY_SCANS, 'show_indexes':True}),
    #url(r'^survey_scans/$',                        view_surveys.surveyscansfolders, name="surveyscansfolders"), 
    #url(r'^survey_scans/(?P<path>[^/]+)/$',        view_surveys.surveyscansfolder,  name="surveyscansfolder"), 
    #url(r'^survey_scans/(?P<path>[^/]+)/(?P<file>[^/]+(?:png|jpg))$', view_surveys.surveyscansingle,   name="surveyscansingle"), 
    
    url(r'^tunneldata/$',                          view_surveys.tunneldata,         name="tunneldata"), 
    url(r'^tunneldataraw/(?P<path>.+?\.xml)$',     view_surveys.tunnelfile,         name="tunnelfile"), 
    url(r'^tunneldataraw/(?P<path>.+?\.xml)/upload$',view_surveys.tunnelfileupload, name="tunnelfileupload"), 
    
    #url(r'^tunneldatainfo/(?P<path>.+?\.xml)$',    view_surveys.tunnelfileinfo,     name="tunnelfileinfo"), 
    
    (r'^photos/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.PHOTOS_ROOT, 'show_indexes':True}),

    # for those silly ideas
    url(r'^experimental.*$',                         views_logbooks.experimental,  name="experimental"),
    
            #url(r'^trip_report/?$',views_other.tripreport,name="trip_report")
)

from datalogging.models import *

databrowse.site.register(Manufacturer)
databrowse.site.register(EquipmentType)
databrowse.site.register(EquipmentItem)
databrowse.site.register(Timeseries)
databrowse.site.register(DataPoint)
