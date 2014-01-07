from .models import Device, Cluster


def brandclub_processor(request):
    cluster_id = request.cluster_id
    device_id = request.device_id
    device = Device.objects.select_related('store').get(device_id = device_id)
    cluster = Cluster.objects.select_related('stores').get(pk = cluster_id)
    return {
        "home_device" : device,
        "home_cluster" : cluster,
        'home_brand' : device.store.brand,
        'home_store' : device.store
    }