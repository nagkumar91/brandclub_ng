from django.contrib import admin

# Register your models here.
from django.forms import ModelForm
from .models import Brand, Store, Cluster, Device, Audio, Video, Wallpaper, Web, SlideShow, Image, Content, \
    ContentType, State, City, SlideShowImage


class BrandClubAdmin(admin.ModelAdmin):
    date_hierarchy = "created"


class DeviceInlineAdmin(admin.TabularInline):
    model = Device


class StoreAdmin(BrandClubAdmin):
    list_display = ('name', 'city', 'state', 'brand', 'cluster', 'map_image_tag')
    search_fields = ('name', 'city', 'brand__name')
    list_filter = ('city', 'brand__name', 'cluster')
    inlines = [
        DeviceInlineAdmin
    ]


class StoreInlineAdmin(admin.TabularInline):
    model = Store


class BrandAdminForm(ModelForm):
    class Meta:
        model = Brand

    def __init__(self, *args, **kwargs):
        super(BrandAdminForm, self).__init__(*args, **kwargs)
        self.fields['competitors'].queryset = Brand.objects.exclude(
            id__exact=self.instance.id)


class BrandAdmin(BrandClubAdmin):
    list_display = ('name', 'description', 'image_tag', )
    readonly_fields = ('image_tag',)
    inlines = [
        StoreInlineAdmin
    ]
    form = BrandAdminForm
    filter_horizontal = ('competitors', )


class ClusterAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

    inlines = [
        StoreInlineAdmin
    ]


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'type', 'store', 'brand_device')
    search_fields = ('device_id', 'type', )
    list_filter = ('store', 'store__brand__name')
    list_select_related = True
    change_list_filter_template = "admin/filter_listing.html"

    def brand_device(self, obj):
        return "%s" % obj.store.brand.name

    brand_device.short_description = "Brand"


class ContentAdmin(admin.ModelAdmin):
    list_display = ('name', 'show_on_home', 'content_type', 'start_date', 'end_date')
    filter_horizontal = ("store", )

    def has_delete_permission(self, request, obj=None):
        return False


class SlideShowImageInline(admin.TabularInline):
    model = SlideShow.image.through
    readonly_fields = ('image_tag',)
    extra = 1


class SlideShowAdmin(ContentAdmin):
    filter_horizontal = ("store", "image")
    inlines = [
        SlideShowImageInline
    ]


class AudioAdmin(ContentAdmin):
    pass


class WebAdmin(ContentAdmin):
    pass


class WallpaperAdmin(ContentAdmin):
    pass


class VideoAdmin(ContentAdmin):
    pass


class ImageAdmin(admin.ModelAdmin):
    pass


class ContentTypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(City)
admin.site.register(State)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Cluster, ClusterAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Audio, AudioAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Wallpaper, WallpaperAdmin)
admin.site.register(Web, WebAdmin)
admin.site.register(SlideShow, SlideShowAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(ContentType, ContentTypeAdmin)
