from django.conf.urls.defaults import *
from expo.views import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^troggle/cave/$', caveindex),
    (r'^troggle/cave/(?P<cave_id>[^/]+)/$', cave),
    (r'^troggle/cave/(?P<cave_id>[^/]+)/(?P<ent_letter>[^/]?)$', ent),
    
    (r'^troggle/survex/(?P<survex_file>.*)\.index$', index),
    (r'^troggle/survex/(?P<survex_file>.*)\.svx$', svx),
    (r'^troggle/survex/(?P<survex_file>.*)\.3d$', threed),
    (r'^troggle/survex/(?P<survex_file>.*)\.log$', log),
    (r'^troggle/survex/(?P<survex_file>.*)\.err$', err),

    (r'^person/$', personindex),
    (r'^person/(.*)$', person),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),

    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'c:/expodjango/troggle/media/'}),

)
