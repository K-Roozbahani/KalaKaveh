from django.urls import include, path
from rest_framework.routers import DefaultRouter

from products.api.views.brand import BrandViewSet
from products.api.views.category import CategoryViewSet
from products.api.views.product import ProductViewSet
from products.api.views.review import ReviewViewSet


router = DefaultRouter()

router.register(
    r"categories",
    CategoryViewSet,
    basename="category",
)

router.register(
    r"brands",
    BrandViewSet,
    basename="brand",
)

router.register(
    r"products",
    ProductViewSet,
    basename="product",
)


urlpatterns = [
    *router.urls,

    path(

    "products/<str:product_slug>/reviews/",
        ReviewViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="product-review-list",
    ),

    path(
        "products/<str:product_slug>/reviews/<int:pk>/",
        ReviewViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="product-review-detail",
    ),
]