from rest_framework.routers import DefaultRouter
from .views import UserApiView, AuthenticationViewSet


router = DefaultRouter()

router.register("auth", AuthenticationViewSet, basename="authentication")

router.register('', UserApiView, basename='user')

urlpatterns = router.urls