from annoying.functions import get_object_or_None
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
import json
from .helpers import id_generator

from .forms import FeedbackForm
from .models import Brand, Cluster, Store, SlideShow, Device, StoreFeedback, Wallpaper


def home_cluster_view(request, slug):
    cluster_id = request.cluster_id
    home_cluster = get_object_or_None(Cluster, id=cluster_id)
    if home_cluster is not None:
        all_contents = home_cluster.get_all_home_content(request.device_id, request.cluster_id)
        home_brand = get_object_or_None(Brand, slug_name=slug)
        context = {'contents': all_contents, 'cluster': home_cluster, 'brand': home_brand}
        context_instance = RequestContext(request, context)
        return render_to_response('home.html', context_instance)
    return render_to_response('default.html', {'cluster': cluster_id})


def store_home(request, slug):
    store = get_object_or_None(Store, slug_name=slug, cluster__id=request.cluster_id)
    contents = store.get_content_for_store()
    context = {'contents': contents, 'store': store, 'brand': store.brand}
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
    context_instance = RequestContext(request, {'content': slides})
    return render_to_response('slide_show.html', context_instance)


def wallpaper_fullscreen(request, wid):
    wallpaper = get_object_or_404(Wallpaper, id=wid)
    context_instance = RequestContext(request, {'content': wallpaper})
    return render_to_response("wallpaper_fullscreen.html", context_instance)


def display_clusters(request):
    context_instance = RequestContext(request)
    return render_to_response('home.html', context_instance)


def store_feedback(request, slug):
    store = get_object_or_404(Store, slug_name=slug)
    form = FeedbackForm()
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.instance.store = store
            form.save()
            return HttpResponseRedirect("/home/%s/" % store.slug_name)
    context = {'form': form, 'brand': store.brand, 'store': store}
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


def cluster_info(request):
    device_id = request.device_id
    device = get_object_or_404(Device, device_id=device_id)
    cluster = device.store.cluster
    contents = cluster.get_cluster_info()
    brand = device.store.brand
    context_instance = RequestContext(request, {"contents": contents, "brand": brand})
    return render_to_response("info.html", context_instance)


def store_info(request):
    device_id = request.device_id
    device = get_object_or_404(Device, device_id=device_id)
    contents = device.store.get_store_info()
    brand = device.store.brand
    context_instance = RequestContext(request, {"contents": contents, "brand": brand})
    return render_to_response("info.html", context_instance)