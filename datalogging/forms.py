from django import forms
from datalogging.models import Timeseries

class TimeseriesDataForm(forms.Form):
    timeseries=forms.ModelChoiceField(queryset=Timeseries.objects.all())
    start_time=forms.DateTimeField()
    end_time=forms.DateTimeField()
    number_of_samples=forms.IntegerField()
    FORMAT_CHOICES=(('JSON','Add to chart'),('csv','Download .csv table'),('matlab','Download Matlab .mat data file'),('newpage','Autoload'))
    action=forms.ChoiceField(choices=FORMAT_CHOICES)
