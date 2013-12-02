from django.db import IntegrityError
from django.test import TestCase
from core.models import Brand


class BrandTest(TestCase):

    def test_check(self):
        #self.assertEquals(1, 2)
        Brand.objects.create(name="B1", description="", logo="")
        with self.assertRaises(IntegrityError):
            Brand.objects.create(name="B1",description="", logo="")