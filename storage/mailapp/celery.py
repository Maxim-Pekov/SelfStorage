import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "storage.settings")
app = Celery("mailapp")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check_rent_remainder_daily': {
        'task': 'mailapp.tasks.check_rent_remainder',
        'schedule': crontab(minute='*/5')
    }
}
