from troggle.expo.models import *
from django.contrib import admin

class RoleInline(admin.TabularInline):
    model = PersonRole
    extra = 4

class SurvexBlockAdmin(admin.ModelAdmin):
    inlines = (RoleInline,)

class ScannedImageInline(admin.TabularInline):
    model = ScannedImage
    extra = 4

class SurveyAdmin(admin.ModelAdmin):
    inlines = (ScannedImageInline,)

class LogbookEntryAdmin(admin.ModelAdmin):
    search_fields = ('title','expedition__year')

class PersonAdmin(admin.ModelAdmin):
    search_fields = ('first_name','last_name')
    
class PersonExpeditionAdmin(admin.ModelAdmin):
    search_fields = ('person__first_name','expedition__year')

admin.site.register(Photo)
admin.site.register(Cave)
admin.site.register(Area)
admin.site.register(OtherCaveName)
admin.site.register(CaveAndEntrance)
admin.site.register(SurveyStation)
admin.site.register(Entrance)
admin.site.register(SurvexBlock, SurvexBlockAdmin)
admin.site.register(Expedition)
admin.site.register(Person,PersonAdmin)
admin.site.register(PersonRole)
admin.site.register(PersonExpedition,PersonExpeditionAdmin)
admin.site.register(Role)
admin.site.register(LogbookEntry, LogbookEntryAdmin)
admin.site.register(PersonTrip)
admin.site.register(QM)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(ScannedImage)

