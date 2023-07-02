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


class LogTriangle(models.Model):
    class AllowedMethods(models.TextChoices):
        GET = "GET"
        POST = "POST"

    request = models.JSONField()
    method = models.CharField(max_length=7, choices=AllowedMethods.choices)
    path = models.TextField(default="-")
    query = models.TextField(default="-")
    body = models.TextField(default="-")
    timestamp = models.DateTimeField(auto_now_add=True)
    response_status = models.IntegerField(default=200)

    def __str__(self):
        return f"{self.method} {self.response_status}"

    def allowed_method(self):
        return self.method in {self.AllowedMethods.GET, self.AllowedMethods.POST}

    @property
    def bad_method(self):
        if self.method not in [x[0] for x in self.AllowedMethods.choices]:
            return True
        return False
