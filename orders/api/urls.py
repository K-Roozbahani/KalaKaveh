from rest_framework.routers import DefaultRouter

from orders.api.views import OrderViewSet

app_name = "orders"

router = DefaultRouter()

router.register(
    r"",
    OrderViewSet,
    basename="orders",
)

urlpatterns = router.urls



# GET     /api/v1/orders/
#
# POST    /api/v1/orders/
#
# GET     /api/v1/orders/latest/
#
# GET     /api/v1/orders/{order_number}/
#
# GET     /api/v1/orders/{order_number}/items/