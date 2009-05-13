from django.db import models

class SurvexBlock(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    parent = models.ForeignKey('SurvexBlock', blank=True, null=True)
    text = models.TextField()
    notes_person = models.ManyToManyField('PersonTrip', related_name="notes", blank=True, null=True)
    pics_person = models.ManyToManyField('PersonTrip', related_name="pics", blank=True, null=True)
    tape_person = models.ManyToManyField('PersonTrip', related_name="tape", blank=True, null=True)
    insts_person = models.ManyToManyField('PersonTrip', related_name="insts", blank=True, null=True)
    begin_file = models.CharField(max_length=200)
    begin_char = models.IntegerField()
    end_file = models.CharField(max_length=200, blank=True, null=True)
    end_char = models.IntegerField(blank=True, null=True)
    def __unicode__(self):
        return unicode(self.name)
