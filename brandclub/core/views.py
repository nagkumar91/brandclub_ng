from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from models import Store, Brand, Content, Device, Cluster
from middleware import ClusterDeviceDetectionMiddleware
from django.template.loader import get_template
from django.template import Context
# Create your views here.


def slug_view(request, slug):
    # device_id = request.device_id
    cluster_id = request.cluster_id
    print cluster_id
    print request.META
    home_cluster = get_object_or_404(Cluster, id=cluster_id)
    all_contents = home_cluster.get_all_home_content()
    t = get_template('cluster_home.html')
    html = t.render(Context({'contents': all_contents}))
    # home_brand = get_object_or_404(Brand, slug_name=slug)
    # home_store = home_brand.stores.all().filter(cluster_id__exact=cluster_id)
    # stores_in_cluster = Store.objects.all().filter(cluster_id__exact=cluster_id)
    # contents_in_cluster = []
    # for sic in stores_in_cluster:
    #     contents_in_cluster.append(sic.contents.filter(show_on_home=True)[:1])
    # print "Contents in cluster before swap "
    # print contents_in_cluster
    # home_store_header = home_store[0].contents.filter(show_on_home=True)[:1]
    # print "Home store content"
    # print home_store_header
    # b = 0
    # a = contents_in_cluster.index(home_store_header)
    # contents_in_cluster[b], contents_in_cluster[a] = contents_in_cluster[a], contents_in_cluster[b]
    # print "After the swap, contents in cluster are"
    # print contents_in_cluster
    # contents_in_cluster = Store.objects.all().filter(cluster_id__exact=cluster_id)
    print all_contents
    return HttpResponse(html)