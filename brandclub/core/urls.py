from django.conf.urls import patterns

urlpatterns = patterns('',
                       (r'store/(?P<store_id>\d+)/$', 'core.views.store_home'),
                       (r'slideshow/(?P<ssid>\d+)/$', 'core.views.slideshow'),
                       (r'(?P<slug>[\-\w]+)/$', 'core.views.slug_view'),
)




