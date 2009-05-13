from django.forms import ModelForm
from models import Cave, Person

class CaveForm(ModelForm):
    class Meta:
        model = Cave

class PersonForm(ModelForm):
    class Meta:
        model = Person