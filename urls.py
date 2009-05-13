from django.conf.urls.defaults import *
import troggle.settings as settings

from expo.views import *  # flat import
from expo.views_caves import *
from expo.views_survex import *
from expo.models import *
from django.views.generic.create_update import create_object
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^$',              views_other.frontpage,      name="frontpage"),
    
    url(r'^caveindex/?$',     views_caves.caveindex,      name="caveindex"),
    url(r'^personindex$',   views_logbooks.personindex, name="personindex"),
    
    
    #(r'^person/(?P<person_id>\d*)/?$', views_logbooks.person),
    url(r'^person/(?P<first_name>[A-Z]*[a-z\-\']*)[^a-zA-Z]*(?P<last_name>[a-z\-\']*[^a-zA-Z]*[A-Z]*[a-z\-]*)/?', views_logbooks.person, name="person"),
    #url(r'^person/(\w+_\w+)$',       views_logbooks.person,      name="person"),
    
    url(r'^expedition/(\d+)$',  views_logbooks.expedition,  name="expedition"),
    url(r'^personexpedition/(?P<first_name>[A-Z]*[a-z]*)[^a-zA-Z]*(?P<last_name>[A-Z]*[a-z]*)/(?P<year>\d+)/?$', views_logbooks.personexpedition, name="personexpedition"),
    url(r'^logbookentry/(?P<date>.*)/(?P<slug>.*)/?$', views_logbooks.logbookentry,name="logbookentry"),
    
    url(r'^survexblock/(.+)$',  views_caves.survexblock,    name="survexblock"),
    url(r'^cave/(?P<cave_id>[^/]+)/?$', views_caves.cave, name="cave"),
    #url(r'^cavehref/(.+)$',     views_caves.cave,       name="cave"),url(r'cave'),

    url(r'^jgtfile/(.*)$',      view_surveys.jgtfile,       name="jgtfile"),
    url(r'^jgtuploadfile$',     view_surveys.jgtuploadfile, name="jgtuploadfile"),
        
            
                
                    
                        
    url(r'^cave/(?P<cave_id>[^/]+)/?(?P<ent_letter>[^/])$', ent),
    #(r'^cave/(?P<cave_id>[^/]+)/edit/$', edit_cave),
    #(r'^cavesearch', caveSearch),
    url(r'^cave/(?P<cave_id>[^/]+)/(?P<subcave>[a-zA-Z/]+)/?$', subcave, name="subcave"),

    url(r'^survex/(.*?)\.index$', views_survex.index, name="survexindex"),
    
    url(r'^cave/(?P<cave_id>[^/]+)/(?P<year>\d\d\d\d)-(?P<qm_id>\d\d)(?P<grade>[ABCDX]?)?$', views_caves.qm, name="qm"),
    (r'^survex/(?P<survex_file>.*)\.svx$', svx),
    (r'^survex/(?P<survex_file>.*)\.3d$', threed),
    (r'^survex/(?P<survex_file>.*)\.log$', log),
    (r'^survex/(?P<survex_file>.*)\.err$', err),

    
    url(r'^logbooksearch/(.*)/?$', views_logbooks.logbookSearch),

        
    url(r'^statistics/?$', views_other.stats, name="stats"),
    
    url(r'^calendar/(?P<year>\d\d\d\d)/?$', views_other.calendar, name="calendar"),

    url(r'^survey/?$', surveyindex, name="survey"),
    url(r'^survey/(?P<year>\d\d\d\d)\#(?P<wallet_number>\d*)$', survey, name="survey"),

    url(r'^controlpanel/?$', views_other.controlPanel, name="survey"),

    (r'^admin/doc/?', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
    #url(r'^admin/', include(admin.site.urls),name="admin"),

    (r'^accounts/', include('registration.urls')),
    (r'^profiles/', include('profiles.urls')),
    
#    (r'^personform/(.*)$', personForm),

    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),

    (r'^survey_files/listdir/(?P<path>.*)$', view_surveys.listdir),
    (r'^survey_files/download/(?P<path>.*)$', view_surveys.download),
    #(r'^survey_files/upload/(?P<path>.*)$', view_surveys.upload),

    (r'^survey_scans/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.SURVEYS, 'show_indexes':True}),

    (r'^photos/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.PHOTOS_ROOT, 'show_indexes':True}),

    #url(r'^trip_report/?$',views_other.tripreport,name="trip_report")
)
