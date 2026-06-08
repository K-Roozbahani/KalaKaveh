from rest_framework.routers import DefaultRouter

from carts.views.cart import CartViewSet

from carts.views.cart_item import CartItemViewSet


router = DefaultRouter()

router.register("", CartViewSet, basename="cart")

router.register("items", CartItemViewSet, basename="cart-item")
urlpatterns = router.urls