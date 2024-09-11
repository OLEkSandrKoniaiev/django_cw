import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings')

app = Celery('settings')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(['core.services'])

app.conf.beat_schedule = {
    "update_currency": {
        "task": "core.services.currency_service.update_currency",
        "schedule": crontab(minute="30", hour="20"),
    }
}
