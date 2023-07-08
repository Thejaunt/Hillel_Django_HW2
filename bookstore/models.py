from django.db import models
from django.db.models import UniqueConstraint


class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Book(models.Model):
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, null=True)
    authors = models.ManyToManyField(Author, through="BookAuthor")
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    pubdate = models.DateField()

    objects = models.Manager()

    def __str__(self):
        return self.name


class Store(models.Model):
    books = models.ManyToManyField(Book, through="StoreBook")
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        UniqueConstraint(fields=["book", "author"], name="unique_book_author")

    def __str__(self):
        return f"{self.book} {self.author}"


class StoreBook(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        UniqueConstraint(fields=["store", "book"], name="unique_store_book")

    def __str__(self):
        return f"{self.store} {self.book}"
