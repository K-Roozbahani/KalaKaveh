from rest_framework.routers import DefaultRouter

from discounts.api.views.coupon import CouponViewSet

router = DefaultRouter()

router.register(
    "coupon",
    CouponViewSet,
    basename="coupon",
)


urlpatterns = router.urls