import datetime
from django.db import IntegrityError
from django.test import TestCase
from ..models import Brand, Cluster, City, State, Wallpaper, ContentType, Store, Content


class ClusterTestCase(TestCase):
    cluster = None
    ctype_wall = None
    some_store = None
    city = None
    state = None

    def _create_stores(self, count, brands):
        stores = []
        for i in range(count):
            store = Store.objects.create(name="S %s" % i, brand=brands[i], address_first_line="Some address",
                                         city=self.city, state=self.state, cluster=self.cluster)
            store.save()
            stores.append(store)
        return stores


    def _create_brands(self, count):
        brands = []
        for i in range(count):
            temp = Brand.objects.create(name="B %s" % i, slug_name="B-%s" % i, logo="/home/test/image.jpg")
            temp.save()
            brands.append(temp)
        return brands

    def _create_dummy_content(self, start_date, end_date, show_on_home_status, archived_status, active_status):
        b = Brand.objects.create(name="Temp brand", slug_name="temp_brand", logo="/home/test/image.jpg")
        b.save()
        s = Store.objects.create(name="Temp Store", brand=b, address_first_line="Some address", city=self.city,
                                 state=self.state, cluster=self.cluster)
        s.save()
        datestr = start_date
        expired_start = datetime.datetime.strptime(datestr, '%Y-%m-%d').date()
        datestr = end_date
        expired_end = datetime.datetime.strptime(datestr, '%Y-%m-%d').date()
        w = Wallpaper.objects.create(name="Expired Object 1", content_type=self.ctype_wall, start_date=expired_start,
                                     end_date=expired_end, show_on_home=show_on_home_status, active=active_status,
                                     archived=archived_status)
        w.store.add(s)
        w.save()

    def _create_content(self, stores, count=5):
        datestr = '2014-05-01'
        dateobj = datetime.datetime.strptime(datestr, '%Y-%m-%d').date()
        for i in range(count):
            w = Wallpaper.objects.create(name="name %s" % i, content_type=self.ctype_wall, end_date=dateobj,
                                         show_on_home=True)
            w.store.add(stores[i])
            w.save()

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

        self._create_content(stores)

        self.some_store = stores[3]


    def test_is_data_empty_if_cluster_has_no_stores_available(self):
        city = City.objects.create(name='Bangalore')
        city.save()
        state = State.objects.create(name='Karnataka')
        state.save()
        cluster, created = Cluster.objects.get_or_create(name='Dummy', city=city, state=state)
        content = cluster.get_all_home_content()
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

    def __get_content_for_current_cluster(self):
        return self.cluster.get_all_home_content()

    def test_only_one_show_on_home_content_appears_for_each_brand_in_a_cluster(self):
        datestr = '2014-05-01'
        dateobj = datetime.datetime.strptime(datestr, '%Y-%m-%d').date()
        temp_wall_obj = Wallpaper.objects.create(name="un important wallpaper", content_type=self.ctype_wall,
                                                 end_date=dateobj, show_on_home=True)
        temp_wall_obj.store.add(self.some_store)
        temp_wall_obj.save()
        home_contents = self.__get_content_for_current_cluster()
        all_contents = Content.objects.filter(store__in=self.cluster.stores.all())
        self.assertNotEqual(len(all_contents), len(home_contents))


class BrandTestCase(TestCase):
    def test_check(self):
        #self.assertEquals(1, 2)
        Brand.objects.create(name="B1", description="", logo="")
        with self.assertRaises(IntegrityError):
            Brand.objects.create(name="B1", description="", logo="")

    def test_image_tag_returns_proper_url(self):
        brand = Brand.objects.create(name="B1", description="Some desc", logo="/home/test/image.jpg")
        self.assertEquals(u"<img src='/home/test/image.jpg' style='height: 50px;max-width: auto'>", brand.image_tag())


class SlideShowTest(TestCase):
    pass