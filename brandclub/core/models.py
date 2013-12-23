import datetime
from math import cos, sin, atan2, sqrt
import uuid
from model_utils.managers import InheritanceManager
import os
from ckeditor.fields import RichTextField
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
import json
# Create your models here.
from django.utils.text import slugify
from model_utils.models import TimeStampedModel
import requests
from .helpers import get_content_info_path, upload_and_rename_images, upload_and_rename_thumbnail, \
    ContentTypeRestrictedFileField
from south.modelsinspector import add_introspection_rules



add_introspection_rules([], ["^core\.helpers\.ContentTypeRestrictedFileField"])


def to_radians(degrees):
        return degrees * 0.0174532925


def to_degrees(radians):
    return radians * 57.2957795


class State(TimeStampedModel):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class City(TimeStampedModel):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Cities"
        verbose_name = "City"

    def __unicode__(self):
        return self.name


class Country(TimeStampedModel):
    name = models.CharField(max_length=100)


class Brand(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    slug_name = models.SlugField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to=upload_and_rename_thumbnail)
    bg_image = models.ImageField(upload_to="brand_background", blank=True, null=True)
    bg_color = models.CharField(max_length=6, blank=True, null=True, help_text='Please enter the hex code')
    competitors = models.ManyToManyField('Brand', related_name='competition', symmetrical=True, blank=True, null=True)

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
    map_name = models.CharField(max_length=200, blank=True, null=True, editable=False)
    city = models.ForeignKey(City, related_name="clusters")
    state = models.ForeignKey(State, related_name="clusters")

    def __unicode__(self):
        return self.name

    def get_all_home_content(self, device_id=settings.DEFAULT_DEVICE_ID):
        device = Device.objects.select_related().get(device_id=device_id)
        home_store = device.store
        all_contents = Content.active_objects.filter(show_on_home=True). \
            filter(store__in=(self.stores.exclude(brand__in=home_store.brand.competitors.all()))).order_by(
            'store__id').distinct('store__id')
        return all_contents

    def _find_center_of_cluster(self):
        locations = []
        for s in self.stores.all():
            lat = float(s.latitude)
            lat = to_radians(lat)
            lon = float(s.longitude)
            lon = to_radians(lon)
            locations.append([lat, lon])
        x = y = z = 0
        for lat, lon in locations:
            lat = float(lat)
            lon = float(lon)
            x += cos(lat) * cos(lon)
            y += cos(lat) * sin(lon)
            z += sin(lat)
        x = float(x / len(locations))
        y = float(y / len(locations))
        z = float(z / len(locations))
        lat = atan2(z, sqrt(x * x + y * y))
        lon = atan2(y, x)
        lat = to_degrees(lat)
        lon = to_degrees(lon)
        return lat, lon

    def _create_map_of_all_atms(self):
        center_lat, center_lon = self._find_center_of_cluster()
        url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?' \
              'key=AIzaSyBOtLGz2PvdRmqZBIVA4fj9VKhk3nyjpk8&location=%s,%s' \
              '&radius=2000&sensor=false&types=atm&' % (center_lat, center_lon)
        r = requests.get(url, stream=True)
        bank_lat_long = []
        if r.status_code == 200:
            json_result = json.loads(r.content)
            json_result = json_result["results"]
            for obj in json_result:
                bank_lat_long.append([obj["geometry"]["location"]["lat"], obj["geometry"]["location"]["lng"]])
        marker_string = "&markers="
        for lat, lon in bank_lat_long:
            marker_string += "%s,%s|" % (lat, lon)

        map_image_url = u"http://maps.google.com/maps/api/staticmap?center=%s,%s&zoom=15&size=600x600&sensor=false" \
                        u"&%s" % (center_lat, center_lon, marker_string)
        r = requests.get(map_image_url, stream=True)
        if r.status_code == 200:
            name = u"%s.png" % uuid.uuid4()
            directory = os.path.join(settings.MEDIA_ROOT, 'cluster_atms')
            if not os.path.exists(directory):
                os.makedirs(directory)

            file_name = os.path.join(settings.MEDIA_ROOT, 'cluster_atms', name)
            with open(file_name, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            self.map_name = name


class Store(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug_name = models.SlugField(max_length=100, default="-1")
    description = models.TextField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address_first_line = models.CharField(max_length=200)
    address_second_line = models.CharField(max_length=200, null=True, blank=True)
    map_name = models.CharField(max_length=200, null=True, blank=True, editable=False)
    city = models.ForeignKey(City, related_name="stores")
    state = models.ForeignKey(State, related_name="stores")
    pin_code = models.CharField(max_length=10, null=True, blank=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    mail_id = models.EmailField(max_length=50, null=True, blank=True)
    brand = models.ForeignKey(Brand, related_name='stores')
    cluster = models.ForeignKey(Cluster, related_name='stores', null=True)

    def create_slug(self):
        return slugify(self.name)

    def get_content_for_store(self):
        all_contents = Content.active_objects.filter(show_on_home=False, store=self.id)
        return all_contents

    def __unicode__(self):
        return self.name

    def _save_map_image(self):
        lat_str = str(self.latitude)
        long_str = str(self.longitude)
        map_image_url = u"http://maps.google.com/maps/api/staticmap?center=%s,%s&zoom=17&markers=color:blue|label" \
                        u":B|" \
                        "%s,%s&size=600x600&sensor=false" % (lat_str, long_str, lat_str, long_str)
        r = requests.get(map_image_url, stream=True)
        if r.status_code == 200:
            name = u"%s.png" % slugify(u'%s'%self.name)
            directory = os.path.join(settings.MEDIA_ROOT, settings.STORE_MAPS_DIRECTORY)
            if not os.path.exists(directory):
                os.makedirs(directory)

            file_name = os.path.join(settings.MEDIA_ROOT, settings.STORE_MAPS_DIRECTORY, name)
            with open(file_name, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            self.map_name = name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if settings.CREATE_STORE_MAPS is True:
            self._save_map_image()
        super(Store, self).save()

    def map_image_tag(self):
        name = self.map_name
        img_url = os.path.join(settings.STORE_MAPS_DIRECTORY, name)
        return u"<a href='%s' target='_blank'><img src='%s' style='height: 50px;max-width: auto'></a>" % (
            img_url, img_url)

    map_image_tag.allow_tags = True


class Device(TimeStampedModel):
    device_id = models.IntegerField(max_length=6, unique=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    mac_address = models.CharField(max_length=20, null=True, blank=True)
    store = models.ForeignKey(Store, related_name='devices', null=True)

    def __unicode__(self):
        return u'%d' % self.device_id


class ContentType(TimeStampedModel):
    name = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return self.name


class ContentManager(InheritanceManager):
    def get_queryset(self):
        date_time_today = datetime.datetime.now()
        return super(ContentManager, self).get_query_set(). \
            filter(active=True, archived=False, start_date__lte=date_time_today, end_date__gte=date_time_today)


class Content(TimeStampedModel):
    name = models.CharField(max_length=100)
    show_on_home = models.BooleanField(default=False)
    short_description = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    rating = models.IntegerField(default=5)
    no_of_people_rated = models.BigIntegerField(default=1)
    start_date = models.DateField(default=datetime.datetime.now)
    end_date = models.DateField(default=lambda: datetime.datetime.now() + datetime.timedelta(days=30))
    active = models.BooleanField(default=True)
    archived = models.BooleanField(default=False, help_text='Select this if you want to delete this content')
    thumbnail = models.ImageField(upload_to=upload_and_rename_thumbnail, verbose_name='Thumbnail for content',
                                  help_text='Ensure that the image size is 500x500')
    store = models.ManyToManyField(Store, related_name='contents', null=True, blank=True)
    content_type = models.ForeignKey(ContentType, related_name='contents')
    objects = InheritanceManager()
    active_objects = ContentManager()

    @property
    def thumbnail_url(self):
        if self.thumbnail and hasattr(self.thumbnail, 'url'):
            return self.thumbnail.url

    def image_tag(self):
        return u"<img src='%s' style='height: 50px;max-width: auto'>" % self.thumbnail_url

    image_tag.short_description = "Logo image"
    image_tag.allow_tags = True

    def __unicode__(self):
        return self.name


class Audio(Content):
    file = models.FileField(upload_to=get_content_info_path)


class Video(Content):
    file = ContentTypeRestrictedFileField(
        upload_to=get_content_info_path,
        content_types=['video/mp4', 'video/3gpp'],
    )
    #file = models.FileField(upload_to=get_content_info_path)


class Wallpaper(Content):
    file = models.ImageField(upload_to=get_content_info_path)


class Web(Content):
    content = RichTextField()


class Image(TimeStampedModel):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=upload_and_rename_images)
    caption = models.CharField(max_length=300, null=True, blank=True)
    target_url = models.URLField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class SlideShowImage(models.Model):
    slideshow = models.ForeignKey('SlideShow')
    image = models.ForeignKey(Image)
    order = models.IntegerField()

    class Meta:
        unique_together = ("slideshow", "order")
        ordering = ['order']

    def image_tag(self):
        return u"<img src='%s' style='height: 100px;max-width: auto'>" % self.image.image.url

    image_tag.short_description = "Slide Show Image"
    image_tag.allow_tags = True


class SlideShow(Content):
    image = models.ManyToManyField(Image, related_name='slideshow', through=SlideShowImage)