from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# setting the Django settings module.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ais.settings')
app = Celery('ais')
app.config_from_object('django.conf:settings')

# Looks up for task modules in Django applications and loads them
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))