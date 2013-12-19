from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.template import Context

from .models import Brand, Cluster

def slug_view(request, slug):
    cluster_id = request.cluster_id
    home_cluster = get_object_or_404(Cluster, id=cluster_id)
    all_contents = home_cluster.get_all_home_content()
    home_brand = get_object_or_404(Brand, slug_name=slug)
    t = get_template('home.html')
    html = t.render(Context({'contents': all_contents, 'cluster': home_cluster, 'brand': home_brand}))
    print cluster_id
    return HttpResponse(html)