from django.db import models
from core.models import TroggleModel, LogbookEntry, Photo

class Sample(TroggleModel):
    name=models.CharField(max_length=10, blank=True, null=True)
    MATERIAL_CHOICES=(
        ('ice_core','Ice Core'),
        ('gas_bag','Gas sample in Teflon bag'),
        ('snow','Snow sample'),
        )
    material=models.CharField(max_length=100, choices=MATERIAL_CHOICES)
    description=models.TextField(blank=True, null=True)
    part_of=models.ForeignKey('Sample', blank=True, null=True)
    distance_from_bottom=models.IntegerField(blank=True, null=True)
    logbook_entry=models.ForeignKey(LogbookEntry, blank=True, null=True)
    d18O=models.FloatField(blank=True, null=True)
    d2H=models.FloatField(blank=True, null=True)
    length=models.FloatField(blank=True, null=True, help_text='In centimeters')
    photo=models.ForeignKey(Photo, blank=True, null=True)
    
    def __unicode__(self):
        return self.name
