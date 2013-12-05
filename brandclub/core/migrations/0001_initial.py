# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'State'
        db.create_table(u'core_state', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'core', ['State'])

        # Adding model 'City'
        db.create_table(u'core_city', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'core', ['City'])

        # Adding model 'Country'
        db.create_table(u'core_country', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'core', ['Country'])

        # Adding model 'Brand'
        db.create_table(u'core_brand', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('bg_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('bg_color', self.gf('django.db.models.fields.CharField')(max_length=6, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Brand'])

        # Adding model 'Cluster'
        db.create_table(u'core_cluster', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('locality', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(related_name='clusters', to=orm['core.City'])),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(related_name='clusters', to=orm['core.State'])),
        ))
        db.send_create_signal(u'core', ['Cluster'])

        # Adding model 'Store'
        db.create_table(u'core_store', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('address_first_line', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('address_second_line', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stores', to=orm['core.City'])),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stores', to=orm['core.State'])),
            ('pin_code', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('brand', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stores', to=orm['core.Brand'])),
            ('cluster', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stores', null=True, to=orm['core.Cluster'])),
        ))
        db.send_create_signal(u'core', ['Store'])

        # Adding model 'Device'
        db.create_table(u'core_device', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('device_id', self.gf('django.db.models.fields.IntegerField')(unique=True, max_length=6)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('mac_address', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('store', self.gf('django.db.models.fields.related.ForeignKey')(related_name='devices', null=True, to=orm['core.Store'])),
        ))
        db.send_create_signal(u'core', ['Device'])

        # Adding model 'ContentType'
        db.create_table(u'core_contenttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
        ))
        db.send_create_signal(u'core', ['ContentType'])

        # Adding model 'Content'
        db.create_table(u'core_content', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('show_on_home', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('short_description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('rating', self.gf('django.db.models.fields.IntegerField')(default=5)),
            ('no_of_people_rated', self.gf('django.db.models.fields.BigIntegerField')(default=1)),
            ('start_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now)),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('archived', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='contents', to=orm['core.ContentType'])),
        ))
        db.send_create_signal(u'core', ['Content'])

        # Adding M2M table for field store on 'Content'
        m2m_table_name = db.shorten_name(u'core_content_store')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('content', models.ForeignKey(orm[u'core.content'], null=False)),
            ('store', models.ForeignKey(orm[u'core.store'], null=False))
        ))
        db.create_unique(m2m_table_name, ['content_id', 'store_id'])

        # Adding model 'Audio'
        db.create_table(u'core_audio', (
            (u'content_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Content'], unique=True, primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'core', ['Audio'])

        # Adding model 'Video'
        db.create_table(u'core_video', (
            (u'content_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Content'], unique=True, primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'core', ['Video'])

        # Adding model 'Wallpaper'
        db.create_table(u'core_wallpaper', (
            (u'content_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Content'], unique=True, primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'core', ['Wallpaper'])

        # Adding model 'Web'
        db.create_table(u'core_web', (
            (u'content_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Content'], unique=True, primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'core', ['Web'])

        # Adding model 'Image'
        db.create_table(u'core_image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('target_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Image'])

        # Adding model 'SlideShowImage'
        db.create_table(u'core_slideshowimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slideshow', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.SlideShow'])),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Image'])),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'core', ['SlideShowImage'])

        # Adding unique constraint on 'SlideShowImage', fields ['slideshow', 'order']
        db.create_unique(u'core_slideshowimage', ['slideshow_id', 'order'])

        # Adding model 'SlideShow'
        db.create_table(u'core_slideshow', (
            (u'content_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Content'], unique=True, primary_key=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'core', ['SlideShow'])


    def backwards(self, orm):
        # Removing unique constraint on 'SlideShowImage', fields ['slideshow', 'order']
        db.delete_unique(u'core_slideshowimage', ['slideshow_id', 'order'])

        # Deleting model 'State'
        db.delete_table(u'core_state')

        # Deleting model 'City'
        db.delete_table(u'core_city')

        # Deleting model 'Country'
        db.delete_table(u'core_country')

        # Deleting model 'Brand'
        db.delete_table(u'core_brand')

        # Deleting model 'Cluster'
        db.delete_table(u'core_cluster')

        # Deleting model 'Store'
        db.delete_table(u'core_store')

        # Deleting model 'Device'
        db.delete_table(u'core_device')

        # Deleting model 'ContentType'
        db.delete_table(u'core_contenttype')

        # Deleting model 'Content'
        db.delete_table(u'core_content')

        # Removing M2M table for field store on 'Content'
        db.delete_table(db.shorten_name(u'core_content_store'))

        # Deleting model 'Audio'
        db.delete_table(u'core_audio')

        # Deleting model 'Video'
        db.delete_table(u'core_video')

        # Deleting model 'Wallpaper'
        db.delete_table(u'core_wallpaper')

        # Deleting model 'Web'
        db.delete_table(u'core_web')

        # Deleting model 'Image'
        db.delete_table(u'core_image')

        # Deleting model 'SlideShowImage'
        db.delete_table(u'core_slideshowimage')

        # Deleting model 'SlideShow'
        db.delete_table(u'core_slideshow')


    models = {
        u'core.audio': {
            'Meta': {'object_name': 'Audio', '_ormbases': [u'core.Content']},
            u'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        u'core.brand': {
            'Meta': {'object_name': 'Brand'},
            'bg_color': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'bg_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'core.city': {
            'Meta': {'object_name': 'City'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.cluster': {
            'Meta': {'object_name': 'Cluster'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'clusters'", 'to': u"orm['core.City']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locality': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'clusters'", 'to': u"orm['core.State']"})
        },
        u'core.content': {
            'Meta': {'object_name': 'Content'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contents'", 'to': u"orm['core.ContentType']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'no_of_people_rated': ('django.db.models.fields.BigIntegerField', [], {'default': '1'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'show_on_home': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'store': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'contents'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['core.Store']"}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'core.contenttype': {
            'Meta': {'object_name': 'ContentType'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'core.country': {
            'Meta': {'object_name': 'Country'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.device': {
            'Meta': {'object_name': 'Device'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'device_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mac_address': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'devices'", 'null': 'True', 'to': u"orm['core.Store']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'core.image': {
            'Meta': {'object_name': 'Image'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'target_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'core.slideshow': {
            'Meta': {'object_name': 'SlideShow', '_ormbases': [u'core.Content']},
            u'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'slideshow'", 'symmetrical': 'False', 'through': u"orm['core.SlideShowImage']", 'to': u"orm['core.Image']"}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'core.slideshowimage': {
            'Meta': {'ordering': "['order']", 'unique_together': "(('slideshow', 'order'),)", 'object_name': 'SlideShowImage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Image']"}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'slideshow': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.SlideShow']"})
        },
        u'core.state': {
            'Meta': {'object_name': 'State'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.store': {
            'Meta': {'object_name': 'Store'},
            'address_first_line': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'address_second_line': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stores'", 'to': u"orm['core.Brand']"}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stores'", 'to': u"orm['core.City']"}),
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stores'", 'null': 'True', 'to': u"orm['core.Cluster']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pin_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stores'", 'to': u"orm['core.State']"})
        },
        u'core.video': {
            'Meta': {'object_name': 'Video', '_ormbases': [u'core.Content']},
            u'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        u'core.wallpaper': {
            'Meta': {'object_name': 'Wallpaper', '_ormbases': [u'core.Content']},
            u'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'core.web': {
            'Meta': {'object_name': 'Web', '_ormbases': [u'core.Content']},
            'content': ('django.db.models.fields.TextField', [], {}),
            u'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Content']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['core']