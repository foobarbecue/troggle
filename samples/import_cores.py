import csv, re
from samples.models import *

def import_core_segments():
    coresfile=open('/home/aaron/ms/erebus/crds results/cores.csv','r')
    coresreader=csv.reader(coresfile)
    coresreader.next()
    for row in coresreader:
        Sample.objects.get_or_create(name=row[0][0:3], defaults={'length':row[1], 'part_of':Sample.objects.get(pk=row[0][1])})

def import_CRDS_data():
    coresfile=open('/home/aaron/ms/erebus/crds results/samples.csv','r')
    coresreader=csv.reader(coresfile)
    coresfile.seek(0)
    coresreader.next()
    coresreader.next()

    for row in coresreader:
        try:
            parent, found=Sample.objects.get_or_create(name=row[1][0:2])
            Sample.objects.get_or_create(name=row[1], defaults={'distance_from_bottom':row[1][3:], 'part_of':parent, 'd18O':row[10],'d2H':row[11]})
            print 'added %s' % row
        except:
            print 'skipped %s' % row
