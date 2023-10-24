from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

from book.models import Book


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password, **extra_fields):
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        AUTHOR = "AUTHOR", 'Author'
        OTHER = "OTHER", 'Other'

    base_role = Role.OTHER

    role = models.CharField(max_length=50, choices=Role.choices)

    email = models.EmailField(unique=True)
    national_code = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(blank=True, null=True)
    profile_picture = models.FileField(blank=True, null=True)
    is_author = models.BooleanField(default=False)
    # username = phone_number


class Author(User):
    base_role = User.Role.AUTHOR

    class Meta:
        proxy = True


class AuthorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)
