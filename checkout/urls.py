from django.urls import path

from checkout.views import CheckoutView

app_name = "checkout"

urlpatterns = [
    path(
        "",
        CheckoutView.as_view(),
        name="checkout",
    ),
]