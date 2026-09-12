from rest_framework.routers import DefaultRouter

from favorites.api.views.favorite import FavoriteViewSet


router = DefaultRouter()

router.register(
    "",
    FavoriteViewSet,
    basename="favorite",
)

urlpatterns = router.urls