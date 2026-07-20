from django.urls import path

from home.api.views import HomePageAPIView


app_name = "home"


urlpatterns = [
    path(
        "",
        HomePageAPIView.as_view(),
        name="home-page",
    ),
]