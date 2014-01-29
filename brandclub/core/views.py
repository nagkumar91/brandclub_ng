from annoying.functions import get_object_or_None
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
import json
from .helpers import id_generator

from .forms import FeedbackForm
from .models import Brand, Cluster, Store, SlideShow, Device, StoreFeedback, Wallpaper, Offer, OfferDownloadInfo, NavMenu, OrderedNavMenuContent, Content


def home_cluster_view(request, slug=""):
    device_id = request.device_id
    device = get_object_or_None(Device, device_id=device_id)
    if device and device.store and device.store.cluster:
        home_cluster = device.store.cluster
        all_contents = home_cluster.get_all_home_content(request.device_id)
        home_brand = device.store.brand
        if slug is not "":
            home_store = get_object_or_None(Store, slug_name=slug, devices__device_id=device_id)
            home_brand = home_store.brand
        context = {'contents': all_contents, 'cluster': home_cluster, 'brand': home_brand}
        context_instance = RequestContext(request, context)
        return render_to_response('home.html', context_instance)
    context_instance = RequestContext(request, {'device': device})
    return render_to_response('default.html', context_instance)


def store_home(request, slug):
    device_id = request.device_id
    device = get_object_or_None(Device, device_id=device_id)
    if device.store is not None and device is not None:
        redirect = "/%s" % device.store.slug_name
        to = "cluster"
        if device.store.cluster is not None:
            cluster = device.store.cluster
            store = get_object_or_None(Store, slug_name=slug, cluster__id=cluster.id)
            if store is not None:
                contents = store.get_content_for_store()
                context = {'contents': contents, 'store': store, 'brand': store.brand, "redirect": redirect, "to": to}
                context_instance = RequestContext(request, context)
                return render_to_response('store_home.html', context_instance)
            return "Store not found"
        return "No cluster assigned to store"
    return "No store assigned to device"


def contents_loc_view(request, device_id=settings.DEFAULT_DEVICE_ID):
    device = get_object_or_None(Device, device_id=device_id)
    if device is None:
        return "No Device found"
    cluster_id = device.store.cluster.id
    result = "%s/%s" % (settings.CONTENT_CACHE_DIRECTORY, cluster_id)
    return HttpResponse(result, content_type='text/plain')


def redirect_to_outside(request):
    url = request.GET.get('href', 'http://www.brandclub.mobi')
    return HttpResponseRedirect(url)


def slideshow(request, ssid):
    slides = get_object_or_None(SlideShow, id=ssid)
    context_instance = RequestContext(request, {'content': slides})
    return render_to_response('slide_show.html', context_instance)


def wallpaper_fullscreen(request, wid):
    wallpaper = get_object_or_404(Wallpaper, id=wid)
    if wallpaper is not None:
        store = list(wallpaper.store.all())
        if len(store) > 0 :
            store = store[0]
            brand = store.brand
            redirect = "/home/%s/" % store.slug_name
            to = "store"
        else:
            device_id = request.device_id
            device = Device.objects.select_related("store").get(device_id=device_id)
            store = device.store
            brand = store.brand
            redirect = "/%s/" % store.slug_name
            to = "store"
        context_instance = RequestContext(request,
                                          {'content': wallpaper, "redirect": redirect, "to": to, "brand": brand})
        return render_to_response("wallpaper_fullscreen.html", context_instance)
    return "Wallpaper not found"


def display_clusters(request):
    context_instance = RequestContext(request)
    return render_to_response('home.html', context_instance)


def store_feedback(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    redirect = "/home/%s" % store.slug_name
    to = "store"
    form = FeedbackForm()
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.instance.store = store
            form.save()
            return HttpResponseRedirect("/home/%s/" % store.slug_name)
    context = {'form': form, 'brand': store.brand, 'store': store, "redirect": redirect, "to": to}
    return render_to_response("store_feedback.html", context_instance=RequestContext(request, context))


def display_feedback(request):
    feedback = StoreFeedback.objects.all()
    context_instance = RequestContext(request, {"feedback": feedback})
    return render_to_response("all_feedback.html", context_instance)


def display_offers(request):
    device_id = request.device_id
    device = Device.objects.select_related("store").get(device_id=device_id)
    home_store = device.store
    cluster_id = home_store.cluster.id
    home_cluster = home_store.cluster
    offers_in_cluster = home_cluster.get_all_offers(device_id, cluster_id)
    context_instance = RequestContext(request, {"offers": offers_in_cluster, "brand": home_store.brand})
    return render_to_response("offers.html", context_instance)


def create_user_id(request):
    user_id = "bc_"
    user_id += id_generator()
    data = {"user_id": user_id}
    data = json.dumps(data)
    return HttpResponse(data, mimetype='application/json')


def cluster_info(request):
    device_id = request.device_id
    device = get_object_or_404(Device, device_id=device_id)
    if device.store is not None:
        if device.store.cluster is not None:
            cluster = device.store.cluster
            contents = cluster.get_cluster_info()
            brand = device.store.brand
            redirect = "/%s" % device.store.slug_name
            to = "cluster"
            context_instance = RequestContext(request,
                                              {"contents": contents, "brand": brand, "redirect": redirect, "to": to}
            )
            return render_to_response("info.html", context_instance)
        return "No cluster assigned for the store"
    return "No Store assigned to device"


def store_info(request, storeid):
    store = get_object_or_404(Store, pk=storeid)
    contents = store.get_store_info()
    brand = store.brand
    redirect = "/home/%s" % store.slug_name
    to = "store"
    context_instance = RequestContext(request, {"contents": contents, "brand": brand, "redirect": redirect, "to": to})
    return render_to_response("info.html", context_instance)


def offer(request, offer_id):
    offer_obj = get_object_or_None(Offer, id=offer_id)
    if offer_obj is not None:
        store = offer_obj.store.all()
        if store is not None:
            store = store[0]
            brand = store.brand
            redirect = "/home/%s" % store.slug_name
            to = "store"
            context_instance = RequestContext(request,
                                              {'content': offer_obj, "redirect": redirect,
                                               "to": to, "brand": brand}
            )
            return render_to_response("offer_fullscreen.html", context_instance)
        return "Offer not assigned to any store"
    return "Offer not found"


def authenticate_user_for_offer(request):
    response_data = {'show_offer': True}
    user_info = request.GET
    phone_number = user_info['phone_number']
    email_id = user_info['email_id']
    user_name = user_info['user_name']
    offer_id = user_info['offer']
    offer_obj = Offer.objects.get(pk=offer_id)
    odi_obj = OfferDownloadInfo(user_name=user_name, email_id=email_id, mobile_number=phone_number, offer=offer_obj)
    odi_obj.save()
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def navmenu(request, navmenu_id):
    device_id = request.device_id
    device = get_object_or_None(Device, device_id=device_id)
    redirect = "/%s" % device.store.slug_name
    to = "cluster"
    ordered_content_ids = list(OrderedNavMenuContent.objects.filter(nav_menu__id = navmenu_id))
    ordered_ids = [ item.content.id for item in ordered_content_ids ]
    contents = list(Content.objects.select_subclasses().filter(id__in = ordered_ids))
    contents.sort(key=lambda content: ordered_ids.index(content.pk))
    for content in contents:
        setattr(content, 'own_store', device.store)
    context = {'contents': contents, 'store': device.store, 'brand': device.store.brand, "redirect": redirect, "to": to}
    context_instance = RequestContext(request, context)
    return render_to_response('store_home.html', context_instance)



