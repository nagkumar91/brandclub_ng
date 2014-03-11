from celery import Celery
import datetime

from celery import shared_task


from logging import log_data


@shared_task
def log_bc_data(**kwargs):
    log_data(kwargs=kwargs)
