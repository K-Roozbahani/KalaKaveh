"""
ViewSetهای پایه پروژه OnlineShop.

این فایل ViewSetهای مشترک مورد استفاده در API پروژه را
فراهم می‌کند تا سیاست‌های عمومی مانند CSRF در یک نقطه
مدیریت شوند.
"""

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from rest_framework.viewsets import ModelViewSet


@method_decorator(
    csrf_protect,
    name="dispatch",
)
class BaseModelViewSet(ModelViewSet):
    """
    ViewSet پایه برای تمام ModelViewSetهای پروژه.

    تمام درخواست‌های API که از این کلاس ارث‌بری کنند،
    تحت محافظت CSRF قرار می‌گیرند.

    درخواست‌های Safe مانند GET، HEAD و OPTIONS توسط
    مکانیزم CSRF جنگو نیاز به Token ندارند.
    """

    pass