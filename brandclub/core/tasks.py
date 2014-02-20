from celery import Celery
import datetime

app = Celery('tasks', broker='amqp://guest@localhost')

from logging import log_data


@app.task
def log_bc_data(mac_id, content_id, user_agent, page_title, device_id, user_unique_id, redirect_url, referrer, height,
                width, action, user_ip_address, access_date=datetime.datetime.now()):
    log_data(mac_id, content_id, user_agent, page_title, device_id, user_unique_id, redirect_url, referrer, height,
             width, action, user_ip_address, access_date)

