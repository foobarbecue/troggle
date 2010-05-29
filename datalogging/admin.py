from datalogging.models import *
from django.contrib.gis import admin

def import_datapoints_from_plain_csv(modeladmin, request, queryset):
    for timeseries in queryset:
        timeseries.import_csv_simple()

def timeseries_stats(ts):
    return '%s, from %s to %s' % (len(ts.data()), ts.data().latest().time, ts.data().reverse().latest().time)

class TimeseriesAdmin(admin.ModelAdmin):
    actions=[import_datapoints_from_plain_csv]
    list_display=('id', timeseries_stats, 'start_time', 'end_time', 'cave', 'data_type', 'location_in_cave', 'notes')
    list_editable=('start_time', 'end_time', 'location_in_cave', 'notes')

class DataPointAdmin(admin.ModelAdmin):
    date_hierarchy = 'time'
    list_filter=('parent_timeseries',)

admin.site.register(Manufacturer)
admin.site.register(EquipmentType)
admin.site.register(EquipmentItem)
admin.site.register(Timeseries, TimeseriesAdmin)
admin.site.register(DataPoint, DataPointAdmin)
admin.site.register(DataAquisitionSystem)

