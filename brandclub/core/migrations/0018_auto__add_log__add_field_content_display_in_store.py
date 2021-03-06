# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Log'
        db.delete_table(u'core_log')
        db.create_table(u'core_log', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('mac_address', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('content_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('content_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('content_location', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('content_owner_brand_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('content_owner_brand_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('location_device_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('location_store_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('location_store_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('location_brand_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('location_brand_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('location_cluster_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('location_cluster_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('user_agent', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('mobile_make', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('mobile_model', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('user_unique_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('user_ip_address', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('user_device_width', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('user_device_height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('page_title', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('referrer', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('redirect_url', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('access_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Log'])

        # Adding field 'Content.display_in_store'
        db.add_column(u'core_content', 'display_in_store',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Log'
        db.delete_table(u'core_log')

        # Deleting field 'Content.display_in_store'
        db.delete_column(u'core_content', 'display_in_store')


    models = {
        u'core.audio': {
            'Meta': {'object_name': 'Audio', '_ormbases': [u'core.Content']},
            u'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        u'core.brand': {
            'Meta': {'object_name': 'Brand'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'bg_color': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'bg_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'competitors': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'competitors_rel_+'", 'null': 'True', 'to': u"orm['core.Brand']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'footfall': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug_name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
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
            'content': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'clusters'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['core.Content']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locality': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'map_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'clusters'", 'to': u"orm['core.State']"})
        },
        u'core.content': {
            'Meta': {'object_name': 'Content'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content_location': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contents'", 'to': u"orm['core.ContentType']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'display_in_store': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 4, 9, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'no_of_people_rated': ('django.db.models.fields.BigIntegerField', [], {'default': '1'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'store': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'contents'", 'to': u"orm['core.Store']", 'through': u"orm['core.OrderedStoreContent']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
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
        u'core.freeinternet': {
            'Meta': {'object_name': 'FreeInternet', '_ormbases': [u'core.Content']},
            u'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Content']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'core.freeinternetlog': {
            'Meta': {'object_name': 'FreeInternetLog'},
            'access_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Device']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Store']"}),
            'used_status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user_phone_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        u'core.image': {
            'Meta': {'object_name': 'Image'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Image_for_slideshow'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'target_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'core.log': {
            'Meta': {'object_name': 'Log'},
            'access_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'action': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'content_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'content_location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'content_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'content_owner_brand_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'content_owner_brand_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location_brand_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'location_brand_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'location_cluster_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'location_cluster_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'location_device_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'location_store_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'location_store_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mac_address': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'mobile_make': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'mobile_model': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'page_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'redirect_url': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'referrer': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user_agent': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'user_device_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user_device_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user_ip_address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user_unique_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'core.navmenu': {
            'Meta': {'object_name': 'NavMenu', '_ormbases': [u'core.Content']},
            u'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'menu_contents': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ordered_contents'", 'symmetrical': 'False', 'through': u"orm['core.OrderedNavMenuContent']", 'to': u"orm['core.Content']"})
        },
        u'core.offer': {
            'Meta': {'object_name': 'Offer', '_ormbases': [u'core.Content']},
            'authenticate_user': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'core.offerdownloadinfo': {
            'Meta': {'object_name': 'OfferDownloadInfo'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'email_id': ('django.db.models.fields.EmailField', [], {'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'offer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'offer_download_info'", 'to': u"orm['core.Offer']"}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'core.orderednavmenucontent': {
            'Meta': {'ordering': "['order']", 'object_name': 'OrderedNavMenuContent'},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nav_contents'", 'to': u"orm['core.Content']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nav_menu': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.NavMenu']"}),
            'order': ('django.db.models.fields.IntegerField', [], {})
        },
        u'core.orderedstorecontent': {
            'Meta': {'ordering': "['order']", 'object_name': 'OrderedStoreContent'},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'store_contents'", 'to': u"orm['core.Content']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Store']"})
        },
        u'core.slideshow': {
            'Meta': {'object_name': 'SlideShow', '_ormbases': [u'core.Content']},
            u'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'slideshow'", 'symmetrical': 'False', 'through': u"orm['core.SlideShowImage']", 'to': u"orm['core.Image']"})
        },
        u'core.slideshowimage': {
            'Meta': {'ordering': "['order']", 'object_name': 'SlideShowImage'},
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
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'address_first_line': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'address_second_line': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stores'", 'to': u"orm['core.Brand']"}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stores'", 'to': u"orm['core.City']"}),
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stores'", 'null': 'True', 'to': u"orm['core.Cluster']"}),
            'contact_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'demo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '6'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '6'}),
            'mail_id': ('django.db.models.fields.EmailField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'map_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'pin_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'slug_name': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '100'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stores'", 'to': u"orm['core.State']"})
        },
        u'core.storefeedback': {
            'Meta': {'object_name': 'StoreFeedback'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'email_id': ('django.db.models.fields.EmailField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'feedback'", 'to': u"orm['core.Store']"})
        },
        u'core.video': {
            'Meta': {'object_name': 'Video', '_ormbases': [u'core.Content']},
            u'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'file': ('core.helpers.ContentTypeRestrictedFileField', [], {'max_length': '100'})
        },
        u'core.wallpaper': {
            'Meta': {'object_name': 'Wallpaper', '_ormbases': [u'core.Content']},
            u'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'core.web': {
            'Meta': {'object_name': 'Web', '_ormbases': [u'core.Content']},
            'content': ('ckeditor.fields.RichTextField', [], {}),
            u'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Content']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'core.webcontent': {
            'Meta': {'object_name': 'WebContent', '_ormbases': [u'core.Content']},
            u'content_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.Content']", 'unique': 'True', 'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['core']