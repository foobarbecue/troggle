from samples.models import *
from django.contrib import admin

def absolute_distance(obj):
    return obj.absolute_distance()

def absolute_depth(obj):
    return obj.absolute_depth()

class SampleAdmin(admin.ModelAdmin):
    list_display=('name','length','level','distance_from_bottom',absolute_distance, absolute_depth)
    list_editable=('length','distance_from_bottom','level')

admin.site.register(Sample, SampleAdmin)
