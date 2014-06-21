from django.conf.urls import patterns, url, include
from tastypie.api import Api
from .api import *
import forms_builder.forms.urls

v1_api = Api(api_name='v1')
v1_api.register(ContentTypeResource())
v1_api.register(ContentResource())
v1_api.register(StoreResource())
v1_api.register(ClusterContentResource())
v1_api.register(WallpaperResource())
v1_api.register(SlideShowResource())
v1_api.register(SlideShowImageResource())
v1_api.register(ImageResource())
v1_api.register(StoreContentResource())
v1_api.register(ClusterResource())
v1_api.register(DeviceResource())
v1_api.register(BrandResource())
v1_api.register(AppPreferenceResource())
v1_api.register(AppUserPreferenceCategoryResource())
v1_api.register(BrandClubAppUserResource())
v1_api.register(CustomAppPreferenceResource())
v1_api.register(AppUserPreferenceCategoryCustomResource())




urlpatterns = patterns('',
                       url(r'^api/', include(v1_api.urls)),
                       url(r'^store_find/(?P<latitude>\d+\.\d+)/(?P<longitude>\d+\.\d+)/(?P<radius>\d+)/$', 'core.views.get_stores_within_range'),
                       url(r'store_authenticate/(?P<user_name>[\-\w]+)/(?P<password>[\-\w]+)/$', 'core.views.store_authenticate'),
                       url(r'verify_user/(?P<user_id>[\-\w]+)/(?P<auth_key>[\-\w]+)/$', 'core.views.coupon_redemption'),
                       url(r'^display_qr/$', 'core.views.display_qr'),
                       url(r'^redirect/$', 'core.views.redirect_to_outside'),
                       url(r'^contents_dir/(?P<device_id>\d+)/$', 'core.views.contents_loc_view'),
                       url(r'home/(?P<slug>[\-\w]+)/$', 'core.views.store_home'),
                       url(r'feedback/(?P<store_id>\d+)/$', 'core.views.store_feedback'),
                       url(r'all_feedback/$', 'core.views.display_feedback'),
                       url(r'custom_feedback/$', 'core.views.display_custom_feedback'),
                       url(r'offers/$', 'core.views.display_offers'),
                       url(r'offer/(?P<offer_id>\d+)/$', 'core.views.offer'),
                       url(r'navmenu/(?P<navmenu_id>\d+)/$', 'core.views.navmenu'),
                       url(r'authenticateUserForOffer/$', 'core.views.authenticate_user_for_offer'),
                       url(r'create_user_id/$', 'core.views.create_user_id'),
                       url(r'qr_valid_in_store/$', 'core.views.qr_valid_in_store'),
                       url(r'slideshow/(?P<ssid>\d+)/$', 'core.views.slideshow'),
                       url(r'wallpaper/(?P<wid>\d+)/$', 'core.views.wallpaper_fullscreen'),
                       url(r'web/(?P<wid>\d+)/$', 'core.views.web_fullscreen'),
                       url(r'ci/$', 'core.views.cluster_info'),
                       url(r'call_log/$', 'core.views.call_log'),
                       url(r'si/(?P<storeid>\d+)/$', 'core.views.store_info'),
                       url(r'ch/(?P<hid>\d+)/$', 'core.views.home_cluster_hid'),
                       url(r'sh/(?P<hid>\d+)/$', 'core.views.store_home_hid'),
                       url(r'free_internet_codes/(?P<st_id>\d+)/$', 'core.views.free_internet_codes'),
                       url(r'free_internet_confirm/(?P<content_id>\d+)/$', 'core.views.free_internet_confirm'),
                       url(r'verify_log/$', 'core.views.verify_log'),
                       url(r'authorize_free_internet/$', 'core.views.authorize_free_internet'),
                       url(r'upload_log', 'core.views.upload_log'),
                       url(r'^forms/', include(forms_builder.forms.urls)),
                       url(r'^$', 'core.views.home_cluster_view'),
                       url(r'^(?P<slug>[\-\w]+)/$', 'core.views.home_cluster_view'),
)




