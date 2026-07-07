from rest_framework.routers import DefaultRouter

from checkout.api.views import CheckoutViewSet


app_name = "checkout"

router = DefaultRouter()

router.register(
    "",
    CheckoutViewSet,
    basename="",
)

urlpatterns = router.urls


# GET     /checkout/
# POST    /checkout/
# POST    /checkout/confirm/