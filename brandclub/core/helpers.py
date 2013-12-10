from django.conf import settings
import os
import uuid
from django.db.models import FileField
from django.forms import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _


class ContentTypeRestrictedFileField(FileField):
    """
    Same as FileField, but you can specify:
        * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
        * max_upload_size - a number indicating the maximum file size allowed for upload.
            2.5MB - 2621440
            5MB - 5242880
            10MB - 10485760
            20MB - 20971520
            50MB - 5242880
            100MB 104857600
            250MB - 214958080
            500MB - 429916160
    """
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types")
        self.max_length = 300
        #self.max_upload_size = kwargs.pop("max_upload_size")

        super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)
        file = data.file
        try:
            content_type = file.content_type
            if content_type in self.content_types:
                pass
            else:
                raise forms.ValidationError(_('File type not supported.'))
        except AttributeError:
            pass
        print "Successful format"
        return data

    def __init__(self, content_types=None, **kwargs):
        self.content_types = content_types
        #self.max_upload_size = max_upload_size
        super(ContentTypeRestrictedFileField, self).__init__(**kwargs)



def _upload_and_rename(filename, media_dir):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(settings.MEDIA_ROOT, media_dir, filename)


def get_content_info_path(instance, filename):
    content_type_name = instance.content_type.name.lower()
    return _upload_and_rename(filename, content_type_name)


# noinspection PyUnusedLocal
def upload_and_rename_images(instance, filename):
    return _upload_and_rename(filename, "images")


# noinspection PyUnusedLocal
def upload_and_rename_thumbnail(instance, filename):
    return _upload_and_rename(filename, "thumbnails")


