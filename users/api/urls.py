from rest_framework.routers import DefaultRouter
from .views import UserApiView, AddressViewSet
router = DefaultRouter()
router.register(r'', UserApiView, basename='user-api')
router.register(r'addresses', AddressViewSet, basename='address')
urlpatterns = router.urls