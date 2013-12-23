import datetime
from django.conf import settings
from django.test import TestCase
from django.test.client import Client

from ..models import Brand, Cluster, City, State, Wallpaper, ContentType, Store, Device
from pyquery import PyQuery


class ClusterTestCase(TestCase):
    cluster = None
    state = None
    city = None
    stores = None

    def _create_brands(self, count=5):
        brands = []
        for i in range(count):
            temp = Brand.objects.create(name="B %s" % i, slug_name="B-%s" % i, logo="/home/test/image.jpg")
            temp.save()
            brands.append(temp)
        return brands

    def _create_stores(self, brands, count=5):
        stores = []
        for i in range(count):
            store = Store.objects.create(name="S %s" % i, slug_name="s-%s" % i, brand=brands[i],
                                         address_first_line="Some address", city=self.city, state=self.state,
                                         cluster=self.cluster, latitude=12.708, longitude=71.9)
            store.save()
            stores.append(store)
        device, created = Device.objects.get_or_create(device_id = settings.DEFAULT_DEVICE_ID, store=stores[1])
        device.save()
        return stores

    def _create_content(self, stores, count=5, show_on_home=True):
        datestr = '2014-05-01'
        ctype, status = ContentType.objects.get_or_create(name="Wallpaper")
        dateobj = datetime.datetime.strptime(datestr, '%Y-%m-%d').date()
        for i in range(count):
            w = Wallpaper.objects.create(name="name %s" % i, content_type=ctype, end_date=dateobj,
                                         show_on_home=show_on_home)
            w.store.add(stores[i])
            w.save()

    def _create_initial_defaults(self):
        self.state = State.objects.create(name="Karnataka")
        self.state.save()
        self.city = City.objects.create(name="Bangalore")
        self.city.save()
        self.cluster = Cluster.objects.create(name="Cluster", city=self.city, state=self.state)
        self.cluster.save()

    def setUp(self):
        self._create_initial_defaults()
        brands = self._create_brands(5)
        stores = self._create_stores(brands, 5)
        self.stores = stores
        self._create_content(stores)
        settings.DEFAULT_CLUSTER_ID = self.cluster.id

    def test_Cluster_View(self):
        client = Client()
        response = client.get("/B-1/")
        query = PyQuery(response.content)
        h5 = query("h5")
        self.assertTrue(5, len(h5))
        self.assertTrue("name 1", PyQuery(query("h5")[1]).html())