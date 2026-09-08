from rest_framework.routers import DefaultRouter

from discounts.api.views.coupon import CouponViewSet
from discounts.api.views.discount import DiscountViewSet


router = DefaultRouter()

router.register(
    "coupon",
    CouponViewSet,
    basename="coupon",
)

router.register(
    "",
    DiscountViewSet,
    basename="discount",
)


urlpatterns = router.urls