from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.api.views.product import ProductViewSet


router = DefaultRouter()
# router.register(r'categories', CategoryViewSet)
# router.register(r'brands', BrandViewSet)
# router.register(r'attributes', ProductAttributeViewSet)
# router.register(r'products', ProductViewSet)
# router.register(r'reviews', ReviewViewSet)

router.register(r'products', ProductViewSet, basename="product")

urlpatterns = router.urls

