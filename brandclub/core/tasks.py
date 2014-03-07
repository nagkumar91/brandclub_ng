from celery import Celery
import datetime

from celery import shared_task


from logging import log_data


@shared_task
def log_bc_data(mac_id, content_id, user_agent, page_title, device_id, user_unique_id, redirect_url, referrer, height,
                width, action, user_ip_address, access_date=datetime.datetime.now()):
    log_data(mac_id, content_id, user_agent, page_title, device_id, user_unique_id, redirect_url, referrer, height,
             width, action, user_ip_address, access_date)

