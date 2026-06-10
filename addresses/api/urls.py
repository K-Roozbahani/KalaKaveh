from django.urls import path, include
from rest_framework.routers import DefaultRouter

from addresses.api.views import AddressViewSet

router = DefaultRouter()
router.register(r"", AddressViewSet, basename="addresses")

urlpatterns = [
    path("", include(router.urls)),
]

# GET     /addresses/                 لیست آدرس‌ها
# POST    /addresses/                 ایجاد آدرس
#
# GET     /addresses/{id}/            جزئیات
# PATCH   /addresses/{id}/            ویرایش
# DELETE  /addresses/{id}/            حذف
#
# POST    /addresses/{id}/set_default/   آدرس پیش‌فرض

