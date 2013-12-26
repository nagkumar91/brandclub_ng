from annoying.functions import get_object_or_None
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from .forms import FeedbackForm

from .models import Brand, Cluster, Store, Content, SlideShow, Device, StoreFeedback


def slug_view(request, slug):
    cluster_id = request.cluster_id
    home_cluster = get_object_or_None(Cluster, id=cluster_id)
    if home_cluster is not None:
        all_contents = home_cluster.get_all_home_content(request.device_id)
        home_brand = get_object_or_None(Brand, slug_name=slug)
        context = {'contents': all_contents, 'cluster': home_cluster, 'brand': home_brand}
        context_instance = RequestContext(request, context)
        return render_to_response('home.html', context_instance)
    return render_to_response('default.html', {'cluster': cluster_id})


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
    return render_to_response('slide_show.html', {'content': slides})


def display_clusters(request):
    return render_to_response('home.html', {})


def store_feedback(request, slug):
    store = get_object_or_404(Store, slug_name=slug)
    form = FeedbackForm()
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.instance.store = store
            form.save()
            return HttpResponseRedirect("/home/%s/" % store.slug_name)
    context = {'form': form,'brand': store.brand,'store': store}
    return render_to_response("store_feedback.html", context_instance = RequestContext(request, context))


def display_feedback(request):
    feedback = StoreFeedback.objects.all()
    return render_to_response("all_feedback.html", {"feedback": feedback})