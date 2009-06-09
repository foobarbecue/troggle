from troggle.expo.models import *
from django.contrib import admin
from feincms.admin import editor
from django.forms import ModelForm
import django.forms as forms
from expo.forms import LogbookEntryForm, QMsFoundInlineForm
from django.http import HttpResponse
from django.core import serializers
#from troggle.reversion.admin import VersionAdmin #django-reversion version control

#overriding admin save so we have the new since parsing field
class TroggleModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
	obj.new_since_parsing=True
	obj.save()

class RoleInline(admin.TabularInline):
    model = PersonRole
    extra = 4

class SurvexBlockAdmin(TroggleModelAdmin):
    inlines = (RoleInline,)

class ScannedImageInline(admin.TabularInline):
    model = ScannedImage
    extra = 4

class SurveyAdmin(TroggleModelAdmin):
    inlines = (ScannedImageInline,)
    search_fields = ('expedition__year','wallet_number')    

class QMsFoundInline(admin.TabularInline):
        #form=QMsFoundInlineForm
        model=QM
        fk_name='found_by'

class QMsTickedOffInline(admin.TabularInline):
        model=QM
        fk_name='ticked_off_by'

class PhotoInline(admin.TabularInline):
    model = Photo
    exclude = ['is_mugshot' ]
    extra = 1

class PersonTripInline(admin.TabularInline):
    model = PersonTrip
    exclude = ['persontrip_next','Delete']
    extra = 1

#class LogbookEntryAdmin(VersionAdmin):
class LogbookEntryAdmin(TroggleModelAdmin):
    prepopulated_fields = {'slug':("title",)}
    search_fields = ('title','expedition__year')
    date_heirarchy = ('date')
    inlines = (PersonTripInline, PhotoInline, QMsFoundInline, QMsTickedOffInline)
    form = LogbookEntryForm

class PersonExpeditionInline(admin.TabularInline):
    model = PersonExpedition
    extra = 1

class PersonAdmin(TroggleModelAdmin):
    search_fields = ('first_name','last_name')
    inlines = (PersonExpeditionInline,)

class QMAdmin(TroggleModelAdmin):
    search_fields = ('found_by__cave__kataster_number','number','found_by__date__year')
    list_display = ('__unicode__','grade','found_by','ticked_off_by')
    list_display_links = ('__unicode__',)
    list_editable = ('found_by','ticked_off_by','grade')
    list_per_page = 20

class PersonExpeditionAdmin(TroggleModelAdmin):
    search_fields = ('person__first_name','expedition__year')

class CaveAdmin(TroggleModelAdmin):
    search_fields = ('official_name','kataster_number','unofficial_number')
    #inlines = (QMInline,)
    extra = 4

class SubcaveAdmin(editor.TreeEditorMixin,TroggleModelAdmin):
    pass

admin.site.register(Photo)
admin.site.register(Subcave, SubcaveAdmin)
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
#admin.site.register(PersonTrip)
admin.site.register(QM, QMAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(ScannedImage)

def export_as_json(modeladmin, request, queryset):
    response = HttpResponse(mimetype="text/json")
    response['Content-Disposition'] = 'attachment; filename=troggle_output.json'
    serializers.serialize("json", queryset, stream=response)
    return response

def export_as_xml(modeladmin, request, queryset):
    response = HttpResponse(mimetype="text/xml")
    response['Content-Disposition'] = 'attachment; filename=troggle_output.xml'
    serializers.serialize("xml", queryset, stream=response)
    return response

admin.site.add_action(export_as_xml)
admin.site.add_action(export_as_json)

try:
    mptt.register(Subcave, order_insertion_by=['name'])
except mptt.AlreadyRegistered:
    print "mptt already registered"
