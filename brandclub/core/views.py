from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from models import Store, Brand, Content, Device, Cluster
from middleware import ClusterDeviceDetectionMiddleware
from django.template.loader import get_template
from django.template import Context
# Create your views here.


def slug_view(request, slug):
    cluster_id = request.cluster_id
    home_cluster = get_object_or_404(Cluster, id=cluster_id)
    all_contents = home_cluster.get_all_home_content()
    home_brand = get_object_or_404(Brand, slug_name=slug)
    t = get_template('cluster_home.html')
    html = t.render(Context({'contents': all_contents, 'cluster': home_cluster, 'home_brand': home_brand}))
    return HttpResponse(html)