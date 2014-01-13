from annoying.functions import get_object_or_None
from django.conf import settings
from .models import Device, Cluster


def brandclub_processor(request):
    device_id = request.device_id
    mac_id = request.mac_id
    device = get_object_or_None(Device, device_id=device_id)
    cluster = device.store.cluster if device else None
    return {
        "home_device": device,
        "home_cluster": cluster,
        'home_brand': device.store.brand if device else None,
        'home_store': device.store if device else None,
        "mac_id": mac_id,
        "piwik_site_token": settings.PIWIK_SITE_TOKEN,
        "piwik_site_id": settings.PIWIK_SITE_ID
    }
