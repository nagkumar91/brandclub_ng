from annoying.functions import get_object_or_None
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.core.cache import cache

from .models import Brand, Cluster, Store, Content, SlideShow


def slug_view(request, slug):
    cluster_id = request.cluster_id
    home_cluster = get_object_or_None(Cluster, id=cluster_id)
    if home_cluster is not None:
        all_contents = home_cluster.get_all_home_content(request.device_id)
        home_brand = get_object_or_None(Brand, slug_name=slug)
        context = {'contents': all_contents, 'cluster': home_cluster, 'brand': home_brand}
        context_instance = RequestContext(request, context)
        return render_to_response('home.html', context_instance)
    return render_to_response('default.html', {'cluster':cluster_id})


def store_home(request, slug):
    cache_key = "%s-%s" % (slug, request.cluster_id)
    store = cache.get(cache_key)
    if not store:
        store = get_object_or_None(Store, slug_name=slug, cluster__id=request.cluster_id)
        cache.set(cache_key, store, 1800)
    contents_key = "contents-%s" % cache_key
    contents = cache.get(contents_key)
    if not contents:
        contents = Content.active_objects.filter(show_on_home=False, store=store).select_subclasses()
        cache.set(contents_key, contents, 1800)
    return render_to_response('store_home.html', {'contents': contents, 'store': store, 'brand': store.brand})


def slideshow(request, ssid):
    slides = get_object_or_None(SlideShow, id=ssid)
    return render_to_response('slide_show.html', {'content': slides})


def display_clusters(request):
    return render_to_response('home.html', {})
