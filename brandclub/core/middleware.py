
class ClusterDeviceDetectionMiddleware(object):
    def process_request(self, request):
        device_id = request.META.get('X-DEVICE-ID', '121')
        cluster_id = request.META.get('X-CLUSTER-ID', '-1')
        request.cluster_id = cluster_id
        request.device_id = device_id
        return None