from datetime import time
import os
from annoying.functions import get_object_or_None
import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
import json
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .logging import log_data
from django.views.decorators.csrf import csrf_exempt
from .helpers import id_generator

from .forms import FeedbackForm, CustomFeedbackForm
from .models import Brand, Cluster, Store, SlideShow, Device, StoreFeedback, Wallpaper, Offer, OfferDownloadInfo, \
    NavMenu, OrderedNavMenuContent, Content, Web, Log, FreeInternetLog, OrderedStoreContent, CustomStoreFeedback, \
    BrandClubUser, BrandClubRedemptionLog, BrandClubRetailerLog
from .tasks import log_bc_data

content_type_mapping = {
    1: 'Store Home',
    2: 'Cluster Home',
    3: 'Cluster Info',
    4: 'Store Info',
}


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


def home_cluster_hid(request, hid=""):
    device_id = int(hid)
    device = get_object_or_None(Device, device_id=device_id)
    if device and device.store and device.store.cluster:
        home_cluster = device.store.cluster
        all_contents = home_cluster.get_all_home_content(device_id)
        home_brand = device.store.brand
        contents_to_be_displayed = []
        for c in all_contents:
            content_store = c.store.all()[:1]
            content_store = content_store[0]
            content_device = content_store.devices.all()[:1]
            if content_device:
                setattr(c, "device_id", content_device[0].device_id)
                contents_to_be_displayed.append(c)
        context = {'contents': contents_to_be_displayed, 'cluster': home_cluster, 'brand': home_brand}
        context_instance = RequestContext(request, context)
        return render_to_response('home.html', context_instance)
    context_instance = RequestContext(request, {'device': device})
    return render_to_response('default.html', context_instance)


def store_home_hid(request, hid):
    device_id = int(hid)
    device = get_object_or_None(Device, device_id=device_id)
    if device.store is not None and device is not None:
        redirect = "/%s" % device.store.slug_name
        to = "cluster"
        if device.store.cluster is not None:
            cluster = device.store.cluster
            store = device.store
            if store is not None:
                contents = store.get_content_for_store(device_id=device_id)
                context = {'contents': contents, 'store': store, 'brand': store.brand, "redirect": redirect, "to": to}
                context_instance = RequestContext(request, context)
                return render_to_response('store_home.html', context_instance)
            return "Store not found"
        return "No cluster assigned to store"
    return "No store assigned to device"


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
                contents = store.get_content_for_store(device_id=device_id)
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
    osc = OrderedStoreContent.objects.filter(content=slides)[:1]
    osc = osc[0]
    context_instance = RequestContext(request, {'content': slides, 'owner_brand': osc.store.brand.name})
    return render_to_response('slide_show.html', context_instance)


def wallpaper_fullscreen(request, wid):
    wallpaper = get_object_or_404(Wallpaper, id=wid)
    if wallpaper is not None:
        location = wallpaper.content_location
        store = wallpaper.store.all()
        if store.exists():
            store = store[0]
            brand = store.brand
            redirect = "/home/%s/" % store.slug_name
        else:
            device_id = request.device_id
            device = Device.objects.select_related("store").get(device_id=device_id)
            store = device.store
            brand = store.brand
            redirect = "/%s/" % store.slug_name
        context_instance = RequestContext(request,
                                          {'content': wallpaper, "redirect": redirect,
                                           "to": content_type_mapping[int(location)], "brand": brand})
        return render_to_response("wallpaper_fullscreen.html", context_instance)
    return "Wallpaper not found"


def web_fullscreen(request, wid):
    web = get_object_or_404(Web, id=wid)
    if web is not None:
        location = web.content_location
        store = web.store.all()
        if store.exists():
            store = store[0]
            brand = store.brand
            redirect = "/home/%s/" % store.slug_name
        else:
            device_id = request.device_id
            device = Device.objects.select_related("store").get(device_id=device_id)
            store = device.store
            brand = store.brand
            redirect = "/%s/" % store.slug_name
        context_instance = RequestContext(request,
                                          {'content': web, "redirect": redirect,
                                           "to": content_type_mapping[int(location)], "brand": brand})
        return render_to_response("web_template.html", context_instance)
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
        if store.has_custom_form:
            form = CustomFeedbackForm(request.POST)
            if form.is_valid():
                form.instance.store = store
                form.save()
                return HttpResponseRedirect("/home/%s/" % store.slug_name)
        else:
            form = FeedbackForm(request.POST)
            if form.is_valid():
                form.instance.store = store
                form.save()
                return HttpResponseRedirect("/home/%s/" % store.slug_name)
    if store.has_custom_form:
        form = CustomFeedbackForm()
    context = {'form': form, 'brand': store.brand, 'store': store, "redirect": redirect, "to": to}
    return render_to_response("store_feedback.html", context_instance=RequestContext(request, context))


@login_required
def display_feedback(request):
    feedback = StoreFeedback.objects.all()
    context_instance = RequestContext(request, {"feedback": feedback})
    return render_to_response("all_feedback.html", context_instance)


@login_required
def display_custom_feedback(request):
    feedback = CustomStoreFeedback.objects.all()
    context_instance = RequestContext(request, {"feedback": feedback})
    return render_to_response("custom_feedback.html", context_instance)


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
    # create_bc_user(request)
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
            return render_to_response("cluster_info.html", context_instance)
        return "No cluster assigned for the store"
    return "No Store assigned to device"


def store_info(request, storeid):
    store = get_object_or_404(Store, pk=storeid)
    contents = store.get_store_info()
    brand = store.brand
    redirect = "/home/%s" % store.slug_name
    to = "store"
    context_instance = RequestContext(request, {"contents": contents, "brand": brand, "redirect": redirect, "to": to})
    return render_to_response("store_info.html", context_instance)


def offer(request, offer_id):
    offer_obj = get_object_or_None(Offer, id=offer_id)
    if offer_obj is not None:
        store = offer_obj.store.all()
        if store:
            store = store[0]
            brand = store.brand
            redirect = "/home/%s" % store.slug_name
            to = "store"
        else:
            device = Device.objects.get(device_id=request.device_id)
            device_store = device.store
            if device_store is not None:
                store = device_store
                brand = store.brand
                redirect = "/home/%s" % store.slug_name
                to = "store"
        context_instance = RequestContext(request,
                                          {'content': offer_obj, "redirect": redirect,
                                           "to": to, "brand": brand, "stores": store.cluster.stores.all}
        )
        return render_to_response("offer_fullscreen.html", context_instance)
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
    ordered_content_ids = list(OrderedNavMenuContent.objects.filter(nav_menu__id=navmenu_id))
    ordered_ids = [item.content.id for item in ordered_content_ids]
    contents = list(Content.objects.select_subclasses().filter(id__in=ordered_ids))
    contents.sort(key=lambda content: ordered_ids.index(content.pk))
    for content in contents:
        setattr(content, 'own_store', device.store)
    context = {'contents': contents, 'store': device.store, 'brand': device.store.brand, "redirect": redirect, "to": to}
    context_instance = RequestContext(request, context)
    return render_to_response('store_home.html', context_instance)


@csrf_exempt
def call_log(request):
    log_bc_data.delay(post_params=request.POST,
                      date_time_custom=timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone()),
                      mac_address=request.META.get('HTTP_X_MAC_ADDRESS', ''),
                      user_unique_id=request.COOKIES.get('user_unique_id', ''),
                      device_id=request.device_id,
                      user_agent=request.META['HTTP_USER_AGENT'],
                      user_ip_address=request.META['REMOTE_ADDR'])
    data = json.dumps({})
    return HttpResponse(data, mimetype='application/json')


def free_internet_codes(request, st_id):
    store = Store.objects.get(pk=st_id)
    free_internet_code = FreeInternetLog.objects.filter(store=store, used_status=False)
    return render_to_response("free_internet_codes.html", {'store': store, 'codes': free_internet_code})


def retailer_credentials(request, cluster_id):
    cluster = get_object_or_None(Cluster, pk=cluster_id)
    stores = cluster.stores.all()
    print stores
    return render_to_response("retailer_codes.html", {'cluster': cluster, 'stores': stores})


@csrf_exempt
def upload_log(request):
    print request.POST
    file_path = save_file(request.FILES['file'], request.POST['device_id'])
    return HttpResponse(json.dumps({"Success": True}), mimetype='application/json')


def save_file(csv_file, device_id):
    filename = csv_file._get_name()
    direct = os.path.join(settings.LOG_SAVE_PATH, device_id)
    if not os.path.exists(direct):
        os.makedirs(direct)
    file_path = os.path.join(direct, filename)
    fd = open(file_path, 'wb')
    for chunk in csv_file.chunks():
        fd.write(chunk)
    fd.close()
    return True


def free_internet_confirm(request, content_id):
    dev_id = request.device_id
    device = get_object_or_None(Device, device_id=dev_id)
    store = device.store
    brand = store.brand
    redirect = "/%s/" % store.slug_name
    to = "store"
    context_instance = RequestContext(request,
                                      {"redirect": redirect, "to": to, "brand": brand, "content_id": content_id})
    return render_to_response("free_internet.html", context_instance)


@csrf_exempt
def authorize_free_internet(request):
    device_id = request.device_id
    device = get_object_or_None(Device, device_id=device_id)
    store = device.store
    if store is not None:
        fil = FreeInternetLog.objects.filter(store=store, used_status=False, code=request.POST['user_code'])
        if fil:
            fil = fil[0]
            fil.used_status = True
            fil.access_date = datetime.datetime.now()
            fil.device = device
            fil.user_name = request.POST["user_name"]
            fil.user_phone_number = request.POST["user_phone"]
            fil.save()
            return HttpResponse(json.dumps({'success': True, "log_obj": fil.id}), content_type="application/json")
        return HttpResponse(json.dumps({"success": False, "reason": "Invalid code"}), content_type="application/json")
    return HttpResponse(json.dumps({"success": False, "reason": "Store doesn't have free internet"}),
                        content_type="application/json")


def verify_log(request):
    logs = Log.objects.all().order_by("-id")[:10]
    # logs = list(logs)
    context_instance = RequestContext(request,
                                      {"logs": logs})
    return render_to_response("verify_log.html", context_instance)


def get_stores_within_range(request, latitude, longitude, radius):
    store = Store.objects.get_stores_in_radius(latitude, longitude)
    default_device = settings.DEFAULT_DEVICE_ID
    if store:
        devices = store.devices.all()
        if len(devices) > 0:
            return HttpResponse(json.dumps({"device": devices[0].device_id}), content_type="application/json")
    return HttpResponse(json.dumps({"device": default_device}), content_type="application/json")


def store_authenticate(request, user_name, password):
    store_obj = get_object_or_None(Store, username=user_name, password=password)
    if store_obj is not None:
        store_obj.create_auth_key()
        store_obj.save()
        return HttpResponse(json.dumps({"auth_key": store_obj.auth_key, "success": True}),
                            content_type="application/json")
    return HttpResponse(json.dumps({"success": False}), content_type="application/json")


def qr_log(request, user_id, auth_key, action):
    user_obj = get_object_or_None(BrandClubUser, user_id=user_id)
    if user_obj is not None:
        store = get_object_or_None(Store, auth_key=auth_key)
        device_id = 121
        log_info = dict(
            mac_address=user_obj.mac_id,
            access_date=datetime.datetime.now(),
            content_id=-5,
            content_name="Brandclub coupon",
            content_type="Offer",
            content_location="Cluster Home",
            content_owner_brand_id=-5,
            content_owner_brand_name="Offer",
            location_device_id=device_id,
            location_store_name=store.name,
            location_store_id=store.id,
            location_brand_id=store.brand.id,
            location_brand_name=store.brand.name,
            location_cluster_id=store.cluster.id,
            location_cluster_name=store.cluster.name,
            user_agent="",
            mobile_make='',
            mobile_model='',
            user_unique_id=user_obj.user_unique_id,
            user_ip_address="",
            user_device_width=0,
            user_device_height=0,
            page_title="Offer",
            referrer="",
            redirect_url="",
            action=action,
            city=store.city.name,
            state=store.state.name
        )
        log = Log(**log_info)
        log.save()


def coupon_redemption(request, user_id, auth_key):
    user_obj = get_object_or_None(BrandClubUser, user_id=user_id)
    if user_obj is not None:
        store = get_object_or_None(Store, auth_key=auth_key)
        if store is not None:
            device_id = 121
            if user_obj.coupon_generated_at == store:
                qr_log(request, user_id, auth_key, "Offer redemption failed")
                context_instance = RequestContext(request, {"valid": False})
                return render_to_response("point_scan_result.html", context_instance)
            user_obj.redeemed_coupon_at(store)
            user_obj.save()
            bcr_log = BrandClubRedemptionLog(bc_user=user_obj, store=store, cluster=store.cluster)
            bcr_log.save()
            qr_log(request, user_id, auth_key, "Offer redeemed")
            context_instance = RequestContext(request, {"valid": True})
            return render_to_response("point_scan_result.html", context_instance)
        qr_log(request, user_id, auth_key, "Offer redemption failed")
        context_instance = RequestContext(request, {"valid": False})
        return render_to_response("point_scan_result.html", context_instance)
    qr_log(request, user_id, auth_key, "Offer redemption failed")
    context_instance = RequestContext(request, {"valid": False})
    return render_to_response("point_scan_result.html", context_instance)


def redeem_coupon_for_user(request, user_id, ):
    context_instance = RequestContext(request)
    return render_to_response("point_scan_others.html", context_instance)


def redeem_coupon_for_user_retail(request, user_id, retailer_id):
    if retailer_id:
        user_obj = get_object_or_None(BrandClubUser, user_id=user_id)
        if user_obj is not None:
            store = get_object_or_None(Store, auth_key=retailer_id)
            if store is not None:
                device_id = 121
                user_obj.redeemed_coupon_at(store)
                user_obj.save()
                bcr_log = BrandClubRedemptionLog(bc_user=user_obj, store=store, cluster=store.cluster)
                bcr_log.save()
                qr_log(request, user_id, retailer_id, "Offer redeemed")
                context_instance = RequestContext(request, {"valid": True, "user_id": user_id, "store": store.id})
                return render_to_response("point_scan_result.html", context_instance)
        # qr_log(request, user_id, retailer_id, "Offer redeemed")
        context_instance = RequestContext(request, {"valid": False})
        return render_to_response("point_scan_result.html", context_instance)

    else:
        # request from xyz
        context_instance = RequestContext(request, {"valid": False})
        return render_to_response("point_scan_others.html", context_instance)


def retailer_form_sumbit(request, user_pk, store_pk, amount, phone):
    log_entry = BrandClubRetailerLog(user=user_pk, store_id=store_pk, amount=amount, phone_number=phone)
    log_entry.save()
    return HttpResponse(json.dumps({"success": True}), content_type="application/json")


def qr_valid_in_store(request):
    device_id = request.device_id
    device = get_object_or_None(Device, device_id=device_id)
    store = device.store
    mac_address = request.META.get('HTTP_X_MAC_ADDRESS', '')
    bcu = None
    if mac_address:
        bcu = get_object_or_None(BrandClubUser, mac_id=mac_address)
    else:
        user_unique_id = request.COOKIES.get('user_unique_id', '')
        bcu = get_object_or_None(BrandClubUser, user_unique_id=user_unique_id)
    if bcu is None:
        clust = store.cluster
        stores_in_cluster = clust.stores.all()
        stores_to_display = []
        for s in stores_in_cluster:
            if s.pk == store.pk:
                pass
            else:
                stores_to_display.append(s.name)
        return HttpResponse(json.dumps({"valid": False, "stores": stores_to_display}), content_type="application/json")
    else:
        if bcu.coupon_generated_at.pk == store.pk:
            clust = store.cluster
            stores_in_cluster = clust.stores.all()
            stores_to_display = []
            for s in stores_in_cluster:
                if s.pk == store.pk:
                    pass
                else:
                    stores_to_display.append(s.name)
            return HttpResponse(json.dumps({"valid": False, "stores": stores_to_display}),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({"valid": True}), content_type="application/json")


def create_bc_user(request):
    mac_address = request.META.get('HTTP_X_MAC_ADDRESS', '')
    user_unique_id = request.COOKIES.get('user_unique_id', '')
    device_id = request.device_id
    return create_user(mac_address, user_unique_id, device_id)


def create_brandclub_user(request):
    return create_bc_user(request)


def create_user(mac_address=None, user_unique_id=None, device_id=None):
    device = get_object_or_None(Device, device_id=device_id)
    store = None
    user = None
    if device is not None:
        store = device.store



    if mac_address and user_unique_id:
        user = get_object_or_None(BrandClubUser, user_unique_id=user_unique_id, mac_id=mac_address)

    if user is None and mac_address:
        user = get_object_or_None(BrandClubUser, mac_id=mac_address)

    if user is None and user_unique_id:
        user = get_object_or_None(BrandClubUser, user_unique_id=user_unique_id)

    if user:
        if mac_address:
            user.mac_id = mac_address

        if user_unique_id:
           user.user_unique_id = user_unique_id

        user.save()
        return HttpResponse(json.dumps({"valid": True, 'user_obj': user.pk}), content_type="application/json")

    if user is None:
        if user_unique_id is None:
            user_unique_id = "bc_%s" % id_generator()
        user = BrandClubUser(mac_id=mac_address, user_unique_id=user_unique_id, coupon_generated_at=store)
        user.save()
        return HttpResponse(json.dumps({"valid": True, 'user_obj': user.pk}), content_type="application/json")


def display_qr(request):
    mac_address = request.META.get('HTTP_X_MAC_ADDRESS', '')
    user_unique_id = request.COOKIES.get('user_unique_id', '')
    device_id = request.device_id
    if mac_address is not '':
        bcu = get_object_or_None(BrandClubUser, mac_id=mac_address)
        # bcu = BrandClubUser.objects.get(mac_id=mac_address)
        if bcu is None:
            bcu = create_user(mac_address=mac_address, user_unique_id=user_unique_id, device_id=device_id)
            bcu.save()

        context_instance = RequestContext(request, {"qr_link": bcu.qr_code})
        return HttpResponse(json.dumps(
            {
                "qr_link": bcu.qr_code,
                "header": "Flash this QR to avail discount",
                "desc": "Get a chance to win amazing prizes",
            }), content_type="application/json")
    else:
        bcu = get_object_or_None(BrandClubUser, user_unique_id=user_unique_id)
        # bcu = BrandClubUser.objects.get(user_unique_id=user_unique_id)
        if bcu is None:
            bcu = create_user(mac_address=None, user_unique_id=user_unique_id, device_id=device_id)
            bcu.save()
        context_instance = RequestContext(request, {"qr_link": bcu.qr_code})
        return HttpResponse(json.dumps(
            {
                "qr_link": bcu.qr_code,
                "header": "Flash this QR to avail discount",
                "desc": "Get a chance to win amazing prizes",
            }), content_type="application/json")