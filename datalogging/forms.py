from django import forms
from datalogging.models import Timeseries

class TimeseriesDataForm(forms.Form):
    timeseries=forms.ModelChoiceField(queryset=Timeseries.objects.all())
    start_time=forms.DateTimeField(required=False,)
    end_time=forms.DateTimeField(required=False,)
    number_of_samples=forms.IntegerField(
        required=False,
        help_text="<span class='helptext'>Leave blank to load all samples. Entering a smaller number of than the database contains will resample the data using fast Fourier methods.</span>")
    FORMAT_CHOICES=(('JSON','Add to chart'),('csv','Download .csv table'),('matlab','Download Matlab .mat data file'),('newpage','Autoload'),('stats','Load statistics'))
    action=forms.ChoiceField(choices=FORMAT_CHOICES)
