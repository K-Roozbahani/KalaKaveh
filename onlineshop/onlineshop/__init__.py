"""
پیکربندی اولیه پکیج اصلی پروژه.

برای اینکه Celery هنگام اجرای دستور
`celery -A onlineshop ...`
بتواند Application را پیدا کند، شیء
celery_app در سطح پکیج Export می‌شود.
"""

from .config.celery import app as celery_app

__all__ = ("celery_app",)