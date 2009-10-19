from core.models import *
from django.contrib.gis import admin
from django.forms import ModelForm
import django.forms as forms
from django.http import HttpResponse
from django.core import serializers
from core.views_other import downloadLogbook
#from troggle.reversion.admin import VersionAdmin #django-reversion version control


class TroggleModelAdmin(admin.ModelAdmin):
    
    def save_model(self, request, obj, form, change):
        """overriding admin save to fill the new_since parsing_field"""
	obj.new_since_parsing=True
	obj.save()
    
    class Media:
        js = ('js/jquery.js','js/QM_helper.js')

class RoleInline(admin.TabularInline):
    model = SurvexPersonRole
    extra = 4

class SurvexBlockAdmin(TroggleModelAdmin):
    inlines = (RoleInline,)

class ScannedImageInline(admin.TabularInline):
    model = ScannedImage
    extra = 4

class OtherCaveInline(admin.TabularInline):
    model = OtherCaveName
    extra = 1

class SurveyAdmin(TroggleModelAdmin):
    inlines = (ScannedImageInline,)
    search_fields = ('expedition__year','wallet_number')    

class QMsFoundInline(admin.TabularInline):
    model=QM
    fk_name='found_by'
    fields=('number','grade','location_description','comment')#need to add foreignkey to cave part
    extra=1
    
class PhotoInline(admin.TabularInline):
    model = Photo
    exclude = ['is_mugshot' ]
    extra = 1

class PersonTripInline(admin.TabularInline):
    model = PersonTrip
    exclude = ['persontrip_next','Delete']
    raw_id_fields = ('personexpedition',)
    extra = 3

class SurveyInline(admin.TabularInline):
    model = Survey
    extra = 1

#class LogbookEntryAdmin(VersionAdmin):
class LogbookEntryAdmin(TroggleModelAdmin):
    prepopulated_fields = {'slug':("title",)}
    search_fields = ('title','expedition__year')
    date_heirarchy = ('date',)
    inlines = (PersonTripInline, SurveyInline, PhotoInline, 
QMsFoundInline)
    class Media:
        css = {
            "all": ("css/troggleadmin.css",)
        }
    actions=('export_logbook_entries_as_html','export_logbook_entries_as_txt')
    
    def export_logbook_entries_as_html(modeladmin, request, queryset):
        response=downloadLogbook(request=request, queryset=queryset, extension='html')
        return response
        
    def export_logbook_entries_as_txt(modeladmin, request, queryset):
        response=downloadLogbook(request=request, queryset=queryset, extension='txt')
        return response
    
    

class PersonExpeditionInline(admin.TabularInline):
    model = PersonExpedition
    extra = 1

class ExpeditionAdmin(TroggleModelAdmin):
    inlines = (PersonExpeditionInline,)

class PersonAdmin(TroggleModelAdmin):
    search_fields = ('first_name','last_name')
    inlines = (PersonExpeditionInline,)

class QMAdmin(TroggleModelAdmin):
    search_fields = ('found_by__cave__kataster_number','number','found_by__date')
    list_display = ('__unicode__','grade','found_by','ticked_off_by')
    list_display_links = ('__unicode__',)
    list_editable = ('found_by','ticked_off_by','grade')
    list_per_page = 20
    raw_id_fields=('found_by','ticked_off_by')

class PersonExpeditionAdmin(TroggleModelAdmin):
    search_fields = ('person__first_name','expedition__year')

class CaveAndEntranceInline(admin.TabularInline):
    model = CaveAndEntrance
    extra = 3

class CaveAdmin(TroggleModelAdmin):
    search_fields = ('official_name','kataster_number','unofficial_number')
    fields = ('official_name','type','underground_description','equipment','area','slug')
    inlines = (OtherCaveInline, CaveAndEntranceInline, PhotoInline,)
    prepopulated_fields = {'slug':("official_name",)}
    extra = 4

class EntranceAdmin(admin.GeoModelAdmin):
    search_fields = ('caveandentrance__cave__kataster_number','')
    fields = ('entrance_description','name','location')
    display_wkt = True
    inlines = (CaveAndEntranceInline,)

class PhotoAdmin(admin.GeoModelAdmin):
    display_wkt = True
    exclude=('location')
    prepopulated_fields = {'slug':("caption",)}
    
class AreaAdmin(TroggleModelAdmin):
    prepopulated_fields = {'slug':("name",)}

admin.site.register(Photo, PhotoAdmin)
admin.site.register(Cave, CaveAdmin)
admin.site.register(Area, AreaAdmin)
#admin.site.register(OtherCaveName)
#admin.site.register(CaveAndEntrance)
#admin.site.register(SurveyStation)
#admin.site.register(NewSubCave)
#admin.site.register(CaveDescription)
admin.site.register(Entrance, EntranceAdmin)
#admin.site.register(SurvexBlock, SurvexBlockAdmin)
admin.site.register(Expedition,ExpeditionAdmin)
admin.site.register(Person,PersonAdmin)
#admin.site.register(SurvexPersonRole)
admin.site.register(PersonExpedition,PersonExpeditionAdmin)
admin.site.register(LogbookEntry, LogbookEntryAdmin)
#admin.site.register(PersonTrip)
admin.site.register(QM, QMAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(ScannedImage)

#admin.site.register(SurvexScansFolder)
#admin.site.register(SurvexScanSingle)

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
