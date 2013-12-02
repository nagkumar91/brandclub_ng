from django.contrib import admin

# Register your models here.
from .models import Brand, Store, Cluster


class BrandClubAdmin(admin.ModelAdmin):
    date_hierarchy = "created"


class StoreAdmin(BrandClubAdmin):
    list_display = ('name', 'city', 'state', 'brand')


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
    inlines = [
        StoreInlineAdmin
    ]

admin.site.register(Brand, BrandAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Cluster, ClusterAdmin)

