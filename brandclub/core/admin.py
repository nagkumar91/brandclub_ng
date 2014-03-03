import datetime
from django import forms
from django.contrib import admin

# Register your models here.
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from .models import Brand, Store, Cluster, Device, Audio, Video, Wallpaper, Web, SlideShow, Image, ContentType,\
    State, City, WebContent, StoreFeedback, Content, Offer, OrderedStoreContent, OrderedNavMenuContent, NavMenu


class BrandClubAdmin(admin.ModelAdmin):
    date_hierarchy = "created"


class DeviceInlineAdmin(admin.TabularInline):
    model = Device


class OrderContentStoreInline(admin.TabularInline):
    model = Content.store.through
    sortable_field_name = 'order'


class StoreAdmin(BrandClubAdmin):
    list_display = ('name', 'slug_name', 'city', 'state', 'brand', 'cluster', 'store_device')
    search_fields = ('name', 'slug_name', 'city', 'brand__name')
    list_filter = ('city', 'brand__name', 'cluster')
    save_as = True
    inlines = [
        OrderContentStoreInline,
        DeviceInlineAdmin
    ]

    def store_device(self, obj):
        return ",".join(["%s" % d.device_id for d in obj.devices.all()])


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
    list_display = ('pk', 'name', 'description', 'image_tag', )
    list_display_links = ('pk', 'name')
    readonly_fields = ('image_tag',)
    inlines = [
        StoreInlineAdmin
    ]
    form = BrandAdminForm
    filter_horizontal = ('competitors', )


class ClusterAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', )
    filter_horizontal = ('content', )
    search_fields = ('name',)
    actions = ['create_atm_map_for_cluster']
    inlines = [
        StoreInlineAdmin
    ]

    def create_atm_map_for_cluster(self, request, queryset):
        for c in queryset:
            c._create_map_of_all_atms()
        self.message_user(request, "Successfully created the map image.")

    actions = ['generate_atm_images']

    def generate_atm_images(self, request, queryset):
        for clust in queryset:
            clust._create_map_of_all_atms()
        self.message_user(request, "Successfully generated images.")


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
    list_display = ('name', 'content_location', 'content_type', 'start_date', 'end_date')
    list_filter = ('content_location', )
    filter_horizontal = ("store", )
    save_as = True
    actions = ['assign_to_brand', 'increase_validity_by_1_month']

    def has_delete_permission(self, request, obj=None):
        return False

    class BrandSelectForm(forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        brand = forms.ModelChoiceField(Brand.objects)

    def assign_to_brand(self, request, queryset):
        form = None

        if 'apply' in request.POST:
            form = self.BrandSelectForm(request.POST)
            if form.is_valid():
                brand = form.cleaned_data['brand']

                for content in queryset:
                    stores = Store.objects.filter(brand=brand)
                    for st in stores:
                        order_index = 0
                        all_ordered_content = OrderedStoreContent.objects.filter(store=st)
                        for aoc in all_ordered_content:
                            if aoc.order > order_index:
                                order_index = aoc.order
                        order_index += 1
                        o = OrderedStoreContent(store=st, order=order_index, content=content)
                        o.save()

                self.message_user(request, "Done!")
                return HttpResponseRedirect(request.get_full_path())

        if not form:
            form = self.BrandSelectForm(
                initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)}
            )
        context = {'contents': queryset, 'brand_form': form}
        return render_to_response('add_tag.html', RequestContext(request,context))

    def increase_validity_by_1_month(self, request, queryset):

        form = None
        for content in queryset:
            old_end_date = content.end_date
            new_end_date = old_end_date + datetime.timedelta(days=30)
            content.end_date = new_end_date
            content.save()
        self.message_user(request, "Done!")



class ContentNonEditableAdmin(admin.ModelAdmin):
    actions = ['assign_to_brand', 'increase_validity_by_1_month']
    list_display = ('name', 'content_location', 'content_type', 'image_tag', 'start_date', 'end_date',
                    'active', 'archived',)
    list_filter = ('content_location', 'content_type', 'store', 'store__brand', 'active', 'archived')
    filter_horizontal = ("store", )
    search_fields = ('name', )
    date_hierarchy = "created"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    class BrandSelectForm(forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        brand = forms.ModelChoiceField(Brand.objects)

    def assign_to_brand(self, request, queryset):
        form = None

        if 'apply' in request.POST:
            form = self.BrandSelectForm(request.POST)
            if form.is_valid():
                brand = form.cleaned_data['brand']

                for content in queryset:
                    stores = Store.objects.filter(brand=brand)
                    for st in stores:
                        order_index = 0
                        all_ordered_content = OrderedStoreContent.objects.filter(store=st)
                        for aoc in all_ordered_content:
                            if aoc.order > order_index:
                                order_index = aoc.order
                        order_index += 1
                        o = OrderedStoreContent(store=st, order=order_index, content=content)
                        o.save()

                self.message_user(request, "Done!")
                return HttpResponseRedirect(request.get_full_path())

        if not form:
            form = self.BrandSelectForm(
                initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)}
            )
        context = {'contents': queryset, 'brand_form': form}
        return render_to_response('add_tag.html', RequestContext(request,context))

    def increase_validity_by_1_month(self, request, queryset):

        form = None
        for content in queryset:
            old_end_date = content.end_date
            new_end_date = old_end_date + datetime.timedelta(days=30)
            content.end_date = new_end_date
            content.save()
        self.message_user(request, "Done!")


class SlideShowImageInline(admin.TabularInline):
    model = SlideShow.image.through
    readonly_fields = ('image_tag',)
    extra = 1
    sortable_field_name = "order"


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


class StoreFeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email_id', 'phone_number', 'store_name')
    search_fields = ('name', 'store__name', )
    list_filter = ('store', 'store__brand__name')
    list_select_related = True

    def store_name(self, obj):
        return "%s" % obj.store.name


class OfferAdmin(ContentAdmin):
    pass


class OrderedNavMenuContentAdmin(admin.TabularInline):
    model = OrderedNavMenuContent
    fk_name = 'nav_menu'
    sortable_field_name = 'order'


class NavMenuAdmin(ContentAdmin):
    inlines = [
        OrderedNavMenuContentAdmin
    ]

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
admin.site.register(WebContent, ContentAdmin)
admin.site.register(SlideShow, SlideShowAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(ContentType, ContentTypeAdmin)
admin.site.register(StoreFeedback, StoreFeedbackAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Content, ContentNonEditableAdmin)
admin.site.register(NavMenu, NavMenuAdmin)