from django.db import IntegrityError
from django.test import TestCase
from ..models import Brand


class BrandTestCase(TestCase):

    def test_check(self):
        #self.assertEquals(1, 2)
        Brand.objects.create(name="B1", description="", logo="")
        with self.assertRaises(IntegrityError):
            Brand.objects.create(name="B1",description="", logo="")

    def test_image_tag_returns_proper_url(self):
        brand = Brand.objects.create(name="B1", description="Some desc", logo="/home/test/image.jpg")
        self.assertEquals(u"<img src='/home/test/image.jpg' style='height: 50px;max-width: auto'>", brand.image_tag())