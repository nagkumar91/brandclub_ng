from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'device_list/$', 'report.views.device_list'),
                       url(r'footfall/$', 'report.views.footfall'),
                       url(r'brand_clusters/$', 'report.views.brand_clusters'),
                       url(r'brand_associates/$', 'report.views.brand_associates'),
                       url(r'store_contents/$', 'report.views.store_contents'),
                       url(r'brands_footfall/$', 'report.views.brands_footfall'),
                       )
