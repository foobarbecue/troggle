from django.db import models
from core.models import TroggleModel, LogbookEntry, Photo

class Sample(TroggleModel):
    name=models.CharField(max_length=10, blank=True, null=True)
    MATERIAL_CHOICES=(
        ('ice_core','Tower ice'),
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
    LEVEL_CHOICES=(('core','core'),('seg','core_segment'),('sample','sample'))
    level=models.CharField(max_length=100, choices=LEVEL_CHOICES, blank=True, null=True)

    class Meta:
        ordering = ('level', 'name')

    def __unicode__(self):
        return self.name

    def absolute_distance(self):
        if self.level=='sample':
            uncles=Sample.objects.filter(name__startswith=self.name[0:2], level='seg')
            abs_dist=0
            for each in uncles:
                if each == self.part_of:
                    break
                else:
                    if not each.length:
                        each.length=0
                    abs_dist=abs_dist+each.length
            abs_dist=abs_dist+self.distance_from_bottom
            return abs_dist
        
    def absolute_depth(self):
        depths=[]
        try:
            grandparent=self.part_of.part_of
            for sibling in Sample.objects.filter(part_of__part_of=grandparent):
                depths.append(sibling.absolute_distance())
            return max(depths)-self.absolute_distance()
        except:
            return None

