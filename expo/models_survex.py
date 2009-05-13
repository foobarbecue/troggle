from django.db import models

class SurvexBlock(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()
    notes_person = models.ManyToManyField('PersonTrip', related_name="notes")
    pics_person = models.ManyToManyField('PersonTrip', related_name="pics")
    tape_person = models.ManyToManyField('PersonTrip', related_name="tape")
    insts_person = models.ManyToManyField('PersonTrip', related_name="insts")
    begin_file = models.CharField(max_length=200)
    begin_char = models.IntegerField()
    end_file = models.CharField(max_length=200)
    end_char = models.IntegerField()
    def __unicode__(self):
        return unicode(name)
