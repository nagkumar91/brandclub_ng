from annoying.functions import get_object_or_None
from caching.base import CachingMixin, CachingManager
import datetime
from django.core.cache import cache
from django.db.models import Q
from math import cos, sin, atan2, sqrt
from urllib import urlencode
import uuid
from model_utils.managers import InheritanceManager
import os
from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
import json
# Create your models here.
from django.utils.text import slugify
from model_utils.models import TimeStampedModel
import qrcode
import requests
from .helpers import get_content_info_path, upload_and_rename_images, upload_and_rename_thumbnail, \
    ContentTypeRestrictedFileField, id_generator
from south.modelsinspector import add_introspection_rules
from django_earthdistance.expressions import DistanceExpression
from django_earthdistance.functions import CubeDistance, LlToEarth
from djorm_expressions.models import ExpressionManager
from django import forms

add_introspection_rules([], ["^core\.helpers\.ContentTypeRestrictedFileField"])

RECOMMENDATION_OPTION_CHOICES = (
    ('0', 0),
    ('1', 1),
    ('2', 2),
    ('3', 3),
    ('4', 4)
)

PRODUCT_RANGE_OPTIONS = (
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('Not Sure', 'Not Sure'),
)

STAFF_OPTIONS = (
    ('Yes', 'Yes'),
    ('No', 'No'),
    ('Not Particularly', 'Not Particularly'),
)

OVERALL_EXPERIENCE_OPTIONS = (
    ('Very Bad', 'Very Bad'),
    ('Bad', 'Bad'),
    ('Neutral', 'Neutral'),
    ('Good', 'Good'),
    ('Excellent', 'Excellent'),
)

SHOPPING_LENGTH_OPTIONS = (
    ('First Time', 'First Time'),
    ('Less Than 3 Months', 'Less Than 3 Months'),
    ('One Year', 'One Year'),
    ('3 Years', '3 Years'),
    ('Five Years', 'Five Years'),
)


def to_radians(degrees):
    return float(degrees) * 0.0174532925


def to_degrees(radians):
    return radians * 57.2957795


class State(CachingMixin, TimeStampedModel):
    name = models.CharField(max_length=100)
    objects = CachingManager()

    def __unicode__(self):
        return self.name


class City(CachingMixin, TimeStampedModel):
    name = models.CharField(max_length=100)
    objects = CachingManager()

    class Meta:
        verbose_name_plural = "Cities"
        verbose_name = "City"

    def __unicode__(self):
        return self.name


class Country(TimeStampedModel):
    name = models.CharField(max_length=100)


class Brand(CachingMixin, TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    slug_name = models.SlugField(max_length=100, unique=True)
    footfall = models.IntegerField(null=True, default=0)
    description = models.TextField(null=True, blank=True)
    paid = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    logo = models.ImageField(upload_to=upload_and_rename_thumbnail)
    bg_image = models.ImageField(upload_to="brand_background", blank=True, null=True)
    bg_color = models.CharField(max_length=6, blank=True, null=True, help_text='Please enter the hex code')
    competitors = models.ManyToManyField('Brand', related_name='competition', symmetrical=True, blank=True, null=True)

    objects = CachingManager()

    def image_tag(self):
        return u"<img src='%s' style='height: 50px;max-width: auto'>" % self.logo.url

    image_tag.short_description = "Logo image"
    image_tag.allow_tags = True

    def __unicode__(self):
        return "%s - (%d)" % (self.name, self.pk)

    def save(self, *args, **kwargs):
        stores = self.stores.all()
        for st in stores:
            st.active = self.active
            st.save()
        super(TimeStampedModel, self).save(*args, **kwargs)


class Cluster(CachingMixin, TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    locality = models.CharField(max_length=100)
    map_name = models.CharField(max_length=200, blank=True, null=True, editable=False)
    city = models.ForeignKey(City, related_name="clusters")
    state = models.ForeignKey(State, related_name="clusters")
    content = models.ManyToManyField('Content', related_name='clusters', null=True, blank=True,
                                     limit_choices_to={"content_location": "3"})
    objects = CachingManager()

    def __unicode__(self):
        return self.name

    def get_all_home_content_queryset(self, device_id=settings.DEFAULT_DEVICE_ID):
        device = Device.objects.select_related("store").get(device_id=device_id)
        home_store = device.store
        cluster_id = home_store.cluster.id
        cache_key = "Cluster-Home-%s-%s" % (self.id, device_id)
        all_contents = Content.active_objects.select_related('store'). \
            filter(store__cluster__id=cluster_id).filter(content_location="2"). \
            filter(store__in=(self.stores.exclude(brand__in=home_store.brand.competitors.all()))). \
            filter(store__in=(self.stores.exclude(active=False))). \
            order_by('store__brand__id').distinct('store__brand__id')
        return all_contents

    def get_all_home_content(self, device_id=settings.DEFAULT_DEVICE_ID):
        device = Device.objects.select_related("store").get(device_id=device_id)
        home_store = device.store
        all_contents = self.get_all_home_content_queryset(device_id)
        contents = list(all_contents)

        for index, content in enumerate(contents):
            stores = content.store.all()
            stores_in_cluster = Store.objects.filter(cluster_id=self.id, brand=stores[0].brand)
            content_owner = content.store.filter(cluster_id=self.id)[:1]
            content_owner = content_owner[0]
            dist = home_store.get_distance_from(content_owner)
            dist -= dist % -10
            setattr(content, 'distance_from_home_store', int(dist))
            setattr(content, 'own_store', stores_in_cluster[0])
            setattr(content, 'paid', content_owner.brand.paid)
            setattr(content, 'redirect_url', "/home/%s" % content.own_store.slug_name)
        ctype_coupon = get_object_or_None(ContentType, name="Offer")
        coupons_in_cluster = self.content.filter(content_type=ctype_coupon).select_subclasses()
        coupons_in_cluster = list(coupons_in_cluster)
        for index, content in enumerate(coupons_in_cluster):
            setattr(content, 'distance_from_home_store', 0)
            setattr(content, 'is_coupon', True)
            setattr(content, 'redirect_url', "/offer/%s" % content.id)
            setattr(content, 'paid', True)
        for o in contents:
            coupons_in_cluster.append(o)
        return coupons_in_cluster

    def get_all_offers(self, device_id=settings.DEFAULT_DEVICE_ID, cluster_id=settings.DEFAULT_CLUSTER_ID):
        device = Device.objects.select_related("store").get(device_id=device_id)
        home_store = device.store
        offer_ctype = ContentType.objects.get_or_create(name="Offer")
        contents = Content.active_objects.select_related('store'). \
            filter(store__cluster__id=cluster_id). \
            filter(content_type=offer_ctype[0].id). \
            filter(store__in=(self.stores.exclude(brand__in=home_store.brand.competitors.all()))). \
            filter(store__in=(self.stores.exclude(active=False))). \
            order_by('store__id').distinct('store__id'). \
            select_subclasses()
        return contents

    def get_cluster_info(self):
        cache_key = "Cluster-Info-%s" % self.id
        contents = cache.get(cache_key)
        if not contents:
            all_contents = self.content.all().select_subclasses()
            contents = list(all_contents)
        return contents

    def _find_center_of_cluster(self):
        locations = []
        for s in self.stores.all():
            lat = to_radians(s.latitude)
            lon = to_radians(s.longitude)
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

    def create_wallpaper_for_cluster_info(self, image_file, img_type):
        wallpaper_ctype, flag = ContentType.objects.get_or_create(name="Wallpaper")
        widget_name = "%ss in %s" % (img_type.title().replace('_', ' '), self.name)
        wall_obj = Wallpaper.objects.create(name=widget_name, short_description=widget_name, content_location="3",
                                            thumbnail=image_file, content_type=wallpaper_ctype, file=image_file)
        self.content.add(wall_obj)
        self.save()

    def _create_static_map(self, img_type):
        widget_name = "%ss in %s" % (img_type.title().replace('_', ' '), self.name)
        try:
            if self.map_name is not None:
                file_name = os.path.join(settings.MEDIA_ROOT, 'cluster_%ss' % img_type, self.map_name)
                if file_name is not None:
                    os.remove(file_name)
        except OSError:
            pass

        obj = Wallpaper.objects.all().filter(name=widget_name).delete()
        center_lat, center_lon = self._find_center_of_cluster()
        url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?' \
              'key=%s&location=%s,%s' \
              '&radius=2000&sensor=false&types=%s&' % (settings.GOOGLE_STATIC_MAP_KEY, center_lat, center_lon, img_type)
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
            directory = os.path.join(settings.MEDIA_ROOT, 'cluster_%ss' % img_type)
            if not os.path.exists(directory):
                os.makedirs(directory)

            file_name = os.path.join(settings.MEDIA_ROOT, 'cluster_%ss' % img_type, name)
            with open(file_name, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            self.map_name = name
            self.save()
            file_relative_name = os.path.join(settings.MEDIA_URL, 'cluster_%ss' % img_type, name)
            self.create_wallpaper_for_cluster_info(file_relative_name, img_type)


class StoreManager(ExpressionManager):
    def get_stores_in_radius(self, lat, lng, radius=2500):
        latitude = float(lat)
        longitude = float(lng)
        stores = Store.objects.filter(~Q(brand_id=53)).annotate_functions(
            distance=CubeDistance(
                LlToEarth([latitude, longitude]), LlToEarth(['latitude', 'longitude'])
            )
        ).where(
            DistanceExpression(['latitude', 'longitude']).in_distance(radius, [latitude, longitude])
        ).order_by('distance')

        if len(stores) >= 1:
            return stores[0]
        return None


class Store(CachingMixin, TimeStampedModel):
    name = models.CharField(max_length=100)
    slug_name = models.SlugField(max_length=100, default="")
    description = models.TextField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    active = models.BooleanField(default=True)
    demo = models.BooleanField(default=False)
    paid = models.BooleanField(default=True)
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
    has_custom_form = models.BooleanField(default=False)
    custom_form_slug = models.CharField(max_length=1000, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    auth_key = models.CharField(max_length=100, null=True, blank=True)

    objects = StoreManager()

    def reset_user_credentials(self):
        self.username = self.create_slug()
        self.password = id_generator(size=8)
        self.save()

    def create_auth_key(self):
        if not self.auth_key:
            self.auth_key = id_generator(size=20)
            self.save()

    def get_distance_from(self, new_store):
        r = 6371
        dlat = to_radians(new_store.latitude - self.latitude)
        dlon = to_radians(new_store.longitude - self.longitude)
        a = sin(dlat / 2) * sin(dlat / 2) + cos(to_radians(self.latitude)) * cos(to_radians(new_store.latitude)) * sin(
            dlon / 2) * sin(dlon / 2)
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        d = r * c * 1000
        return d

    def create_slug(self):
        return slugify(self.name)


    def get_content_for_store(self, device_id=None):
        cache_key = "Store-Home-%s" % self.id
        contents = None
        is_own_store = self.is_home_store(device_id)
        if not contents:
            all_contents = []
            if self.active:
                all_contents = Content.active_objects.filter(content_location="1", store=self.id)
                if not is_own_store:
                    all_contents = all_contents.filter(display_in_store=False)
                all_contents = all_contents.select_subclasses()
            for index, content in enumerate(all_contents):
                stores = content.store.all()
                setattr(content, 'own_store', stores[0])
            contents = all_contents
            cache.set(cache_key, contents, settings.CACHE_TIME_OUT)
        return contents

    def get_store_info(self):
        cache_key = "Store-Info-%s" % self.id
        contents = cache.get(cache_key)
        if not contents:
            all_contents = []
            if self.active:
                all_contents = Content.active_objects.filter(content_location="4", store=self.id).select_subclasses()
            contents = all_contents
            cache.set(cache_key, contents, settings.CACHE_TIME_OUT)
        return contents

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
            name = u"%s.png" % slugify(u'%s' % uuid.uuid4())
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
        older_obj = get_object_or_None(Store, pk=self.pk)
        if older_obj:
            if older_obj.username != self.username:
                self.auth_key = ""
            if older_obj.password != self.password:
                self.auth_key = ""
        if settings.CREATE_STORE_MAPS is True:
            self._save_map_image()
        if self.brand.active is False:
            self.active = False
        super(Store, self).save()

    def map_image_tag(self):
        name = self.map_name
        img_url = os.path.join(settings.MEDIA_URL, settings.STORE_MAPS_DIRECTORY, name)
        return u"<a href='%s' target='_blank'><img src='%s' style='height: 50px;max-width: auto'></a>" % (
            img_url, img_url)

    def is_home_store(self, device_id):
        if not device_id:
            return False
        devices = self.devices.filter(device_id=device_id)
        return len(devices) > 0

    map_image_tag.allow_tags = True


class StoreFeedback(TimeStampedModel):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email_id = models.EmailField(max_length=100, blank=True, null=True)
    message = models.TextField(max_length=1000, )
    store = models.ForeignKey(Store, related_name="feedback")

    def __unicode__(self):
        return "Feedback from %s for %s " % (self.name, self.store.name)


class CustomStoreFeedback(TimeStampedModel):
    recommendation_options = models.CharField(max_length=2, choices=RECOMMENDATION_OPTION_CHOICES)
    product_range_options = models.CharField(max_length=20, choices=PRODUCT_RANGE_OPTIONS)
    staff_options = models.CharField(max_length=20, choices=STAFF_OPTIONS)
    overall_experience = models.CharField(max_length=20, choices=OVERALL_EXPERIENCE_OPTIONS)
    how_long_have_you_been_shopping = models.CharField(max_length=20, choices=SHOPPING_LENGTH_OPTIONS)
    any_other_feedback = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    store = models.ForeignKey(Store, related_name="custom_feedback")


class Device(CachingMixin, TimeStampedModel):
    device_id = models.IntegerField(max_length=6, unique=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    mac_address = models.CharField(max_length=20, null=True, blank=True)
    store = models.ForeignKey(Store, related_name='devices', null=True)

    objects = CachingManager()

    def __unicode__(self):
        return u'%d' % self.device_id


class ContentType(CachingMixin, TimeStampedModel):
    name = models.CharField(max_length=30, unique=True)
    objects = CachingManager()

    def __unicode__(self):
        return self.name


class ContentManager(InheritanceManager):
    def get_queryset(self):
        date_time_today = datetime.datetime.now()
        return super(ContentManager, self).get_query_set(). \
            filter(active=True, archived=False, start_date__lte=date_time_today,
                   end_date__gte=date_time_today).order_by('store_contents__order')


class OrderedStoreContent(models.Model):
    store = models.ForeignKey('Store')
    content = models.ForeignKey('Content', related_name="store_contents")
    order = models.IntegerField()

    class Meta:
        # unique_together = ("store", "order")
        ordering = ['order']


class OrderedNavMenuContent(models.Model):
    nav_menu = models.ForeignKey('NavMenu')
    content = models.ForeignKey('Content', related_name="nav_contents")
    order = models.IntegerField()

    class Meta:
        # unique_together = ("store", "order")
        ordering = ['order']


class Content(CachingMixin, TimeStampedModel):
    name = models.CharField(max_length=100)
    content_location = models.CharField(max_length=100,
                                        choices=[
                                            ("1", "Store Home"),
                                            ("2", "Cluster Home"),
                                            ("3", "Cluster Info"),
                                            ("4", "Store Info"),
                                            ("5", "User QR")
                                        ],
                                        default="1"
    )
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
    store = models.ManyToManyField(Store, related_name='contents', null=True, blank=True, through=OrderedStoreContent)
    content_type = models.ForeignKey(ContentType, related_name='contents')
    display_in_store = models.BooleanField(default=False)
    objects = InheritanceManager()
    active_objects = ContentManager()

    @property
    def thumbnail_url(self):
        if self.thumbnail and hasattr(self.thumbnail, 'url'):
            return self.thumbnail.url

    @property
    def template_file(self):
        return "partials/dummy.html"

    def image_tag(self):
        return u"<img src='%s' style='height: 50px;max-width: auto'>" % self.thumbnail_url

    image_tag.short_description = "Logo image"
    image_tag.allow_tags = True

    def __unicode__(self):
        return self.name


class NavMenu(Content):
    menu_contents = models.ManyToManyField(Content, related_name='ordered_contents', through=OrderedNavMenuContent,
                                           symmetrical=False)

    def template_file(self):
        return "partials/_navmenu.html"


class Audio(Content):
    file = models.FileField(upload_to=get_content_info_path)

    @property
    def template_file(self):
        return "partials/_audio.html"


class Video(Content):
    file = ContentTypeRestrictedFileField(
        upload_to=get_content_info_path,
        content_types=['video/mp4', 'video/3gpp'],
    )

    @property
    def template_file(self):
        return "partials/_video.html"


class Wallpaper(Content):
    file = models.ImageField(upload_to=get_content_info_path)

    @property
    def template_file(self):
        return "partials/_wallpaper.html"


class Web(Content):
    content = RichTextField()

    @property
    def template_file(self):
        return "partials/_web.html"


class WebContent(Content):
    url = models.CharField(max_length=255)

    @property
    def template_file(self):
        return "partials/_webcontent.html"

    @property
    def redirect_url_path(self):
        return "/redirect?url=%s" % urlencode(self.url)


class Offer(Content):
    authenticate_user = models.BooleanField(default=True)
    show_qr = models.BooleanField(default=False)
    file = models.ImageField(upload_to=get_content_info_path)

    @property
    def template_file(self):
        return "partials/_offer.html"


class Image(CachingMixin, TimeStampedModel):
    name = models.CharField(max_length=100, null=True, blank=True, default="Image_for_slideshow")
    image = models.ImageField(upload_to=upload_and_rename_images)
    caption = models.CharField(max_length=300, null=True, blank=True)
    target_url = models.URLField(null=True, blank=True)

    objects = CachingManager()

    def __unicode__(self):
        return self.name


class SlideShowImage(models.Model):
    slideshow = models.ForeignKey('SlideShow')
    image = models.ForeignKey(Image)
    order = models.IntegerField()

    class Meta:
        # unique_together = ("slideshow", "order")
        ordering = ['order']

    def image_tag(self):
        return u"<img src='%s' style='height: 100px;max-width: auto'>" % self.image.image.url

    image_tag.short_description = "Slide Show Image"
    image_tag.allow_tags = True


class SlideShow(Content):
    image = models.ManyToManyField(Image, related_name='slideshow', through=SlideShowImage)

    @property
    def template_file(self):
        return "partials/_slideshow.html"


class OfferDownloadInfo(TimeStampedModel):
    offer = models.ForeignKey(Offer, related_name='offer_download_info')
    user_name = models.CharField(max_length=50, unique=False)
    email_id = models.EmailField(max_length=100, unique=False, null=True)
    mobile_number = models.CharField(max_length=15, unique=False, null=True)


class FreeInternet(Content):
    @property
    def template_file(self):
        return "partials/_free_internet.html"

    class Meta:
        verbose_name_plural = 'Free Internet'


class FreeInternetLog(models.Model):
    code = models.CharField(max_length=10)
    created_date = models.DateTimeField(blank=True, null=True)
    store = models.ForeignKey(Store)
    used_status = models.BooleanField(default=False)
    access_date = models.DateTimeField(null=True, blank=True)
    device = models.ForeignKey(Device, blank=True, null=True)
    user_name = models.CharField(max_length=100, null=True, blank=True)
    user_phone_number = models.CharField(max_length=10, null=True, blank=True)


class Log(TimeStampedModel):
    mac_address = models.CharField(max_length=25, null=True, blank=True)
    content_id = models.CharField(max_length=100, null=True, blank=True)
    content_name = models.CharField(max_length=100, null=True, blank=True)
    content_type = models.CharField(max_length=100, null=True, blank=True)
    content_location = models.CharField(max_length=100, null=True, blank=True)
    content_owner_brand_id = models.IntegerField(null=True, blank=True)
    content_owner_brand_name = models.CharField(max_length=100, null=True, blank=True)
    location_device_id = models.IntegerField(null=True, blank=True)
    location_store_id = models.IntegerField(null=True, blank=True)
    location_store_name = models.CharField(max_length=100, null=True, blank=True)
    location_brand_id = models.IntegerField(null=True, blank=True)
    location_brand_name = models.CharField(max_length=100, null=True, blank=True)
    location_cluster_id = models.IntegerField(null=True, blank=True)
    location_cluster_name = models.CharField(max_length=200, null=True, blank=True)
    user_agent = models.CharField(max_length=300, null=True, blank=True)
    mobile_make = models.CharField(max_length=300, null=True, blank=True)
    mobile_model = models.CharField(max_length=300, null=True, blank=True)
    user_unique_id = models.CharField(max_length=100, null=True, blank=True)
    user_ip_address = models.CharField(max_length=100, null=True, blank=True)
    user_device_width = models.IntegerField(blank=True, null=True)
    user_device_height = models.IntegerField(blank=True, null=True)
    page_title = models.CharField(max_length=100, null=True, blank=True)
    referrer = models.CharField(max_length=500, null=True, blank=True)
    redirect_url = models.CharField(max_length=300, null=True, blank=True)
    action = models.CharField(max_length=100, null=True, blank=True)
    access_date = models.DateTimeField(default=datetime.datetime.now, blank=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)


class AppUserPreferenceCategory(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    def __unicode__(self):
        return self.name


class AppPreference(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    category = models.ForeignKey(AppUserPreferenceCategory, null=True, blank=True, related_name='category_preference')
    thumbnail = models.ImageField(upload_to=upload_and_rename_thumbnail, null=True, blank=True)

    def __unicode__(self):
        return self.name


class BrandClubAppUser(TimeStampedModel):
    device_id = models.CharField(max_length=500, blank=True, null=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    fb_id = models.CharField(max_length=150, null=True, blank=True)
    email_id = models.EmailField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    imei = models.CharField(max_length=50, null=True, blank=True)
    app_version = models.CharField(max_length=10, null=True, blank=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    mobile_make = models.CharField(max_length=100, blank=True, null=True)
    mobile_model = models.CharField(max_length=100, blank=True, null=True)
    profile_pic = models.CharField(max_length=500, blank=True, null=True)
    latitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    mobile_number = models.CharField(max_length=10, blank=True, null=True)
    registration_id = models.CharField(max_length=500, null=True, blank=True)
    enable_notifications = models.BooleanField(default=True)
    preferences = models.ManyToManyField(AppPreference, null=True, blank=True, related_name='bc_app_user')

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.device_id)


class BrandClubUser(TimeStampedModel):
    user_id = models.CharField(max_length=100, unique=True, primary_key=True)
    mac_id = models.CharField(max_length=100, null=True, blank=True)
    user_unique_id = models.CharField(max_length=100)
    coupon_current_value = models.IntegerField(default=0)
    loyalty_points = models.IntegerField(default=0)
    qr_code = models.CharField(max_length=250, null=True, blank=True)
    last_updated_time = models.DateTimeField(null=True, blank=True)
    coupon_generated_at = models.ForeignKey(Store, related_name='coupon_user', default=None, blank=True, null=True)

    def _create_qr_for_user(self):
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        link = "%sverify_user/%s" % (settings.API_URL_DOMAIN, self.user_id)
        link = "http://brandclub.mobi/rd_qr/%s/" % self.user_id
        data = {
            "a": 1,
            "c": self.user_id
        }
        data = json.dumps(data)
        qr.add_data(link)
        qr.make(fit=True)
        img = qr.make_image()
        img_name = "%s.png" % self.user_id
        directory = os.path.join(settings.MEDIA_ROOT, 'user_qr')
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_name = os.path.join(settings.MEDIA_ROOT, 'user_qr', img_name)
        file_path = os.path.join(settings.MEDIA_URL, 'user_qr', img_name)
        with open(file_name, 'wb') as f:
            img.save(f, "PNG")
        self.qr_code = file_path

    def redeemed_coupon_at(self, store):
        self.coupon_current_value = settings.DEFAULT_COUPON_VALUE
        self.loyalty_points += settings.DEFAULT_LOYALTY_INCREMENT
        self.coupon_generated_at = store
        self.last_updated_time = datetime.datetime.now()
        self.save()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.user_id == "":
            self.coupon_current_value = settings.DEFAULT_COUPON_VALUE
            self.user_id = id_generator()
        if self.qr_code is None:
            self._create_qr_for_user()
        super(BrandClubUser, self).save()

    def __unicode__(self):
        return "%s-%s-%s" % (self.user_id, self.mac_id, self.user_unique_id)


class BrandClubRedemptionLog(TimeStampedModel):
    bc_user = models.ForeignKey(BrandClubUser, null=True, blank=True)
    store = models.ForeignKey(Store, null=True, blank=True)
    cluster = models.ForeignKey(Cluster, null=True, blank=True)
    log_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s-%s-%s" % (self.bc_user, self.store, self.cluster)


class BrandClubRetailerLog(models.Model):
    user = models.CharField(max_length=250, null=True, blank=True)
    store_id = models.CharField(max_length=250, null=True, blank=True)
    amount = models.CharField(max_length=250, null=True, blank=True)
    phone_number = models.CharField(max_length=250, null=True, blank=True)

    def __unicode__(self):
        return self.user