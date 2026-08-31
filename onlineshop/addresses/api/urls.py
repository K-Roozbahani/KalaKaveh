from django.urls import path, include
from rest_framework.routers import DefaultRouter

from addresses.api.views.address import AddressViewSet
from addresses.api.views.province import ProvinceViewSet

router = DefaultRouter()
router.register(r'provinces', ProvinceViewSet, basename='provinces')
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

