from django.forms import ModelForm
from models import Cave, Person, LogbookEntry, QM
import django.forms as forms
from django.forms.formsets import formset_factory
from django.contrib.admin.widgets import AdminDateWidget
import string
from datetime import date

class CaveForm(ModelForm):
    class Meta:
        model = Cave

class PersonForm(ModelForm):
    class Meta:
        model = Person

class LogbookEntryForm(ModelForm):
    class Meta:
        model = LogbookEntry

    def wikiLinkHints(LogbookEntry=None):
        """
        This function returns html-formatted paragraphs for each of the
        wikilink types that are related to this logbookentry. Each paragraph
        contains a list of all of the related wikilinks.
        
        Perhaps an admin javascript solution would be better.
        """
        res = ["Please use the following wikilinks, which are related to this logbook entry:"]
	
        res.append(r'</p><p style="float: left;"><b>QMs found:</b>')
	for QM in LogbookEntry.instance.QMs_found.all():
            res.append(QM.wiki_link())

        res.append(r'</p><p style="float: left;"><b>QMs ticked off:</b>')
	for QM in LogbookEntry.instance.QMs_ticked_off.all():
            res.append(QM.wiki_link())
	
#        res.append(r'</p><p style="float: left; "><b>People</b>')
#	for persontrip in LogbookEntry.instance.persontrip_set.all():
#            res.append(persontrip.wiki_link())
#	res.append(r'</p>')
	
	return string.join(res, r'<br />')

    def __init__(self, *args, **kwargs):
	super(LogbookEntryForm, self).__init__(*args, **kwargs)
        self.fields['text'].help_text=self.wikiLinkHints()