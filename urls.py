from django.conf.urls.defaults import *
from expo.views import *
import expo.view_surveys as view_surveys
import troggle.settings as settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    (r'^$', frontPage),
    (r'^cave/?$', caveindex),
    (r'^cave/(?P<cave_id>[^/]+)/?$', cave),
    (r'^cave/(?P<cave_id>[^/]+)/?(?P<ent_letter>[^/])$', ent),
    #(r'^cave/(?P<cave_id>[^/]+)/edit/$', edit_cave),
    (r'^cavesearch', caveSearch),

    (r'^survex/(?P<survex_file>.*)\.index$', index),
    (r'^survex/(?P<survex_file>.*)\.svx$', svx),
    (r'^survex/(?P<survex_file>.*)\.3d$', threed),
    (r'^survex/(?P<survex_file>.*)\.log$', log),
    (r'^survex/(?P<survex_file>.*)\.err$', err),

    url(r'^personindex$', personindex, name="personindex"),
    (r'^person/(?P<person_id>\d*)(?P<first_name>[a-zA-Z]*)[-_/\.\s(\%20)]*(?P<last_name>[a-zA-Z]*)/?$', person),

    (r'^logbookentry/(.*)/?$', logbookentry),
    url(r'^logbooksearch/(.*)/?$', logbookSearch),
    
    url(r'^statistics/?$', stats, name="stats"),
    
    (r'^survey/?$', surveyindex),
    (r'^survey/(?P<year>\d\d\d\d)\#(?P<wallet_number>\d*)$', survey),
    
    (r'^admin/doc/?', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),

    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),

    (r'^survey_files/listdir/(?P<path>.*)$', view_surveys.listdir),
    (r'^survey_files/download/(?P<path>.*)$', view_surveys.download),
    #(r'^survey_files/upload/(?P<path>.*)$', view_surveys.upload),

    (r'^survey_scans/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.SURVEYS, 'show_indexes':True}),


)
