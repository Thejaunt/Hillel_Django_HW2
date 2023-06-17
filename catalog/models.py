from django.db import models
from django.db.models import UniqueConstraint
from django.utils import timezone


class City(models.Model):
    name = models.CharField(max_length=200)
    state = models.CharField(max_length=100)

    class Meta:
        unique_together = ["name", "state"]
        # UniqueConstraint(fields=["name", "state"], name="unique_city_state")

    def __str__(self):
        return self.name


class Supplier(models.Model):
    city = models.OneToOneField(City, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    #  for now live it with expiry date now
    exp_date = models.DateField(db_comment="Date when the product expires", default=timezone.now())  # Expiry date
    title = models.CharField(max_length=150)
    vendor_code = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Client(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through='ClientsProducts')
    email = models.EmailField(max_length=255)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    def __str__(self):
        return self.email

    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"


class ClientsProducts(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        UniqueConstraint(fields=["client", "product"], name="unique_clients_products")
