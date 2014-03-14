from annoying.functions import get_object_or_None
import datetime
from .models import Device, Content, Log

content_type_mapping = {
    1: 'Store Home',
    2: 'Cluster Home',
    3: 'Cluster Info',
    4: 'Store Info',
}


def log_data(**kwargs):
    post_params = kwargs['post_params']
    device = get_object_or_None(Device, device_id=post_params['device_id'])
    home_store = device.store
    home_brand = home_store.brand
    location_city = home_store.city.name
    location_state = home_store.state.name
    location_cluster = home_store.cluster
    content_name = ''
    content_location = ''
    content_type = ''
    content_owner_brand_id = 0
    content_owner_brand_name = ''
    content = get_object_or_None(Content, pk=post_params['content_id'])
    if content is not None and int(content.content_location) is not 3:
        content_name = content.name
        content_location_int = int(content.content_location)
        content_location = content_type_mapping[content_location_int]
        content_type = content.content_type.name
        if content.store:
            content_owner_store = content.store.all()[:1]
            content_owner_store = content_owner_store[0]
            content_owner_brand = content_owner_store.brand
            content_owner_brand_id = content_owner_brand.id
            content_owner_brand_name = content_owner_brand.name

    log_info = dict(mac_address=kwargs['mac_address'],
        content_id=post_params['content_id'],
        content_name=content_name,
        content_type=content_type,
        content_location=content_location,
        content_owner_brand_id=content_owner_brand_id,
        content_owner_brand_name=content_owner_brand_name,
        location_device_id=post_params['device_id'],
        location_store_name=device.store.name,
        location_store_id=device.store.id,
        location_brand_id=home_brand.id,
        location_brand_name=home_brand.name,
        location_cluster_id=location_cluster.id,
        location_cluster_name=location_cluster.name,
        user_agent=kwargs['user_agent'],
        mobile_make='',
        mobile_model='',
        user_unique_id=post_params['user_unique_id'],
        user_ip_address=kwargs['user_ip_address'],
        user_device_width= post_params['device_width'],
        user_device_height=post_params['device_height'],
        page_title=post_params['page_title'],
        referrer=post_params['referrer'],
        redirect_url=post_params['redirect_url'],
        action= post_params['user_action'],
        city= location_city,
        state=location_state)
    log = Log(**log_info)

    log.save()