# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SurvexDirectory'
        db.create_table('core_survexdirectory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('cave', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Cave'], null=True, blank=True)),
            ('primarysurvexfile', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='primarysurvexfile', null=True, to=orm['core.SurvexFile'])),
        ))
        db.send_create_signal('core', ['SurvexDirectory'])

        # Adding model 'SurvexFile'
        db.create_table('core_survexfile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('survexdirectory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.SurvexDirectory'], null=True, blank=True)),
            ('cave', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Cave'], null=True, blank=True)),
        ))
        db.send_create_signal('core', ['SurvexFile'])

        # Adding model 'SurvexEquate'
        db.create_table('core_survexequate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cave', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Cave'], null=True, blank=True)),
        ))
        db.send_create_signal('core', ['SurvexEquate'])

        # Adding model 'SurvexStation'
        db.create_table('core_survexstation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('block', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.SurvexBlock'])),
            ('equate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.SurvexEquate'], null=True, blank=True)),
        ))
        db.send_create_signal('core', ['SurvexStation'])

        # Adding model 'SurvexLeg'
        db.create_table('core_survexleg', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('block', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.SurvexBlock'])),
            ('stationfrom', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stationfrom', to=orm['core.SurvexStation'])),
            ('stationto', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stationto', to=orm['core.SurvexStation'])),
            ('tape', self.gf('django.db.models.fields.FloatField')()),
            ('compass', self.gf('django.db.models.fields.FloatField')()),
            ('clino', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('core', ['SurvexLeg'])

        # Adding model 'SurvexBlock'
        db.create_table('core_survexblock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.SurvexBlock'], null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('cave', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Cave'], null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('expedition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Expedition'], null=True, blank=True)),
            ('survexfile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.SurvexFile'], null=True, blank=True)),
            ('begin_char', self.gf('django.db.models.fields.IntegerField')()),
            ('survexpath', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('survexscansfolder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.SurvexScansFolder'], null=True)),
            ('totalleglength', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('core', ['SurvexBlock'])

        # Adding model 'SurvexTitle'
        db.create_table('core_survextitle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('survexblock', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.SurvexBlock'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('cave', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Cave'], null=True, blank=True)),
        ))
        db.send_create_signal('core', ['SurvexTitle'])

        # Adding model 'SurvexPersonRole'
        db.create_table('core_survexpersonrole', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('survexblock', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.SurvexBlock'])),
            ('nrole', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('personname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Person'], null=True, blank=True)),
            ('personexpedition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.PersonExpedition'], null=True, blank=True)),
            ('persontrip', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.PersonTrip'], null=True, blank=True)),
        ))
        db.send_create_signal('core', ['SurvexPersonRole'])

        # Adding model 'SurvexScansFolder'
        db.create_table('core_survexscansfolder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fpath', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('walletname', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('core', ['SurvexScansFolder'])

        # Adding model 'SurvexScanSingle'
        db.create_table('core_survexscansingle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ffile', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('survexscansfolder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.SurvexScansFolder'], null=True)),
        ))
        db.send_create_signal('core', ['SurvexScanSingle'])

        # Adding model 'TunnelFile'
        db.create_table('core_tunnelfile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tunnelpath', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('tunnelname', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('bfontcolours', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('filesize', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('npaths', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('core', ['TunnelFile'])

        # Adding M2M table for field survexscansfolders on 'TunnelFile'
        db.create_table('core_tunnelfile_survexscansfolders', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tunnelfile', models.ForeignKey(orm['core.tunnelfile'], null=False)),
            ('survexscansfolder', models.ForeignKey(orm['core.survexscansfolder'], null=False))
        ))
        db.create_unique('core_tunnelfile_survexscansfolders', ['tunnelfile_id', 'survexscansfolder_id'])

        # Adding M2M table for field survexscans on 'TunnelFile'
        db.create_table('core_tunnelfile_survexscans', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tunnelfile', models.ForeignKey(orm['core.tunnelfile'], null=False)),
            ('survexscansingle', models.ForeignKey(orm['core.survexscansingle'], null=False))
        ))
        db.create_unique('core_tunnelfile_survexscans', ['tunnelfile_id', 'survexscansingle_id'])

        # Adding M2M table for field survexblocks on 'TunnelFile'
        db.create_table('core_tunnelfile_survexblocks', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tunnelfile', models.ForeignKey(orm['core.tunnelfile'], null=False)),
            ('survexblock', models.ForeignKey(orm['core.survexblock'], null=False))
        ))
        db.create_unique('core_tunnelfile_survexblocks', ['tunnelfile_id', 'survexblock_id'])

        # Adding M2M table for field tunnelcontains on 'TunnelFile'
        db.create_table('core_tunnelfile_tunnelcontains', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_tunnelfile', models.ForeignKey(orm['core.tunnelfile'], null=False)),
            ('to_tunnelfile', models.ForeignKey(orm['core.tunnelfile'], null=False))
        ))
        db.create_unique('core_tunnelfile_tunnelcontains', ['from_tunnelfile_id', 'to_tunnelfile_id'])

        # Adding M2M table for field survextitles on 'TunnelFile'
        db.create_table('core_tunnelfile_survextitles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tunnelfile', models.ForeignKey(orm['core.tunnelfile'], null=False)),
            ('survextitle', models.ForeignKey(orm['core.survextitle'], null=False))
        ))
        db.create_unique('core_tunnelfile_survextitles', ['tunnelfile_id', 'survextitle_id'])

        # Adding model 'Expedition'
        db.create_table('core_expedition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('new_since_parsing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('non_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('year', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('core', ['Expedition'])

        # Adding model 'Person'
        db.create_table('core_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('new_since_parsing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('non_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('affiliation', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('blurb', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal('core', ['Person'])

        # Adding model 'PersonExpedition'
        db.create_table('core_personexpedition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('new_since_parsing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('non_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('expedition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Expedition'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Person'])),
            ('is_guest', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('core', ['PersonExpedition'])

        # Adding model 'LogbookEntry'
        db.create_table('core_logbookentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('new_since_parsing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('non_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('expedition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Expedition'], null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('cave', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Cave'], null=True, blank=True)),
            ('place', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('core', ['LogbookEntry'])

        # Adding model 'PersonTrip'
        db.create_table('core_persontrip', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('new_since_parsing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('non_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('personexpedition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.PersonExpedition'], null=True)),
            ('time_underground', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('logbook_entry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.LogbookEntry'])),
            ('is_logbook_entry_author', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('core', ['PersonTrip'])

        # Adding model 'Area'
        db.create_table('core_area', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('new_since_parsing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('non_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Area'], null=True, blank=True)),
        ))
        db.send_create_signal('core', ['Area'])

        # Adding model 'CaveAndEntrance'
        db.create_table('core_caveandentrance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('new_since_parsing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('non_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cave', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Cave'])),
            ('entrance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Entrance'])),
            ('entrance_letter', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal('core', ['CaveAndEntrance'])

        # Adding model 'ProtectionCategory'
        db.create_table('core_protectioncategory', (
            ('new_since_parsing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('non_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=1, primary_key=True)),
        ))
        db.send_create_signal('core', ['ProtectionCategory'])

        # Adding model 'Cave'
        db.create_table('core_cave', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('new_since_parsing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('non_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('official_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=160)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('kataster_code', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('unofficial_number', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('explorers', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('underground_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('equipment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('references', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('survey', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('kataster_status', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('underground_centre_line', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('length', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('depth', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('extent', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('survex_file', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('description_file', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('core', ['Cave'])

        # Adding M2M table for field area on 'Cave'
        db.create_table('core_cave_area', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cave', models.ForeignKey(orm['core.cave'], null=False)),
            ('area', models.ForeignKey(orm['core.area'], null=False))
        ))
        db.create_unique('core_cave_area', ['cave_id', 'area_id'])

        # Adding model 'OtherCaveName'
        db.create_table('core_othercavename', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('new_since_parsing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('non_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=160)),
            ('cave', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Cave'])),
        ))
        db.send_create_signal('core', ['OtherCaveName'])

        # Adding model 'SurveyStation'
        db.create_table('core_surveystation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('new_since_parsing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('non_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('core', ['SurveyStation'])

        # Adding model 'Entrance'
        db.create_table('core_entrance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('new_since_parsing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('non_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('entrance_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('explorers', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('map_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('location_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('equipment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('approach', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('underground_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('photo', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('marking', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('marking_comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('findability', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('findability_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('tag_station', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tag_station', null=True, to=orm['core.SurveyStation'])),
            ('exact_station', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='exact_station', null=True, to=orm['core.SurveyStation'])),
            ('other_station', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='other_station', null=True, to=orm['core.SurveyStation'])),
            ('other_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('bearings', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('core', ['Entrance'])

        # Adding model 'CaveDescription'
        db.create_table('core_cavedescription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('new_since_parsing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('non_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('short_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('long_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('core', ['CaveDescription'])

        # Adding M2M table for field linked_subcaves on 'CaveDescription'
        db.create_table('core_cavedescription_linked_subcaves', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cavedescription', models.ForeignKey(orm['core.cavedescription'], null=False)),
            ('newsubcave', models.ForeignKey(orm['core.newsubcave'], null=False))
        ))
        db.create_unique('core_cavedescription_linked_subcaves', ['cavedescription_id', 'newsubcave_id'])

        # Adding M2M table for field linked_entrances on 'CaveDescription'
        db.create_table('core_cavedescription_linked_entrances', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cavedescription', models.ForeignKey(orm['core.cavedescription'], null=False)),
            ('entrance', models.ForeignKey(orm['core.entrance'], null=False))
        ))
        db.create_unique('core_cavedescription_linked_entrances', ['cavedescription_id', 'entrance_id'])

        # Adding M2M table for field linked_qms on 'CaveDescription'
        db.create_table('core_cavedescription_linked_qms', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('cavedescription', models.ForeignKey(orm['core.cavedescription'], null=False)),
            ('qm', models.ForeignKey(orm['core.qm'], null=False))
        ))
        db.create_unique('core_cavedescription_linked_qms', ['cavedescription_id', 'qm_id'])

        # Adding model 'NewSubCave'
        db.create_table('core_newsubcave', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('new_since_parsing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('non_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
        ))
        db.send_create_signal('core', ['NewSubCave'])

        # Adding model 'QM'
        db.create_table('core_qm', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('new_since_parsing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('non_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('found_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='QMs_found', null=True, to=orm['core.LogbookEntry'])),
            ('ticked_off_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='QMs_ticked_off', null=True, to=orm['core.LogbookEntry'])),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('grade', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('location_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('nearest_station_description', self.gf('django.db.models.fields.CharField')(max_length=400, null=True, blank=True)),
            ('nearest_station', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('area', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('completion_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('core', ['QM'])

        # Adding model 'Photo'
        db.create_table('core_photo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('new_since_parsing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('file', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('caption', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('contains_logbookentry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.LogbookEntry'], null=True, blank=True)),
            ('is_mugshot', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('contains_cave', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Cave'], null=True, blank=True)),
            ('contains_entrance', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='photo_file', null=True, to=orm['core.Entrance'])),
            ('nearest_survey_point', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.SurveyStation'], null=True, blank=True)),
            ('nearest_QM', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.QM'], null=True, blank=True)),
            ('taken_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='photographer', null=True, to=orm['core.Person'])),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
        ))
        db.send_create_signal('core', ['Photo'])

        # Adding M2M table for field contains_person on 'Photo'
        db.create_table('core_photo_contains_person', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('photo', models.ForeignKey(orm['core.photo'], null=False)),
            ('person', models.ForeignKey(orm['core.person'], null=False))
        ))
        db.create_unique('core_photo_contains_person', ['photo_id', 'person_id'])

        # Adding model 'ScannedImage'
        db.create_table('core_scannedimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('new_since_parsing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('file', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('scanned_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Person'], null=True, blank=True)),
            ('scanned_on', self.gf('django.db.models.fields.DateField')(null=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Survey'])),
            ('contents', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('number_in_wallet', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('core', ['ScannedImage'])

        # Adding model 'Survey'
        db.create_table('core_survey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('new_since_parsing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('non_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('expedition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Expedition'])),
            ('wallet_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('wallet_letter', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=400, null=True, blank=True)),
            ('subcave', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.NewSubCave'], null=True, blank=True)),
            ('survex_block', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.SurvexBlock'], unique=True, null=True, blank=True)),
            ('logbook_entry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.LogbookEntry'])),
            ('centreline_printed_on', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('centreline_printed_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='centreline_printed_by', null=True, to=orm['core.Person'])),
            ('tunnel_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('tunnel_main_sketch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Survey'], null=True, blank=True)),
            ('integrated_into_main_sketch_on', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('integrated_into_main_sketch_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='integrated_into_main_sketch_by', null=True, to=orm['core.Person'])),
        ))
        db.send_create_signal('core', ['Survey'])


    def backwards(self, orm):
        
        # Deleting model 'SurvexDirectory'
        db.delete_table('core_survexdirectory')

        # Deleting model 'SurvexFile'
        db.delete_table('core_survexfile')

        # Deleting model 'SurvexEquate'
        db.delete_table('core_survexequate')

        # Deleting model 'SurvexStation'
        db.delete_table('core_survexstation')

        # Deleting model 'SurvexLeg'
        db.delete_table('core_survexleg')

        # Deleting model 'SurvexBlock'
        db.delete_table('core_survexblock')

        # Deleting model 'SurvexTitle'
        db.delete_table('core_survextitle')

        # Deleting model 'SurvexPersonRole'
        db.delete_table('core_survexpersonrole')

        # Deleting model 'SurvexScansFolder'
        db.delete_table('core_survexscansfolder')

        # Deleting model 'SurvexScanSingle'
        db.delete_table('core_survexscansingle')

        # Deleting model 'TunnelFile'
        db.delete_table('core_tunnelfile')

        # Removing M2M table for field survexscansfolders on 'TunnelFile'
        db.delete_table('core_tunnelfile_survexscansfolders')

        # Removing M2M table for field survexscans on 'TunnelFile'
        db.delete_table('core_tunnelfile_survexscans')

        # Removing M2M table for field survexblocks on 'TunnelFile'
        db.delete_table('core_tunnelfile_survexblocks')

        # Removing M2M table for field tunnelcontains on 'TunnelFile'
        db.delete_table('core_tunnelfile_tunnelcontains')

        # Removing M2M table for field survextitles on 'TunnelFile'
        db.delete_table('core_tunnelfile_survextitles')

        # Deleting model 'Expedition'
        db.delete_table('core_expedition')

        # Deleting model 'Person'
        db.delete_table('core_person')

        # Deleting model 'PersonExpedition'
        db.delete_table('core_personexpedition')

        # Deleting model 'LogbookEntry'
        db.delete_table('core_logbookentry')

        # Deleting model 'PersonTrip'
        db.delete_table('core_persontrip')

        # Deleting model 'Area'
        db.delete_table('core_area')

        # Deleting model 'CaveAndEntrance'
        db.delete_table('core_caveandentrance')

        # Deleting model 'ProtectionCategory'
        db.delete_table('core_protectioncategory')

        # Deleting model 'Cave'
        db.delete_table('core_cave')

        # Removing M2M table for field area on 'Cave'
        db.delete_table('core_cave_area')

        # Deleting model 'OtherCaveName'
        db.delete_table('core_othercavename')

        # Deleting model 'SurveyStation'
        db.delete_table('core_surveystation')

        # Deleting model 'Entrance'
        db.delete_table('core_entrance')

        # Deleting model 'CaveDescription'
        db.delete_table('core_cavedescription')

        # Removing M2M table for field linked_subcaves on 'CaveDescription'
        db.delete_table('core_cavedescription_linked_subcaves')

        # Removing M2M table for field linked_entrances on 'CaveDescription'
        db.delete_table('core_cavedescription_linked_entrances')

        # Removing M2M table for field linked_qms on 'CaveDescription'
        db.delete_table('core_cavedescription_linked_qms')

        # Deleting model 'NewSubCave'
        db.delete_table('core_newsubcave')

        # Deleting model 'QM'
        db.delete_table('core_qm')

        # Deleting model 'Photo'
        db.delete_table('core_photo')

        # Removing M2M table for field contains_person on 'Photo'
        db.delete_table('core_photo_contains_person')

        # Deleting model 'ScannedImage'
        db.delete_table('core_scannedimage')

        # Deleting model 'Survey'
        db.delete_table('core_survey')


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
