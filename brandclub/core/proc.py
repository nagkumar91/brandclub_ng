from django.conf import settings
from .models import Device, Cluster


def brandclub_processor(request):
    cluster_id = request.cluster_id
    device_id = request.device_id
    mac_id = request.mac_id
    device = None #Device.objects.select_related('store').get(device_id=device_id)
    cluster = None #Cluster.objects.select_related('stores').get(pk=cluster_id)
    return {
        "home_device": device,
        "home_cluster": cluster,
        'home_brand': None,
        'home_store': None,
        "mac_id": mac_id,
        "piwik_site_token": settings.PIWIK_SITE_TOKEN,
        "piwik_site_id": settings.PIWIK_SITE_ID
    }
