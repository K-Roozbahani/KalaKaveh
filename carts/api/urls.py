from django.urls import path, include
from rest_framework.routers import DefaultRouter
from carts.api.view import CartViewSet

router = DefaultRouter()
router.register(r'cart', CartViewSet)

urlpatterns = router.urls

