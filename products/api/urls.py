from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.api.view import (
    CategoryViewSet, BrandViewSet, ProductAttributeViewSet,
    ProductViewSet, ReviewViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'brands', BrandViewSet)
router.register(r'attributes', ProductAttributeViewSet)
router.register(r'products', ProductViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = router.urls

