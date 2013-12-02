from django.conf import settings
from django.db import models

# Create your models here.
from model_utils.models import TimeStampedModel


class Brand(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True)
    logo = models.ImageField(upload_to="%s/brand_logo" % settings.MEDIA_ROOT)

    def __unicode__(self):
        return self.name

