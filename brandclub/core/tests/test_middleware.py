from django.http import HttpRequest
from django.test import TestCase
from ..middleware import ClusterDeviceDetectionMiddleware


class ClusterDetectionMiddlewareTest(TestCase):

    def test_middleware_returns_default_when_header_is_missing(self):
        request = HttpRequest()
        middleware = ClusterDeviceDetectionMiddleware()
        middleware.process_request(request)
        self.assertTrue(hasattr(request, 'cluster_id'))
        self.assertTrue(hasattr(request, 'device_id'))
        self.assertEquals(request.cluster_id, '-1')
        self.assertEquals(request.device_id, '121')

    def test_middleware_returns_proper_device_id(self):
        request = HttpRequest()
        request.META['X-CLUSTER-ID'] = '100'
        request.META['X-DEVICE-ID'] = '3226'
        middleware = ClusterDeviceDetectionMiddleware()
        middleware.process_request(request)
        self.assertTrue(hasattr(request, 'cluster_id'))
        self.assertTrue(hasattr(request, 'device_id'))
        self.assertEquals(request.cluster_id, '100')
        self.assertEquals(request.device_id, '3226')