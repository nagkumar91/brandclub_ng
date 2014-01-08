from django.conf import settings


class ClusterDeviceDetectionMiddleware(object):
    def process_request(self, request):
        device_id = request.META.get('HTTP_X_DEVICE_ID', settings.DEFAULT_DEVICE_ID)
        cluster_id = request.META.get('HTTP_X_CLUSTER_ID', settings.DEFAULT_CLUSTER_ID)
        mac_id = request.META.get('HTTP_X_MAC_ADDRESS', settings.DEFAULT_MAC_ID)
        request.cluster_id = cluster_id
        request.device_id = device_id
        request.mac_id = mac_id
        return None