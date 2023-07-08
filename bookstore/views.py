from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, render

from .models import Author, Book, Publisher, Store


def bookstore_home(request):
    return render(request, "bookstore_home.html")


def author_list(request):
    authors = Author.objects.order_by("-age").prefetch_related("book_set").annotate(num_book=Count("book"))
    paginator = Paginator(authors, 20)
    page_number = request.GET.get("page")
    objs = paginator.get_page(page_number)
    return render(request, "authors_list.html", {"page_obj": objs})


def author_detail(request, pk):
    obj = get_object_or_404(Author.objects.prefetch_related("book_set").annotate(n_books=Count("book")), pk=pk)
    return render(request, "author_detail.html", {"obj": obj})


def publisher_list(request):
    publishers = (
        Publisher.objects.annotate(num_book=Count("book", distinct=True)).prefetch_related("book_set").order_by("name")
    )
    paginator = Paginator(publishers, 25)
    page_number = request.GET.get("page")
    objs = paginator.get_page(page_number)
    num_pub = publishers.aggregate(num_pub=Count("name"))
    return render(request, "publishers_list.html", {"page_obj": objs, "num_pub": num_pub})


def publisher_detail(request, pk):
    obj = get_object_or_404(
        Publisher.objects.prefetch_related("book_set", "book_set__authors").annotate(
            num_book=Count("book", distinct=True), num_auth=Count("book__authors", distinct=True)
        ),
        pk=pk,
    )
    return render(request, "publisher_detail.html", {"obj": obj})


def book_list(request):
    books = (
        Book.objects.order_by("-rating", "-pubdate")
        .select_related("publisher")
        .prefetch_related("authors")
        .annotate(n_auth=Count("authors", distinct=True))
    )
    paginator = Paginator(books, 25)
    page_number = request.GET.get("page")
    objs = paginator.get_page(page_number)
    num = books.aggregate(books=Count("name"))

    return render(request, "books_list.html", {"page_obj": objs, "num": num})


def book_detail(request, pk):
    obj = get_object_or_404(
        Book.objects.prefetch_related("store_set", "authors")
        .annotate(n_authors=Count("authors", distinct=True), n_stores=Count("store", distinct=True))
        .select_related("publisher"),
        pk=pk,
    )
    return render(request, "book_detail.html", {"obj": obj})


def store_list(request):
    stores = Store.objects.prefetch_related("books").annotate(n_books=Count("books")).order_by("-n_books")
    paginator = Paginator(stores, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "stores_list.html", {"page_obj": page_obj, "total": stores.count()})


def store_detail(request, pk):
    obj = get_object_or_404(
        Store.objects.prefetch_related("books")
        .annotate(n_books=Count("books", distinct=True))
        .order_by("-books__rating", "name"),
        pk=pk,
    )
    return render(request, "store_detail.html", {"obj": obj})
