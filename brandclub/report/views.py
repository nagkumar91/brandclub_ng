from django.http import HttpResponse
# from ..core.models import *
import csv
# Create your views here.
from core.models import Device, Brand, Store, Content


def device_list(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="device_list.csv"'
    writer = csv.writer(response)
    devices = Device.objects.all()
    for d in devices:
        if d.store.active is True and d.store.demo is False:
            device_id = d.device_id
            store_id = d.store.id
            store_name = d.store.name.encode("utf-8")
            cluster_id = d.store.cluster.id
            cluster_name = d.store.cluster.name.encode("utf-8")
            city = d.store.cluster.city.name.encode("utf-8")
            brand = d.store.brand
            writer.writerow([device_id, store_id, store_name, cluster_id, cluster_name, city, brand.id])
    return response

def device_all_list(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="device_all_list.csv"'
    writer = csv.writer(response)
    devices = Device.objects.all()
    for d in devices:
        device_id = d.device_id
        store_id = d.store.id
        store_name = d.store.name.encode("utf-8")
        cluster_id = d.store.cluster.id
        cluster_name = d.store.cluster.name.encode("utf-8")
        city = d.store.cluster.city.name.encode("utf-8")
        brand = d.store.brand
        writer.writerow([device_id, store_id, store_name, cluster_id, cluster_name, city, brand.id, d.store.active, d.store.demo])
    return response


def footfall(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="footfall.csv"'
    writer = csv.writer(response)
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
    return response


def brand_clusters(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="brand_clusters.csv"'
    writer = csv.writer(response)
    writer.writerow(['partner_info_id', 'cluster_id'])
    brands = Brand.objects.all()
    for b in brands:
        brand_id = b.id
        stores = b.stores.all()
        for s in stores:
            cluster_id = s.cluster.id
            writer.writerow([brand_id, cluster_id])
    return response


def brand_associates(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="brand_associates.csv"'
    writer = csv.writer(response)
    writer.writerow(['Partner_id', 'associate_partner_id'])

    brands = Brand.objects.all()
    for b in brands:
        brand_id = b.id
        competitors = b.competitors.all()
        all_brands = Brand.objects.all()
        for nc in all_brands:
            if nc not in competitors and nc.id is not brand_id:
                writer.writerow([brand_id, nc.id])
    return response


def store_contents(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="store_contents.csv"'
    writer = csv.writer(response)
    writer.writerow(['store_id', 'cluster_id', 'content_id', 'content_name', 'content_type'])

    stores = Store.objects.filter(active=True, demo=False)

    for st in stores:
        objects = Content.active_objects.filter(store=st)
        for obj in objects:
            writer.writerow([st.id, st.cluster.id, obj.id, obj.name.encode("utf-8"), obj.content_type])

    return response


def brands_footfall(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="brands_footfall.csv"'
    writer = csv.writer(response)
    brands = Brand.objects.all()
    for b in brands:
        brand_id = b.id
        brand_name = b.name.encode("utf-8")
        brand_footfall = b.footfall
        stores = b.stores.filter(demo=False, active=True)
        competitors = b.competitors.all()
        for st in stores:
            store_name = st.name.encode("utf-8")
            store_id = st.id
            cluster_id = st.cluster.id
            cluster_name = st.cluster.name.encode("utf-8")
            city = st.city
            clust = st.cluster
            stores_in_cluster = clust.stores.filter(demo=False, active=True)
            for sic in stores_in_cluster:
                if sic.brand not in competitors and sic.id is not st.id:
                    assoc_partner_name = sic.brand.name.encode("utf-8")
                    assoc_partner_footfall = sic.brand.footfall
                    assoc_partner_id = sic.brand.id
                    assoc_store_id = sic.id
                    assoc_store_name = sic.name.encode("utf-8")
                    writer.writerow([
                        brand_id, brand_name, store_id, store_name, cluster_id, cluster_name, brand_footfall,
                        assoc_partner_id, assoc_partner_name, assoc_partner_footfall, assoc_store_id,
                        assoc_store_name, city])
    return response