from django.conf import settings

from django import http

class ClusterDeviceDetectionMiddleware(object):
    def process_request(self, request):
        device_id = request.META.get('HTTP_X_DEVICE_ID', settings.DEFAULT_DEVICE_ID)
        cluster_id = request.META.get('HTTP_X_CLUSTER_ID', settings.DEFAULT_CLUSTER_ID)
        mac_id = request.META.get('HTTP_X_MAC_ADDRESS', settings.DEFAULT_MAC_ID)
        request.cluster_id = cluster_id
        request.device_id = device_id
        request.mac_id = mac_id
        return None




XS_SHARING_ALLOWED_ORIGINS = '*'
XS_SHARING_ALLOWED_METHODS = ['POST', 'GET', 'OPTIONS', 'PUT', 'DELETE']


class XsSharing(object):
    """
        This middleware allows cross-domain XHR using the html5 postMessage API.


        Access-Control-Allow-Origin: http://foo.example
        Access-Control-Allow-Methods: POST, GET, OPTIONS, PUT, DELETE
    """

    def process_request(self, request):

        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            response = http.HttpResponse()
            response['Access-Control-Allow-Origin'] = XS_SHARING_ALLOWED_ORIGINS
            response['Access-Control-Allow-Methods'] = ",".join(XS_SHARING_ALLOWED_METHODS)
            response['Access-Control-Allow-Headers'] = "*"

            return response

        return None

    def process_response(self, request, response):
        # Avoid unnecessary work
        if response.has_header('Access-Control-Allow-Origin'):
            return response

        response['Access-Control-Allow-Origin'] = XS_SHARING_ALLOWED_ORIGINS
        response['Access-Control-Allow-Methods'] = ",".join(XS_SHARING_ALLOWED_METHODS)

        return response