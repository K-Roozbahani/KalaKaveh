from rest_framework.routers import DefaultRouter
from authentication.api.views import AuthenticationViewSet


router = DefaultRouter()

router.register("", AuthenticationViewSet, basename="authentication")

urlpatterns = router.urls