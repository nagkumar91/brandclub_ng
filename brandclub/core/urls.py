from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^contents_dir/(?P<device_id>\d+)/$', 'core.views.contents_loc_view'),
                       url(r'home/(?P<slug>[\-\w]+)/$', 'core.views.store_home'),
                       url(r'(?P<slug>[\-\w]+)/$', 'core.views.slug_view'),
)




