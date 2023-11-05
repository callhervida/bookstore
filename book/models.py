from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User

from bookstore import settings


class Book(models.Model):
    title = models.CharField(blank=True, null=True, max_length=100)

    genre = models.CharField(blank=True, null=True, max_length=100)

    price = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True)

    quantity = models.IntegerField(blank=True, null=True)

    description = models.TextField(blank=True, null=True)

    average_rate = models.FloatField(default=0, blank=True, null=True, verbose_name="میانگین امتیاز")

    count_comment = models.IntegerField(default=0, blank=True, null=True, verbose_name="تعداد نظرات")

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)


class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, blank=True, null=True, related_name='store_comment',
                             verbose_name="فروشگاه")

    # user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='user_comment',
    #                          verbose_name="کاربر")

    created_date = models.DateTimeField(default=timezone.now, blank=True, null=True, verbose_name="تاریخ ایجاد")

    approved = models.BooleanField(default=False, blank=True, null=True, verbose_name="تایید شده")

    text = models.TextField(blank=True, null=True, verbose_name="متن")
