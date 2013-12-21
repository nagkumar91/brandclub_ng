from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from .models import Brand, Cluster, Store, Content, SlideShow

def slug_view(request, slug):
    cluster_id = request.cluster_id
    home_cluster = get_object_or_404(Cluster, id=cluster_id)
    all_contents = home_cluster.get_all_home_content()
    home_brand = get_object_or_404(Brand, slug_name=slug)
    context = {'contents': all_contents, 'cluster': home_cluster, 'brand': home_brand}
    context_instance = RequestContext(request, context)
    return render_to_response('home.html', context_instance)


def store_home(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    brand = get_object_or_404(Brand, id=store.brand_id)
    contents = Content.active_objects.filter(show_on_home=False, store=store).select_subclasses()
    return render_to_response('store_home.html', {'contents': contents, 'brand': brand, 'store': store})

def slideshow(request, ssid):
    slides = get_object_or_404(SlideShow, id=ssid)
    return render_to_response('slide_show.html', {'content':slides})