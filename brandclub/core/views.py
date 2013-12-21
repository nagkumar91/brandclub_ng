from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template.loader import get_template
from django.template import Context

from .models import Brand, Cluster, Store, Content, SlideShow


def slug_view(request, slug):
    cluster_id = request.cluster_id
    home_cluster = get_object_or_404(Cluster, id=cluster_id)
    all_contents = home_cluster.get_all_home_content()
    home_brand = get_object_or_404(Brand, slug_name=slug)
    return render_to_response('home.html', {'contents': all_contents, 'cluster': home_cluster, 'brand': home_brand})


def store_home(request, slug):
    store = get_object_or_404(Store, slug_name=slug)
    contents = Content.active_objects.filter(show_on_home=False, store=store).select_subclasses()
    return render_to_response('store_home.html', {'contents': contents, 'brand': store.brand, 'store': store})