from rest_framework.routers import DefaultRouter
from .views import UserApiView
router = DefaultRouter()
router.register(r'', UserApiView, basename='user-api')
urlpatterns = router.urls