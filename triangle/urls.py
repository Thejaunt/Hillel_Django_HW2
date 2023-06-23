from django.urls import path

from .views import create_person, find_hypotenuse, update_person

urlpatterns = [
    path("", find_hypotenuse, name="find_hypotenuse"),
    path("person/", create_person, name="person"),
    path("person/<int:pk>", update_person, name="update_person"),
]
