import datetime
from django.db import models

# Create your models here.
from model_utils.models import TimeStampedModel
from .helpers import get_content_info_path, upload_and_rename_images, upload_and_rename_thumbnail


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
    description = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to=upload_and_rename_thumbnail)
    bg_image = models.ImageField(upload_to="brand_background", blank=True, null=True)
    bg_color = models.CharField(max_length=6, blank=True, null=True, help_text='Please enter the hex code')

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
    city = models.ForeignKey(City, related_name="clusters")
    state = models.ForeignKey(State, related_name="clusters")

    def __unicode__(self):
        return self.name


class Store(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    address_first_line = models.CharField(max_length=200)
    address_second_line = models.CharField(max_length=200, null=True, blank=True)
    city = models.ForeignKey(City, related_name="stores")
    state = models.ForeignKey(State, related_name="stores")
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
        return u'%d' % self.device_id


class ContentType(TimeStampedModel):
    name = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return self.name


class Content(TimeStampedModel):
    name = models.CharField(max_length=100)
    show_on_home = models.BooleanField(default=False)
    short_description = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    rating = models.IntegerField(default=5)
    no_of_people_rated = models.BigIntegerField(default=1)
    start_date = models.DateField(default=datetime.datetime.now)
    end_date = models.DateField()
    active = models.BooleanField(default=True)
    archived = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to=upload_and_rename_thumbnail)
    store = models.ManyToManyField(Store, related_name='contents', null=True, blank=True)
    content_type = models.ForeignKey(ContentType, related_name='contents')

    def image_tag(self):
        return u"<img src='%s' style='height: 50px;max-width: auto'>" % self.thumbnail.url

    image_tag.short_description = "Logo image"
    image_tag.allow_tags = True

    def __unicode__(self):
        return self.name


class Audio(Content):
    file = models.FileField(upload_to=get_content_info_path)


class Video(Content):
    file = models.FileField(upload_to=get_content_info_path)


class Wallpaper(Content):
    file = models.ImageField(upload_to=get_content_info_path)


class Web(Content):
    content = models.TextField()


class Image(TimeStampedModel):
    image = models.ImageField(upload_to = upload_and_rename_images)
    caption = models.CharField(max_length=300, null=True, blank=True)
    target_url = models.URLField()


class SlideShow(Content):
    image = models.ManyToManyField(Image, related_name='slideshow')
    order = models.IntegerField(default=1)