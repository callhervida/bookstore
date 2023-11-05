from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import MaxValueValidator, RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password, **extra_fields):
        print(extra_fields)

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

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')

        if not extra_fields.get('is_superuser'):
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
    username = None
    email = models.EmailField(unique=True)
    national_code = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(unique=True,  validators=[
      RegexValidator(
        regex=r'^\+9899?\d{9}$',
        message="Phone number must be entered in the format '+989123456789'. Up to 12 digits allowed."
      ),
    ],)
    profile_picture = models.FileField(blank=True, null=True)
    is_author = models.BooleanField(default=False)
    # username = phone_number
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number

    def clean(self):
        super().clean()

    def save(self, *args, **kwargs):
        if self.role == User.Role.AUTHOR:
            AuthorProfile.objects.get_or_create(user=self)
        super().save(*args, **kwargs)


class AuthorProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # book = models.OneToOneField(Book, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=False)
