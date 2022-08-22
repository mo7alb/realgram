from __future__ import absolute_import
from celery import Celery
from django.conf import settings
import os

os.environ.setdefault(
	'DJANGO_SETTINGS_MODULE',
	'config.settings'
)

app = Celery(
	'realgram',
	broker='redis://localhost/',
	backend='redis://localhost/'
)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks