from troggle.expo.models import *
from django.contrib import admin

class RoleInline(admin.TabularInline):
    model = PersonRole
    extra = 4

class SurvexBlockAdmin(admin.ModelAdmin):
    inlines = (RoleInline,)


admin.site.register(Cave)
admin.site.register(Area)
admin.site.register(OtherCaveName)
admin.site.register(CaveAndEntrance)
admin.site.register(SurveyStation)
admin.site.register(Entrance)
admin.site.register(SurvexBlock, SurvexBlockAdmin)
admin.site.register(Expedition)
admin.site.register(Person)
admin.site.register(PersonRole)
admin.site.register(PersonExpedition)
admin.site.register(Role)
admin.site.register(LogbookEntry)
admin.site.register(PersonTrip)
admin.site.register(QM)
