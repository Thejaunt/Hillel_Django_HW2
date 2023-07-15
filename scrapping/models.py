from django.db import models
from django.db.models import UniqueConstraint


class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)
    born_date = models.TextField()
    born_location = models.TextField()
    bio = models.TextField()

    def __str__(self):
        return self.name


class Quote(models.Model):
    author = models.ForeignKey("Quote", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    tags = models.ManyToManyField("Tag", through="QuotesTags")

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class QuotesTags(models.Model):
    quotes = models.ForeignKey(Quote, on_delete=models.CASCADE)
    tags = models.ForeignKey(Tag, on_delete=models.CASCADE)

    objects = models.Manager()

    class Meta:
        UniqueConstraint(fields=["quotes", "tags"], name="unique_quotes_tags")

    def __str__(self):
        return f"{self.quotes} {self.tags}"
