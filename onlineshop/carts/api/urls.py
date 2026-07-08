from rest_framework.routers import DefaultRouter

from carts.api.views.cart import CartViewSet
from carts.api.views.cart_item import CartItemViewSet

router = DefaultRouter()

router.register(
    "items",
    CartItemViewSet,
    basename="cart-item",
)

router.register(
    "",
    CartViewSet,
    basename="cart",
)


urlpatterns = router.urls