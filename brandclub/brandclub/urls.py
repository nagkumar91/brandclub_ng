from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^grappelli/', include('grappelli.urls')),
                       url(r'^ckeditor/', include('ckeditor.urls')),
                       url(r'^report/', include('report.urls')),
                       url(r'^', include('core.urls')),



)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
                            (r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
    )

