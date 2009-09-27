from datalogging.models import *
from django.contrib.gis import admin

admin.site.register(Manufacturer)
admin.site.register(EquipmentType)
admin.site.register(EquipmentItem)
admin.site.register(Timeseries)
admin.site.register(DataPoint)