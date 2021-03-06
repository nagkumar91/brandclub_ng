# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BrandClubAppWidgetImage'
        db.create_table(u'core_brandclubappwidgetimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.AppWidgetBackground'])),
            ('widget', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.BrandClubAppWidget'])),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'core', ['BrandClubAppWidgetImage'])

        # Adding model 'AppWidgetBackground'
        db.create_table(u'core_appwidgetbackground', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='App Widget Image', max_length=50)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'core', ['AppWidgetBackground'])

        # Adding model 'BrandClubAppWidget'
        db.create_table(u'core_brandclubappwidget', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'core', ['BrandClubAppWidget'])


    def backwards(self, orm):
        # Deleting model 'BrandClubAppWidgetImage'
        db.delete_table(u'core_brandclubappwidgetimage')

        # Deleting model 'AppWidgetBackground'
        db.delete_table(u'core_appwidgetbackground')

        # Deleting model 'BrandClubAppWidget'
        db.delete_table(u'core_brandclubappwidget')


    models = {
        u'core.apppreference': {
            'Meta': {'object_name': 'AppPreference'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'category_preference'", 'null': 'True', 'to': u"orm['core.AppUserPreferenceCategory']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'core.appuserpreferencecategory': {
            'Meta': {'object_name': 'AppUserPreferenceCategory'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'})
        },
        u'core.appwidgetbackground': {
            'Meta': {'object_name': 'AppWidgetBackground'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'App Widget Image'", 'max_length': '50'})
        },
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
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug_name': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'core.brandclubappuser': {
            'Meta': {'object_name': 'BrandClubAppUser'},
            'app_version': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'device_id': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'email_id': ('django.db.models.fields.EmailField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'enable_notifications': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'fb_id': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imei': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '8', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '8', 'blank': 'True'}),
            'mobile_make': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mobile_model': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'preferences': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'bc_app_user'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['core.AppPreference']"}),
            'profile_pic': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'registration_id': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'})
        },
        u'core.brandclubappwidget': {
            'Meta': {'ordering': "['order']", 'object_name': 'BrandClubAppWidget'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['core.AppWidgetBackground']", 'null': 'True', 'through': u"orm['core.BrandClubAppWidgetImage']", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'order': ('django.db.models.fields.IntegerField', [], {})
        },
        u'core.brandclubappwidgetimage': {
            'Meta': {'ordering': "['order']", 'object_name': 'BrandClubAppWidgetImage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.AppWidgetBackground']"}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'widget': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.BrandClubAppWidget']"})
        },
        u'core.brandclubredemptionlog': {
            'Meta': {'object_name': 'BrandClubRedemptionLog'},
            'bc_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.BrandClubUser']", 'null': 'True', 'blank': 'True'}),
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Cluster']", 'null': 'True', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Store']", 'null': 'True', 'blank': 'True'})
        },
        u'core.brandclubretailerlog': {
            'Meta': {'object_name': 'BrandClubRetailerLog'},
            'amount': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'store_id': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'core.brandclubuser': {
            'Meta': {'object_name': 'BrandClubUser'},
            'coupon_current_value': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'coupon_generated_at': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'coupon_user'", 'null': 'True', 'blank': 'True', 'to': u"orm['core.Store']"}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'last_updated_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'loyalty_points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'mac_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'qr_code': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'primary_key': 'True'}),
            'user_unique_id': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'end_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 8, 10, 0, 0)'}),
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
        u'core.customstorefeedback': {
            'Meta': {'object_name': 'CustomStoreFeedback'},
            'any_other_feedback': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'how_long_have_you_been_shopping': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'overall_experience': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'product_range_options': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'recommendation_options': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'staff_options': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'store': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'custom_feedback'", 'to': u"orm['core.Store']"})
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
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'show_qr': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
            'auth_key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stores'", 'to': u"orm['core.Brand']"}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stores'", 'to': u"orm['core.City']"}),
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stores'", 'null': 'True', 'to': u"orm['core.Cluster']"}),
            'contact_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'custom_form_slug': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'demo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'has_custom_form': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '6'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '6'}),
            'mail_id': ('django.db.models.fields.EmailField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'map_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pin_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'slug_name': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '100'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stores'", 'to': u"orm['core.State']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
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