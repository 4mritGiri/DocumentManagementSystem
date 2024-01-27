import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DocumentManagementSystem.settings')

app = Celery('DocumentManagementSystem')
app.conf.enable_utc = False # Nepal is 5:45 hours ahead of UTC
app.conf.update(timezone='Asia/Kathmandu') # Nepal is 5:45 hours ahead of UTC


app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# @app.task(bind=True, ignore_result=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')