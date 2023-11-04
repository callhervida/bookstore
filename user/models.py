from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

from book.models import Book


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password, **extra_fields):

        if not phone_number:
            raise ValueError('phone number is required')

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        AUTHOR = "AUTHOR", 'Author'
        OTHER = "OTHER", 'Other'

    base_role = Role.OTHER

    role = models.CharField(max_length=50, choices=Role.choices)

    user_name = None
    email = models.EmailField(unique=True)
    national_code = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(blank=True, null=True, unique=True)
    profile_picture = models.FileField(blank=True, null=True)
    is_author = models.BooleanField(default=False)
    # username = phone_number
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class AuthorProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.OneToOneField(Book, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=False)
