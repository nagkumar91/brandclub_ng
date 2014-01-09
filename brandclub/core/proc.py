from annoying.functions import get_object_or_None
from django.conf import settings
from .models import Device, Cluster


def brandclub_processor(request):
    cluster_id = request.cluster_id
    device_id = request.device_id
    mac_id = request.mac_id
    device = get_object_or_None(Device, pk=device_id)
    cluster = get_object_or_None(Cluster, pk=cluster_id)
    return {
        "home_device": device,
        "home_cluster": cluster,
        'home_brand': device.store.brand if device else None,
        'home_store': device.store if device else None,
        "mac_id": mac_id,
        "piwik_site_token": settings.PIWIK_SITE_TOKEN,
        "piwik_site_id": settings.PIWIK_SITE_ID
    }
