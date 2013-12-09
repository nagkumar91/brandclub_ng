from django.db import IntegrityError
from django.test import TestCase
from ..models import Brand


class BrandTestCase(TestCase):
    store2 = None

    def setUp(self):
        store1 = Brand.objects.create(name="pnrao", description="some company")
        store1.save()
        store2 = Brand.objects.create(name="ccd", description="another coeffee shop")
        store2.save()
        store1.competitors.add(store2)
        store1.save()
        self.store2 = store2


    def test_check(self):
        Brand.objects.create(name="B1", description="", logo="")
        with self.assertRaises(IntegrityError):
            Brand.objects.create(name="B1", description="", logo="")

    def test_image_tag_returns_proper_url(self):
        brand = Brand.objects.create(name="B1", description="Some desc", logo="/home/test/image.jpg")
        self.assertEquals(u"<img src='/home/test/image.jpg' style='height: 50px;max-width: auto'>", brand.image_tag())


    def test_for_brand_competitors(self):
        store = Brand.objects.get(name='pnrao')
        self.assertEquals("pnrao", store.name)
        all_competitors = store.competitors.all()
        self.assertEquals(1, len(all_competitors))
        self.assertEquals(all_competitors[0].id, self.store2.id)
        self.assertEquals(all_competitors[0].name, self.store2.name)

    def test_brand_competition_is_symmetrical(self):
        store = Brand.objects.get(name="pnrao")
        competing_store = self.store2.competitors.all()[0]
        self.assertIsNotNone(competing_store)
        self.assertEquals(store.id, competing_store.id)
        self.assertEquals(store.name, competing_store.name)






