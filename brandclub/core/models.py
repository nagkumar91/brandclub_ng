from django.db import models

# Create your models here.
from model_utils.models import TimeStampedModel


class Brand(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to="brand_logo")

    def image_tag(self):
        return u"<img src='%s' style='height: 50px;max-width: auto'>" % self.logo.url

    image_tag.short_description = "Logo image"
    image_tag.allow_tags = True

    def __unicode__(self):
        return self.name


class Cluster(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    locality = models.CharField(max_length=100)
    city = models.CharField(max_length=100, default="Bangalore")
    state = models.CharField(max_length=100, default="Karnataka")

    def __unicode__(self):
        return self.name


class Store(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    address_first_line = models.CharField(max_length=200)
    address_second_line = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=50, default='Bangalore')
    state = models.CharField(max_length=50, default='Karnataka')
    pin_code = models.CharField(max_length=10, null=True, blank=True)
    brand = models.ForeignKey(Brand, related_name='stores')
    cluster = models.ForeignKey(Cluster, related_name='stores', null=True)

    def __unicode__(self):
        return self.name


class Device(TimeStampedModel):
    device_id = models.IntegerField(max_length=6, unique=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    mac_address = models.CharField(max_length=20, null=True, blank=True)
    store = models.ForeignKey(Store, related_name='devices', null=True)

    def __unicode__(self):
        a = self.name
        return str(a)