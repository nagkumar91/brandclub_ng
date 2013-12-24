from django.conf.urls import patterns

urlpatterns = patterns('',
                       (r'home/(?P<slug>[\-\w]+)/$', 'core.views.store_home'),
                       (r'feedback/$', 'core.views.submit_feedback'),
                       (r'feedback/(?P<slug>[\-\w]+)/$', 'core.views.store_feedback'),
                       (r'(?P<slug>[\-\w]+)/$', 'core.views.slug_view'),

)




