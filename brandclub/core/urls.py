from django.conf.urls import patterns

urlpatterns = patterns('',
                       (r'home/(?P<slug>[\-\w]+)/$', 'core.views.store_home'),
                       (r'(?P<slug>[\-\w]+)/$', 'core.views.slug_view'),
)




