from django.contrib import admin

# Register your models here.
from .models import Brand, Store, Cluster, Device


class BrandClubAdmin(admin.ModelAdmin):
    date_hierarchy = "created"


class DeviceInlineAdmin(admin.TabularInline):
    model = Device


class StoreAdmin(BrandClubAdmin):
    list_display = ('name', 'city', 'state', 'brand')
    search_fields = ('name', 'city', 'brand')
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
    list_display = ('name', 'type', 'store')
    search_fields = ('name', 'type', )
    list_filter = ('type',)
    pass

admin.site.register(Brand, BrandAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Cluster, ClusterAdmin)
admin.site.register(Device, DeviceAdmin)
