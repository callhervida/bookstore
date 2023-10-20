from django.db import models
from django.contrib.auth.models import User

from book.models import Book


class CartItem(models.Model):
    product = models.OneToOneField(Book, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(null=True)
    quantity = models.IntegerField(blank=True, null=True)


class Cart(models.Model):
    ref_code = models.CharField(max_length=15)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(CartItem)
    date_ordered = models.DateTimeField(auto_now=True)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product for item in self.items.all()])
