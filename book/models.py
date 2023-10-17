from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    """A Model for blog post's information including content's title, content
    author and Publication Date"""

    title = models.CharField(blank=True, null=True, max_length=100)

    price = models.DecimalField(max_digits=10, decimal_places=1)

    quantity = models.IntegerField(blank=True, null=True)

    description = models.TextField(blank=True, null=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
