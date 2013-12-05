from django.conf import settings
import os
import uuid


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

