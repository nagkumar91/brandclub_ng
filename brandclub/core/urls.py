from django.conf.urls import patterns

urlpatterns = patterns('',
    (r'(?P<slug>[\-\w]+)/$', 'core.views.slug_view'),
)




