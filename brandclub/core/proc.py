from django.conf import settings
from django.core.cache import cache
from .models import Device, Cluster


def brandclub_processor(request):
    cluster_id = request.cluster_id
    device_id = request.device_id
    mac_id = request.mac_id
    device = cache.get("Device-%s" % device_id)
    if not device:
        device = Device.objects.select_related('store').get(device_id=device_id)
        cache.set('Device-%s' % device_id, device, 1800)
    cluster = cache.get("Cluster-%s" % device_id)
    if not cluster:
        cluster = Cluster.objects.select_related('stores').get(pk=cluster_id)
        cache.set('Cluster-%s' % cluster_id, cluster, 1800)
    return {
        "home_device" : device,
        "home_cluster" : cluster,
        'home_brand' : device.store.brand,
        'home_store' : device.store,
        "mac_id" : mac_id,
        "piwik_site_token" : settings.PIWIK_SITE_TOKEN,
        "piwik_site_id" : settings.PIWIK_SITE_ID
    }