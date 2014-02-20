from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from .models import *


class StoreResource(ModelResource):
    class Meta:
        queryset = Store.objects.all()
        resource_name = 'store'


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


class WallpaperResource(ModelResource):
    class Meta:
        queryset = Wallpaper.objects.all()
        resource_name = 'wallpaper'


class ImageResource(ModelResource):
    class Meta:
        queryset = Image.objects.all()
        resource_name = 'image'
        excludes = ('image', )


class SlideShowImageResource(ModelResource):
    # image = fields.ForeignKey(ImageResource, 'image', full=True, null=True)
    # slideshow = fields.ForeignKey('core.api.SlideShowResource', 'slideshow')
    # order = fields.CharField('order', default=0)
    class Meta:
        queryset = SlideShowImage.objects.all()
        resource_name = 'slideshow_images'

    def full_dehydrate(self, bundle, for_list=False):
        print bundle.obj.__class__.__name__


class SlideShowResource(ModelResource):
    images = fields.ToManyField(SlideShowImageResource, 'image', full=True)

    class Meta:
        queryset = SlideShow.objects.all()
        resource_name = 'slideshow'


class ClusterContentResource(ModelResource):
    distance = fields.DecimalField(blank=True, null=True)
    content_type_name = fields.CharField()

    def get_object_list(self, request):
        device = Device.objects.get(device_id=request.device_id)
        cluster = device.store.cluster
        return cluster.get_all_home_content_queryset(request.device_id)

    def dehydrate_distance(self, bundle):
        request = bundle.request
        device = Device.objects.get(device_id=request.device_id)
        home_store = device.store
        stores = bundle.obj.store.all()
        # stores_in_cluster = Store.objects.filter(cluster_id=self.id, brand=stores[0].brand)
        content_owner = bundle.obj.store.filter(cluster_id=home_store.cluster.id)[:1]
        content_owner = content_owner[0]
        dist = home_store.get_distance_from(content_owner)
        dist -= dist % -10
        return dist

    def dehydrate_content_type_name(self, bundle):
        content_type = bundle.obj.content_type
        return content_type.name

    def dehydrate(self, bundle):
        if isinstance(bundle.obj, Wallpaper):
            wallpaper_resource = WallpaperResource()
            wallpaper_bundle = wallpaper_resource.build_bundle(obj=bundle.obj, request=bundle.request)
            bundle.data = wallpaper_resource.full_dehydrate(wallpaper_bundle).data
        elif isinstance(bundle.obj, SlideShow):
            resource = SlideShowResource()
            c_bundle = resource.build_bundle(obj=bundle.obj, request=bundle.request)
            bundle.data = resource.full_dehydrate(c_bundle).data
            print bundle.data

        return bundle

    class Meta:
        resource_name = 'cluster_content'
        queryset = Content.active_objects.select_subclasses()

