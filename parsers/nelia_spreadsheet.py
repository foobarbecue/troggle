from core.models import Cave, Entrance, CaveAndEntrance
from django.template.defaultfilters import slugify
from django.contrib.gis.geos import Point
import csv



def import_csv_simple(path):
    import_file_reader = csv.reader(open(path,'r'))
    header=import_file_reader.next()
    header = dict(zip(header, range(len(header))))
    
    for line in import_file_reader:
        
        newcave, created=Cave.objects.get_or_create(official_name='2000-wp'+line[header['GPS waypoint']])
        print str(newcave) + str(created)
        newcave.slug=slugify(newcave.official_name)
        newcave.save()
        if created:
            for n in range(1,4):
                ent_field='Entrance '+str(n)
                print line[header['Long']]
                print line[header['Lat']]
                newent=Entrance(name=ent_field, location=Point(-float(line[header['Long']]), float(line[header['Lat']]), srid=4326))
                newent.entrance_description=r'x entrance width (in):' + line[header[ent_field]]  + r'y entrance width (in):' + line[header[ent_field]+1] 
                newent.save()
                
                new_cave_n_ent=CaveAndEntrance(cave=newcave, entrance=newent, entrance_letter=chr(64+n))
                new_cave_n_ent.save()
                
            
        