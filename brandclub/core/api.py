from django.conf.urls import url
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from .models import *


def dehydrate_subclasses(bundle):
    bundle.data = _dehydrate_content(bundle.obj, bundle)
    bundle.data['type_name'] = bundle.obj.content_type.name
    bundle.data['distance'] = dehydrate_distance(bundle)
    bundle.data['store_id'] = dehydrate_own_store(bundle)
    return bundle


def _dehydrate_content(content, request):
    resource = WallpaperResource()
    if isinstance(content, Wallpaper):
        resource = WallpaperResource()
    elif isinstance(content, SlideShow):
        resource = SlideShowResource()
    elif isinstance(content, Video):
        resource = VideoResource()
    elif isinstance(content, Audio):
        resource = AudioResource()

    c_bundle = resource.build_bundle(obj=content, request=request)
    c_bundle.data['type_name'] = content.content_type.name
    c_bundle.data['store_id'] = content.own_store.id
    if content.distance_from_home_store:
        c_bundle.data['distance'] = content.distance_from_home_store
    if resource:
        return resource.full_dehydrate(c_bundle).data
    return None

def _dehydrate_store_content(content, request):
    resource = WallpaperResource()
    if isinstance(content, Wallpaper):
        resource = WallpaperResource()
    elif isinstance(content, SlideShow):
        resource = SlideShowResource()
    elif isinstance(content, Video):
        resource = VideoResource()
    elif isinstance(content, Audio):
        resource = AudioResource()
    elif isinstance(content, FreeInternet):
        resource = FreeInternetResource()

    c_bundle = resource.build_bundle(obj=content, request=request)
    c_bundle.data['type_name'] = content.content_type.name
    c_bundle.data['store_id'] = content.own_store.id
    if resource:
        return resource.full_dehydrate(c_bundle).data
    return None


def dehydrate_distance(bundle):
    request = bundle.request
    device = Device.objects.get(device_id=request.device_id)
    home_store = device.store
    content_owner = bundle.obj.store.filter(cluster_id=home_store.cluster.id)[:1]
    dist = 100
    if len(content_owner) > 0:
        content_owner = content_owner[0]
        dist = home_store.get_distance_from(content_owner)
        dist -= dist % -10
    return dist


def dehydrate_own_store(bundle):
    request = bundle.request
    device = Device.objects.get(device_id=request.device_id)
    stores = bundle.obj.store.all()
    stores_in_cluster = Store.objects.filter(cluster_id=device.store.cluster.id, brand=stores[0].brand)
    return stores_in_cluster[0].id

class BrandResource(ModelResource):
    class Meta:
        queryset = Brand.objects.all()
        resource_name = 'brand'

class StoreResource(ModelResource):
    contents = fields.ToManyField('core.api.ContentResource', 'contents')
    brand = fields.ToOneField('core.api.BrandResource', 'brand')
    class Meta:
        queryset = Store.objects.all()
        resource_name = 'store'
        depth = 1

    def dehydrate_contents(self, bundle):
        store = bundle.obj
        contents = store.get_content_for_store()
        dehydrated = []
        for content in contents:
            dehydrated.append(_dehydrate_store_content(content, bundle.request))
        return dehydrated

    def dehydrate(self, bundle):
        store = bundle.obj
        brand = store.brand
        bundle.data['brand_id'] = brand.id
        return bundle

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/device/(?P<device_id>\d*)/$" % self._meta.resource_name,
                self.wrap_view('get_by_device_id'), name="api_get_by_device_id"),
        ]

    def get_by_device_id(self, request, **kwargs):
        device = Device.objects.get(device_id=int(kwargs['device_id']))
        store = device.store
        bundle = self.build_bundle(obj=store, request=request)
        bundle = self.full_dehydrate(bundle)
        bundle = self.alter_detail_data_to_serialize(request, bundle)
        return self.create_response(request, bundle)


class ClusterResource(ModelResource):
    contents = fields.ToManyField('core.api.ContentResource', 'contents', null=True)

    class Meta:
        queryset = Cluster.objects.all()
        resource_name = 'cluster'

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/device/(?P<device_id>\d*)/$" % self._meta.resource_name,
                self.wrap_view('get_by_device'), name="api_get_by_device"),
        ]

    def get_by_device(self, request, **kwargs):
        device = Device.objects.get(device_id=int(kwargs['device_id']))
        cluster = device.store.cluster
        bundle = self.build_bundle(obj=cluster, request=request)
        bundle = self.full_dehydrate(bundle)
        bundle = self.alter_detail_data_to_serialize(request, bundle)
        return self.create_response(request, bundle)

    def dehydrate_contents(self, bundle):
        cluster = bundle.obj
        device_id = bundle.request.device_id
        contents = cluster.get_all_home_content(device_id=device_id)
        dehydrated = []
        for content in contents:
            dehydrated.append(_dehydrate_content(content, bundle.request))
        return dehydrated


class DeviceResource(ModelResource):
    class Meta:
        model = Device
        queryset = Device.objects.all()
        resource_name = 'device'
        depth = 1

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/device_info/$" % self._meta.resource_name,
                self.wrap_view('get_device_info'), name="api_get_device_info"),
        ]

    def get_device_info(self, request, **kwargs):
        device_id = request.device_id
        if not device_id:
            device_id = settings.DEFAULT_DEVICE_ID
        device = Device.objects.get(device_id=device_id)
        bundle = self.build_bundle(obj=device, request=request)
        bundle = self.full_dehydrate(bundle)
        bundle = self.alter_detail_data_to_serialize(request, bundle)
        return self.create_response(request, bundle)


class ContentTypeResource(ModelResource):
    class Meta:
        model = ContentType
        queryset = ContentType.objects.all()


class ContentResource(ModelResource):
    content_type = fields.ToOneField(ContentTypeResource, 'content_type', full=True)
    store = fields.ToManyField(StoreResource, 'store', full=True)

    class Meta:
        queryset = Content.active_objects.select_subclasses()
        resource_name = 'content'

    def dehydrate(self, bundle):
        bundle = dehydrate_subclasses(bundle)
        bundle.data['content_type_name'] = bundle.obj.content_type.name
        print bundle.data
        return bundle


class WallpaperResource(ModelResource):
    class Meta:
        queryset = Wallpaper.objects.all()
        resource_name = 'wallpaper'


class ImageResource(ModelResource):
    class Meta:
        queryset = Image.objects.all()
        resource_name = 'image'


class SlideShowImageResource(ModelResource):
    image = fields.ToOneField(ImageResource, 'image', full=True, null=True)

    class Meta:
        queryset = SlideShowImage.objects.all()
        resource_name = 'slideshow_images'


class SlideShowResource(ModelResource):
    images = fields.ToManyField(SlideShowImageResource,
                                attribute=lambda bundle: bundle.obj.image.through.objects.filter(
                                    slideshow=bundle.obj) or bundle.obj.image, full=True)

    class Meta:
        queryset = SlideShow.objects.all()
        resource_name = 'slideshow'


class VideoResource(ModelResource):
    class Meta:
        queryset = Video.objects.all()
        resource_name = 'video'


class AudioResource(ModelResource):
    class Meta:
        queryset = Audio.objects.all()
        resource_name = 'audio'

class FreeInternetResource(ModelResource):
    class Meta:
        queryset = FreeInternet.objects.all()
        resource_name = 'free_internet'


class ClusterContentResource(ModelResource):
    distance = fields.DecimalField(blank=True, null=True)
    content_type_name = fields.CharField()

    def get_object_list(self, request):
        device = Device.objects.get(device_id=request.device_id)
        cluster = device.store.cluster
        return cluster.get_all_home_content_queryset(request.device_id)

    def dehydrate(self, bundle):
        return dehydrate_subclasses(bundle)

    class Meta:
        resource_name = 'cluster_content'
        queryset = Content.active_objects.select_subclasses()


class StoreContentResource(ModelResource):
    def get_detail(self, request, **kwargs):
        store = Store.objects.get(pk=kwargs['pk'])
        if store:
            content = store.get_content_for_store()
            bundle = self.build_bundle(obj=content, request=request)
            bundle = self.full_dehydrate(bundle)
            bundle = self.alter_detail_data_to_serialize(request, bundle)
            return self.create_response(request, bundle)
        return None

    def dehydrate(self, bundle):
        return dehydrate_subclasses(bundle)

    class Meta:
        resource_name = 'store_content'
        queryset = Content.active_objects.select_subclasses()
