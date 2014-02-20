from annoying.functions import get_object_or_None
import datetime
from .models import Device, Content, Log

content_type_mapping = {
    1: 'Store Home',
    2: 'Cluster Home',
    3: 'Cluster Info',
    4: 'Store Info',
}


def log_this(mac_id, content_id, user_agent, page_title, device_id, user_unique_id, redirect_url, referrer, height,
             width, action, user_ip_address, access_date=datetime.datetime.now()):
    device = get_object_or_None(Device, device_id=device_id)
    home_store = device.store
    home_store_name = device.store.name
    home_store_id = device.store.id
    home_brand_name = home_store.brand.name
    home_brand_id = home_store.brand.id
    location_city = home_store.city.name
    location_state = home_store.state.name
    location_cluster = home_store.cluster
    location_cluster_id = location_cluster.id
    location_cluster_name = location_cluster.name
    mobile_make = ''
    mobile_model = ''
    content_name = ''
    content_location = ''
    content_type = ''
    content_owner_brand_id = 0
    content_owner_brand_name = ''
    content = get_object_or_None(Content, pk=content_id)
    if content is not None:
        content_name = content.name
        content_location_int = int(content.content_location)
        content_location = content_type_mapping[content_location_int]
        content_type = content.content_type.name
        content_owner_store = content.store.all()[:1]
        content_owner_store = content_owner_store[0]
        content_owner_brand = content_owner_store.brand
        content_owner_brand_id = content_owner_brand.id
        content_owner_brand_name = content_owner_brand.name

    log = Log(mac_address=mac_id, content_id=content_id, content_name=content_name, content_type=content_type,
              content_location=content_location, content_owner_brand_id=content_owner_brand_id,
              content_owner_brand_name=content_owner_brand_name, location_device_id=device_id,
              location_store_name=home_store_name, location_store_id=home_store_id, location_brand_id=home_brand_id,
              location_brand_name=home_brand_name, location_cluster_id=location_cluster_id,
              location_cluster_name=location_cluster_name, user_agent=user_agent, mobile_make=mobile_make,
              mobile_model=mobile_model, user_unique_id=user_unique_id, user_ip_address=user_ip_address,
              user_device_width=width, user_device_height=height, page_title=page_title, referrer=referrer,
              redirect_url=redirect_url, action=action, city=location_city, state=location_state, access_date=access_date)
    log.save()