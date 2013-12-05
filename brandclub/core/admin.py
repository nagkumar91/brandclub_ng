from django.contrib import admin

# Register your models here.
from .models import Brand, Store, Cluster, Device, Audio, Video, Wallpaper, Web, SlideShow, Image, Content, \
    ContentType, State, City


class BrandClubAdmin(admin.ModelAdmin):
    date_hierarchy = "created"


class DeviceInlineAdmin(admin.TabularInline):
    model = Device


class StoreAdmin(BrandClubAdmin):
    list_display = ('name', 'city', 'state', 'brand', 'cluster')
    search_fields = ('name', 'city', 'brand__name')
    list_filter = ('city', 'brand__name', 'cluster')
    inlines = [
        DeviceInlineAdmin
    ]


class StoreInlineAdmin(admin.TabularInline):
    model = Store


class BrandAdmin(BrandClubAdmin):
    list_display = ('name', 'description', 'image_tag')
    readonly_fields = ('image_tag',)
    inlines = [
        StoreInlineAdmin
    ]


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


class AudioAdmin(admin.ModelAdmin):
    pass


class WebAdmin(admin.ModelAdmin):
    pass


class WallpaperAdmin(admin.ModelAdmin):
    pass


class VideoAdmin(admin.ModelAdmin):
    pass


class SlideShowAdmin(admin.ModelAdmin):
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
