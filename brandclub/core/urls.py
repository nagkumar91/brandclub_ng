from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^redirect/$', 'core.views.redirect_to_outside'),
                       url(r'^contents_dir/(?P<device_id>\d+)/$', 'core.views.contents_loc_view'),
                       url(r'home/(?P<slug>[\-\w]+)/$', 'core.views.store_home'),
                       url(r'feedback/(?P<slug>[\-\w]+)/$', 'core.views.store_feedback'),
                       url(r'all_feedback/$', 'core.views.display_feedback'),
                       url(r'create_user_id/$', 'core.views.create_user_id'),
                       url(r'slideshow/(?P<ssid>\d+)/$', 'core.views.slideshow'),
                       url(r'(?P<slug>[\-\w]+)/$', 'core.views.slug_view'),
)




