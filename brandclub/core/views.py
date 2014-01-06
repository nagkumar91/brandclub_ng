from annoying.functions import get_object_or_None
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.core.cache import cache
import json
from .helpers import id_generator

from .forms import FeedbackForm
from .models import Brand, Cluster, Store, Content, SlideShow, Device, StoreFeedback, Wallpaper


def home_cluster_view(request, slug):
    cluster_id = request.cluster_id
    device_id = request.device_id
    home_cluster = get_object_or_None(Cluster, id=cluster_id)
    device = get_object_or_404(Device, device_id=device_id)
    if home_cluster is not None:
        all_contents = home_cluster.get_all_home_content(request.device_id, request.cluster_id)
        home_brand = get_object_or_None(Brand, slug_name=slug)
        context = {'contents': all_contents, 'cluster': home_cluster, 'brand': home_brand, 'home_store': device.store,
                   'home_brand': device.store.brand, "home_cluster": home_cluster, "content_brand": home_brand,
                   "content_name": home_brand.name, "content_type": "home"}
        context_instance = RequestContext(request, context)
        return render_to_response('home.html', context_instance)
    return render_to_response('default.html', {'cluster': cluster_id})


def store_home(request, slug):
    cache_key = "%s-%s" % (slug, request.cluster_id)
    device_id = request.device_id
    device = get_object_or_404(Device, device_id=device_id)
    home_cluster = get_object_or_404(Cluster, id=request.cluster_id)
    store = cache.get(cache_key)
    if not store:
        store = get_object_or_None(Store, slug_name=slug, cluster__id=request.cluster_id)
        cache.set(cache_key, store, 1800)
    contents_key = "contents-%s" % cache_key
    contents = cache.get(contents_key)
    if not contents:
        contents = store.get_content_for_store()
        cache.set(contents_key, contents, 1800)
    context = {'contents': contents, 'store': store, 'brand': store.brand, 'home_store': device.store,
               'home_brand': device.store.brand, "home_cluster": home_cluster, "content_brand": store.brand}
    context_instance = RequestContext(request, context)
    return render_to_response('store_home.html', context_instance)


def contents_loc_view(request, device_id=5678):
    device = get_object_or_None(Device, device_id=device_id)
    if device is None:
        return "No Device found"
    cluster_id = device.store.cluster.id
    result = "%s/%s" % (settings.CONTENT_CACHE_DIRECTORY, cluster_id)
    return HttpResponse(result, content_type='text/plain')


def redirect_to_outside(request):
    url = request.GET.get('href', 'http://www.google.com')
    return HttpResponseRedirect(url)


def slideshow(request, ssid):
    slides = get_object_or_None(SlideShow, id=ssid)
    content_brand = slides.store.all()[0].brand
    device_id = request.device_id
    device = get_object_or_404(Device, device_id=device_id)
    home_cluster = get_object_or_404(Cluster, id=request.cluster_id)
    context_instance = RequestContext(request, {'content': slides, 'home_store': device.store,
                                                'home_brand': device.store.brand, "home_cluster": home_cluster,
                                                "content_brand": content_brand})
    return render_to_response('slide_show.html', context_instance)


def wallpaper_fullscreen(request, wid):
    wallpaper = get_object_or_404(Wallpaper, id=wid)
    content_brand = wallpaper.store.all()[0].brand
    device_id = request.device_id
    device = get_object_or_404(Device, device_id=device_id)
    brand = device.store.brand
    home_cluster = get_object_or_404(Cluster, id=request.cluster_id)
    context_instance = RequestContext(request, {'content': wallpaper, 'home_store': device.store, "brand": content_brand,
                                                'home_brand': brand, "home_cluster": home_cluster,
                                                "content_brand": content_brand})
    return render_to_response("wallpaper_fullscreen.html", context_instance)


def display_clusters(request):
    context_instance = RequestContext(request)
    return render_to_response('home.html', context_instance)


def store_feedback(request, slug):
    store = get_object_or_404(Store, slug_name=slug)
    device_id = request.device_id
    device = get_object_or_404(Device, device_id=device_id)
    home_cluster = get_object_or_404(Cluster, id=request.cluster_id)
    form = FeedbackForm()
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.instance.store = store
            form.save()
            return HttpResponseRedirect("/home/%s/" % store.slug_name)
    context = {'form': form, 'brand': store.brand, 'store': store, 'home_store': device.store,
               'home_brand': device.store.brand, "home_cluster": home_cluster, "content_brand": store.brand}
    return render_to_response("store_feedback.html", context_instance=RequestContext(request, context))


def display_feedback(request):
    feedback = StoreFeedback.objects.all()
    context_instance = RequestContext(request, {"feedback": feedback})
    return render_to_response("all_feedback.html", context_instance)


def create_user_id(request):
    user_id = "bc_"
    user_id += id_generator()
    data = {"user_id": user_id}
    data = json.dumps(data)
    return HttpResponse(data, mimetype='application/json')