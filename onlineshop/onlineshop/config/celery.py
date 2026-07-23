"""
تنظیمات Celery پروژه
"""

import os

from celery import Celery

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings",
)

app = Celery("config")

# بارگذاری تنظیمات Celery از Django Settings
app.config_from_object(
    "django.conf:settings",
    namespace="CELERY",
)

# جستجوی خودکار فایل‌های tasks.py در تمام Appها
app.autodiscover_tasks()