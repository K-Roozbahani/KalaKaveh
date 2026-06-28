from django.urls import path, include
from rest_framework.routers import DefaultRouter

from products.api.views.brand import BrandViewSet
from products.api.views.category import CategoryViewSet
from products.api.views.product import ProductViewSet


router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename="category")
router.register(r'brands', BrandViewSet, basename="brand")
# router.register(r'reviews', ReviewViewSet)

router.register(r'products', ProductViewSet, basename="product")

urlpatterns = router.urls

