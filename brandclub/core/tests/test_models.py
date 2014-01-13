import datetime
from django.db import IntegrityError
from django.test import TestCase
from ..models import Brand, Cluster, City, State, Wallpaper, ContentType, Store, Content, Device, OrderedStoreContent


class ClusterTestCase(TestCase):
    cluster = None
    ctype_wall = None
    some_store = None
    city = None
    state = None
    devices = None

    def _create_stores(self, count, brands):
        stores = []
        for i in range(count):
            store = Store.objects.create(name="S %s" % i, brand=brands[i], address_first_line="Some address",
                                         city=self.city, state=self.state, cluster=self.cluster, latitude=12.708,
                                         longitude=71.9, demo=False, paid=True)
            store.save()
            stores.append(store)
        return stores

    def _create_brands(self, count):
        brands = []
        for i in range(count):
            temp = Brand.objects.create(name="B %s" % i, slug_name="B-%s" % i, logo="/home/test/image.jpg", footfall=10)
            temp.save()
            brands.append(temp)
        return brands

    def _create_devices(self, count, stores):
        devices = []
        for i in range(count):
            device = Device.objects.create(device_id=i, type="Simple", store=stores[i])
            devices.append(device)
            device.save()
        return devices

    def _create_dummy_content(self, start_date, end_date, show_on_home_status, archived_status, active_status):
        b = Brand.objects.create(name="Temp brand", slug_name="temp_brand", logo="/home/test/image.jpg", footfall=10)
        b.save()
        s = Store.objects.create(name="Temp Store", brand=b, address_first_line="Some address", city=self.city,
                                 state=self.state, cluster=self.cluster, latitude=12.708, longitude=71.9,
                                 demo=False, paid=True)
        s.save()
        datestr = start_date
        expired_start = datetime.datetime.strptime(datestr, '%Y-%m-%d').date()
        datestr = end_date
        expired_end = datetime.datetime.strptime(datestr, '%Y-%m-%d').date()
        w = Wallpaper.objects.create(name="Expired Object 1", content_type=self.ctype_wall, start_date=expired_start,
                                     end_date=expired_end, show_on_home=show_on_home_status, active=active_status,
                                     archived=archived_status, content_location=2)
        o = OrderedStoreContent(store=s, content=w, order=1)
        w.save()
        o.save()

    def _create_content(self, stores, count=5):
        datestr = '2014-05-01'
        dateobj = datetime.datetime.strptime(datestr, '%Y-%m-%d').date()
        for i in range(count):
            w = Wallpaper.objects.create(name="name %s" % i, content_type=self.ctype_wall, end_date=dateobj,
                                         show_on_home=True)
            o = OrderedStoreContent(store=stores[i], content=w, order=i)
            w.save()
            o.save()

    def _create_initial_defaults(self):
        self.state = State.objects.create(name="Karnataka")
        self.state.save()
        self.city = City.objects.create(name="Bangalore")
        self.city.save()
        self.cluster = Cluster.objects.create(name="Cluster", city=self.city, state=self.state)
        self.cluster.save()
        self.ctype_wall = ContentType.objects.create(name="Wallpaper")

    def setUp(self):
        self._create_initial_defaults()
        brands = self._create_brands(5)
        stores = self._create_stores(5, brands)
        devices = self._create_devices(5, stores)
        self.devices = devices
        self._create_content(stores)
        self.some_store = stores[3]

    def test_is_data_empty_if_cluster_has_no_stores_available(self):
        city = City.objects.create(name='Bangalore')
        city.save()
        state = State.objects.create(name='Karnataka')
        state.save()
        cluster, created = Cluster.objects.get_or_create(name='Dummy', city=city, state=state)
        b = Brand.objects.create(name="Dummy", slug_name="dummy", logo="/home/test/image.jpg", footfall=10)
        b.save()
        s = Store.objects.create(name="dummy store", brand=b, address_first_line="Some address", city=self.city,
                                 state=self.state, cluster=self.cluster, latitude=12.708, longitude=71.9,
                                 demo=False, paid=True)
        s.save()
        dev = Device.objects.create(device_id=1234, type="Simple", store=s)
        dev.save()
        content = cluster.get_all_home_content(device_id=1234)
        self.assertEquals(0, len(content))

    def test_content_fetching_according_to_cluster_is_not_null(self):
        home_contents = self.__get_content_for_current_cluster()
        self.assertNotEqual(None, home_contents)

    def test_only_show_on_home_content_is_returned_for_each_brand_in_a_cluster(self):
        self._create_dummy_content('2011-04-01', '2014-05-01', False, False, True)
        home_contents = self.__get_content_for_current_cluster()
        all_contents = Content.objects.filter(store__in=self.cluster.stores.all())
        self.assertNotEqual(len(all_contents), len(home_contents))

    def test_no_expired_contents_are_returned(self):
        self._create_dummy_content('2011-05-04', '2011-06-05', True, False, True)
        home_contents = self.__get_content_for_current_cluster()
        all_contents = Content.objects.filter(store__in=self.cluster.stores.all())
        self.assertNotEqual(len(all_contents), len(home_contents))

    def test_all_contents_on_home_have_active_true(self):
        self._create_dummy_content('2011-05-04', '2014-06-07', True, False, False)
        home_contents = self.__get_content_for_current_cluster()
        all_contents = Content.objects.filter(store__in=self.cluster.stores.all())
        self.assertNotEqual(len(all_contents), len(home_contents))

    def test_all_contents_on_home_are_not_archived(self):
        self._create_dummy_content('2011-05-04', '2014-06-07', True, True, True)
        home_contents = self.__get_content_for_current_cluster()
        all_contents = Content.objects.filter(store__in=self.cluster.stores.all())
        self.assertNotEqual(len(all_contents), len(home_contents))

    def test_all_contents_has_first_from_current_cluster(self):
        self._create_dummy_content('2011-05-04', '2014-06-07', True, False, True)
        home_contents = self.__get_content_for_current_cluster()
        all_contents = Content.objects.filter(store__in=self.cluster.stores.all())
        self.assertNotEquals(home_contents[0].id, all_contents[0].id)

    def __get_content_for_current_cluster(self):
        cluster_id = self.cluster.id
        return self.cluster.get_all_home_content(4)

    def test_only_one_show_on_home_content_appears_for_each_brand_in_a_cluster(self):
        datestr = '2014-05-01'
        dateobj = datetime.datetime.strptime(datestr, '%Y-%m-%d').date()
        temp_wall_obj = Wallpaper.objects.create(name="un important wallpaper", content_type=self.ctype_wall,
                                                 end_date=dateobj, show_on_home=True)
        # temp_wall_obj.store.add(self.some_store)
        temp_wall_obj.save()
        o = OrderedStoreContent(store=self.some_store, content = temp_wall_obj, order = 100)
        o.save()
        home_contents = self.__get_content_for_current_cluster()
        all_contents = Content.objects.filter(store__in=self.cluster.stores.all())
        self.assertNotEqual(len(all_contents), len(home_contents))

    def test_content_from_active_stores_are_displayed(self):
        b = Brand.objects.create(name="Dummy", slug_name="dummy", logo="/home/test/image.jpg", footfall=10)
        b.save()
        s = Store.objects.create(name="dummy store", brand=b, address_first_line="Some address", city=self.city,
                                 state=self.state, cluster=self.cluster, latitude=12.708, longitude=71.9,
                                 demo=False, paid=True, active=False)
        s.save()
        dev = Device.objects.create(device_id=1234, type="Simple", store=s)
        dev.save()
        temp_wall_obj = Wallpaper.objects.create(name="un important wallpaper", content_type=self.ctype_wall,
                                                 show_on_home=True)
        # temp_wall_obj.store.add(s)
        temp_wall_obj.save()
        o = OrderedStoreContent(store = s, content = temp_wall_obj, order = 1000)
        o.save()
        all_contents = Content.objects.filter(store__in=self.cluster.stores.all())
        home_contents = self.__get_content_for_current_cluster()
        self.assertNotEqual(len(all_contents), len(home_contents))


class BrandTestCase(TestCase):
    store2 = None

    def setUp(self):
        store1 = Brand.objects.create(name="pnrao", description="some company", slug_name='pn-rao', footfall=10)
        store1.save()
        store2 = Brand.objects.create(name="ccd", description="another coffee shop", slug_name='ccd-123', footfall=10)
        store2.save()
        store1.competitors.add(store2)
        store1.save()
        self.store2 = store2

    def test_check(self):
        Brand.objects.create(name="B1", description="", logo="", footfall=10)
        with self.assertRaises(IntegrityError):
            Brand.objects.create(name="B1", description="", logo="", footfall=10)

    def test_image_tag_returns_proper_url(self):
        brand = Brand.objects.create(name="B1", description="Some desc", logo="/home/test/image.jpg", footfall=10)
        self.assertEquals(u"<img src='/home/test/image.jpg' style='height: 50px;max-width: auto'>", brand.image_tag())

    def test_for_brand_competitors(self):
        store, created = Brand.objects.get_or_create(name='pnrao', footfall=10)
        self.assertEquals("pnrao", store.name)
        all_competitors = self.store2.competitors.all()
        self.assertEquals(1, len(all_competitors))
        self.assertEquals(all_competitors[0].name, store.name)

    def test_brand_competition_is_symmetrical(self):
        store = Brand.objects.get(name="pnrao", footfall=10)
        competing_store = self.store2.competitors.all()[0]
        self.assertIsNotNone(competing_store)
        self.assertEquals(store.id, competing_store.id)
        self.assertEquals(store.name, competing_store.name)

    def _create_initial_defaults(self):
        self.state = State.objects.create(name="Karnataka")
        self.state.save()
        self.city = City.objects.create(name="Bangalore")
        self.city.save()
        self.cluster = Cluster.objects.create(name="Cluster", city=self.city, state=self.state)
        self.cluster.save()
        self.ctype_wall = ContentType.objects.create(name="Wallpaper")

    def test_competition_brand_is_excluded_in_our_store(self):
        self._create_initial_defaults()
        brand_names = ['b1', 'b2', 'b3', 'b4', 'b5']
        brands = []
        for name in brand_names:
            brand = Brand.objects.create(name=name, description="some company", slug_name=name, footfall=10)
            brand.save()
            brands.append(brand)
        b2 = brands[1]
        b2.competitors.add(brands[2])
        b2.competitors.add(brands[3])
        b2.save()
        self.assertEqual(2, len(b2.competitors.all()))
        store_names = ['s1', 's2', 's3', 's4', 's5']
        stores = []
        for idx, store in enumerate(store_names):
            brand = brands[idx]
            s = Store.objects.create(name=store, brand=brand, address_first_line="Some address", city=self.city,
                                     state=self.state, cluster=self.cluster, latitude=12.708, longitude=71.9,
                                     demo=False, paid=True)
            s.save()
            stores.append(s)

        datestr = '2014-05-01'
        dateobj = datetime.datetime.strptime(datestr, '%Y-%m-%d').date()
        for i in range(5):
            w = Wallpaper.objects.create(name="name %s" % i, content_type=self.ctype_wall, end_date=dateobj,
                                         show_on_home=True, content_location=2)
            w.save()
            o = OrderedStoreContent(store=stores[i], content=w, order=i)
            o.save()

        device = Device(device_id=3226, store=stores[1])
        device.save()
        cluster_id = self.cluster.id
        home_content = self.cluster.get_all_home_content(3226)
        self.assertEqual(3, len(home_content))
