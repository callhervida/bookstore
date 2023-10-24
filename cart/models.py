from django.db import models
from django.contrib.auth.models import User

from book.models import Book


class CartItem(models.Model):
    product = models.OneToOneField(Book, on_delete=models.CASCADE, null=True)
    is_ordered = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(null=True)
    quantity = models.IntegerField(blank=True, null=True)


class Cart(models.Model):
    ref_code = models.CharField(max_length=15)
    # owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(CartItem)
    date_ordered = models.DateTimeField(auto_now=True)

    def get_cart_items(self):
        return self.items.all().values('product__title', 'quantity')

    def get_cart_total(self):
        return sum([item.product.price for item in self.items.all()])


class UserOrder(models.Model):
    # owner = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    ordered_on = models.DateTimeField(auto_now_add=True)
