from django.urls import path

from .views import create_person, find_hypotenuse, list_persons_view, person_detail_view, update_person

urlpatterns = [
    path("", find_hypotenuse, name="find_hypotenuse"),
    path("person/", create_person, name="person"),
    path("person/<int:pk>", update_person, name="update_person"),
    path("persons-list", list_persons_view, name="list_persons"),
    path("person-detail/<int:pk>", person_detail_view, name="person-detail"),
]
