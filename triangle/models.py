from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.email} - {self.first_name} {self.last_name}"

    def fullname(self):
        return f"{self.first_name} {self.last_name}"
