import os
import sys

from celery import Celery
from celery.schedules import crontab

from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_name.settings")

app = Celery("project_name", broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.beat_schedule = {
    "add-every-30-seconds": {
        "task": "scrapping.tasks.scrap_scrap",
        # "schedule": crontab(minute="*"),
        "schedule": crontab(hour="*/3,1-23"),
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    sys.stdout.write(f"Request: {self.request!r}")
