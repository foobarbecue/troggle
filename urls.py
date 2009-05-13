from django.conf.urls.defaults import *
from expo.views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^cave/$', caveindex),
    (r'^cave/(?P<cave_id>[^/]+)/$', cave),
    (r'^cave/(?P<cave_id>[^/]+)/(?P<ent_letter>[^/]?)$', ent),
    
    (r'^survex/(?P<survex_file>.*)\.index$', index),
    (r'^survex/(?P<survex_file>.*)\.svx$', svx),
    (r'^survex/(?P<survex_file>.*)\.3d$', threed),
    (r'^survex/(?P<survex_file>.*)\.log$', log),
    (r'^survex/(?P<survex_file>.*)\.err$', err),

    (r'^person/$', personindex),
    (r'^person/(.*)$', person),

    (r'^logbookentry/(.*)$', logbookentry),
    
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),

    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'c:/expodjango/troggle/media/'}),

)
