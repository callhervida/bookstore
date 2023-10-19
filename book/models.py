from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):

    title = models.CharField(blank=True, null=True, max_length=100)

    genre = models.CharField(blank=True, null=True, max_length=100)

    price = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True)

    quantity = models.IntegerField(blank=True, null=True)

    description = models.TextField(blank=True, null=True)

    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
