import datetime
from django.db import models

# Create your models here.
from model_utils.models import TimeStampedModel
from .helpers import get_content_info_path, upload_and_rename_images, upload_and_rename_thumbnail, \
    ContentTypeRestrictedFileField
from south.modelsinspector import add_introspection_rules

add_introspection_rules([], ["^core\.helpers\.ContentTypeRestrictedFileField"])


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

    def get_all_home_content(self):
        date_time_today = datetime.datetime.now()
        all_contents = Content.objects.filter(show_on_home=True, end_date__gte=date_time_today,
                                              start_date__lte=date_time_today, active=True, archived=False).\
            filter(store__in=self.stores.all()).order_by('store__id').distinct('store__id')
        return all_contents


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
    archived = models.BooleanField(default=False, help_text='Select this if you want to delete this content')
    thumbnail = models.ImageField(upload_to=upload_and_rename_thumbnail, verbose_name='Thumbnail for content',
                                  help_text='Ensure that the image size is 500x500')
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
    file = ContentTypeRestrictedFileField(
        upload_to=get_content_info_path,
        content_types=['video/mp4', 'video/3gpp'],
    )
    #file = models.FileField(upload_to=get_content_info_path)


class Wallpaper(Content):
    file = models.ImageField(upload_to=get_content_info_path)


class Web(Content):
    content = models.TextField()


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
    order = models.IntegerField(default=1)