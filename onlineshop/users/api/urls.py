from rest_framework.routers import DefaultRouter
from .views import UserApiView


router = DefaultRouter()

router.register('', UserApiView, basename='user')

urlpatterns = router.urls