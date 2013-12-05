from django.test import TestCase
from ..models import Video, ContentType
from ..helpers import upload_and_rename_thumbnail


class HelperTest(TestCase):
    # noinspection
    def test_thumbnail_file_name_is_mangled(self):
        file_name = "hello.jpg"
        changed_name = upload_and_rename_thumbnail(None, file_name)
        self.assertNotEqual(file_name, changed_name)

    def test_content_file_name_is_mangled(self):
        content_type = ContentType(name='Video')
        video = Video(file='hello.mp4', content_type=content_type)
        file_name = "hello.mp4"
        changed_name = upload_and_rename_thumbnail(video, file_name)
        self.assertNotEqual(file_name, changed_name)