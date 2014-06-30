from annoying.functions import get_object_or_None
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from django.conf import settings
from django.core.management import BaseCommand
from core.models import Cluster, Store, Brand, OrderedStoreContent, ContentType, Device, NavMenu
from django.test import Client
from optparse import make_option
import os
import shutil


def print_encoded(text):
    try:
        print text
    except UnicodeEncodeError:
        pass


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-d', dest='device_id', help="The id of the device"),
    )

    def generate_response(self, cluster_id, device_id, page):
        client = Client()
        response = client.get(page, **{'HTTP_X_CLUSTER_ID': cluster_id, 'HTTP_X_DEVICE_ID': device_id,
                                       'HTTP_HOST': settings.BRANDCLUB_HOST})
        print_encoded("Generating %s and got code %d " % (page, response.status_code))
        return response

    @staticmethod
    def _page_headers(cluster_id, device_id):
        return {'X_CLUSTER_ID': cluster_id, 'X_DEVICE_ID': device_id, 'HTTP_HOST': settings.BRANDCLUB_HOST}

    def _generate_page(self, dir, cluster_id, device_id, store):
        print_encoded("Generating contents for cluster %s and device %s " % (cluster_id, device_id))
        print_encoded("===================================================================")
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
            ctype_nav_menu = get_object_or_None(ContentType, name="Nav Menu")
            ctype_free_internet = get_object_or_None(ContentType, name="Free Internet")
            for individual_content in contents:
                content = individual_content.content
                if content.content_type.id == ctype_slideshow.id:
                    self._generate_slideshow(content.id, cluster_id, device_id, dir)
                if content.content_type.id == ctype_wallpaper.id:
                    self._generate_wallpapers(content.id, cluster_id, device_id, dir)
                if content.content_type.id == ctype_nav_menu.id:
                    self._generate_navmenu(content.id, cluster_id, device_id, dir)
                if content.content_type.id == ctype_free_internet.id:
                    self._generate_free_internet(content.id, cluster_id, device_id, dir)
        print_encoded("===================================================================")

    def _generate_main_page(self, slug, cluster_id, device_id, static_dir):
        page = "/%s/" % slug
        response = self.generate_response(cluster_id, device_id, page)
        content = response.content
        output_file = "/%s/%s" % (static_dir, slug)
        with open(output_file, 'w') as f:
            f.write(content)
            f.close()
        output_file = "/%s/%s" % (static_dir, "index.html")
        with open(output_file, 'w') as f:
            f.write(content)
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

    def _generate_free_internet(self, content_id, cluster_id, device_id, static_dir):
        page = "/free_internet_confirm/%s/" % content_id
        response = self.generate_response(cluster_id, device_id, page)
        output_file = "%s/free_internet_confirm" % static_dir
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

    def _generate_navmenu(self, wid, cluster_id, device_id, static_dir):
        page = "/navmenu/%s/" % wid
        response = self.generate_response(cluster_id, device_id, page)
        output_dir = "%s/navmenu" % static_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_file = "/%s/%s" % (output_dir, wid)
        with open(output_file, 'w') as f:
            f.write(response.content)
            f.close()
        navmenu = NavMenu.objects.get(id=wid)
        contents = navmenu.menu_contents.all()
        ctype_slideshow = get_object_or_None(ContentType, name="Slide Show")
        ctype_wallpaper = get_object_or_None(ContentType, name="Wallpaper")
        ctype_nav_menu = get_object_or_None(ContentType, name="Nav Menu")

        for content in contents:
            if content.content_type.id == ctype_slideshow.id:
                self._generate_slideshow(content.id, cluster_id, device_id, static_dir)
            if content.content_type.id == ctype_wallpaper.id:
                self._generate_wallpapers(content.id, cluster_id, device_id, static_dir)
            if content.content_type.id == ctype_nav_menu.id:
                self._generate_navmenu(content.id, cluster_id, device_id, static_dir)


    def handle(self, *args, **options):
        path = os.path.join(settings.CONTENT_CACHE_DIRECTORY, "content")
        if os.path.exists(path):
            shutil.rmtree(path)
        stores = []
        if not options['device_id']:
            stores = Store.objects.all()
        else:
            device_id = options['device_id']
            device = get_object_or_None(Device, device_id=device_id)
            stores.append(device.store)

        enable_s3 = True if settings.AWS_SECRET_KEY is not None else False
        conn = None
        if enable_s3:
            conn = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
        for store in stores:
            cluster = store.cluster.id
            print_encoded("Store is %s" % store.name)
            for device in store.devices.all():
                device_id = "%s" % device.device_id
                print_encoded("Device is %s" % device_id)
                static_dir = os.path.join(settings.CONTENT_CACHE_DIRECTORY, "content", device_id)
                if not os.path.exists(static_dir):
                    os.makedirs(static_dir)
                tar_dir = os.path.join(settings.CONTENT_CACHE_DIRECTORY, "content", "compressed")
                if not os.path.exists(tar_dir):
                    os.makedirs(tar_dir)
                self._generate_page(static_dir, cluster, device.device_id, store)
                file_name = "%s/%s.tar.gz" % (tar_dir, device_id)
                os.system("tar czf %s %s" % (file_name, static_dir))
                if conn:
                    bucket = conn.get_bucket(settings.AWS_BUCKET_NAME)
                    key = Key(bucket)
                    key.key = "%s.tar.gz" % device_id
                    key.set_contents_from_filename(file_name)
                    key.set_acl('public-read')




