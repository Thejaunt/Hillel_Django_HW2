from django.urls import path

from .views import find_hypotenuse

urlpatterns = [
    path("", find_hypotenuse, name="find_hypotenuse"),
]
