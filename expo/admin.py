from troggle.expo.models import *
from django.contrib import admin
from django.forms import ModelForm
import django.forms as forms
#from troggle.reversion.admin import VersionAdmin #django-reversion version control

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

class QMInline(admin.TabularInline):
	model=QM
	extra = 4

#class LogbookEntryAdmin(VersionAdmin):
class LogbookEntryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':("title",)}
    search_fields = ('title','expedition__year')
    #inlines = (QMInline,) #doesn't work because QM has two foreignkeys to Logbookentry- need workaround

class PersonExpeditionInline(admin.TabularInline):
    model = PersonExpedition
    extra = 1

class PersonAdmin(admin.ModelAdmin):
    search_fields = ('first_name','last_name')
    inlines = (PersonExpeditionInline,)

class QMAdmin(admin.ModelAdmin):
    search_fields = ('found_by__cave__kataster_number','number')
    def save_model(self, request, obj, form, change):
	obj.new_since_parsing=True
	obj.save()

class PersonExpeditionAdmin(admin.ModelAdmin):
    search_fields = ('person__first_name','expedition__year')

class CaveAdmin(admin.ModelAdmin):
    search_fields = ('official_name','kataster_number','unofficial_number')
    #inlines = (QMInline,)
    extra = 4



admin.site.register(Photo)
admin.site.register(Cave, CaveAdmin)
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
admin.site.register(QM, QMAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(ScannedImage)

