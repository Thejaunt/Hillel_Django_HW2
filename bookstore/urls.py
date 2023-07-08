from django.urls import path

from .views import (author_detail, author_list,
                    book_detail, book_list,
                    bookstore_home,
                    publisher_detail, publisher_list,
                    store_detail, store_list,)


app_name = "bookstore"
urlpatterns = [
    path("", bookstore_home, name="bookstore_home"),
    path("authors", author_list, name="authors_list"),
    path("author/<int:pk>", author_detail, name="author"),
    path("publishers", publisher_list, name="publishers"),
    path("publisher/<int:pk>", publisher_detail, name="publisher"),
    path("books", book_list, name="books"),
    path("book/<int:pk>", book_detail, name="book"),
    path("stores", store_list, name="stores"),
    path("store/<int:pk>", store_detail, name="store"),
]
