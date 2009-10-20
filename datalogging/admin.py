from datalogging.models import *
from django.contrib.gis import admin

def import_datapoints_from_plain_csv(modeladmin, request, queryset):
    for timeseries in queryset:
        timeseries.import_csv_simple()


class TimeseriesAdmin(admin.ModelAdmin):
    actions=[import_datapoints_from_plain_csv]

admin.site.register(Manufacturer)
admin.site.register(EquipmentType)
admin.site.register(EquipmentItem)
admin.site.register(Timeseries, TimeseriesAdmin)
admin.site.register(DataPoint)