from django.urls import path
from .views import SplashView


app_name = "Account"


urlpatterns = [
    path("splash", SplashView.as_view(), name="Splash"),
]
