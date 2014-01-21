from annoying.functions import get_object_or_None
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from django.conf import settings
from django.core.management import BaseCommand
from core.models import Cluster, Store, Brand, OrderedStoreContent, ContentType
from django.test import Client
import os
import shutil


class Command(BaseCommand):

    def generate_response(self, cluster_id, device_id, page):
        client = Client()
        response = client.get(page, **{'HTTP_X_CLUSTER_ID': cluster_id, 'HTTP_X_DEVICE_ID': device_id, 'HTTP_HOST' : settings.BRANDCLUB_HOST})
        print "Generating %s and got code %d " % (page, response.status_code)
        return response

    @staticmethod
    def _page_headers(cluster_id, device_id):
        return {'X_CLUSTER_ID': cluster_id, 'X_DEVICE_ID': device_id, 'HTTP_HOST' : settings.BRANDCLUB_HOST}

    def _generate_page(self, dir, cluster_id, device_id, store):
        print "Generating contents for cluster %s and device %s " % (cluster_id, device_id)
        print "==================================================================="
        self._generate_main_page(store.slug_name, cluster_id, device_id, dir)
        self._generate_cluster_info(cluster_id, device_id, dir)
        cluster = Cluster.objects.get(pk=cluster_id)
        stores = cluster.stores.all()
        for cluster_store in stores:
            slug = cluster_store.slug_name
            self._generate_store_home_page(slug, cluster_id, device_id, dir)
            self._generate_feedback_forms(cluster_store.id, cluster_id, device_id, dir)
            self._generate_store_info(cluster_store.id, cluster_id, device_id, dir)
            contents = OrderedStoreContent.objects.filter(store=cluster_store)
            ctype_slideshow = get_object_or_None(ContentType, name="Slide Show")
            ctype_wallpaper = get_object_or_None(ContentType, name="Wallpaper")
            for individual_content in contents:
                content = individual_content.content
                if content.content_type.id == ctype_slideshow.id:
                    self._generate_slideshow(content.id, cluster_id, device_id, dir)
                if content.content_type.id == ctype_wallpaper.id:
                    self._generate_wallpapers(content.id, cluster_id, device_id, dir)
        print "==================================================================="

    def _generate_main_page(self, slug, cluster_id, device_id, static_dir):
        page = "/%s/" % slug
        response = self.generate_response(cluster_id, device_id, page)
        output_file = "/%s/%s" % (static_dir, slug)
        with open(output_file, 'w') as f:
            f.write(response.content)
            f.close()

    def _generate_store_info(self, storeid, cluster_id, device_id, static_dir):
        page = "/si/%d/" % storeid
        response = self.generate_response(cluster_id, device_id, page)
        output_dir = "%s/si" % static_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_file = "/%s/%s" % (output_dir, storeid)
        with open(output_file, 'w') as f:
            f.write(response.content)
            f.close()

    def _generate_cluster_info(self, cluster_id, device_id, static_dir):
        page = "/ci/"
        response = self.generate_response(cluster_id, device_id, page)
        output_file = "/%s/ci" % static_dir
        with open(output_file, 'w') as f:
            f.write(response.content)
            f.close()

    def _generate_store_home_page(self, slug, cluster_id, device_id, static_dir):
        page = "/home/%s/" % slug
        response = self.generate_response(cluster_id, device_id, page)
        output_dir = "%s/home" % static_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_file = "/%s/%s" % (output_dir, slug)
        with open(output_file, 'w') as f:
            f.write(response.content)
            f.close()

    def _generate_feedback_forms(self, store_id, cluster_id, device_id, static_dir):
        page = "/feedback/%s/" % store_id
        response = self.generate_response(cluster_id, device_id, page)
        output_dir = "%s/feedback" % static_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_file = "/%s/%s" % (output_dir, store_id)
        with open(output_file, 'w') as f:
            f.write(response.content)
            f.close()

    def _generate_slideshow(self, ssid, cluster_id, device_id, static_dir):
        page = "/slideshow/%s/" % ssid
        response = self.generate_response(cluster_id, device_id, page)
        output_dir = "%s/slideshow" % static_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_file = "/%s/%s" % (output_dir, ssid)
        with open(output_file, 'w') as f:
            f.write(response.content)
            f.close()

    def _generate_wallpapers(self, wid, cluster_id, device_id, static_dir):
        page = "/wallpaper/%s/" % wid
        response = self.generate_response(cluster_id, device_id, page)
        output_dir = "%s/wallpaper" % static_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_file = "/%s/%s" % (output_dir, wid)
        with open(output_file, 'w') as f:
            f.write(response.content)
            f.close()

    def handle(self, *args, **options):
        path = os.path.join(settings.CONTENT_CACHE_DIRECTORY, "content")
        if os.path.exists(path):
            shutil.rmtree(path)
        stores = Store.objects.all()
        enable_s3 = True if settings.AWS_SECRET_KEY is not None else False
        conn = None
        if enable_s3:
            conn = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
        for store in stores:
            cluster = store.cluster.id
            print "Store is %s" % store.name
            for device in store.devices.all():
                device_id = "%s" % device.device_id
                print "Device is %s" % device_id
                static_dir = os.path.join(settings.CONTENT_CACHE_DIRECTORY, "content", device_id)
                os.makedirs(static_dir)
                tar_dir = os.path.join(settings.CONTENT_CACHE_DIRECTORY, "content", "compressed")
                if not os.path.exists(tar_dir):
                    os.makedirs(tar_dir)
                self._generate_page(static_dir, cluster, device.device_id, store)
                file_name = "%s/%s.tar.gz" % (tar_dir, device_id)
                os.system("tar czf %s %s" % (file_name, static_dir))
                if conn:
                    bucket = conn.get_bucket('tib.bcng.content')
                    key = Key(bucket)
                    key.key = "%s.tar.gz" % device_id
                    key.set_contents_from_filename(file_name)
                    key.set_acl('public-read')




