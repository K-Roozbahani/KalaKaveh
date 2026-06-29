from rest_framework.routers import DefaultRouter

from carts.api.views import CartViewSet

from carts.api.views import CartItemViewSet


router = DefaultRouter()

router.register("", CartViewSet, basename="cart")

router.register("items", CartItemViewSet, basename="cart-item")
urlpatterns = router.urls