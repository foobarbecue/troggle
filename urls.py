from django.conf.urls.defaults import *
import troggle.settings as settings

from expo.views import *  # flat import
from expo.views_caves import *
from expo.views_survex import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^$',              views_other.frontpage,      name="frontpage"),
    
    url(r'^caveindex$',     views_caves.caveindex,      name="caveindex"),
    url(r'^personindex$',   views_logbooks.personindex, name="personindex"),
    
    url(r'^person/(.+)$',       views_logbooks.person,      name="person"),
    url(r'^expedition/(\d+)$',  views_logbooks.expedition,  name="expedition"),
    url(r'^personexpedition/(.+?)/(\d+)$', views_logbooks.personexpedition, name="personexpedition"),
    url(r'^logbookentry/(.+)$', views_logbooks.logbookentry,name="logbookentry"),
    
    url(r'^survexblock/(.+)$',  views_caves.survexblock,    name="survexblock"),
    url(r'^cavehref/(.+)$',     views_caves.cavehref,       name="cave"),
    
    url(r'^jgtfile/(.*)$',      view_surveys.jgtfile,       name="jgtfile"),
    url(r'^jgtuploadfile$',     view_surveys.jgtuploadfile, name="jgtuploadfile"),
        
            
                
                    
                        
    (r'^cave/(?P<cave_id>[^/]+)/?(?P<ent_letter>[^/])$', ent),
    #(r'^cave/(?P<cave_id>[^/]+)/edit/$', edit_cave),
    (r'^cavesearch', caveSearch),
    url(r'^cavearea', caveArea, name="caveArea"),

    url(r'^survex/(.*?)\.index$', views_survex.index, name="survexindex"),
    url(r'^cave/(?P<cave_id>[^/]+)/?$', views_caves.cavehref), # deprecated
    (r'^survex/(?P<survex_file>.*)\.svx$', svx),
    (r'^survex/(?P<survex_file>.*)\.3d$', threed),
    (r'^survex/(?P<survex_file>.*)\.log$', log),
    (r'^survex/(?P<survex_file>.*)\.err$', err),

    
    url(r'^logbooksearch/(.*)/?$', views_logbooks.logbookSearch),

        
    url(r'^statistics/?$', views_other.stats, name="stats"),
    
    url(r'^calendar/(?P<year>\d\d\d\d)?$', views_other.calendar, name="calendar"),

    url(r'^survey/?$', surveyindex, name="survey"),
    (r'^survey/(?P<year>\d\d\d\d)\#(?P<wallet_number>\d*)$', survey),
    
    (r'^admin/doc/?', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),

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


)
