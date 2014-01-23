import csv
from django.conf import settings
from django.core.management import BaseCommand
import os
import sys
from core.models import Device, Brand, Store, Content


class Command(BaseCommand):
    dir_path = settings.REPORT_DOWNLOAD_PATH

    @staticmethod
    def remove_comma(string):
        return string.replace(",", " ").replace('"', '')

    def device_list(self):
        file_name = "device_list.csv"
        complete_path = os.path.join(self.dir_path, file_name)
        if os.path.exists(complete_path):
            os.remove(complete_path)
        with open(complete_path, 'w+') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            devices = Device.objects.all()
            for d in devices:
                if d.store.active is True and d.store.demo is False:
                    device_id = d.device_id
                    store_id = d.store.id
                    store_name = d.store.name.encode("utf-8")
                    store_name = self.remove_comma(store_name)
                    cluster_id = d.store.cluster.id
                    cluster_name = d.store.cluster.name.encode("utf-8")
                    cluster_name = self.remove_comma(cluster_name)
                    city = d.store.cluster.city.name.encode("utf-8")
                    city = self.remove_comma(city)
                    brand = d.store.brand
                    writer.writerow([device_id, store_id, store_name, cluster_id, cluster_name, city, brand.id])
            csv_file.close()

    def footfall(self):
        file_name = "footfall.csv"
        complete_path = os.path.join(self.dir_path, file_name)
        if os.path.exists(complete_path):
            os.remove(complete_path)
        with open(complete_path, 'w+') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(['partner_info_id', 'total_outlets', 'footfalls_in_outlets', 'monthly_footfalls'])
            brands = Brand.objects.all()
            for b in brands:
                brand_id = b.id
                stores = b.stores.all()
                store_count = len(stores)
                store_footfall = store_count * b.footfall
                total_footfall = 0
                for s in stores:
                    clust = s.cluster
                    all_stores_in_cluster = Store.objects.filter(cluster=clust, active=True, demo=False). \
                        exclude(brand__in=b.competitors.all())
                    for st in all_stores_in_cluster:
                        total_footfall += st.brand.footfall
                writer.writerow([brand_id, store_count, store_footfall, total_footfall])
            csv_file.close()

    def brand_clusters(self):
        file_name = "brand_clusters.csv"
        complete_path = os.path.join(self.dir_path, file_name)
        if os.path.exists(complete_path):
            os.remove(complete_path)
        with open(complete_path, 'w+') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(['partner_info_id', 'cluster_id'])
            brands = Brand.objects.all()
            for b in brands:
                brand_id = b.id
                stores = b.stores.all()
                for s in stores:
                    cluster_id = s.cluster.id
                    writer.writerow([brand_id, cluster_id])
            csv_file.close()

    def brand_associates(self):
        file_name = "brand_associates.csv"
        complete_path = os.path.join(self.dir_path, file_name)
        if os.path.exists(complete_path):
            os.remove(complete_path)
        with open(complete_path, 'w+') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(['Partner_id', 'associate_partner_id'])
            brands = Brand.objects.all()
            for b in brands:
                brand_id = b.id
                competitors = b.competitors.all()
                all_brands = Brand.objects.all()
                for nc in all_brands:
                    if nc not in competitors and nc.id is not brand_id:
                        writer.writerow([brand_id, nc.id])
            csv_file.close()

    def store_contents(self):
        file_name = "store_contents.csv"
        complete_path = os.path.join(self.dir_path, file_name)
        if os.path.exists(complete_path):
            os.remove(complete_path)
        with open(complete_path, 'w+') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(['store_id', 'cluster_id', 'content_id', 'content_name', 'content_type'])
            stores = Store.objects.filter(active=True, demo=False)
            for st in stores:
                objects = Content.active_objects.filter(store=st)
                for obj in objects:
                    obj_name = obj.name.encode("utf-8")
                    obj_name = self.remove_comma(obj_name)
                    writer.writerow([st.id, st.cluster.id, obj.id, obj_name, obj.content_type])
            csv_file.close()

    def brands_footfall(self):
        file_name = "brands_footfall.csv"
        complete_path = os.path.join(self.dir_path, file_name)
        if os.path.exists(complete_path):
            os.remove(complete_path)
        with open(complete_path, 'w+') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            brands = Brand.objects.all()
            for b in brands:
                brand_id = b.id
                brand_name = b.name.encode("utf-8")
                brand_name = self.remove_comma(brand_name)
                brand_footfall = b.footfall
                stores = b.stores.filter(demo=False, active=True)
                competitors = b.competitors.all()
                for st in stores:
                    store_name = st.name.encode("utf-8")
                    store_name = self.remove_comma(store_name)
                    store_id = st.id
                    cluster_id = st.cluster.id
                    cluster_name = st.cluster.name.encode("utf-8")
                    cluster_name = self.remove_comma(cluster_name)
                    city = st.city.name
                    city = self.remove_comma(city)
                    clust = st.cluster
                    stores_in_cluster = clust.stores.filter(demo=False, active=True)
                    for sic in stores_in_cluster:
                        if sic.brand not in competitors and sic.id is not st.id:
                            assoc_partner_name = sic.brand.name.encode("utf-8")
                            assoc_partner_name = self.remove_comma(assoc_partner_name)
                            assoc_partner_footfall = sic.brand.footfall
                            assoc_partner_id = sic.brand.id
                            assoc_store_id = sic.id
                            assoc_store_name = sic.name.encode("utf-8")
                            assoc_store_name = self.remove_comma(assoc_store_name)
                            writer.writerow([
                                brand_id, brand_name, store_id, store_name, cluster_id, cluster_name, brand_footfall,
                                assoc_partner_id, assoc_partner_name, assoc_partner_footfall, assoc_store_id,
                                assoc_store_name, city])
            csv_file.close()

    def handle(self, *args, **options):
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)
        self.device_list()
        self.footfall()
        self.brand_clusters()
        self.brand_associates()
        self.store_contents()
        self.brands_footfall()
        print "Files created"

    @staticmethod
    def error(message, code=1):
        print message
        sys.exit(code)

