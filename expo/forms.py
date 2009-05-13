from django.forms import ModelForm
from models import Cave

class CaveForm(ModelForm):
    class Meta:
        model = Cave