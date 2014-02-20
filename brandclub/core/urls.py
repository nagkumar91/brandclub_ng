from django.conf.urls import patterns, url, include
from tastypie.api import Api
from .api import *

v1_api = Api(api_name='v1')
v1_api.register(ContentTypeResource())
v1_api.register(ContentResource())
v1_api.register(StoreResource())
v1_api.register(ClusterContentResource())
v1_api.register(WallpaperResource())
v1_api.register(SlideShowResource())
v1_api.register(SlideShowImageResource())
v1_api.register(ImageResource())




urlpatterns = patterns('',
                       url(r'^api/', include(v1_api.urls)),
                       url(r'^redirect/$', 'core.views.redirect_to_outside'),
                       url(r'^contents_dir/(?P<device_id>\d+)/$', 'core.views.contents_loc_view'),
                       url(r'home/(?P<slug>[\-\w]+)/$', 'core.views.store_home'),
                       url(r'feedback/(?P<store_id>\d+)/$', 'core.views.store_feedback'),
                       url(r'all_feedback/$', 'core.views.display_feedback'),
                       url(r'offers/$', 'core.views.display_offers'),
                       url(r'offer/(?P<offer_id>\d+)/$', 'core.views.offer'),
                       url(r'navmenu/(?P<navmenu_id>\d+)/$', 'core.views.navmenu'),
                       url(r'authenticateUserForOffer/$', 'core.views.authenticate_user_for_offer'),
                       url(r'create_user_id/$', 'core.views.create_user_id'),
                       url(r'slideshow/(?P<ssid>\d+)/$', 'core.views.slideshow'),
                       url(r'wallpaper/(?P<wid>\d+)/$', 'core.views.wallpaper_fullscreen'),
                       url(r'web/(?P<wid>\d+)/$', 'core.views.web_fullscreen'),
                       url(r'ci/$', 'core.views.cluster_info'),
                       url(r'call_log/$', 'core.views.call_log'),
                       url(r'si/(?P<storeid>\d+)/$', 'core.views.store_info'),
                       url(r'ch/(?P<hid>\d+)/$', 'core.views.home_cluster_hid'),
                       url(r'sh/(?P<hid>\d+)/$', 'core.views.store_home_hid'),
                       url(r'^$', 'core.views.home_cluster_view'),
                       url(r'^(?P<slug>[\-\w]+)/$', 'core.views.home_cluster_view'),
)




