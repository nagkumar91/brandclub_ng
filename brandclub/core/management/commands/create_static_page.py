from django.conf import settings
from django.core.management import BaseCommand
from core.models import Cluster, Store, Brand
from django.test import Client
import os


class Command(BaseCommand):

    def _generate_page(self, dir, cluster_id, device_id, store):
        store_slug = store.slug_name
        self._generate_main_page(store_slug, cluster_id, device_id, dir)
        cluster = Cluster.objects.get(pk = cluster_id)
        stores = cluster.stores.all()
        for cluster_store in stores:
            slug = cluster_store.slug_name
            self._generate_store_home_page(slug, cluster_id, device_id, dir)

    def _generate_main_page(self, slug, cluster_id, device_id, static_dir):
        client = Client()
        page = "/%s/" % slug
        response = client.get(page, **{'X_CLUSTER_ID': cluster_id, 'X_DEVICE_ID': device_id})
        print "Generating %s and got code %d " % (slug, response.status_code)
        output_file = "/%s/%s" % (static_dir, slug)
        with open(output_file, 'w') as f:
            f.write(response.content)
            f.close()

    def _generate_store_home_page(self, slug, cluster_id, device_id, static_dir):
        client = Client()
        page = "/home/%s/" % slug
        response = client.get(page, **{'X_CLUSTER_ID': cluster_id, 'X_DEVICE_ID': device_id})
        print "Generating %s and got code %d " % (page, response.status_code)
        output_dir = "%s/home" % static_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_file = "/%s/%s" % (output_dir, slug)
        with open(output_file, 'w') as f:
            f.write(response.content)
            f.close()

    def handle(self, *args, **options):
        stores = Store.objects.all()
        for store in stores:
            cluster = store.cluster.id
            for device in store.devices.all():
                device_id = "%s" % device.device_id
                static_dir = os.path.join(settings.CONTENT_CACHE_DIRECTORY, "content", device_id)
                os.makedirs(static_dir)
                self._generate_page(static_dir, cluster, device.device_id, store)


