from django.urls import path
from .views import (
    success,
    home_view,
    digit_image_view,
    display_digit_images,
    canvas_image,
)


app_name = "Digit"


urlpatterns = [
    path('', home_view, name='homeDigit'),
    path('image_upload/', digit_image_view, name = 'image_upload'),
    path('digit_images/', display_digit_images, name = 'digit_images'),
    path('canvas/', canvas_image, name = 'canvas'),   
]
