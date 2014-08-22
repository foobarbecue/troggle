# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Cave.protection_category'
        db.add_column('core_cave', 'protection_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.ProtectionCategory'], null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Cave.protection_category'
        db.delete_column('core_cave', 'protection_category_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.area': {
            'Meta': {'object_name': 'Area'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Area']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        },
        'core.cave': {
            'Meta': {'ordering': "['-official_name']", 'object_name': 'Cave'},
            'area': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Area']", 'null': 'True', 'blank': 'True'}),
            'depth': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'description_file': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'equipment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'explorers': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'extent': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kataster_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'kataster_status': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'length': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'official_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '160'}),
            'protection_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ProtectionCategory']", 'null': 'True', 'blank': 'True'}),
            'references': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'survex_file': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'survey': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'underground_centre_line': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'underground_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'unofficial_number': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'})
        },
        'core.caveandentrance': {
            'Meta': {'object_name': 'CaveAndEntrance'},
            'cave': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Cave']"}),
            'entrance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Entrance']"}),
            'entrance_letter': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'core.cavedescription': {
            'Meta': {'object_name': 'CaveDescription'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linked_entrances': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Entrance']", 'null': 'True', 'blank': 'True'}),
            'linked_qms': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.QM']", 'null': 'True', 'blank': 'True'}),
            'linked_subcaves': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.NewSubCave']", 'null': 'True', 'blank': 'True'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'short_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'core.entrance': {
            'Meta': {'ordering': "['caveandentrance__cave']", 'object_name': 'Entrance'},
            'approach': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'bearings': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'entrance_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'equipment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'exact_station': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'exact_station'", 'null': 'True', 'to': "orm['core.SurveyStation']"}),
            'explorers': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'findability': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'findability_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'location_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'map_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'marking': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'marking_comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'other_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'other_station': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'other_station'", 'null': 'True', 'to': "orm['core.SurveyStation']"}),
            'photo': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tag_station': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tag_station'", 'null': 'True', 'to': "orm['core.SurveyStation']"}),
            'underground_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'core.expedition': {
            'Meta': {'ordering': "('-year',)", 'object_name': 'Expedition'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'year': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        'core.logbookentry': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'LogbookEntry'},
            'cave': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Cave']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'expedition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Expedition']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'core.newsubcave': {
            'Meta': {'object_name': 'NewSubCave'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'core.othercavename': {
            'Meta': {'object_name': 'OtherCaveName'},
            'cave': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Cave']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'core.person': {
            'Meta': {'ordering': "('last_name', 'first_name')", 'object_name': 'Person'},
            'affiliation': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'blurb': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'core.personexpedition': {
            'Meta': {'ordering': "('-expedition',)", 'object_name': 'PersonExpedition'},
            'expedition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Expedition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_guest': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Person']"}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'core.persontrip': {
            'Meta': {'object_name': 'PersonTrip'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_logbook_entry_author': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'logbook_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.LogbookEntry']"}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'personexpedition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.PersonExpedition']", 'null': 'True'}),
            'time_underground': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'core.photo': {
            'Meta': {'object_name': 'Photo'},
            'caption': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contains_cave': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Cave']", 'null': 'True', 'blank': 'True'}),
            'contains_entrance': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'photo_file'", 'null': 'True', 'to': "orm['core.Entrance']"}),
            'contains_logbookentry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.LogbookEntry']", 'null': 'True', 'blank': 'True'}),
            'contains_person': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Person']", 'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_mugshot': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'nearest_QM': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.QM']", 'null': 'True', 'blank': 'True'}),
            'nearest_survey_point': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SurveyStation']", 'null': 'True', 'blank': 'True'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'taken_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'photographer'", 'null': 'True', 'to': "orm['core.Person']"})
        },
        'core.protectioncategory': {
            'Meta': {'object_name': 'ProtectionCategory'},
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '1', 'primary_key': 'True'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'core.qm': {
            'Meta': {'object_name': 'QM'},
            'area': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'completion_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'found_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'QMs_found'", 'null': 'True', 'to': "orm['core.LogbookEntry']"}),
            'grade': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'nearest_station': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'nearest_station_description': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'ticked_off_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'QMs_ticked_off'", 'null': 'True', 'to': "orm['core.LogbookEntry']"})
        },
        'core.scannedimage': {
            'Meta': {'object_name': 'ScannedImage'},
            'contents': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number_in_wallet': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'scanned_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Person']", 'null': 'True', 'blank': 'True'}),
            'scanned_on': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Survey']"})
        },
        'core.survexblock': {
            'Meta': {'ordering': "('id',)", 'object_name': 'SurvexBlock'},
            'begin_char': ('django.db.models.fields.IntegerField', [], {}),
            'cave': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Cave']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'expedition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Expedition']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SurvexBlock']", 'null': 'True', 'blank': 'True'}),
            'survexfile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SurvexFile']", 'null': 'True', 'blank': 'True'}),
            'survexpath': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'survexscansfolder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SurvexScansFolder']", 'null': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'totalleglength': ('django.db.models.fields.FloatField', [], {})
        },
        'core.survexdirectory': {
            'Meta': {'ordering': "('id',)", 'object_name': 'SurvexDirectory'},
            'cave': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Cave']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'primarysurvexfile': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'primarysurvexfile'", 'null': 'True', 'to': "orm['core.SurvexFile']"})
        },
        'core.survexequate': {
            'Meta': {'object_name': 'SurvexEquate'},
            'cave': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Cave']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'core.survexfile': {
            'Meta': {'ordering': "('id',)", 'object_name': 'SurvexFile'},
            'cave': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Cave']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'survexdirectory': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SurvexDirectory']", 'null': 'True', 'blank': 'True'})
        },
        'core.survexleg': {
            'Meta': {'object_name': 'SurvexLeg'},
            'block': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SurvexBlock']"}),
            'clino': ('django.db.models.fields.FloatField', [], {}),
            'compass': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stationfrom': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stationfrom'", 'to': "orm['core.SurvexStation']"}),
            'stationto': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stationto'", 'to': "orm['core.SurvexStation']"}),
            'tape': ('django.db.models.fields.FloatField', [], {})
        },
        'core.survexpersonrole': {
            'Meta': {'object_name': 'SurvexPersonRole'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nrole': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Person']", 'null': 'True', 'blank': 'True'}),
            'personexpedition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.PersonExpedition']", 'null': 'True', 'blank': 'True'}),
            'personname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'persontrip': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.PersonTrip']", 'null': 'True', 'blank': 'True'}),
            'survexblock': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SurvexBlock']"})
        },
        'core.survexscansfolder': {
            'Meta': {'ordering': "('walletname',)", 'object_name': 'SurvexScansFolder'},
            'fpath': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'walletname': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'core.survexscansingle': {
            'Meta': {'ordering': "('name',)", 'object_name': 'SurvexScanSingle'},
            'ffile': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'survexscansfolder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SurvexScansFolder']", 'null': 'True'})
        },
        'core.survexstation': {
            'Meta': {'object_name': 'SurvexStation'},
            'block': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SurvexBlock']"}),
            'equate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SurvexEquate']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'core.survextitle': {
            'Meta': {'object_name': 'SurvexTitle'},
            'cave': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Cave']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'survexblock': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.SurvexBlock']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'core.survey': {
            'Meta': {'object_name': 'Survey'},
            'centreline_printed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'centreline_printed_by'", 'null': 'True', 'to': "orm['core.Person']"}),
            'centreline_printed_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'expedition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Expedition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'integrated_into_main_sketch_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'integrated_into_main_sketch_by'", 'null': 'True', 'to': "orm['core.Person']"}),
            'integrated_into_main_sketch_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'logbook_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.LogbookEntry']"}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subcave': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.NewSubCave']", 'null': 'True', 'blank': 'True'}),
            'survex_block': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.SurvexBlock']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'tunnel_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tunnel_main_sketch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Survey']", 'null': 'True', 'blank': 'True'}),
            'wallet_letter': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'wallet_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'core.surveystation': {
            'Meta': {'object_name': 'SurveyStation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'new_since_parsing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'non_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'core.tunnelfile': {
            'Meta': {'ordering': "('tunnelpath',)", 'object_name': 'TunnelFile'},
            'bfontcolours': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'filesize': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'npaths': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'survexblocks': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.SurvexBlock']", 'symmetrical': 'False'}),
            'survexscans': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.SurvexScanSingle']", 'symmetrical': 'False'}),
            'survexscansfolders': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.SurvexScansFolder']", 'symmetrical': 'False'}),
            'survextitles': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.SurvexTitle']", 'symmetrical': 'False'}),
            'tunnelcontains': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.TunnelFile']", 'symmetrical': 'False'}),
            'tunnelname': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tunnelpath': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['core']
